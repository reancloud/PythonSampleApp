"""Delete provider module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy.constants import Constants
from deploy import set_provider_header


class DeleteProvider(Command):
    """Delete provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteProvider, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Provider name\
                            ', required=False)
        parser.add_argument('--id', '-id', help='Provider id', required=False)
        return parser

    def take_action(self, parsed_args):
        """Delete provider action."""
        api_instance = set_provider_header.set_header()
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
                raise RuntimeError('Provider with id does not exist' % prov_id)

            api_response = api_instance.delete_provider(prov_id)

            if api_response is None:
                pprint("Provider deleted successfully")
        except Exception as e:
            print("Exception when calling ProviderApi->\
            delete_provider: %s\n" % e)
