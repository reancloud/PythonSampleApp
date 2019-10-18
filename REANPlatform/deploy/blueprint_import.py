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
from deploy.utility import DeployUtility


class ImportBlueprint(Command):
    """Import the REAN Deploy blueprint."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy import-blueprint --blueprint_file /Users/reandeploy/importEnvironment.blueprint.reandeploy --attribute_file /Users/reandeploy/import_blueprint_attributes.json'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ImportBlueprint, self).get_parser(prog_name)
        parser.add_argument('--blueprint_file', '-b', help='Blueprint file. REAN Deploy blueprint file path. A path can be absolute path.', required=True)
        parser.add_argument('--attribute_file', '-a', help='Blueprint attributes. REAN Deploy blueprint attributes file path. A path can be absolute path.', required=True)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        blueprint_path = parsed_args.blueprint_file
        attribute_path = parsed_args.attribute_file

        ImportBlueprint.validate_parameters(blueprint_path, attribute_path)

        ImportBlueprint.blueprint_import(blueprint_path, attribute_path, parsed_args)    # noqa: E501

    @staticmethod
    def validate_parameters(blueprint_path, attribute_path):
        """Validate cli parameters."""
        if blueprint_path is None and attribute_path is None:
            raise RuntimeError("Please provide REAN Deploy\
                blueprint file and attributes file absolute path")

    @staticmethod
    def blueprint_import(blueprint_path, attribute_path, parsed_args):
        """blueprint_import."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_env_instance = deploy_sdk_client.EnvironmentApi(api_client)
            blueprint_all_env = api_env_instance.prepare_import_blueprint(file=blueprint_path)
            os.chdir(os.path.dirname(attribute_path))
            with open(basename(attribute_path), "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            index = 0
            env_names = []

            # Read data from blueprint
            for one_env in blueprint_all_env.environment_imports:
                key = one_env.import_config.name + '-' + one_env.import_config.env_version

                # Data load from prepar blueprint attribute file
                for blueprint_attribute_key in jsondata:
                    if blueprint_attribute_key == key:
                        if (jsondata[blueprint_attribute_key]['connection_id'] and jsondata[blueprint_attribute_key]['provider_id']):
                            blueprint_all_env.environment_imports[index].import_config.connection_id = jsondata[blueprint_attribute_key]['connection_id']
                            blueprint_all_env.environment_imports[index].import_config.provider_id = jsondata[blueprint_attribute_key]['provider_id']
                            blueprint_all_env.environment_imports[index].import_config.name = jsondata[blueprint_attribute_key]['name']
                            blueprint_all_env.environment_imports[index].import_config.description = jsondata[blueprint_attribute_key]['description']
                            blueprint_all_env.environment_imports[index].import_config.env_version = jsondata[blueprint_attribute_key]['env_version']
                            blueprint_all_env.environment_imports[index].import_config.region = jsondata[blueprint_attribute_key]['region']
                            env_names.append(blueprint_all_env.environment_imports[index].import_config.name)
                            index = index + 1
                        else:
                            exception_msg = "Connection_id and provider_id are\
                                missing to %s environment in the file\
                                 location %s: " % (blueprint_all_env.environment_imports[index].import_config.name, attribute_path)
                            raise RuntimeError(re.sub(' +', ' ', exception_msg))

            api_env_instance.import_blueprint(body=blueprint_all_env)
            Utility.print_output_as_str("Blueprint imported successfully. Environment names : {}".format(env_names), parsed_args.output)

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
