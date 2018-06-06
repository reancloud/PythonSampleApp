"""Provider module."""
import logging
from pprint import pprint
from cliff.command import Command
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
import json
import os
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility


class Provider(Command):
    """Rean-Deploy provider."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Parser of Provider."""
        parser = super(Provider, self).get_parser(prog_name)
        provider_parser = parser.add_subparsers(help='Provider sub-commands')  # noqa: E501

        list_prov_par = provider_parser.add_parser(
                                                        "list",
                                                        help='List provider\
                                                        Usage: [rean-deploy\
                                                        provider list\
                                                        --format json/table]'
                                                    )
        list_prov_par.add_argument(
                                    '--format', '-f',
                                    help='Allowed values are: [json, table]',
                                    type=str, default='json',
                                    nargs='?',
                                    required=False
                                )
        list_prov_par.add_argument(
                                    'action', nargs='?',
                                    type=str,
                                    default='list',
                                    help='List command default action'
                                )

        delete_provider_parser = provider_parser.add_parser(
                                                        "delete",
                                                        help='Delete provider\
                                                        Usage: [rean-deploy\
                                                        provider delete\
                                                        --id provider_id]'
                                                    )
        delete_provider_parser.add_argument(
                                            '--prov_id', '-id',
                                            help='Provider id',
                                            required=False
                                            )
        delete_provider_parser.add_argument('--prov_name', '-name',
                                            help='Provider name',
                                            required=False
                                            )
        delete_provider_parser.add_argument(
                                    'action', nargs='?',
                                    type=str,
                                    default='delete',
                                    help='Delete command default action'
                                    )

        create_provider_par = provider_parser.add_parser(
                                                        "create",
                                                        help='Delete provider\
                                                        Usage: [rean-deploy\
                                                        provider create\
                                                        --name provider_name\
                                                        --type provider_type\
                                                        --provider_details\
                                                        json file with\
                                                        applicable key-value\
                                                        pair]'
                                                    )
        create_provider_par.add_argument(
                                        '--name', '-n',
                                        help='Provider name',
                                        required=True
                                        )
        create_provider_par.add_argument(
                                        '--type', '-t',
                                        help='Provider type',
                                        required=True
                                        )
        create_provider_par.add_argument(
                                        '--provider_details', '-f',
                                        help='Json file with\
                                        applicable key-value pair\
                                        for provider type',
                                        required=True
                                        )
        create_provider_par.add_argument(
                                    'action', nargs='?',
                                    type=str,
                                    default='create',
                                    help='Delete command default action'
                                    )
        return parser

    def take_action(self, parsed_args):
        """take_action of ListProvider."""
        provider_api_instance = deploy_sdk_client.ProviderApi()
        api_instance = set_header_parameter(provider_api_instance)
        self.provider_operations(api_instance, parsed_args)

    def provider_operations(self, api_instance, parsed_args):
        """provider_operations."""
        try:
            if parsed_args.action == 'list':
                api_response = api_instance.get_all_providers()
                if parsed_args.format == 'table':
                    table = PrettyTable(['Name', 'Id', 'Type'])
                    table.padding_width = 1
                    for provider in api_response:
                        table.add_row(
                                    [
                                        provider.name,
                                        provider.id,
                                        provider.type
                                    ]
                                )
                    print("Provider list ::\n%s" % (table))
                else:
                    print(
                            json.dumps(
                                    api_response,
                                    default=lambda o: o.__dict__,
                                    sort_keys=True, indent=4
                                    ).replace("\"_", '"')
                        )
            elif parsed_args.action == 'delete':
                prov_id = parsed_args.prov_id
                if parsed_args.prov_name and parsed_args.prov_id is None:
                    prov_id = self.get_id(parsed_args.prov_name, api_instance)

                if(prov_id is None):
                    raise RuntimeError("Exception : \
                        connection does not exit", parsed_args.prov_name)

                api_response = api_instance.delete_provider(prov_id)
                print("Provider deleted successfully id", prov_id)

            elif parsed_args.action == 'create':
                file_path = parsed_args.provider_details
                if not os.path.isfile(file_path):
                    raise RuntimeError('Provider details file %s \
                                does not exists' % file_path)

                with open(file_path, "r") as handle:
                    filedata = handle.read()

                jsondata = json.loads(filedata)
                provider = deploy_sdk_client.SaveProvider(
                                name=parsed_args.name,
                                type=parsed_args.type,
                                json=jsondata
                            )
                api_response = api_instance.save_provider(provider)

                # Get all providers for user
                id = self.get_id(parsed_args.name, api_instance)
                print("Provider created successfully \
                        Name: %s,  Id: %i" % (parsed_args.name, id))
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
