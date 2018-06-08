"""Delete provider module."""
import logging
import re
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility


class DeleteProvider(Command):
    """Delete provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteProvider, self).get_parser(prog_name)
        parser.add_argument(
                            '--prov_id', '-id',
                            help='Provider id. This parameter is\
                            not required when --prov_name is specified',
                            required=False)
        parser.add_argument(
                            '--prov_name', '-name',
                            help='Provider name. This parameter is\
                            not required when --prov_id is specified',
                            required=False
                        )
        return parser

    def validate_parameters(self, id, prov_name):
        exception_msg = "Specify either --prov_id OR --prov_name"
        if id and prov_name:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        elif id is None and prov_name is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """Delete provider action."""
        prov_id = parsed_args.prov_id
        prov_name = parsed_args.prov_name
        self.validate_parameters(prov_id, prov_name)

        self.delete_provider(prov_id, prov_name)

    def delete_provider(self, prov_id, prov_name):
        try:
            provider_api_instance = deploy_sdk_client.ProviderApi()
            api_instance = set_header_parameter(provider_api_instance)
            if prov_name:
                prov_id = self.get_id(prov_name, api_instance)

            if(prov_id is None):
                raise RuntimeError("Exception provider does not exit: ", prov_name)     # noqa: E501

            api_response = api_instance.delete_provider(prov_id)
            print("Provider deleted successfully id", prov_id)
        except ApiException as e:
            Utility.print_exception(e)

    def get_id(self, name, api_instance):
        """get_id."""
        id = None
        list_api_response = api_instance.get_all_providers()
        for provider in list_api_response:
            if provider.name == name:
                id = provider.id
                break
        return id
