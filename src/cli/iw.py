# -*- coding: utf-8 -*-

import os


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


def run(filePath, verbose = False):
    os.system(_get_iw_command(filePath))
    contents = _get_iw_command_result(filePath)
    results = []

    for c in contents:
        line = c.replace("\n", "").replace(" dBm", "")
        if not line.isspace():
            i = line.split(" ")

            item = {
                "bssid": i[0],
                "dBm": i[1],
                "ssid": " ".join(i[2:])
            }

            results.append(item)

    if verbose:
        print("[iw]")
        for r in results:
            print(r)

    return results
