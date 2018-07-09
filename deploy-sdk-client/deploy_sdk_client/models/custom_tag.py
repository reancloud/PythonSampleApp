# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class CustomTag(object):
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
        'name': 'str',
        'description': 'str',
        'tags': 'object'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'tags': 'tags'
    }

    def __init__(self, id=None, name=None, description=None, tags=None):
        """
        CustomTag - a model defined in Swagger
        """

        self._id = None
        self._name = None
        self._description = None
        self._tags = None

        if id is not None:
          self.id = id
        self.name = name
        if description is not None:
          self.description = description
        self.tags = tags

    @property
    def id(self):
        """
        Gets the id of this CustomTag.

        :return: The id of this CustomTag.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CustomTag.

        :param id: The id of this CustomTag.
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this CustomTag.
        Unique name for Custom Tag

        :return: The name of this CustomTag.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CustomTag.
        Unique name for Custom Tag

        :param name: The name of this CustomTag.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this CustomTag.
        Description for Custom Tag

        :return: The description of this CustomTag.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CustomTag.
        Description for Custom Tag

        :param description: The description of this CustomTag.
        :type: str
        """

        self._description = description

    @property
    def tags(self):
        """
        Gets the tags of this CustomTag.
        Tags json for Custom Tag

        :return: The tags of this CustomTag.
        :rtype: object
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this CustomTag.
        Tags json for Custom Tag

        :param tags: The tags of this CustomTag.
        :type: object
        """
        if tags is None:
            raise ValueError("Invalid value for `tags`, must not be `None`")

        self._tags = tags

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
        if not isinstance(other, CustomTag):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
