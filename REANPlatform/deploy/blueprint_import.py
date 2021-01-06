"""Import blueprint module."""
import os
from os.path import basename
import logging
import json
import re
from cliff.command import Command
import authnz_sdk_client
from auth.utility import AuthnzUtility
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility
from deploy.share_entity import ShareEntity


class ImportBlueprint(Command):
    """Import the HCAP Deploy blueprint."""

    log = logging.getLogger(__name__)

    # EPILog will get print after commands
    _epilog = 'Example : rean-deploy import-blueprint --blueprint_file /Users/reandeploy/importEnvironment.blueprint.reandeploy --attribute_file /Users/reandeploy/import_blueprint_attributes.json --group_name dummyGroup --actions "VIEW, EDIT, DEPLOY"'

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(ImportBlueprint, self).get_parser(prog_name)
        parser.add_argument('--blueprint_file', '-b', help='Blueprint file. HCAP Deploy blueprint file path. A path can be absolute path.', required=True)
        parser.add_argument('--attribute_file', '-a', help='Blueprint attributes. HCAP Deploy blueprint attributes file path. A path can be absolute path.', required=True)
        parser.add_argument('--group_name', '-gn', help='Group name. This parameter is to share environments with that specified group.', required=False)
        parser.add_argument('--actions', '-p', help='Resource Actions. Sample value for this attribute is: "VIEW, DELETE, DEPLOY, EDIT, EXPORT".', required=False)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.", required=False)
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        blueprint_path = parsed_args.blueprint_file
        attribute_path = parsed_args.attribute_file
        group_name = parsed_args.group_name
        actions = parsed_args.actions

        ImportBlueprint.validate_parameters(blueprint_path, attribute_path, group_name, actions)

        ImportBlueprint.blueprint_import(blueprint_path, attribute_path, group_name, actions, parsed_args)    # noqa: E501

    @staticmethod
    def validate_parameters(blueprint_path, attribute_path, group_name, actions):
        """Validate cli parameters."""
        if blueprint_path is None and attribute_path is None:
            raise RuntimeError("Please provide HCAP Deploy blueprint file and attributes file absolute path")
        if group_name is not None and actions is None:
            raise RuntimeError("Please provider Resource Actions: --actions")
        if actions is not None and group_name is None:
            raise RuntimeError("Please provider Group name: --group_name")

    @staticmethod
    def blueprint_import(blueprint_path, attribute_path, group_name, actions, parsed_args):
        """blueprint_import."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_env_instance = deploy_sdk_client.ImportBlueprintApi(api_client)
            blueprint_all_env = api_env_instance.prepare_import_blueprint(file=blueprint_path)
            os.chdir(os.path.dirname(attribute_path))
            with open(basename(attribute_path), "r") as handle:
                filedata = handle.read()

            jsondata = json.loads(filedata)
            index = 0
            env_names = []

            # Read data from blueprint
            for one_env in blueprint_all_env.environment_imports:
                # Data load from prepar blueprint attribute file
                for blueprint_attribute_key in jsondata:
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
                        exception_msg = "Connection_id and provider_id are missing to %s environment in the file location %s: " % (blueprint_all_env.environment_imports[index].import_config.name, attribute_path)
                        raise RuntimeError(re.sub(' +', ' ', exception_msg))

            if group_name is not None and actions is not None:
                api_instance_group = authnz_sdk_client.GroupControllerApi(AuthnzUtility.set_headers())
                group = api_instance_group.get_group_with_name(group_name)
                blueprint_all_env.share_policy = ShareEntity.get_share_policy('ENVIRONMENT', group, actions)
            api_env_instance.import_blueprint(body=blueprint_all_env)
            Utility.print_output_as_str("Blueprint imported successfully. Environment names : {}".format(env_names), parsed_args.output)

        except ApiException as api_exception:
            Utility.print_exception(api_exception)
