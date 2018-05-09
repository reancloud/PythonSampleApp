"Contains constats required for Utility"


class Constants(object):
    "Contains constats required for Utility"

    REAN_PLATFORM = 'reanplatform'
    REAN_SECRET_KEY = 'ReanPlatform@24'

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
