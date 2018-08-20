import os
import pytest
import argparse
import mock
import builtins
from mock import MagicMock
from unittest.mock import patch
from reanplatform.configure import Configure

CONTEXT = ""

EVENT_JSON = {}

class TestConfigure():

    def test_take_action(self):
        parsed_args = {}
        path = '/home/priyanka'
        # self.createFile = MagicMock(return_value=True)
        parser = argparse.ArgumentParser()
        parser.add_argument('--auto_approve',
                            '-y',
                            help='Skip interactive approval before updating user credentials.',
                            required=False,
                            action='store_true')
        parser.add_argument('-s', default='bar')
        parser.add_argument('-v', default='bar')
        parsed_args = parser.parse_args()
        with patch('builtins.input', side_effect='x'):
            response = Configure.createFile(self, parsed_args, path)
        assert True

    def test_create_file(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--auto_approve',
                            '-y',
                            help='Skip interactive approval before updating user credentials.',
                            required=False,
                            action='store_true')
        parser.add_argument('-s', default='bar')
        parser.add_argument('-v', default='bar')
        # parser.add_argument('tests/test_configure.py', default='bar', required=False)
        parsed_args = parser.parse_args()
        path = '/home/priyanka'

        self.createFile = MagicMock(return_value=True)
        with patch('builtins.input', side_effect='x'):
            response = Configure.take_action(self, parsed_args)
            print(response)
        assert True
