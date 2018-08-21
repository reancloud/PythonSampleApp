"""Contains constats required for commands."""


class DeployConstants(object):
    """Contains constats required for CLI."""

    DEPLOY_URL = '/api/reandeploy/DeployNow/rest'
    NAME_REEFERENCE = 'name'
    PROVIDER_DETAILS_REFERENCE = 'provider_details'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
