# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class TFResource(object):
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
        'type': 'str',
        'id': 'str',
        'tags': 'dict(str, str)',
        'other_attributes': 'dict(str, str)',
        'status': 'str',
        'ref_id': 'int'
    }

    attribute_map = {
        'name': 'name',
        'type': 'type',
        'id': 'id',
        'tags': 'tags',
        'other_attributes': 'otherAttributes',
        'status': 'status',
        'ref_id': 'refId'
    }

    def __init__(self, name=None, type=None, id=None, tags=None, other_attributes=None, status=None, ref_id=None):
        """
        TFResource - a model defined in Swagger
        """

        self._name = None
        self._type = None
        self._id = None
        self._tags = None
        self._other_attributes = None
        self._status = None
        self._ref_id = None

        if name is not None:
          self.name = name
        if type is not None:
          self.type = type
        if id is not None:
          self.id = id
        if tags is not None:
          self.tags = tags
        if other_attributes is not None:
          self.other_attributes = other_attributes
        if status is not None:
          self.status = status
        if ref_id is not None:
          self.ref_id = ref_id

    @property
    def name(self):
        """
        Gets the name of this TFResource.

        :return: The name of this TFResource.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this TFResource.

        :param name: The name of this TFResource.
        :type: str
        """

        self._name = name

    @property
    def type(self):
        """
        Gets the type of this TFResource.

        :return: The type of this TFResource.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this TFResource.

        :param type: The type of this TFResource.
        :type: str
        """

        self._type = type

    @property
    def id(self):
        """
        Gets the id of this TFResource.

        :return: The id of this TFResource.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this TFResource.

        :param id: The id of this TFResource.
        :type: str
        """

        self._id = id

    @property
    def tags(self):
        """
        Gets the tags of this TFResource.

        :return: The tags of this TFResource.
        :rtype: dict(str, str)
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this TFResource.

        :param tags: The tags of this TFResource.
        :type: dict(str, str)
        """

        self._tags = tags

    @property
    def other_attributes(self):
        """
        Gets the other_attributes of this TFResource.

        :return: The other_attributes of this TFResource.
        :rtype: dict(str, str)
        """
        return self._other_attributes

    @other_attributes.setter
    def other_attributes(self, other_attributes):
        """
        Sets the other_attributes of this TFResource.

        :param other_attributes: The other_attributes of this TFResource.
        :type: dict(str, str)
        """

        self._other_attributes = other_attributes

    @property
    def status(self):
        """
        Gets the status of this TFResource.

        :return: The status of this TFResource.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this TFResource.

        :param status: The status of this TFResource.
        :type: str
        """

        self._status = status

    @property
    def ref_id(self):
        """
        Gets the ref_id of this TFResource.

        :return: The ref_id of this TFResource.
        :rtype: int
        """
        return self._ref_id

    @ref_id.setter
    def ref_id(self, ref_id):
        """
        Sets the ref_id of this TFResource.

        :param ref_id: The ref_id of this TFResource.
        :type: int
        """

        self._ref_id = ref_id

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
        if not isinstance(other, TFResource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
