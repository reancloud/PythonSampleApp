"""Utility class for authnz."""


class AuthnzUtility(object):
    """Utility class contains all common method requried for Authnz CLI."""

    @staticmethod
    def get_user_dict(user):
        """Return dictionary of user details."""
        dict_object = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'verified': user.verified,
            'disabled': user.disabled
        }
        return dict_object
