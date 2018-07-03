"""MNC Configure module."""
import logging
from cliff.command import Command
import deploy_sdk_client
import authnz_sdk_client
import json
import re
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from reanplatform.set_header import set_header_parameter_auth_service
from prettytable import PrettyTable
from reanplatform.utility import Utility
from deploy.destroydeployment import DestroyDeployment
import boto3
import os.path
import yaml
from yaml import YAMLError
import botocore
import inflection
import zipfile
import datetime
import urllib3


def change_keys_to_camel_case(obj):
        """Recursively goes through the dictionary obj and chane keys to Camel Case."""
        if isinstance(obj, (str, int, float)):
            return obj
        if isinstance(obj, dict):
            new = obj.__class__()
            for k, v in obj.items():
                new[inflection.camelize(k, False)] = change_keys_to_camel_case(v)
        elif isinstance(obj, (list, set, tuple)):
            new = obj.__class__(change_keys_to_camel_case(v) for v in obj)
        else:
            return obj
        return new

class Configure(Command):
    """Configure MNC."""
    __configuration_bucket_path = os.path.expanduser("~/.reanplatform")
    __version = ""

    
    log = logging.getLogger(__name__)
    logging.basicConfig()
    logging.getLogger().setLevel(logging.WARNING)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



    def get_parser(self, prog_name):
        """get parser"""
        parser = super(Configure, self).get_parser(prog_name)
        parser.add_argument('--configuration-bucket', '-conf-bucket', help='Managed Cloud CLI configuration bucket.',
                            required=True)
        parser.add_argument('--deploy-group', '-d', help='REANDeploy Group for Managed Cloud',
                            required=True)
        parser.add_argument('--master-provider', '-p',
                            help='Master Account Provider for REANDeploy.', required=True)
        parser.add_argument('--artifactory-bucket', '-a',
                            help='Artifactory Bucket Name for Managed Cloud',
                            required=True)
        parser.add_argument('--master-acc-no', '-master-acc',
                            help='Managed Cloud AWS master account number',
                            required=True)
        parser.add_argument('--master-connection', '-master-conn',
                            help='Master Account Connection for REANDeploy',
                            required=True)
        return parser

    def check_bucket_configuration_path(self):
        if not os.path.exists(self.__configuration_bucket_path):
            try:
                os.makedirs(self.__configuration_bucket_path)
            except OSError as e:
                print("Failed to create directory ",self.__configuration_bucket_path)
                return False
    
    def create_configuration_bucket_file(self, configuration_bucket):
        configuration_bucket_file_path = os.path.join(
            self.__configuration_bucket_path, 'config_bucket.yaml'
        )
        if not os.path.isfile(configuration_bucket_file_path):
            configuration_bucket_file_data = dict(
                configuration_bucket_name=configuration_bucket
            )
            try:
                with open(configuration_bucket_file_path, 'w') as configuration_file:
                    yaml.dump(configuration_bucket_file_data, configuration_file, default_flow_style=False)
            except yaml.YAMLError as e:
                print("Failed to create bucket_configuration file at path", configuration_bucket_file_path)
                return False

    def create_and_store_configuration_file_data(self,configuration_bucket, deploy_group, master_provider, artifactory_bucket, master_acc_no, master_connection):
        file_path = os.path.expanduser("~/.reanplatform/reanplatform.yaml")
        with open(file_path, 'r') as configuration_file:
            try:
                data = yaml.load(configuration_file)
            except yaml.YAMLError as e:
                print(e)
        rean_deploy_endpoint = data['deploy']['host']
        rean_deploy_api_key = data['deploy']['username'].decode('ascii')+":"+data['deploy']['password'].decode('ascii')

        configuration_file_data = dict(
            mnc_master_account_number=master_acc_no,
            rean_deploy_endpoint=rean_deploy_endpoint,
            rean_deploy_api_key=rean_deploy_api_key,
            rean_deploy_mnc_master_provider=master_provider,
            rean_deploy_mnc_master_connection=master_connection,
            rean_deploy_mnc_group=deploy_group,
            mnc_artifact_bucket=artifactory_bucket
        )
        try:
            s3Resource = boto3.resource('s3')
            is_configuration_bucket_present = False
            for bucket in s3Resource.buckets.all():
                if bucket.name == configuration_bucket:
                    is_configuration_bucket_present = True
                    break
            if is_configuration_bucket_present == False:
                s3Resource.create_bucket(Bucket=configuration_bucket)
                print("Created configuration bucket ",configuration_bucket)
            else:
                print("Configuration bucket already exist!")
            s3Object = s3Resource.Object(configuration_bucket,'config_bucket.yaml')
            s3Object.put(Body=yaml.dump(configuration_file_data, default_flow_style=False))
            print("Configuration file stored in s3 successfully!")
        except botocore.exceptions.ClientError as e:
            print(e)

    def get_blueprints_from_s3(self, artifactory_bucket):
        try:
            prefix = "PROD/"
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(name=artifactory_bucket)
            folderList = []
            for obj in bucket.objects.filter(Prefix=prefix):
                folderList.append(obj.key.split('/')[1])
            folderList = sorted(folderList,reverse=True)
            self.__version = folderList[0]
            newPrefix = "PROD/"+folderList[0]
            file_name = "rean_mnc_blueprint_"+folderList[0]+".zip"
            blueprint_file_name = newPrefix + "/" + file_name
            local_zip_path = os.path.expanduser("/tmp/artifacts.zip")
            bucket.download_file(blueprint_file_name, local_zip_path)
            print("\nDownloaded blueprints zip from s3")
        except botocore.exceptions.ClientError as e:
            print(e)

    def extract_artifacts_zip(self):
        local_zip_path = os.path.expanduser("/tmp/artifacts.zip")
        local_artifacts_path = os.path.expanduser("/tmp/mnc_artifacts")

        if not os.path.exists(local_artifacts_path):
            try:
                os.makedirs(local_artifacts_path)
            except OSError as e:
                print("Failed to create directory ",local_artifacts_path)
                return False

        with zipfile.ZipFile(local_zip_path, "r") as artifacts_zip:
            artifacts_zip.extractall(local_artifacts_path)
            print("Extracted blueprints zip successfully!")

    def get_provider_id(self, master_provider):
        instance = deploy_sdk_client.ProviderApi()
        provider_api_instance = set_header_parameter(instance)
        providers_list = provider_api_instance.get_all_providers()
        provider_id = ""

        for provider in providers_list:
            if provider.name == master_provider:
                provider_id = provider.id
                break

        return provider_id
    
    def get_connection_id(self, master_connection):
        instance = deploy_sdk_client.ConnectionApi()
        connection_api_instance = set_header_parameter(instance)
        connection_list = connection_api_instance.get_all_vm_connections()
        connection_id = ""

        for connection in connection_list:
            if connection.name == master_connection:
                connection_id = connection.id
                break

        return connection_id

    def import_blueprints(self, master_provider, master_connection):
        local_artifacts_path = os.path.expanduser("/tmp/mnc_artifacts/rules")
        master_account_provider_id = ""
        master_account_connection_id = ""
        try:
            os.chdir(local_artifacts_path)
        except OSError as e:
            print(e)
        
        number_of_rules = len([name for name in os.listdir(local_artifacts_path) if name.endswith('.reandeploy') and os.path.isfile(os.path.join(local_artifacts_path, name))])
        print("\nTotal Rule Count : ",number_of_rules)

        master_account_provider_id = self.get_provider_id(master_provider)
        master_account_connection_id = self.get_connection_id(master_connection)

        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)
        for file_name in os.listdir(local_artifacts_path):
            environmentNameList = []
            if file_name.endswith('.reandeploy'):
                try:
                    deploy_api_response = api_instance.prepare_import_blueprint(
                        file=file_name)
                    deploy_api_response = deploy_api_response.to_dict()
                except ApiException as e:
                    Utility.print_exception(e)

                deploy_api_response_dict_new = []
                deploy_env_details = {}        
                for total_environments in range(len(deploy_api_response['environment_imports'])):
                    environment_name = deploy_api_response['environment_imports'][total_environments]['import_config']['name']
                    if environment_name == "mnc_rule_processor_lambda_setup":
                        continue
                    if environment_name == "mnc_rule_processor_lambda_permission_setup":
                        continue
                    if environment_name == "mnc_notifier_lambda":
                        continue
                    deploy_api_response['environment_imports'][total_environments]['import_config']['env_version'] = self.get_release_version()
                    deploy_api_response['environment_imports'][total_environments]['import_config']['connection_id'] = master_account_connection_id
                    deploy_api_response['environment_imports'][total_environments]['import_config']['provider_id'] = master_account_provider_id

                    deploy_env_details[deploy_api_response['environment_imports'][total_environments]['import_config']['name']] = deploy_api_response['environment_imports'][total_environments]['import_config']['env_version']
                
                    try:
                        envResponse = api_instance.check_environment_import_for_name_and_version(body=deploy_env_details)
                    except ApiException as e:
                        Utility.print_exception(e)

                    if envResponse:
                        continue

                    deploy_api_response_dict_new.append(deploy_api_response['environment_imports'][total_environments])

                if deploy_api_response_dict_new:
                    blueprint_body_to_import = deploy_sdk_client.BlueprintImport(environment_imports=deploy_api_response_dict_new)
                    blueprint_body_to_import = change_keys_to_camel_case(
                    blueprint_body_to_import.to_dict())

                    try:
                        import_response = api_instance.import_blueprint(
                            body=blueprint_body_to_import
                        )
                        print("\nImported ",file_name,"successfully!")
                    except ApiException as e:
                        Utility.print_exception(e)
                else:
                    print(file_name," already imported in rean deploy!")

    def get_release_version(self):
        splitString = self.__version.replace('v','').split('.')
        splitString = [str1.zfill(2) for str1 in splitString]
        release_version = '.'.join(splitString)
        return release_version


    def release_environments(self):
        is_released_environments = False
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)
        environment_list = api_instance.get_all_environments()
        version = self.get_release_version()
        print("\nReleasing the environments with version ", version)
        for environment in environment_list:
            environment = environment.to_dict()
            
            if environment['name'] == "mnc_rule_processor_lambda_permission_setup":
                continue
            elif environment['name'] == "mnc_rule_processor_lambda_setup":
                continue
            elif environment['name'] == "mnc_notifier_lambda":
                continue
            elif environment['released'] == True:
                continue

            provider = environment['provider']
            providerObject = deploy_sdk_client.Provider(created_by=provider['created_by'],id=provider['id'],modified_by=provider['modified_by'],name=provider['name'],type=provider['type'])
            environmentObject = deploy_sdk_client.Environment(id=environment['id'],created_by=environment['created_by'],modified_by=environment['modified_by'],name=environment['name'],description=environment['description'],provider=providerObject,connection_id=environment['connection_id'],env_version=version,released=True)
            modifiedOn = int(datetime.datetime.now().strftime("%s")) * 1000
            response = api_instance.update_environment(header_env_id=environment['id'],modified_on=modifiedOn,body=environmentObject)
            is_released_environments = True
            print("Released environment ",environment['name'])
        if not is_released_environments:
            print("All environments are already released!")

    def share_blueprints(self, deploy_group):
        print("\nSharing the blueprints with", deploy_group, "group...")
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance)
        api_response = api_instance.get_all_environments()
        environment_ids_list = []
        for response in api_response:
            if response.name == "mnc_rule_processor_lambda_permission_setup":
                continue
            elif response.name == "mnc_rule_processor_lambda_setup":
                continue
            elif response.name == "mnc_notifier_lambda":
                continue
            environment_ids_list.append(response.config.env_id)
        instance = authnz_sdk_client.GroupcontrollerApi()
        api_instance_auth = set_header_parameter_auth_service(instance)
        api_response = api_instance_auth.get_group_with_name_using_get_with_http_info(name=deploy_group)
        group_id = api_response[0].id

        for environment_id in environment_ids_list:
            groupDtoInstance = deploy_sdk_client.GroupDto(id=group_id, name=deploy_group)
            actionList = ['VIEW','CREATE','DELETE','EDIT','EXPORT','DEPLOY','DESTROY','IMPORT']
            shareGrpPermissionInstance = deploy_sdk_client.ShareGroupPermission(groupDtoInstance,actionList)
            environmentPolicyInstance = deploy_sdk_client.EnvironmentPolicy(environment_id ,[shareGrpPermissionInstance])
            api_instance.share_environment(environment_id ,body=environmentPolicyInstance)
        
        print("Shared all the blueprints!")

    def take_action(self, parsed_args):
        """start taking action"""
        try:
            configuration_bucket = parsed_args.configuration_bucket
            deploy_group = parsed_args.deploy_group
            master_provider = parsed_args.master_provider
            artifactory_bucket = parsed_args.artifactory_bucket
            master_acc_no = parsed_args.master_acc_no
            master_connection = parsed_args.master_connection

            self.check_bucket_configuration_path()
            self.create_configuration_bucket_file(configuration_bucket)
            self.create_and_store_configuration_file_data(configuration_bucket, deploy_group, master_provider, artifactory_bucket, master_acc_no, master_connection)
            self.get_blueprints_from_s3(artifactory_bucket)
            self.extract_artifacts_zip()
            self.import_blueprints(master_provider, master_connection)
            self.share_blueprints(deploy_group)
            self.release_environments()

        except ApiException as e:
            Utility.print_exception(e)