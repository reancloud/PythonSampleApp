# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class EnvironmentPolicy(object):
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
        'env_id': 'int',
        'env_permission': 'list[object]'
    }

    attribute_map = {
        'env_id': 'envId',
        'env_permission': 'envPermission'
    }

    def __init__(self, env_id=None, env_permission=None):
        """
        EnvironmentPolicy - a model defined in Swagger
        """

        self._env_id = None
        self._env_permission = None

        if env_id is not None:
          self.env_id = env_id
        if env_permission is not None:
          self.env_permission = env_permission

    @property
    def env_id(self):
        """
        Gets the env_id of this EnvironmentPolicy.
        Environment id

        :return: The env_id of this EnvironmentPolicy.
        :rtype: int
        """
        return self._env_id

    @env_id.setter
    def env_id(self, env_id):
        """
        Sets the env_id of this EnvironmentPolicy.
        Environment id

        :param env_id: The env_id of this EnvironmentPolicy.
        :type: int
        """

        self._env_id = env_id

    @property
    def env_permission(self):
        """
        Gets the env_permission of this EnvironmentPolicy.
        List allowed permissions on Environment

        :return: The env_permission of this EnvironmentPolicy.
        :rtype: list[object]
        """
        return self._env_permission

    @env_permission.setter
    def env_permission(self, env_permission):
        """
        Sets the env_permission of this EnvironmentPolicy.
        List allowed permissions on Environment

        :param env_permission: The env_permission of this EnvironmentPolicy.
        :type: list[object]
        """

        self._env_permission = env_permission

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
        if not isinstance(other, EnvironmentPolicy):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
