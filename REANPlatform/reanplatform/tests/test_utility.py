import os
import unittest
import pytest
import argparse
import mock
import builtins
from mock import MagicMock
from unittest.mock import patch
from reanplatform.utility import Utility

CONTEXT = ""

EVENT_JSON = {}

class TestUtility():

    def test_get_url(self):
        host_url = '/api'
        response = Utility.get_url(host_url)
        print(response)
        assert response == 'https://52.61.49.36/api'
