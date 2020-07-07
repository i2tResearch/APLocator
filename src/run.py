# -*- coding: utf-8 -*-

import sys
from cli import iw
from cli import nmcli
from storage import storage
from configmanager import ConfigManager
from providers import locproviderfactory


def main(output_file):
    print("Hi! I'm working...")
    print("--")

    settings = ConfigManager.load("config.ini")

    provider = locproviderfactory.get_location_provider(settings)
    provider.start();


    location = provider.get_location()

    nmcli_results = nmcli.run()
    iw_results = iw.run(settings.tmp_cli_file)

    print("latitude (ddmm.mmmmm)............. ", location.lat, location.lat_d)
    print("longitude (dddmm.mmmmm)...........", location.lon, location.lon_d)
    print("altitude (m)......................", location.alt)
    print("satellites........................", location.satellites)
    print("nmcli results.....................", len(nmcli_results))
    print("iw results........................", len(iw_results))

    results_dict = {
        "location": {
            "lat": location.lat,
            "latd": location.lat_d,
            "lon": location.lon,
            "lond": location.lon_d,
            "alt": location.alt,
            "sat": location.satellites,
            "raw": location.raw
        },
        "nmcli": nmcli_results,
        "iw": iw_results
    }

    file_path = settings.output_folder + "/" + output_file
    storage.save(file_path, results_dict)

    provider.stop()
    print("Done! Bye.")


if __name__ == "__main__":
    main(sys.argv[1])

# Final notes. Useful linux commands:
# nmcli dev wifi
# sudo iw dev wlp2s0 scan | egrep "signal:|SSID:" | sed -e "s/\tsignal: //" -e "s/\tSSID: //" | awk '{ORS = (NR % 2 == 0)? "\n" : " "; print}' | sort
# sudo iw dev wlp2s0 scan | egrep "on wlp2s0|signal:|SSID:" | sed -e "s/\tsignal: //" -e "s/\tSSID: //" -e "s/BSS //" -e "s/associated//" -e "s/ -- //" | awk '{ORS = (NR % 3 == 0)? "\n" : " "; print}' | sort
