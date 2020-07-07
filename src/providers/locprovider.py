"""Base location provider."""
# -*- coding: utf-8 -*-


class LocProvider(object):
    """Default location provider."""

    def start(self):
        """Start the location provider and return status."""
        return True

    def stop(self):
        """Stop the location provider and return status."""
        return True

    def get_location(self):
        """Should return a Location instance."""
        return None
