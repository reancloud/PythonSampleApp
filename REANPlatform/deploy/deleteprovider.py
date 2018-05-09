import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy.constants import Constants


class DeleteProvider(Command):

    "DeleteProvider"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DeleteProvider, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Set name to \
                            check existance', required=False)
        parser.add_argument('--id', '-id', help='provider id', required=False)
        return parser

    def take_action(self, parsed_args):

        api_instance = deploy_sdk_client.ProviderApi()

        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH
        try:
            if(parsed_args.id is None and parsed_args.name is None):
                raise RuntimeError('Either \'name\' or \
                        \'id\' field is required')

            prov_id = None

            if (parsed_args.id is not None):
                prov_id = parsed_args.id
            else:
                data = api_instance.get_provider_by_name(
                        prov_name=parsed_args.name)
                prov_id = data.id

            if(prov_id is None):
                raise RuntimeError('Provider \'name\' or \'id\' does not exit')

            api_response = api_instance.delete_provider(prov_id)

            if api_response is None:
                pprint("Provider deleted successfully")
        except ApiException as e:
            print("Exception when calling ProviderApi->\
            delete_provider: %s\n" % e)
