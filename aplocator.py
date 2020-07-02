# -*- coding: utf-8 -*-

import os
import sys
import time
import traceback
import serial
import pynmea2
import pynmcli
import json


class Location(object):
    """Represents the location of the device.

    Args:
        lat (str) -- latitude.
        lat_d (str) -- latitude direction.
        lon (str) -- longitude.
        lon_d (str) -- longitude direction.
        alt (float) -- altitude in meters.
        satellites (int) -- number of satellites. default -1.
        gngga_str (str) -- full GNGGA/GPGGA string. default None.
    """

    def __init__(self, lat, lat_d, lon, lon_d, alt, satellites, gngga_str=None):
        self.lat = lat
        self.lat_d = lat_d
        self.lon = lon
        self.lon_d = lon_d
        self.alt = alt
        self.satellites = satellites
        self.gngga_str = gngga_str

    @classmethod
    def build_from_gngga(cls, gngga_str):
        """Build a Location object from a GNGGA/GPGGA string.

        $GNGGA,203800.00,0320.56190,N,07631.70957,W,1,12,0.61,1048.1,M,8.3,M,,*5F
        $GPGGA,215840.000,0320.5609,N,07631.7120,W,1,05,1.5,1033.1,M,8.9,M,,0000*48
        $GNGGA,142048.00,,,,,0,00,99.99,,,,,,*73

        0 tag $GPGGA/$GNGGA
        1 timestamp 215840.000
        2 latitude 0320.5609, 03º 20.5609'
        3 latitude direction N
        4 longitude 07631.7120, 076º 31.7120'
        5 longitude direction W
        6 fix quality
                    0 invalid                 5 Float RTK
                    1 fixed *                 6 Estimated
                    2 DGPS                    7 Manual input
                    3 PPS                     8 Simulation
                    4 Real time kinematic
        7 number of satellites 5
        8 horizontal dilution of position 1.5
        9 altitude 1033.1
        10 altitude units M
        11 height of geoid (mean sea level) above WGS84 ellipsoid 8.9
        12 height of geoid units M
        13 empty
        14 DGPS station Id 0000 and checksum 48
        """
        try:
            gps_params = pynmea2.parse(gngga_str)

            loc = Location(
                gps_params.lat if gps_params.lat != "" else "0",
                gps_params.lat_dir if gps_params.lat_dir != "" else "N",
                gps_params.lon if gps_params.lon != "" else "0",
                gps_params.lon_dir if gps_params.lon_dir != "" else "W",
                gps_params.altitude if gps_params.altitude is not None else 0,
                gps_params.num_sats if gps_params.num_sats != "" else "00",
                gngga_str
            )

            return loc

        except pynmea2.ChecksumError:
            return None
        except pynmea2.ParseError:
            return None
        except AttributeError:
            return None


class BU353LocProvider(object):
    """BU-353 location provider. Return location from serial port."""

    def __init__(self, port, speed, timeout):
        self.port = port
        self.speed = speed
        self.timeout = timeout
        self.socket = None

    def start(self):
        """Start the location provider and return status."""
        try:
            self.socket = serial.Serial(self.port, self.speed, timeout=self.timeout)
            return True

        except serial.SerialException:
            traceback.print_exc()
            return False

    def stop(self):
        """Stop the location provider and return status."""
        if self.socket is not None:
            self.socket.close()
        return True

    def get_location(self):
        """Return a location from the BU-353 GNGGA device.

        Tries to read a valid location 20 times. If no valid
        location is obtained, returns None
        """
        try:
            count = 0
            while count < 20:
                count = count + 1

                gngga_str = self.socket.readline()
                gngga_str = gngga_str.strip(b'\r\n')
                gngga_str = str(gngga_str, "utf-8")
                location = Location.build_from_gngga(gngga_str)

                if location is not None:
                    return location

        except:
            traceback.print_exc()

        return None


def _get_iw_command(filePath):
    # sudo iw dev wlp2s0 scan | egrep "on wlp2s0|signal:|SSID:" | sed -e "s/\tsignal: //" -e "s/\tSSID: //" -e "s/BSS //" -e "s/associated//" -e "s/ -- //" | awk '{ORS = (NR % 3 == 0)? "\n" : " "; print}' | sort
    cmd = 'sudo iw dev wlp2s0 scan | egrep "on wlp2s0|signal:|SSID:" | sed -e "s/\\tsignal: //" -e "s/\\tSSID: //" -e "s/BSS //" -e "s/associated//" -e "s/ -- //" -e "s/(on wlp2s0)//" | awk \'{ORS = (NR % 3 == 0)? "\\n" : " "; print}\' | sort'
    return cmd + " > " + filePath


def _get_iw_command_result(filePath):
    contents = []

    with open(filePath, "r") as f:
        for line in f:
            contents.append(line)

    return contents


def run_iw_command(filePath):
    os.system(_get_iw_command(filePath))
    contents = _get_iw_command_result(filePath)
    results = []

    for c in contents:
        line = c.replace("\n", "").replace(" dBm", "")
        if not line.isspace():
            i = line.split(" ")

            item = {
                "BSSID": i[0],
                "dBm": i[1],
                "SSID": " ".join(i[2:])
            }

            results.append(item)

    return results


def save(file_path, content):
    content_str = json.JSONEncoder().encode(content)

    suffix = time.strftime("%Y%m%d_%H%M%S")
    file_name = file_path + "_" + suffix + ".json"

    with open(file_name, "w+") as f:
        f.write(content_str)

    print("file saved", file_name)


def main(output_file):
    print("Hi! I'm working...")
    print("--")

    gps_port = "/dev/ttyACM0"
    gps_speed = 4800
    gps_timeout = 5

    provider = BU353LocProvider(gps_port, gps_speed, gps_timeout)
    provider.start()

    raw_networks = pynmcli.NetworkManager.Device().wifi('list').execute()
    networks = pynmcli.get_data(raw_networks)
    location = provider.get_location()
    iw = run_iw_command("/tmp/aplocator.txt")

    print("latitude (ddmm.mmmmm)............. ", location.lat, location.lat_d)
    print("longitude (dddmm.mmmmm)...........", location.lon, location.lon_d)
    print("altitude (m)......................", location.alt)
    print("satellites........................", location.satellites)
    print("Access points:")
    print(raw_networks)
    print("Access points details:")
    print(iw)

    final = {
        "location": { "lat": location.lat, "latd": location.lat_d, "lon": location.lon, "lond": location.lon_d, "alt": location.alt, "sat": location.satellites },
        "nmcli": networks,
        "iw": iw
    }

    save(output_file, final)

    provider.stop()
    print("Done! Bye.")


if __name__ == "__main__":
    main(sys.argv[1])

# Final notes. Useful linux commands:
# nmcli dev wifi
# sudo iw dev wlp2s0 scan | egrep "signal:|SSID:" | sed -e "s/\tsignal: //" -e "s/\tSSID: //" | awk '{ORS = (NR % 2 == 0)? "\n" : " "; print}' | sort
# sudo iw dev wlp2s0 scan | egrep "on wlp2s0|signal:|SSID:" | sed -e "s/\tsignal: //" -e "s/\tSSID: //" -e "s/BSS //" -e "s/associated//" -e "s/ -- //" | awk '{ORS = (NR % 3 == 0)? "\n" : " "; print}' | sort

# Dependencies:
# pip3 install pyserial pynmea2 pynmcli
