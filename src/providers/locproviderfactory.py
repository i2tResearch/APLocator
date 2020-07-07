"""Location provider builder."""
# -*- coding: utf-8 -*-


from providers.locprovider import LocProvider
from providers.bu353 import BU353LocProvider


BU353 = "bu353"
UBLOX = "ublox"


def get_location_provider(settings):
    """Build the location provider.

    Args:
        settings (SettingsHolder) -- application settings.
    """

    if settings.device == BU353 or settings.device == UBLOX:
        return BU353LocProvider(settings.port, settings.speed, settings.timeout)
    else:
        return LocProvider()
