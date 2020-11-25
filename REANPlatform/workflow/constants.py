"""Contains constats required for commands."""


class WorkflowConstants:
    """Contains constats required for CLI."""

    SOLUTION_URL = '/api/reansolutionpackage'
    WORKFLOW_URL = '/api/reanworkflowengine'
    NAME_REFERENCE = 'name'
    PROVIDER_DETAILS_REFERENCE = 'provider_details'
    PROVIDER_TYPE_REFERENCE = 'type'

    def __setattr__(self, attr, value):
        """__setattr__."""
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
