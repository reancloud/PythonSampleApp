"""Import blueprint module."""
import os
import logging
import json
import re
from os.path import basename
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class PrepareBlueprint(Command):
    """Prepare input file for blueprint import."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(PrepareBlueprint, self).get_parser(prog_name)
        parser.add_argument(
            '--file', '-f', help='Blueprint file. REAN Deploy blueprint file path. A path can be absolute path.', required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        blueprint_path = parsed_args.file
        attribute_path = os.getcwd() + '/' + 'import_blueprint_attributes.json'    # noqa: E501

        PrepareBlueprint.validate_parameters(attribute_path)

        PrepareBlueprint.blueprint_prepare(blueprint_path, attribute_path)       # noqa: E501

    @staticmethod
    def validate_parameters(file_path):
        """Validate cli parameters."""
        if file_path is None:
            raise RuntimeError("Please provide REAN Deploy\
                blueprint file absolute path")

    @staticmethod
    def blueprint_prepare(blueprint_path, attribute_path):     # noqa: E501
        """blueprint_prepare."""
        try:
            api_env_instance = deploy_sdk_client.EnvironmentApi()
            env_instance = set_header_parameter(api_env_instance)
            blueprint_all_env = env_instance.prepare_import_blueprint(file=blueprint_path)     # noqa: E501

            prepare_data = {}
            for one_env in blueprint_all_env.environment_imports:
                prepare_data[one_env.import_config.name + '-' + one_env.import_config.env_version] = {  # noqa: E501
                          'name': one_env.import_config.name,
                          'connection_id': one_env.import_config.connection_id,
                          'provider_id': one_env.import_config.provider_id,
                          'env_version': one_env.import_config.env_version,
                          'description': one_env.import_config.description
                          }
            os.chdir(os.path.dirname(attribute_path))
            with open(basename(attribute_path), 'w') as outfile:
                json.dump(prepare_data, outfile, indent=4, sort_keys=True)
            msg = "Blueprint attributes file created successfully.\
                Before import a blueprint, Update the blueprint attributes\
                in file: " + (attribute_path)
            print(re.sub(' +', ' ', msg))
        except ApiException as e:
            Utility.print_exception(e)
