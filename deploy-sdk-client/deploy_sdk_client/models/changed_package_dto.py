# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ChangedPackageDto(object):
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
        'name': 'str',
        'old_sequence': 'int',
        'new_sequence': 'int',
        'change_attributes': 'list[ChangedAttributeDto]'
    }

    attribute_map = {
        'name': 'name',
        'old_sequence': 'oldSequence',
        'new_sequence': 'newSequence',
        'change_attributes': 'changeAttributes'
    }

    def __init__(self, name=None, old_sequence=None, new_sequence=None, change_attributes=None):
        """
        ChangedPackageDto - a model defined in Swagger
        """

        self._name = None
        self._old_sequence = None
        self._new_sequence = None
        self._change_attributes = None

        if name is not None:
          self.name = name
        if old_sequence is not None:
          self.old_sequence = old_sequence
        if new_sequence is not None:
          self.new_sequence = new_sequence
        if change_attributes is not None:
          self.change_attributes = change_attributes

    @property
    def name(self):
        """
        Gets the name of this ChangedPackageDto.

        :return: The name of this ChangedPackageDto.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ChangedPackageDto.

        :param name: The name of this ChangedPackageDto.
        :type: str
        """

        self._name = name

    @property
    def old_sequence(self):
        """
        Gets the old_sequence of this ChangedPackageDto.

        :return: The old_sequence of this ChangedPackageDto.
        :rtype: int
        """
        return self._old_sequence

    @old_sequence.setter
    def old_sequence(self, old_sequence):
        """
        Sets the old_sequence of this ChangedPackageDto.

        :param old_sequence: The old_sequence of this ChangedPackageDto.
        :type: int
        """

        self._old_sequence = old_sequence

    @property
    def new_sequence(self):
        """
        Gets the new_sequence of this ChangedPackageDto.

        :return: The new_sequence of this ChangedPackageDto.
        :rtype: int
        """
        return self._new_sequence

    @new_sequence.setter
    def new_sequence(self, new_sequence):
        """
        Sets the new_sequence of this ChangedPackageDto.

        :param new_sequence: The new_sequence of this ChangedPackageDto.
        :type: int
        """

        self._new_sequence = new_sequence

    @property
    def change_attributes(self):
        """
        Gets the change_attributes of this ChangedPackageDto.

        :return: The change_attributes of this ChangedPackageDto.
        :rtype: list[ChangedAttributeDto]
        """
        return self._change_attributes

    @change_attributes.setter
    def change_attributes(self, change_attributes):
        """
        Sets the change_attributes of this ChangedPackageDto.

        :param change_attributes: The change_attributes of this ChangedPackageDto.
        :type: list[ChangedAttributeDto]
        """

        self._change_attributes = change_attributes

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
        if not isinstance(other, ChangedPackageDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
