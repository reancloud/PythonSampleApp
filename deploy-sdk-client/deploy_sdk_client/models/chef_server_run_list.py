# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ChefServerRunList(object):
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
        'id': 'int',
        'environment': 'str',
        'items': 'list[ChefServerRunListItem]'
    }

    attribute_map = {
        'id': 'id',
        'environment': 'environment',
        'items': 'items'
    }

    def __init__(self, id=None, environment=None, items=None):
        """
        ChefServerRunList - a model defined in Swagger
        """

        self._id = None
        self._environment = None
        self._items = None

        if id is not None:
          self.id = id
        if environment is not None:
          self.environment = environment
        if items is not None:
          self.items = items

    @property
    def id(self):
        """
        Gets the id of this ChefServerRunList.

        :return: The id of this ChefServerRunList.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ChefServerRunList.

        :param id: The id of this ChefServerRunList.
        :type: int
        """

        self._id = id

    @property
    def environment(self):
        """
        Gets the environment of this ChefServerRunList.

        :return: The environment of this ChefServerRunList.
        :rtype: str
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """
        Sets the environment of this ChefServerRunList.

        :param environment: The environment of this ChefServerRunList.
        :type: str
        """

        self._environment = environment

    @property
    def items(self):
        """
        Gets the items of this ChefServerRunList.

        :return: The items of this ChefServerRunList.
        :rtype: list[ChefServerRunListItem]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this ChefServerRunList.

        :param items: The items of this ChefServerRunList.
        :type: list[ChefServerRunListItem]
        """

        self._items = items

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
        if not isinstance(other, ChefServerRunList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
