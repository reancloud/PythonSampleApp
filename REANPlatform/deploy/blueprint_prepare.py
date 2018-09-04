"""Import blueprint module."""
import os
from os.path import basename
import logging
import json
import re
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from reanplatform.utilityconstants import PlatformConstants
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class PrepareBlueprint(Command):
    """Prepare input file for blueprint import."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(PrepareBlueprint, self).get_parser(prog_name)
        parser.add_argument(
            '--file', '-f',
            help='Blueprint file. REAN Deploy blueprint\
            file path. A path can be absolute path.',
            required=False
        )
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False
                           )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        blueprint_path = parsed_args.file
        attribute_path = os.getcwd() + '/' + 'import_blueprint_attributes.json'    # noqa: E501

        PrepareBlueprint.validate_parameters(attribute_path)

        PrepareBlueprint.blueprint_prepare(blueprint_path, attribute_path, parsed_args)       # noqa: E501

    @staticmethod
    def validate_parameters(file_path):
        """Validate cli parameters."""
        if file_path is None:
            raise RuntimeError("Please provide REAN Deploy\
                blueprint file absolute path")

    @staticmethod
    def blueprint_prepare(blueprint_path, attribute_path, parsed_args):     # noqa: E501
        """blueprint_prepare."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_env_instance = deploy_sdk_client.EnvironmentApi(api_client)
            blueprint_all_env = api_env_instance.prepare_import_blueprint(file=blueprint_path)     # noqa: E501

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
            Utility.print_output(re.sub(' +', ' ', msg), parsed_args.output, PlatformConstants.STR_REFERENCE)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)
