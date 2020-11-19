"""Contains constats required for commands."""


class SolutionConstants(object):
    """Contains constats required for CLI."""

    SOLUTION_URL = '/api/reansolutionpackage'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
