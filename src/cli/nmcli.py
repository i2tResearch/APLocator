# -*- coding: utf-8 -*-

import pynmcli


def run():
    raw_networks = pynmcli.NetworkManager.Device().wifi('list').execute()
    networks = pynmcli.get_data(raw_networks)
    return networks
