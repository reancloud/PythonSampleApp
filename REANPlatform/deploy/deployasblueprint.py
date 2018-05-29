import os
import logging
from cliff.command import Command
import deploy_sdk_client
from pprint import pprint
from deploy.constants import Constants
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


# class Depoly(Command):
#     "Command to Depoly the healnow services"

#     log = logging.getLogger(__name__)

#     def get_parser(self, prog_name):
#         # Define parser
#         parser = super(Depoly, self).get_parser(prog_name)
        
#         # Define subparser
#         chelpmsg = "Deploying Environment and blueprint"
#         subparsers = parser.add_subparsers(dest='cmd',help='sub-command help')  #there are subparsers for the parser
        
#         # Add positional arguments
#         envhelpmsg = """Deploying Environment
#                    Usage: rean-deploy deploy environment [-h]
#                    -id --env_id -n --name -v --version
#                    (for Environment deployment)"""
                   
#         bphelpmsg = """Usage: rean-deploy deploy blueprint [-h]
#                    -id --env_id -n --name -v --version
#                    (for blueprint deployment)"""

#         environment_parser = subparsers.add_parser('environment', help=envhelpmsg)
#         blueprint_parser = subparsers.add_parser('blueprint', help=bphelpmsg)

#         try:
#             environment_parser.add_argument('--env_id', '-id',
#                                 help='Environment id to deploy',
#                                 required=False)
#             environment_parser.add_argument('--name', '-n',
#                                 help='Environment name to deploy',
#                                 required=False)
#             environment_parser.add_argument('--version', '-v',
#                                 help='Environment version to deploy',
#                                 required=False)

#         except Exception:
#             environment_parser.print_help()
        
#         try:
#             blueprint_parser.add_argument('--env_id', '-id',
#                                 help='Environment id to deploy',
#                                 required=false)
#             blueprint_parser.add_argument('--name', '-n',
#                                 help='Environment name to deploy',
#                                 required=False)
#             blueprint_parser.add_argument('--version', '-v',
#                                 help='Environment version to deploy',
#                                 required=False)

#         except Exception:
#             blueprint_parser.print_help()

#         return parser

#     def take_action(self, parsed_args):
#         """take_action."""
#         api_instance = deploy_sdk_client.EnvironmentApi()
#         env_api_instance = set_header_parameter(api_instance)
#         api_instance = deploy_sdk_client.EnvironmentApi()
        
#         if parsed_args.cmd == 'environment':
#             print("you are deploying environment")
#             if parsed_args.name and parsed_args.version:
#                 try:
#                     body = deploy_sdk_client.DeploymentConfiguration(env_name=parsed_args.name, env_version=parsed_args.version)
#                     api_response = api_instance.deploy_0(parsed_args.env_id, body=body)
#                     print("Environment deployed successfully")
#                 except ApiException as e:
#                     Utility.print_exception(e)

# # class Error(Command):
# #     "Always raises an error"

# #     log = logging.getLogger(__name__)

# #     def take_action(self, parsed_args):
# #         self.log.info('causing error')
# #         raise RuntimeError('this is the expected exception')
class DepolyEnv(Command):

    "DepolyEnv"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DepolyEnv, self).get_parser(prog_name)
        parser.add_argument('--env_id', '-id', help='Environment ID to deploy', required=True)
        parser.add_argument('--name', '-n',
                                help='Environment name to deploy',
                                required=False)
        return parser

    def take_action(self, parsed_args):
        # create an instance of the API class
        env_api_instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(env_api_instance)

        try:
            env_api_instance = deploy_sdk_client.EnvironmentApi()
            api_instance = set_header_parameter(env_api_instance)
            body = deploy_sdk_client.DeploymentConfiguration(environment_id=parsed_args.env_id)  # DeploymentConfiguration |  (optional)
            api_response = api_instance.deploy_as_blueprint(parsed_args.env_id)
            status = api_instance.get_deploy_status(parsed_args.env_id, parsed_args.name)
            print(api_response)
            pprint(status)
        except ApiException as e:
            print("Exception when calling EnvironmentApi->deploy: %s\n" % e)