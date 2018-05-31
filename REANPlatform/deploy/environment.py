"""Environment module."""
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class Environment(Command):
    """Destroy Environment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(Environment, self).get_parser(prog_name)
        environment_parser = parser.add_subparsers(help='Environment sub-commands')  # noqa: E501

        parser_destroy = environment_parser.add_parser(
                                                        "destroy",
                                                        help='Destroy environment,\
                                                        Usage:[rean-deploy\
                                                        environment destroy\
                                                        --env_id]'
                                                        )
        parser_destroy.add_argument('--env_id', '-id',
                                    help='Environment id',
                                    required=False
                                    )
        parser_destroy.add_argument('action', nargs='?',
                                    type=str,
                                    default='destroy',
                                    help='Destroy command\
                                    default action'
                                    )
        parser_destroy.add_argument('--env_name', '-name',
                                    help='Environment name',
                                    required=False
                                    )
        parser_destroy.add_argument('--env_version', '-env_v',
                                    help='Environment version',
                                    required=False
                                    )
        return parser

    def take_action(self, parsed_args):
        """take_action."""
        api_instance = deploy_sdk_client.EnvironmentApi()
        env_api_instance = set_header_parameter(api_instance)

        if parsed_args.action == 'destroy':
            try:
                environment_id = parsed_args.env_id
                if environment_id is None:
                    get_env_resp = env_api_instance.get_environment_by_version_and_name(env_name=parsed_args.env_name, env_version=parsed_args.env_version)  # noqa: E501
                    environment_id = get_env_resp.config.env_id
                response = env_api_instance.destroy(environment_id)
                print("Environment status %s: %s" % (response.environment.name, response.status))  # noqa: E501
            except ApiException as e:
                Utility.print_exception(e)
