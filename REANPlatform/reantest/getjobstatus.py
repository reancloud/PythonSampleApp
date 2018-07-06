import logging
from . import config
from . import utility
from cliff.command import Command

import test_sdk_client
from test_sdk_client.rest import ApiException
from ast import literal_eval
import json

from reanplatform.constants import Constants


class GetJobStatus(Command):
    log = logging.getLogger(__name__)

    "getjobstatus"
    def get_parser(self, prog_name):
        parser = super(GetJobStatus, self).get_parser(prog_name)

        # 'jobId': 'str',
        parser.add_argument('--job_id', '-j', help='Set Job Id to get Job status example:396f4cfc2c4d46c7921532741c7ab63e.', required=True)
        return parser

    def take_action(self, parsed_args):
        self.log.debug(parsed_args)

        try:
             apiInstance = test_sdk_client.RunTestApi()
             api_response = apiInstance.get_job_status(parsed_args.job_id)
             self.log.debug(api_response)
             print(api_response)
        except Exception as e:
             self.log.error("Exception when calling GetJobStatus->get_job_status: %s\n" % e)


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
