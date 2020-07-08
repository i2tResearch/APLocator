# -*- coding: utf-8 -*-

import sys
from cli import iw
from cli import nmcli
from storage import storage
from configmanager import ConfigManager
from providers import locproviderfactory


def main(output_file):
    test_mode = output_file == "-t" or output_file == "-d"
    dev_mode = output_file == "-d"

    print("Hi! I'm working on test mode" if test_mode else "Hi! I'm working...")

    if dev_mode:
        print("You are a dev!")

    print("--")

    settings = ConfigManager.load("config.ini")

    provider = locproviderfactory.get_location_provider(settings)
    provider.start()

    location = provider.get_location()

    nmcli_results = nmcli.run(dev_mode)
    iw_results = iw.run(settings.tmp_cli_file, dev_mode)

    print("\n[results]")
    print("location..........................", str(location))
    print("altitude (m)......................", location.alt)
    print("satellites........................", location.sats)
    print("quality...........................", location.qual, location.qual_description())
    print("nmcli results.....................", len(nmcli_results))
    print("iw results........................", len(iw_results))

    results_dict = {
        "location": {
            "full": str(location),
            "lat": location.lat,
            "latd": location.lat_d,
            "lon": location.lon,
            "lond": location.lon_d,
            "alt": location.alt,
            "sat": location.sats,
            "qual": location.qual,
            "qual_desc": location.qual_description(),
            "raw": location.raw
        },
        "nmcli": nmcli_results,
        "iw": iw_results
    }

    if not test_mode:
        file_path = settings.output_folder + "/" + output_file
        storage.save(file_path, results_dict)

    provider.stop()

    print("--")
    print("Done! Bye.")


def print_help():
    print("GPS formats:")
    print("\t", "latitude: ddmm.mmmmm")
    print("\t", "e.g. 0324,74169", "is:", "03° 24.74169'")
    print("\t", "longitude: dddmm.mmmmm")
    print("\t", "e.g. 07631.58999", "is:", "076° 31.58999'")

    print("GPS quality:")

    print("\t", "0", "invalid")
    print("\t", "1", "fixed")
    print("\t", "2", "DGPS")
    print("\t", "3", "PPS")
    print("\t", "4", "Real time kinematic")
    print("\t", "5", "Float RTK")
    print("\t", "6", "Estimated")
    print("\t", "7", "Manual input")
    print("\t", "8", "Simulation")

    print("Modes")

    print("\t", "-h", "Help mode")
    print("\t", "-t", "Test mode")
    print("\t", "-d", "Dev mode")
    print("\t", "file-prefix", "Normal mode")


if __name__ == "__main__":
    param = sys.argv[1]

    if param == "-h":
        print_help()
    else:
        main(sys.argv[1])
