import os
from pprint import pprint
import logging
from cliff.command import Command
from . import utility
import swagger_client
from swagger_client.rest import ApiException
from deploy.constants import Constants

class DeleteEnv(Command):

    "DeleteEnv"
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DeleteEnv, self).get_parser(prog_name)
        parser.add_argument('--name', '-n', help='Set name to environment', required=False)
        parser.add_argument('--id', '-id', help='Set description to environment', required=False)
        return parser

    def take_action(self, parsed_args):

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
            all_envs = api_instance.get_all_environments()

            if(parsed_args.id is not None):
                env_id=parsed_args.id
                for env in all_envs:
                    if(env.id==parsed_args.id):
                        modified_on=env.modified_on
                        break
            else:
                for env in all_envs:
                    import pdb;pdb.set_trace()
                    if(env.name==parsed_args.name):
                        env_id=env.id
                        modified_on=env.modified_on
                        break

            if(env_id is None):
                raise RuntimeError('Environment \'name\' or \'id\' does not exit')
           
            # Deletes environment by id
            api_response = api_instance.delete_environment(env_id=env_id, header_env_id=env_id, modified_on=modified_on)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling EnvironmentApi->delete_environment: %s\n" % e)
