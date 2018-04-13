import logging
from cliff.command import Command


class Configure(Command):
    log = logging.getLogger(__name__)

    "Configure"

    def get_parser(self, prog_name):
        parser = super(Configure, self).get_parser(prog_name)

        parser.add_argument(
            '--configuration-bucket', help='Managed Cloud CLI configuration bucket', action="store", required=True)
        parser.add_argument(
            '--deploy-endpoint', help='REANDeploy endpoint', action="store", required=False)
        parser.add_argument(
            '--deploy-api-key', help='REANDeploy API key', action="store", required=False)
        parser.add_argument(
            '--deploy-group', help='REANDeploy group for Managed Cloud', action="store", required=False)
        parser.add_argument(
            '--master-provider', help='REANDeploy provider for Managed Cloud AWS master account', action="store", required=False)
        parser.add_argument(
            '--artifactory-bucket', help='Managed Cloud artifactory S3 bucket', action="store", required=False)

        return parser

    def take_action(self, parsed_args):
        print(self.app)
