"""Create Provider."""
import logging
import json
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class CreateProvider(Command):
    """Create Provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(CreateProvider, self).get_parser(prog_name)
        parser.add_argument('--provider_name', '-n', help='Set provider name', required=True)
        parser.add_argument('--provider_type', '-t', help='Set provider type. Example:AWS', required=True)
        parser.add_argument('--provider_details', '-pd', help='Json file with applicable key-value pair for provider type. File absolute path', required=True)
        parser.add_argument('--instance_profile_arn', '-a', help='Set Instance profile ARN', required=True)
        parser.add_argument('--subnet_id', '-s', help='Set subnet Id', required=True)
        parser.add_argument('--security_group', '-sg', help='Set security group', required=True)
        parser.add_argument('--key_pair_name', '-k', help='Set kep pair name', required=True)
        parser.add_argument('--bucket_name', '-b', help='Set Bucket name', required=True)
        parser.add_argument('--instance_profile_role', '-r', help='Set Instance profile role', required=True)
        parser.add_argument('--use_public_ip', '-p', help='Set true to use public ip, Default value is false', default=False)
        parser.add_argument('--default_provider', '-d', help='Set true to set default provider, Default value is false', default=False)
        parser.add_argument('--private_key', '-pk', help='Private Key to connect to instance', required=True)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            self.log.debug(parsed_args)

            with Utility.open_file(parsed_args.provider_details) as handle:
                filedata = handle.read()

            provider_details_json = json.loads(filedata)

            with Utility.open_file(parsed_args.private_key) as handle:
                private_key = handle.read()

            body = test_sdk_client.ProviderDto(
                name=parsed_args.provider_name,
                type=parsed_args.provider_type,
                data=provider_details_json
            )

            body.instance_profile_arn = parsed_args.instance_profile_arn
            body.subnet_id = parsed_args.subnet_id
            body.security_group_id = parsed_args.security_group
            body.key_pair_name = parsed_args.key_pair_name
            body.bucket_name = parsed_args.bucket_name
            body.test_instance_role = parsed_args.instance_profile_role
            body.use_public_ip = parsed_args.use_public_ip
            body.default_provider = parsed_args.default_provider
            body.private_key = private_key

            self.log.debug(body)

            self.log.debug("Execution stared for create provider")
            api_instance = test_sdk_client.ProviderApi(Utility.set_headers())
            api_response = api_instance.save_provider(body)

            self.log.debug(api_response)

        except Exception as exception:
            Utility.print_exception(exception)
