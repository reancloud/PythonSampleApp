"""Update Provider."""

import logging
import json
from cliff.command import Command
import test_sdk_client
from reantest.utility import Utility


class UpdateProvider(Command):
    """Update  provider."""

    log = logging.getLogger(__name__)
    _epilog = 'Example : \n\t rean-test update-provider --provider_name <provider_name>' \
              '--provider_type aws --provider_file_path <path_to provider_credential_file> ' \
              '--subnet_id <subnet_id> --security_group <security_group_id> --bucket_name <bucket_name> ' \
              '--instance_profile_name <instance_profile_name> --key_pair_name <keypair_name> ' \
              '--private_key_file_path <path_to_pem_file> --use_public_ip <true/false> --default_provider <true/false>'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(UpdateProvider, self).get_parser(prog_name)
        parser.add_argument('--provider_name', '-n', help='Set provider name', required=True)
        parser.add_argument('--provider_type', '-t', help='Set provider type', choices=['aws'])
        parser.add_argument('--provider_file_path', '-pd', help='Json file with applicable key-value pair for '
                                                                'provider type. File absolute path')
        parser.add_argument('--subnet_id', '-s', help='Subnet id to launch EC2 instances to perform testing')
        parser.add_argument('--security_group', '-sg', help='Security Group Id to associate to launched EC2 instance')
        parser.add_argument('--bucket_name', '-b', help='Bucket name to store REAN Test Report')
        parser.add_argument('--instance_profile_name', '-a', help='Instance Profile Name is used to '
                                                                  'upload reports to s3')
        parser.add_argument('--key_pair_name', '-k', help='Set key pair name')
        parser.add_argument('--private_key_file_path', '-pk', help='Private Key to connect to instance')
        parser.add_argument('--use_public_ip', '-p', help='Is Use Public IP for connecting test instance',
                            choices=['true', 'false'])
        parser.add_argument('--default_provider', '-d', help='Set true to set default provider, Default value is false',
                            choices=['true', 'false'])
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        try:
            self.log.debug(parsed_args)

            api_instance = test_sdk_client.ProviderApi(Utility.set_headers())
            old_provider = api_instance.get_provider_by_name(parsed_args.provider_name)

            if parsed_args.provider_type is not None:
                old_provider.provider_type = parsed_args.provider_type

            if parsed_args.subnet_id is not None:
                old_provider.subnet_id = parsed_args.subnet_id

            if parsed_args.security_group is not None:
                old_provider.security_group = parsed_args.security_group

            if parsed_args.bucket_name is not None:
                old_provider.bucket_name = parsed_args.bucket_name

            if parsed_args.instance_profile_name is not None:
                old_provider.test_instance_role = parsed_args.instance_profile_name

            if parsed_args.key_pair_name is not None:
                old_provider.key_pair_name = parsed_args.key_pair_name

            if parsed_args.provider_file_path is not None:
                with Utility.open_file(parsed_args.provider_file_path) as handle:
                    filedata = handle.read()
                    provider_details_json = json.loads(filedata)
                    old_provider.data = provider_details_json

            if parsed_args.private_key_file_path is not None:
                with Utility.open_file(parsed_args.private_key_file_path) as handle:
                    private_key = handle.read()
                    old_provider.private_key = private_key

            if parsed_args.use_public_ip is not None:
                old_provider.use_public_ip = parsed_args.use_public_ip

            if parsed_args.default_provider is not None:
                old_provider.default_provider = parsed_args.default_provider

            self.log.debug("Execution started for update provider")

            api_response = api_instance.update_provider(old_provider)

            self.log.debug(api_response)

            print("Provider Updated successfully.")
        except Exception as exception:
            Utility.print_exception(exception)
