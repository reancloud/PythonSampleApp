"""Import blueprint module."""
import os
from pprint import pprint
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.constants import Constants
import json
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class Blueprint(Command):
    """ImportBlueprint."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(Blueprint, self).get_parser(prog_name)
        blueprint_parser = parser.add_subparsers(help='Blueprint sub-commands')  # noqa: E501

        blueprint_prepare = blueprint_parser.add_parser(
                                                        "prepare",
                                                        help="Create a\
                                                        attribute file for\
                                                        blueprint,\
                                                        Usage:[rean-deploy\
                                                        blueprint prepare\
                                                        --file blueprint_path]\n"      # noqa: E501
                                                    )
        blueprint_prepare.add_argument(
                                        '--file', '-f',
                                        help='Blueprint file',
                                        required=False
                                    )
        blueprint_prepare.add_argument(
                                        'action', nargs='?',
                                        type=str,
                                        default='prepare',
                                        help='Prepare command\
                                        default action'
                                    )

        blueprint_import = blueprint_parser.add_parser(
                                                        "import",
                                                        help='Import the blueprint\
                                                        Usage:[rean-deploy\
                                                        blueprint import\
                                                        --file blueprint_path]'
                                                    )
        blueprint_import.add_argument(
                                        '--file', '-f',
                                        help='Blueprint file',
                                        required=False
                                    )

        blueprint_import.add_argument(
                                        'action', nargs='?',
                                        type=str,
                                        default='import',
                                        help='Import command\
                                        default action'
                                    )

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        api_env_instance = deploy_sdk_client.EnvironmentApi()
        env_instance = set_header_parameter(api_env_instance)
        attribute_file = 'import_blueprint_attributes.txt'
        dir_path = os.path.expanduser('~') + '/.' + Constants.PLATFORM_CONFIG_FILE_NAME      # noqa: E501
        blueprint_all_env = env_instance.prepare_import_blueprint(file=parsed_args.file)   # noqa: E501

        try:

            if parsed_args.action == 'prepare':
                prepare_data = []
                for one_env in blueprint_all_env.environment_imports:
                    default_data = {}
                    default_data = {
                        one_env.import_config.name+one_env.import_config.env_version:       # noqa: E501
                        {
                                'name': one_env.import_config.name,   # noqa: E501
                                'connection_id': one_env.import_config.connection_id,  # noqa: E501
                                'provider_id': one_env.import_config.provider_id,   # noqa: E501
                                'env_version': one_env.import_config.env_version,     # noqa: E501
                                'description': one_env.import_config.description   # noqa: E501
                        }
                    }

                    prepare_data.append(default_data)

                os.chdir(dir_path)
                with open(attribute_file, 'w') as outfile:
                    json.dump(prepare_data, outfile)

                print("Blueprint attributes file created successfully...\n\
                    Please update the attributes in %s before\
                    import a blueprint" % (dir_path + '/' + attribute_file))

            elif parsed_args.action == 'import':
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
