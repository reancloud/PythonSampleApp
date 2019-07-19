"""run_security_test."""
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunSecurityTest(Command):
    """Run security test."""

    log = logging.getLogger(__name__)
    _description = 'Run Security test'
    _epilog = 'Example : rean-test run-security-test -n <name> -u <url> -p AppScan'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunSecurityTest, self).get_parser(prog_name)

        parser.add_argument('--name', '-n', help='Set the name for this Job.', required=True)
        parser.add_argument('--url', '-u', help='Set url To test example:http://www.google.com.', required=True)
        parser.add_argument('--security_packs', '-p', choices=['AppScan', 'HttpHeader', 'All'],
                            help='Set Security packs', required=True)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            # add validation

            security_packs_list = []
            if parsed_args.security_packs == 'AppScan':
                security_packs_list.append('AppScan')
            elif parsed_args.security_packs == 'HttpHeader':
                security_packs_list.append('HttpHeader')
            elif parsed_args.security_packs == 'All':
                security_packs_list.append('AppScan')
                security_packs_list.append('HttpHeader')

            security_test_dto_new = test_sdk_client.SecurityTestDtoNew()

            security_test_dto_new.test_url = parsed_args.url
            security_test_dto_new.name = parsed_args.name
            security_test_dto_new.security_pack = security_packs_list
            self.log.debug(security_test_dto_new)
            self.log.debug("Execution stared for Security Test")

            response_security_test_dto_new = test_sdk_client.RunTestNewApi(Utility.set_headers()).run_security_test(security_test_dto_new)

            job_id = response_security_test_dto_new.id

            self.log.debug("Response is------------: %s ", job_id)
            print("The request URL test submitted successfully. Job Id is : ", job_id)

            if job_id is not None and hasattr(parsed_args, 'wait') and parsed_args.wait == "true":
                api_instance = test_sdk_client.RunTestApi(Utility.set_headers())
                Utility.wait_while_job_running(api_instance, job_id)

        except Exception as exception:
            Utility.print_exception(exception)
