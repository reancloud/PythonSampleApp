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


class ImportBlueprint(Command):
    """Import the REAN Deploy blueprint."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ImportBlueprint, self).get_parser(prog_name)
        parser.add_argument(
                            '--file', '-f',
                            help='Blueprint file. REAN Deploy blueprint\
                            file path. A path can be absolute path.',
                            required=False
                            )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        file_path = parsed_args.file
        attribute_file = 'import_blueprint_attributes.txt'
        dir_path = os.getcwd()

        self.validate_parameters(file_path)

        self.blueprint_import(file_path, dir_path, attribute_file)    # noqa: E501

    def validate_parameters(self, file_path):
        """Validate cli parameters."""
        if file_path is None:
            raise RuntimeError("Please provide REAN Deploy\
                blueprint file absolute path")

    def blueprint_import(self, file_path, dir_path, attribute_file):      # noqa: E501
        """blueprint_import."""
        try:
            api_env_instance = deploy_sdk_client.EnvironmentApi()
            env_instance = set_header_parameter(api_env_instance)
            blueprint_all_env = env_instance.prepare_import_blueprint(file=file_path)   # noqa: E501
            os.chdir(dir_path)
            with open(attribute_file, "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            index = 0

            # Read data from blueprint
            for one_env in blueprint_all_env.environment_imports:
                key = one_env.import_config.name+one_env.import_config.env_version   # noqa: E501

                # Data load from prepar blueprint attribute file
                for blueprint_data_to_update in jsondata:
                    for env_name_ver_key in blueprint_data_to_update:

                        if env_name_ver_key == key:
                            if blueprint_data_to_update[env_name_ver_key]['connection_id'] and blueprint_data_to_update[env_name_ver_key]['provider_id']:    # noqa: E501
                                blueprint_all_env.environment_imports[index].import_config.connection_id = blueprint_data_to_update[env_name_ver_key]['connection_id']    # noqa: E501
                                blueprint_all_env.environment_imports[index].import_config.provider_id = blueprint_data_to_update[env_name_ver_key]['provider_id']   # noqa: E501
                                blueprint_all_env.environment_imports[index].import_config.name = blueprint_data_to_update[env_name_ver_key]['name']    # noqa: E501
                                blueprint_all_env.environment_imports[index].import_config.description = blueprint_data_to_update[env_name_ver_key]['description']     # noqa: E501
                                index = index + 1
                            else:
                                raise RuntimeError("Please provide connection_id and provider_id in the file location %s:" % (dir_path + '/' + attribute_file))  # noqa: E501

            env_instance.import_blueprint(body=blueprint_all_env)
            print("Blueprint imported successfully")
        except ApiException as e:
            Utility.print_exception(e)
