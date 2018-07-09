# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class MultiSharePolicy(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'ids': 'list[int]',
        'share_policy': 'SharePolicy'
    }

    attribute_map = {
        'ids': 'ids',
        'share_policy': 'sharePolicy'
    }

    def __init__(self, ids=None, share_policy=None):
        """
        MultiSharePolicy - a model defined in Swagger
        """

        self._ids = None
        self._share_policy = None

        if ids is not None:
          self.ids = ids
        if share_policy is not None:
          self.share_policy = share_policy

    @property
    def ids(self):
        """
        Gets the ids of this MultiSharePolicy.

        :return: The ids of this MultiSharePolicy.
        :rtype: list[int]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """
        Sets the ids of this MultiSharePolicy.

        :param ids: The ids of this MultiSharePolicy.
        :type: list[int]
        """

        self._ids = ids

    @property
    def share_policy(self):
        """
        Gets the share_policy of this MultiSharePolicy.

        :return: The share_policy of this MultiSharePolicy.
        :rtype: SharePolicy
        """
        return self._share_policy

    @share_policy.setter
    def share_policy(self, share_policy):
        """
        Sets the share_policy of this MultiSharePolicy.

        :param share_policy: The share_policy of this MultiSharePolicy.
        :type: SharePolicy
        """

        self._share_policy = share_policy

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, MultiSharePolicy):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
