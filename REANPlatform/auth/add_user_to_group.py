"""Get Users module."""
import re
import logging
from cliff.command import Command
import authnz_sdk_client
from auth.utility import AuthnzUtility


class AddUserToGroup(Command):
    """Add user to group"""

    log = logging.getLogger(__name__)

    _description = 'Add user to group'
    _epilog = 'Example : \n\t rean-auth add-user-to-group --user_name <user_name> --group_name <group_name>'

    # EPILog will get print after commands

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(AddUserToGroup, self).get_parser(prog_name)
        parser.add_argument('--user_name', '-un', help='User name.', required=False)
        parser.add_argument('--group_name', '-gn', help='Group name.', required=False)

        parser.add_argument('--user_id', '-ui', help='User id', required=False)
        parser.add_argument('--group_id', '-gi', help='Group id', required=False)

        return parser

    @staticmethod
    def validate_parameters(parsed_args):
        """validate_parameters."""

        if (parsed_args.user_name or parsed_args.user_id) and parsed_args.user_name and parsed_args.user_id:
            raise RuntimeError("Specify either user-name OR user-id")

        if (parsed_args.group_name or parsed_args.group_id) and parsed_args.group_name and parsed_args.group_id:
            raise RuntimeError("Specify either --group-name OR --group-id")

    def take_action(self, parsed_args):
        """take_action."""

        try:
            # Validate parameters
            AddUserToGroup.validate_parameters(parsed_args)

            # Initialise instance and api_instance

            api_user_instance = authnz_sdk_client.UserControllerApi(AuthnzUtility.set_headers())
            api_group_instance = authnz_sdk_client.GroupControllerApi(AuthnzUtility.set_headers())

            if parsed_args.user_name:
                logging.debug("fetching user data ...")
                user_dto = api_user_instance.get_by_username(parsed_args.user_name)
                if user_dto and user_dto.id is not None:
                    user_id = user_dto.id
                else:
                    raise RuntimeError("Invalid User name")
            else:
                user_id = parsed_args.user_id

            if parsed_args.group_name:
                logging.debug("fetching group data ...")
                try:
                    group_dto = api_group_instance.get_group_with_name(parsed_args.group_name)
                except Exception as exception:
                    logging.debug(exception)
                    raise RuntimeError("Invalid group name")

                if group_dto and group_dto.id is not None:
                    group_id = group_dto.id
                else:
                    raise RuntimeError("Invalid group name")
            else:
                group_id = parsed_args.group_id

            logging.debug('user_id : ' + str(user_id))
            logging.debug('group_id : ' + str(group_id))

            add_user_to_group_dto = authnz_sdk_client.models.AddUserToGroup(user_id, group_id)
            api_group_instance.add_user_to_group(body=add_user_to_group_dto)
            print("User added to group successfully.")

        except Exception as exception:
            print(exception)
            exit(1)
