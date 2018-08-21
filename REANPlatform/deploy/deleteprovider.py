"""Delete provider module."""
import logging
import re
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.utility import Utility
from deploy.constants import DeployConstants
from deploy.utility import DeployUtility


class DeleteProvider(Command):
    """Delete provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
        parser = super(DeleteProvider, self).get_parser(prog_name)
        parser.add_argument('--prov_id', '-i', help='Provider id. This parameter is not required when --prov_name is specified', required=False)
        parser.add_argument('--prov_name', '-n', help='Provider name. This parameter is not required when --prov_id is specified', required=False)
        return parser

    @staticmethod
    def validate_parameters(prov_id, prov_name):
        """validate_parameters."""
        exception_msg = "Specify either --prov_id OR --prov_name"
        if prov_id and prov_name:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))
        elif prov_id is None and prov_name is None:
            raise RuntimeError(re.sub(' +', ' ', exception_msg))

    def take_action(self, parsed_args):
        """Delete provider action."""
        prov_id = parsed_args.prov_id
        prov_name = parsed_args.prov_name
        DeleteProvider.validate_parameters(prov_id, prov_name)

        if prov_id:
            DeleteProvider.delete_provider_by_id(prov_id)
        elif prov_name:
            DeleteProvider.delete_provider_by_name(prov_name)

    @staticmethod
    def delete_provider_by_id(prov_id):
        """delete_provider."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            provider_api_instance = deploy_sdk_client.ProviderApi(api_client)
            api_response = provider_api_instance.delete_provider(prov_id)
            print("Provider deleted successfully :%s, id: %s" % (api_response.name, api_response.id))
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def delete_provider_by_name(prov_name):
        """delete_provider_by_name."""
        try:
            api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
            provider_api_instance = deploy_sdk_client.ProviderApi(api_client)
            prov_id = DeleteProvider.get_id(prov_name, provider_api_instance)
            if prov_id is None:
                raise RuntimeError("Exception provider does not exit: ", prov_name)     # noqa: E501

            DeleteProvider.delete_provider_by_id(prov_id)
        except ApiException as api_exception:
            Utility.print_exception(api_exception)

    @staticmethod
    def get_id(name, api_instance):
        """get_id."""
        provider_id = None
        api_client = set_header_parameter(DeployUtility.create_api_client(), Utility.get_url(DeployConstants.DEPLOY_URL))
        list_api_response = api_instance.get_all_providers(api_client)
        for provider in list_api_response:
            if provider.name == name:
                provider_id = provider.id
                break
        return provider_id
