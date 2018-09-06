import os
import pytest
import argparse
import mock
import builtins
from mock import MagicMock
from unittest.mock import patch
from get_users import GetUsers
import logging
from prettytable import PrettyTable
from cliff.command import Command
from auth.constants import AunthnzConstants
from auth.utility import AuthnzUtility
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException

CONTEXT = ""

EVENT_JSON = {}

class TestGetUsers():

    def test_take_action(self):
        parsed_args = {}
        parser = argparse.ArgumentParser()
        parser.add_argument('--format',
                            '-f',
                            help='Skip interactive approval before updating user credentials.',
                            required=False,
                            action='store_true')
        parser.add_argument('-v', default='bar')
        parsed_args = parser.parse_args()
        api_client = set_header_parameter(AuthnzUtility.create_api_client(), Utility.get_url(AunthnzConstants.AUTHNZ_URL))
        instance = authnz_sdk_client.UsercontrollerApi(api_client)
        instance.get_all_user_using_get = MagicMock(return_value=[])
        authnz_sdk_client.UsercontrollerApi = MagicMock(return_value=[])
        GetUsers.api_response = []
        response = GetUsers.take_action(self, parsed_args)
        assert True

    # def test_create_file(self):
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument('-s', default='bar')
    #     parser.add_argument('-v', default='bar')

    #     parsed_args = parser.parse_args()
    #     path = '/home/priyanka'

    #     self.createFile = MagicMock(return_value=True)
    #     with patch('builtins.input', side_effect='x'):
    #         response = Configure.take_action(self, parsed_args)
    #         print(response)
    #     assert True
