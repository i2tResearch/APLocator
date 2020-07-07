# -*- coding: utf-8 -*-

import pynmcli


def run(verbose = False):
    raw_networks = pynmcli.NetworkManager.Device().wifi('list').execute()
    networks = pynmcli.get_data(raw_networks)
    results = [_lower_keys(n) for n in networks]

    if verbose:
        print("[nmcli]")
        print(raw_networks)

    return results


def _lower_keys(d):
    new_dict = dict((k.lower(), v) for k, v in d.items())
    return new_dict
