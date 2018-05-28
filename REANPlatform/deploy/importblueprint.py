import os
from pprint import pprint
import logging
from cliff.command import Command
from reanplatform.utility import Utility
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy.constants import Constants
import json

class ImportBlueprint(Command):

    "ImportBlueprint"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ImportBlueprint, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Set name to environment', required=True)
        parser.add_argument('--description', '-desc', help='Set description to environment', required=False)
        parser.add_argument('--connection_id', '-c', help='Set connection_id to environment', required=True)
        parser.add_argument('--region', '-r', help='Set region to environment', required=True)
        parser.add_argument('--provider', '-p', help='Set provider  to environment', required=True)
        parser.add_argument('--provider_type', '-t', help='Provider Type', required=True)
        parser.add_argument('--file', '-f', help='blueprint file',required=True)
        return parser

    def take_action(self, parsed_args):

        api_provider = deploy_sdk_client.ProviderApi()
        
        api_provider.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_provider.api_client.host = Constants.HOST_PATH
        api_instance = deploy_sdk_client.EnvironmentApi()
             
        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH

       
        try:
            file_path=parsed_args.file

            if not os.path.isfile(file_path):
                raise RuntimeError('No such file or directory')

            # Parse parameters
            with open(file_path, "r") as handle:
                filedata = handle.read()

            jsondata=json.loads(filedata)
            provider_response = api_provider.get_provider_by_name(prov_name=parsed_args.provider)
            print("*********")
            # print(provider_response)
            # import pdb;pdb.set_trace()
            
            # response_body=deploy_sdk_client.ImportConfig(name=parsed_args.name,connection_id=parsed_args.connection_id,description=parsed_args.description,region=parsed_args.region,provider_id=provider_response.id)
           
            # blueprint=api_instance.prepare_import_blueprint(file=parsed_args.file)
            
            # body = deploy_sdk_client.BlueprintImport(environment_imports=jsondata) # BlueprintImport |  (optional)
            
            
            # # Use after import/blueprint/prepare.
            # api_instance.import_blueprint(body=body)
        except ApiException as e:
            print("Exception when calling EnvironmentApi->import_blueprint: %s\n" % e)