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
        env__parser = parser.add_subparsers(help='Environment sub-commands')

        parser_destroy = env__parser.add_parser(
                                                "destroy",
                                                help='Destroy environment\
                                                Usage: [rean-deploy\
                                                environment destroy\
                                                --env_id\--env_name env_name\
                                                --env_version env_version]'
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

        parser_destroy_deployment = env__parser.add_parser(
                                                        "destroy-deployment",
                                                        help='Destroy\
                                                        deployment,\
                                                        Usage:[rean-deploy\
                                                        environment\
                                                        destroy-deployment\
                                                        --deployment_id\
                                                         id\--env_name\
                                                        env_name\
                                                        --deployment_name\
                                                         deployment_name]'
                                                         )
        parser_destroy_deployment.add_argument(
                                    '--env_name', '-name',
                                    help='Environment name',
                                    required=False
                                    )
        parser_destroy_deployment.add_argument(
                                    '--deployment_name', '-d_name',
                                    help='Deployment name',
                                    required=False
                                    )
        parser_destroy_deployment.add_argument(
                                    '--deployment_id', '-d_id',
                                    help='Deployment id',
                                    required=False
                                    )
        parser_destroy_deployment.add_argument(
                                    'action', nargs='?',
                                    type=str,
                                    default='destroy-deployment',
                                    help='Destroy deployment command\
                                    default action'
                                    )
        return parser

    def environment_operation(self, parsed_args, api_instance, env_api_instance):       # noqa: E501
        """Environment_operation."""
        try:
            if parsed_args.action == 'destroy':
                environment_id = parsed_args.env_id
                if environment_id is None:
                    get_env_resp = env_api_instance.get_environment_by_version_and_name(env_name=parsed_args.env_name, env_version=parsed_args.env_version)  # noqa: E501
                    environment_id = get_env_resp.config.env_id
                response = env_api_instance.destroy(environment_id)
                print("Environment status %s: %s" % (response.environment.name, response.status))  # noqa: E501

            elif parsed_args.action == 'destroy-deployment':
                    if parsed_args.env_name and parsed_args.deployment_name:
                        deployment_response = api_instance.destroy_deployment_0(parsed_args.env_name, parsed_args.deployment_name)  # noqa: E501
                        print("Deployment status %s: %s" % (deployment_response.environment.name, deployment_response.status))  # noqa: E501
                    elif parsed_args.deployment_id:
                        deployment_response = api_instance.destroy_deployment(parsed_args.deployment_id)     # noqa: E501
                        print("Deployment status %s: %s" % (deployment_response.environment.name, deployment_response.status))  # noqa: E501
                    else:
                        raise RuntimeError("Please provide values to deployment_id\
                            Or env_name and deployment_name")

        except ApiException as e:
            Utility.print_exception(e)

    def take_action(self, parsed_args):
        """take_action."""
        api_instance = deploy_sdk_client.EnvironmentApi()
        env_api_instance = set_header_parameter(api_instance)
        self.environment_operation(parsed_args, api_instance, env_api_instance)
