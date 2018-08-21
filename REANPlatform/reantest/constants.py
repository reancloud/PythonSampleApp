"""Contains constats required for commands."""


class TestConstants(object):
    """Contains constats required for CLI."""

    TEST_URL = '/api/reantest/TestNow/rest'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
