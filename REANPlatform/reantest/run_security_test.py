"""run_security_test."""
import logging
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class RunSecurityTest(Command):
    """Run security test."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(RunSecurityTest, self).get_parser(prog_name)

        parser.add_argument('--url', '-u', help='Set url To test example:http://www.google.com.', required=True)
        parser.add_argument('--security_test_type', '-t', help='Set Security test type example:@app_scan/@http_headers/@app_scan,@http_headers.', required=True)

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        self.log.debug(parsed_args)
        try:
            error_message = Utility.validate_security_test_inputs(parsed_args)
            if error_message:
                self.app.stdout.write(error_message)
                return

            body = test_sdk_client.SecurityTestDto()

            body.test_url = parsed_args.url
            body.type = "securitytest"
            body.security_test = True
            body.security_test_type = parsed_args.security_test_type
            body.execution_strategy = "security"
            self.log.debug(body)
            self.log.debug("Execution stared for Security Test")
            Utility.execute_test(body, parsed_args, self.log, test_sdk_client.RunJobsApi(Utility.set_headers()).submit_security_test_job)
        except Exception as exception:
            Utility.print_exception(exception)
