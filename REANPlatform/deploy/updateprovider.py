import logging
import json
from pprint import pprint
from cliff.command import Command
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants
import os


class UpdateProvider(Command):

    "UpdateProvider"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(UpdateProvider, self).get_parser(prog_name)
        parser.add_argument('--updatename', '-uname', help='Update name to Provider', required=False)
        parser.add_argument('--input_json_file', '-f', help='Json File with applicable key-value pair for provider type', required=False)
        parser.add_argument('--existingname', '-ename', help='existing provider name',required=True)
        return parser

    def take_action(self, parsed_args):
        api_instance = swagger_client.ProviderApi()

        api_instance.api_client.set_default_header(
            Constants.AUTHORIZATION,
            Constants.CREDENTIALS
        )
        api_instance.api_client.host = Constants.HOST_PATH
        try:
            file_path=parsed_args.input_json_file

            if not os.path.isfile(file_path):
                raise RuntimeError('No such file or directory')

            # Parse parameters
            with open(file_path, "r") as handle:
                filedata = handle.read()

            jsondata=json.loads(filedata)
            import pdb; pdb.set_trace()
            if(jsondata is None and parsed_args.updatename is None):
                raise RuntimeError('Either \'updatename\' or \'json\'  field is required')
            
            data = api_instance.get_provider_by_name(parsed_args.existingname)
            
            if(data is None):
                raise RuntimeError('Provider does not exist')
            if(jsondata is not None and parsed_args.updatename is not None):
                
                data.name = parsed_args.updatename
                data.json = jsondata
                provider = swagger_client.SaveProvider(name=data.name, json=data.json, id=data.id, type=data.type)
            elif(parsed_args.updatename is not None and jsondata is None):
                data.name = parsed_args.updatename
                provider = swagger_client.SaveProvider(name=data.name, id=data.id, type=data.type)
            else:
                data.json = jsondata
                provider = swagger_client.SaveProvider(name=data.name, json=data.json,id=data.id, type=data.type)
      
            # Update Provider
            api_instance.update_provider(provider)
            pprint( "Updated Provider successfully")
        except ApiException as e:
            print("Exception when calling ProviderApi->update_provider: %s\n" % e)
