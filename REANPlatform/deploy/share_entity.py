"""CLI to share entity with specified Group."""
import logging
from cliff.command import Command
import authnz_sdk_client
from auth.utility import AuthnzUtility
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility
from deploy.get_resource_actions import GetResourceActions


class ShareEntity(Command):
    """CLI to share entity with specified Group."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(ShareEntity, self).get_parser(prog_name)
        parser.add_argument('--entity_id', '-ei', help='Entity id like environment id, provider id or connection id.', required=True)
        parser.add_argument('--entity_type', '-et', help='Entity type. Allowed values are: [ENVIRONMENT, PACKAGE, PROVIDER, CONNECTION, DEPLOYMENT]', required=True)
        parser.add_argument('--group_name', '-gn', help='Group name. This parameter is to share entity with that specified group', required=True)
        parser.add_argument('--actions', '-p', help='Resource Actions. Allowed values for specific entity type can be viewed by get-resource-actions CLI. Sample value for this attribute is: "VIEW, EDIT, CREATE, DELETE"', required=True)
        parser.add_argument('--output', '-o',
                            help="Write output to <file> instead of stdout.",
                            required=False)
        return parser

    @staticmethod
    def get_entity(api_client, entity_id, entity_type):
        """get_entity."""
        try:
            if entity_type == 'ENVIRONMENT':
                return deploy_sdk_client.EnvironmentApi(api_client).get_environment(entity_id)
            elif entity_type == 'PACKAGE':
                return deploy_sdk_client.PackageApi(api_client).get_package(entity_id)
            elif entity_type == 'PROVIDER':
                return deploy_sdk_client.ProviderApi(api_client).get_provider(entity_id)
            elif entity_type == 'CONNECTION':
                return deploy_sdk_client.ConnectionApi(api_client).get_vm_connection(entity_id)
            elif entity_type == 'DEPLOYMENT':
                return deploy_sdk_client.EnvironmentApi(api_client).get_deployment_by_deployment_id(entity_id)
            else:
                raise RuntimeError("Invalid entity type. Allowed values are: [ENVIRONMENT, PACKAGE, PROVIDER, CONNECTION, DEPLOYMENT]")
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    def take_action(self, parsed_args):
        """take_action."""
        # Define parsed arguments
        try:
            entity_id = parsed_args.entity_id
            entity_type = parsed_args.entity_type
            group_name = parsed_args.group_name
            actions = parsed_args.actions
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            api_instance_group = authnz_sdk_client.GroupControllerApi(AuthnzUtility.set_headers())
            group = api_instance_group.get_group_with_name(group_name)
            api_instance_share = deploy_sdk_client.ShareApi(api_client)
            entity = ShareEntity.get_entity(api_client, entity_id, entity_type)

            if entity is not None:
                multi_share_policy = deploy_sdk_client.MultiSharePolicy(
                    ids={entity_id: entity.name},
                    resource_type=entity_type,
                    share_policy=ShareEntity.get_share_policy(entity_type, group, actions),
                    share_all_versions='false'
                )
                api_instance_share.share_resource(multi_share_policy)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def get_actions(entity_type, actions):
        """get_actions."""
        split_actions = actions.split(",")
        resource_actions = []
        for x in split_actions:
            action = x.strip()
            ShareEntity.validate_action_by_resource(entity_type, action)
            resource_actions.append(action)
        return resource_actions

    @staticmethod
    def get_share_policy(entity_type, group, actions):
        """get_share_policy."""
        entity_actions = ShareEntity.get_actions(entity_type, actions)
        share_group_permission = deploy_sdk_client.ShareGroupPermission(
            group=group,
            actions=entity_actions
        )
        list_share_group_permission = []
        list_share_group_permission.append(share_group_permission)
        share_policy = deploy_sdk_client.SharePolicy(
            id=None,
            permission=list_share_group_permission
        )
        return share_policy

    @staticmethod
    def validate_action_by_resource(entity_type, action):
        """validate_action_by_resource."""
        actual_actions = GetResourceActions.get_resource_actions(entity_type)
        if action not in actual_actions:
            raise RuntimeError("Invalid action " + action + " for resource " + entity_type)
