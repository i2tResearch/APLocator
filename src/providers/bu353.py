# -*- coding: utf-8 -*-

import serial
import traceback
from models.location import Location
from providers.locprovider import LocProvider


class BU353LocProvider(LocProvider):
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
