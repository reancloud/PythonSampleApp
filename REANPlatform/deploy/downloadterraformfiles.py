import os
from pprint import pprint
import logging
from cliff.command import Command
from . import utility
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants

class DownloadTerraformFiles(Command):
    
    "DownloadTerraformFiles"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DownloadTerraformFiles, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Connection name', required=False)
        parser.add_argument('--id', '-id', help='Connection ID',required=False)
        return parser

    def take_action(self, parsed_args):
        # create an instance of the API class
        api_instance = swagger_client.EnvironmentApi()
        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH
        try:
            if(parsed_args.id is None and parsed_args.name is None):
                raise RuntimeError('Either \'name\' or \'id\'  field is required')
            env_id = None
            if(parsed_args.id is not None):
                env_id = parsed_args.id # int | connection Id
            elif(parsed_args.name is not None):
                all_envs=api_instance.get_all_environments()
                for env in all_envs:
                    if(env.name==parsed_args.name):
                        env_id=env.id
                        break

            if(env_id is None):
               raise RuntimeError('Environment \'name\' or \'id\' does not exit')
            
            # Gives zip stream of all terraform files for an environment
            api_instance.download_terraform_files(env_id)
        except ApiException as e:
            print("Exception when calling EnvironmentApi->download_terraform_files: %s\n" % e)