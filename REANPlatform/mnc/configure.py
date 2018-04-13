import logging
import json
from cliff.command import Command


class Configure(Command):
    log = logging.getLogger(__name__)

    "Configure"

    def get_parser(self, prog_name):
        parser = super(Configure, self).get_parser(prog_name)

        # 'jobId': 'str',
        parser.add_argument(
            '--job_id', '-j', help='Set Job Id to get Job status example:396f4cfc2c4d46c7921532741c7ab63e.', required=True)
        return parser

    def take_action(self, parsed_args):
        return True
