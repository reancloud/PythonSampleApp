"""Import blueprint module."""
import os
import logging
import json
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.constants import Constants
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from os.path import basename


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
        attribute_path = os.getcwd() + '/' + 'import_blueprint_attributes.json'

        self.validate_parameters(blueprint_path, attribute_path)

        self.blueprint_import(blueprint_path, attribute_path)    # noqa: E501

    def validate_parameters(self, blueprint_path, attribute_path):
        """Validate cli parameters."""
        if blueprint_path is None and attribute_path is None:
            raise RuntimeError("Please provide REAN Deploy\
                blueprint file and attributes file absolute path")

    def blueprint_import(self, blueprint_path, attribute_path):      # noqa: E501
        """blueprint_import."""
        try:
            api_env_instance = deploy_sdk_client.EnvironmentApi()
            env_instance = set_header_parameter(api_env_instance)
            blueprint_all_env = env_instance.prepare_import_blueprint(file=blueprint_path)   # noqa: E501
            os.chdir(os.path.dirname(attribute_path))
            with open(basename(attribute_path), "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            index = 0

            # Read data from blueprint
            for one_env in blueprint_all_env.environment_imports:
                key = one_env.import_config.name+one_env.import_config.env_version   # noqa: E501

                # Data load from prepar blueprint attribute file
                for blueprint_attribute_key in jsondata:
                    if blueprint_attribute_key == key:
                        if (jsondata[blueprint_attribute_key]['connection_id'] and jsondata[blueprint_attribute_key]['provider_id']):     # noqa: E501
                            blueprint_all_env.environment_imports[index].import_config.connection_id = jsondata[blueprint_attribute_key]['connection_id']    # noqa: E501
                            blueprint_all_env.environment_imports[index].import_config.provider_id = jsondata[blueprint_attribute_key]['provider_id']   # noqa: E501
                            blueprint_all_env.environment_imports[index].import_config.name = jsondata[blueprint_attribute_key]['name']    # noqa: E501
                            blueprint_all_env.environment_imports[index].import_config.description = jsondata[blueprint_attribute_key]['description']     # noqa: E501
                            index = index + 1
                        else:
                            raise RuntimeError("Connection_id and provider_id are\
                                missing to %s environment in the file location %s:\
                                " % (blueprint_all_env.environment_imports[index].import_config.name, attribute_path))  # noqa: E501

            env_instance.import_blueprint(body=blueprint_all_env)
            print("Blueprint imported successfully")

        except ApiException as e:
            Utility.print_exception(e)