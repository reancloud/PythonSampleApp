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
from deploy.constants import DeployConstants


class ImportBlueprint(Command):
    """Import the REAN Deploy blueprint."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ImportBlueprint, self).get_parser(prog_name)
        parser.add_argument(
            '--blueprint_file', '-b_file',
            help='Blueprint file. REAN Deploy blueprint\
            file path. A path can be absolute path.',
            required=True
        )
        parser.add_argument(
            '--attribute_file', '-a_file',
            help='Blueprint attributes. REAN Deploy blueprint\
            attributes file path. A path can be absolute\
            path.', required=True
        )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        blueprint_path = parsed_args.blueprint_file
        attribute_path = parsed_args.attribute_file

        ImportBlueprint.validate_parameters(blueprint_path, attribute_path)

        ImportBlueprint.blueprint_import(blueprint_path, attribute_path)    # noqa: E501

    @staticmethod
    def validate_parameters(blueprint_path, attribute_path):
        """Validate cli parameters."""
        if blueprint_path is None and attribute_path is None:
            raise RuntimeError("Please provide REAN Deploy\
                blueprint file and attributes file absolute path")

    @staticmethod
    def blueprint_import(blueprint_path, attribute_path):      # noqa: E501
        """blueprint_import."""
        try:
            api_env_instance = deploy_sdk_client.EnvironmentApi()
            env_instance = set_header_parameter(api_env_instance, Utility.get_url(DeployConstants.DEPLOY_URL))
            blueprint_all_env = env_instance.prepare_import_blueprint(file=blueprint_path)   # noqa: E501
            os.chdir(os.path.dirname(attribute_path))
            with open(basename(attribute_path), "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            index = 0
            env_names = []

            # Read data from blueprint
            for one_env in blueprint_all_env.environment_imports:
                key = one_env.import_config.name + '-' + one_env.import_config.env_version   # noqa: E501

                # Data load from prepar blueprint attribute file
                for blueprint_attribute_key in jsondata:
                    if blueprint_attribute_key == key:
                        if (jsondata[blueprint_attribute_key]['connection_id'] and jsondata[blueprint_attribute_key]['provider_id']):     # noqa: E501
                            blueprint_all_env.environment_imports[index].import_config.connection_id = jsondata[blueprint_attribute_key]['connection_id']    # noqa: E501
                            blueprint_all_env.environment_imports[index].import_config.provider_id = jsondata[blueprint_attribute_key]['provider_id']   # noqa: E501
                            blueprint_all_env.environment_imports[index].import_config.name = jsondata[blueprint_attribute_key]['name']    # noqa: E501
                            blueprint_all_env.environment_imports[index].import_config.description = jsondata[blueprint_attribute_key]['description']     # noqa: E501
                            env_names.append(blueprint_all_env.environment_imports[index].import_config.name)           # noqa: E501
                            index = index + 1
                        else:
                            exception_msg = "Connection_id and provider_id are\
                                missing to %s environment in the file\
                                 location %s: " % (blueprint_all_env.environment_imports[index].import_config.name, attribute_path)   # noqa: E501
                            raise RuntimeError(re.sub(' +', ' ', exception_msg))  # noqa: E501

            env_instance.import_blueprint(body=blueprint_all_env)
            print("Blueprint imported successfully. Environment names : ", env_names)       # noqa: E501

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
