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
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        file_path = parsed_args.file
        attribute_file = 'import_blueprint_attributes.txt'
        dir_path = os.getcwd()

        self.validate_parameters(file_path)

        self.blueprint_prepare(file_path, dir_path, attribute_file)       # noqa: E501

    def validate_parameters(self, file_path):
        """Validate cli parameters."""
        if file_path is None:
            raise RuntimeError("Please provide REAN Deploy\
                blueprint file absolute path")

    def blueprint_prepare(self, file_path, dir_path, attribute_file):     # noqa: E501
        """blueprint_prepare."""
        try:
            api_env_instance = deploy_sdk_client.EnvironmentApi()
            env_instance = set_header_parameter(api_env_instance)
            blueprint_all_env = env_instance.prepare_import_blueprint(file=file_path)     # noqa: E501

            prepare_data = []
            for one_env in blueprint_all_env.environment_imports:
                default_data = {}
                default_data = {
                    one_env.import_config.name+one_env.import_config.env_version:       # noqa: E501
                        {
                            'name': one_env.import_config.name,
                            'connection_id': one_env.import_config.connection_id,       # noqa: E501
                            'provider_id': one_env.import_config.provider_id,
                            'env_version': one_env.import_config.env_version,
                            'description': one_env.import_config.description
                        }
                    }

                prepare_data.append(default_data)

            os.chdir(dir_path)
            with open(attribute_file, 'w') as outfile:
                json.dump(prepare_data, outfile)

            print("Blueprint attributes file created successfully...\
                Please update the attributes in %s before\
                import a blueprint" % (dir_path + '/' + attribute_file))
        except ApiException as e:
            Utility.print_exception(e)
