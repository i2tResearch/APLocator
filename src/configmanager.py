"""Configuration manager."""
# -*- coding: utf-8 -*-

from configparser import ConfigParser


class ConfigManager(object):
    """Loads the config file to an object."""

    @staticmethod
    def load(file_path):
        parser = ConfigParser()
        parser.read(file_path)

        device = parser.get("GPS", "device")
        port = parser.get("GPS", "port")
        speed = parser.getint("GPS", "speed")
        timeout = parser.getint("GPS", "timeout")
        output_folder = parser.get("Results", "output_folder")
        tmp_cli_file = parser.get("CLI", "tmp_cli_file")

        settings = SettingsHolder(device, port, speed, timeout, output_folder, tmp_cli_file)

        return settings


class SettingsHolder(object):

    def __init__(self, device, port, speed, timeout, output_folder, tmp_cli_file):
        self.device = device
        self.port = port
        self.speed = speed
        self.timeout = timeout
        self.output_folder = output_folder
        self.tmp_cli_file = tmp_cli_file
