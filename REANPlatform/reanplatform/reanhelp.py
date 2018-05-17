"""Configure platform."""
import os
import io
import getpass
import logging
import yaml
from deploy_sdk_client.rest import ApiException
from cliff.command import Command


class Helpdeploy(Command):
    """Details of rean-deploy cli."""

    def get_parser(self, prog_name):
        """get_parser."""
    def take_action(self, parsed_args):
        """take_action."""


class Helptest(Command):
    """Details of rean-test cli."""

    def get_parser(self, prog_name):
        """get_parser."""
    def take_action(self, parsed_args):
        """take_action."""


class Helpmnc(Command):
    """Details of rean-mnc cli."""

    def get_parser(self, prog_name):
        """get_parser."""
    def take_action(self, parsed_args):
        """take_action."""
