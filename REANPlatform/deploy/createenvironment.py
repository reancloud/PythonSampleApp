import os
from pprint import pprint
import logging
from cliff.command import Command
from . import utility
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants

class CreateEnv(Command):

    "CreateEnv"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateEnv, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Set name to environment', required=True)
        parser.add_argument('--description', '-desc', help='Set description to environment', required=False)
        parser.add_argument('--connection_id', '-c', help='Set connection_id to environment', required=True)
        parser.add_argument('--region', '-r', help='Set region to environment', required=True)
        parser.add_argument('--provider', '-p', help='Set provider  to environment', required=True)
        parser.add_argument('--provider_type', '-t', help='Provider Type', required=True)
        return parser

    def take_action(self, parsed_args):

        api_provider = swagger_client.ProviderApi()
        
        api_provider.api_client.set_default_header(
        	Constants.AUTHORIZATION,
        	Constants.CREDENTIALS
        )
        api_provider.api_client.host = Constants.HOST_PATH
        api_instance = swagger_client.EnvironmentApi()
             
        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH
        try:
            if (parsed_args.provider_type == 'aws' && parsed_args.provider is not None):   
                
                provider_response = api_provider.get_provider_by_name(prov_name=parsed_args.provider)

                body = swagger_client.Environment(
                    name=parsed_args.name,
                    description=parsed_args.description,
                    connection_id=parsed_args.connection_id,
                    region=parsed_args.region,
                    provider={'id': provider_response.id,'name': parsed_args.provider,'type': 'aws'}
                   )

                api_response = api_instance.save_environment(body=body)
                pprint(api_response)

        except ApiException as e:
            self.log.error(e)
