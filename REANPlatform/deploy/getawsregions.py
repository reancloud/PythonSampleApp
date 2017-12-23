import logging
from pprint import pprint
from cliff.command import Command
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants


class GetAwsRegions(Command):

    "GetAwsRegions"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetAwsRegions, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        
        # create an instance of the API class
        api_instance = swagger_client.ProviderApi()

        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH       
        try: 
            # Get available aws regions
            api_response = api_instance.get_aws_regions()
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ProviderApi->get_aws_regions: %s\n" % e)
