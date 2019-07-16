"""Get Group module."""
import logging
from cliff.command import Command
import authnz_sdk_client
from authnz_sdk_client.rest import ApiException
from reanplatform.utility import Utility
from auth.utility import AuthnzUtility


class CreateGroup(Command):
    """create user."""

    log = logging.getLogger(__name__)

    _description = 'Create Group and add user in it'
    _epilog = 'Example : \n\t rean-auth create-group -p "policy1 policy2 policy3" -d clidescription -u "user1 user2 user3" -n groupName'
    # EPILog will get print after commands

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(CreateGroup, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Group name', required=True)
        parser.add_argument('--description', '-d', help='Group Description ', required=True)
        parser.add_argument('--policies', '-p', help='Group Policies', required=True)
        parser.add_argument('--user', '-u', help='User Name', required=True)
        parser.add_argument('--output', '-o', help="Write output to <file> instead of stdout.",
                            required=False)
        return parser

    def take_action(self, parsed_args):
        """Take action."""
        try:
            list_of_policy = parsed_args.policies.split()
            policy_dto_list = []
            api_instance_policy = authnz_sdk_client.PolicyControllerApi(AuthnzUtility.set_headers())
            for policy in list_of_policy:
                policyDto = api_instance_policy.get_policy(policy)
                policy_dto_list.append(policyDto)

            groupdto = authnz_sdk_client.GroupDto(name=parsed_args.name, description=parsed_args.description,
                                                  policies=policy_dto_list, group_level_sharing=False)
            api_instance_group = authnz_sdk_client.GroupControllerApi(AuthnzUtility.set_headers())
            api_response_group = api_instance_group.save_group(body=groupdto)
            print(api_response_group)
            Utility.print_output_as_str("Group saved successfully :{}, id: {}"
                                        .format(api_response_group.name, api_response_group.id), parsed_args.output)
            groupId = api_response_group.id

            list_of_user = parsed_args.user.split()
            for user in list_of_user:
                api_instance_user = authnz_sdk_client.UserControllerApi(AuthnzUtility.set_headers())
                baseUserDto = api_instance_user.get_by_username(user)
                userId = baseUserDto.id
                addUserToGroupDto = authnz_sdk_client.AddUserToGroup(user_id=userId, group_id=groupId)
                api_instance_group.add_user_to_group(body=addUserToGroupDto)
                Utility.print_output_as_str("user :{} added to group :{}"
                                            .format(baseUserDto.name, parsed_args.name), parsed_args.output)

        except ApiException as api_exception:
            print(api_exception)
            Utility.print_exception(api_exception)
