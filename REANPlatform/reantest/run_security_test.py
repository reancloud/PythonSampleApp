"""run_security_test."""
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunSecurityTest(Command):
    """Run security test."""

    log = logging.getLogger(__name__)
    _description = 'Run Security test'
    _epilog = 'Example : rean-test run-security-test -n <name> -u <url> -p AppScan -w true'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunSecurityTest, self).get_parser(prog_name)

        parser.add_argument('--name', '-n', help='Set the name for this Job.', required=True)
        parser.add_argument('--url', '-u', help='Set url To test example:http://www.google.com.', required=True)
        parser.add_argument('--security_packs', '-p', choices=['AppScan', 'HttpHeader', 'All'],
                            help='Set Security packs', required=True)

        parser.add_argument('--spider_depth', '-sd', help='Set spider depth', default=0, required=False)
        parser.add_argument('--use_ajax_spider', '-as', action='store_true',
                            help='Set to use ajax spider', default=False)

        parser.add_argument('--username', '-un', help='Set User name', required=False)
        parser.add_argument('--password', '-pw', help='Set password', required=False)
        parser.add_argument('--username_field_xpath', '-ux', help='Set username field xpath', required=False)
        parser.add_argument('--password_field_xpath', '-px', help='Set password field xpath', required=False)
        parser.add_argument('--submit_button_xpath', '-bx', help='Set submit button xpath', required=False)
        parser.add_argument('--login_url', '-li', help='Set login url', required=False)
        parser.add_argument('--logout_url', '-lo', help='Set logout url', required=False)

        parser.add_argument('--export_jobid_path', '-ej', help='Export job id to file absolute path.')
        parser.add_argument('--wait', '-w', action='store_true', help='Wait until job finish', default=False)

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

            if parsed_args.username is not None and (parsed_args.password is None or parsed_args.username_field_xpath is None or parsed_args.password_field_xpath is None or parsed_args.submit_button_xpath is None):
                raise RuntimeError('Invalid login details')

            security_test_dto_new = test_sdk_client.SecurityTestDtoOld()

            security_test_dto_new.test_url = parsed_args.url
            security_test_dto_new.name = parsed_args.name
            security_test_dto_new.security_pack = security_packs_list
            security_test_dto_new.spider_depth = parsed_args.spider_depth
            security_test_dto_new.ajax_spider = parsed_args.use_ajax_spider

            if parsed_args.username:
                security_test_dto_new.username = parsed_args.username
                security_test_dto_new.password = parsed_args.password

                security_test_login_url_detail_dto = test_sdk_client.SecurityTestLoginUrlDetailDtoOld()

                security_test_login_url_detail_dto.username_field_xpath = parsed_args.username_field_xpath
                security_test_login_url_detail_dto.password_field_xpath = parsed_args.password_field_xpath
                security_test_login_url_detail_dto.submit_button_xpath = parsed_args.submit_button_xpath
                security_test_login_url_detail_dto.login_url = parsed_args.login_url
                security_test_login_url_detail_dto.logout_url = parsed_args.logout_url

                security_test_dto_new.url_login_detail = security_test_login_url_detail_dto

            self.log.debug(security_test_dto_new)
            self.log.debug("Execution stared for Security Test")

            response_security_test_dto_new = test_sdk_client.TestbackwardscompatibilitycontrollerApi(
                Utility.set_headers()).run_security_test_using_post1(security_test_dto_new)
            job_id = ''
            if response_security_test_dto_new.id:
                job_id = response_security_test_dto_new.id

            self.log.debug("Response is------------: %s ", job_id)
            Utility.export_jobid(parsed_args.name, job_id, parsed_args.export_jobid_path)
            print("The request Security test submitted successfully. Job Id is : ", job_id)

            if parsed_args.wait:
                Utility.wait_while_job_running(job_id)

        except Exception as exception:
            Utility.print_exception(exception)
