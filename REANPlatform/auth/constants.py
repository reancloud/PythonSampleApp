"""Contains constats required for commands."""


class Constants(object):
    """Contains constats required for CLI."""

    AUTHNZ_URL = '/api'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
