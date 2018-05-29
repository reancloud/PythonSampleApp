import os
from pprint import pprint
import logging
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class Depoly(Command):
    """Depoly Environment."""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        # Define parser
        parser = super(Depoly, self).get_parser(prog_name)
        # Define subparser
        chelpmsg = "Deploying Environment and blueprint"
        subparsers = parser.add_subparsers(dest='cmd', help='sub-command help')

        # Add positional arguments
        envhelpmsg = """Deploying Environment
                   Usage: rean-deploy deploy environment [-h]
                   -id --env_id / -n --name -v --version
                   (for Environment deployment)"""
                   
        bphelpmsg = """Usage: rean-deploy deploy blueprint [-h]
                   -id --env_id / -n --name -v --version
                   (for blueprint deployment)"""

        env_subparser = subparsers.add_parser('environment', help=envhelpmsg)
        blueprint_subparser = subparsers.add_parser('blueprint', help=bphelpmsg)

        try:
            env_subparser.add_argument('--env_id', '-id',
                                help='Environment id to deploy',
                                required=False)
            env_subparser.add_argument('--name', '-n',
                                help='Environment name to deploy',
                                required=False)
            env_subparser.add_argument('--version', '-v',
                                help='Environment version to deploy',
                                required=False)

        except Exception:
            env_subparser.print_help()
        
        try:
            blueprint_subparser.add_argument('--env_id', '-id',
                                help='Environment id to deploy',
                                required=False)
            blueprint_subparser.add_argument('--name', '-n',
                                help='Environment name to deploy',
                                required=False)
            blueprint_subparser.add_argument('--version', '-v', type=float,
                                help='Environment version to deploy',
                                required=False)

        except Exception:
            blueprint_subparser.print_help()

        return parser

    def take_action(self, parsed_args):
        """take_action."""
        print(parsed_args.name and parsed_args.version)
                
        print(parsed_args.name and parsed_args.version)
        if parsed_args.cmd == 'environment':
            print(parsed_args.name and parsed_args.version)
            if parsed_args.name and parsed_args.version:
                try:
                    instance = deploy_sdk_client.EnvironmentApi()
                    api_instance = set_header_parameter(instance)
                    body = deploy_sdk_client.DeploymentConfiguration(env_name=parsed_args.name, env_version=parsed_args.version)
                    api_response = api_instance.deploy_0(parsed_args.env_id, parsed_args.version)
                    print("Environment deploying by name and version")
                except ApiException as e:
                    Utility.print_exception(e)

            elif parsed_args.env_id:
                try:
                    instance = deploy_sdk_client.EnvironmentApi()
                    api_instance = set_header_parameter(instance)
                    body = deploy_sdk_client.DeploymentConfiguration(environment_id=parsed_args.env_id)
                    api_response = api_instance.deploy(parsed_args.env_id, body=body)
                    status = api_instance.get_deploy_status(parsed_args.env_id, parsed_args.name)
                    pprint(api_response)
                    pprint(status)
                    print("Environment deploying by ID")
                except ApiException as e:
                    Utility.print_exception(e)
            else:
                print("You are going wrong")            

        elif parsed_args.cmd == 'blueprint':
            if parsed_args.env_id:           
                try:
                    env_api_instance = deploy_sdk_client.EnvironmentApi()
                    api_instance = set_header_parameter(env_api_instance)
                    body = deploy_sdk_client.DeploymentConfiguration(environment_id=parsed_args.env_id)  # DeploymentConfiguration |  (optional)
                    api_response = api_instance.deploy_as_blueprint(parsed_args.env_id)
                    status = api_instance.get_deploy_status(parsed_args.env_id, parsed_args.name)
                    pprint(api_response)
                    pprint(status)
                    print("Blueprint deploying by ID")
                except ApiException as e:
                    Utility.print_exception(e)
