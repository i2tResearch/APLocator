# -*- coding: utf-8 -*-

import pynmea2


class Location(object):
    """Represents the location of the device.

    Args:
        lat (str) -- latitude.
        lat_d (str) -- latitude direction.
        lon (str) -- longitude.
        lon_d (str) -- longitude direction.
        alt (float) -- altitude in meters.
        sats (int) -- number of satellites. default -1.
        raw (str) -- full GNGGA/GPGGA string. default None.
    """

    def __init__(self, lat, lat_d, lon, lon_d, alt, qual, sats, raw=None):
        self.lat = lat
        self.lat_d = lat_d
        self.lon = lon
        self.lon_d = lon_d
        self.alt = alt
        self.sats = sats
        self.qual = qual
        self.raw = raw

    def __str__(self):
        lat = self.lat[0:2] + "° " + self.lat[2:] + "' " + self.lat_d
        lon = self.lon[0:3] + "° " + self.lon[3:] + "' " + self.lon_d
        return lat + " " + lon

    def qual_description(self):
        descriptions = {
            0: "invalid",
            1: "fixed",
            2: "DGPS",
            3: "PPS",
            4: "Real time kinematic",
            5: "Float RTK",
            6: "Estimated",
            7: "Manual input",
            8: "Simulation"
        }
        return descriptions[self.qual]

    @classmethod
    def build_from_gngga(cls, raw):
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
            gps_params = pynmea2.parse(raw)

            loc = Location(
                gps_params.lat if gps_params.lat != "" else "0",
                gps_params.lat_dir if gps_params.lat_dir != "" else "N",
                gps_params.lon if gps_params.lon != "" else "0",
                gps_params.lon_dir if gps_params.lon_dir != "" else "W",
                gps_params.altitude if gps_params.altitude is not None else 0,
                gps_params.gps_qual if gps_params.gps_qual is not None else 0,
                gps_params.num_sats if gps_params.num_sats != "" else "00",
                raw
            )

            return loc

        except pynmea2.ChecksumError:
            return None
        except pynmea2.ParseError:
            return None
        except AttributeError:
            return None
