# pylint: disable=C0301
"""MNC Configure module."""
import logging
import zipfile
import os.path
import datetime
import yaml
import boto3
import botocore
import inflection
from cliff.command import Command
from mnc.parameters_constants import MncConstats
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
import authnz_sdk_client
from auth.constants import AunthnzConstants
from deploy.constants import DeployConstants
from reanplatform.utility import Utility
from reanplatform.set_header import set_header_parameter
from reanplatform.utilityconstants import PlatformConstants


def change_keys_to_camel_case(obj):
    """Recursively goes through the dictionary obj and change keys to Camel Case."""
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

    __version = ""

    def get_parser(self, prog_name):
        """get parser"""
        parser = super(Configure, self).get_parser(prog_name)
        parser.add_argument('--configuration_bucket', '-conf_bucket', help='Managed Cloud CLI configuration bucket.',
                            required=True)
        parser.add_argument('--deploy_group', '-d', help='REANDeploy Group for Managed Cloud',
                            required=True)
        parser.add_argument('--master_provider', '-p',
                            help='Master Account Provider for REANDeploy.', required=True)
        parser.add_argument('--artifactory_bucket', '-a',
                            help='Artifactory Bucket Name for Managed Cloud',
                            required=True)
        parser.add_argument('--master_acc_no', '-master_acc',
                            help='Managed Cloud AWS master account number',
                            required=True)
        parser.add_argument('--master_connection', '-master_conn',
                            help='Master Account Connection for REANDeploy',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        """start taking action."""
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
            self.get_blueprints_from_s3_and_unzip(artifactory_bucket)
            self.import_blueprints(master_provider, master_connection, MncConstats.LOCAL_ARTIFACTS_ZIP_PATH + 'rules')
            self.share_blueprints(deploy_group)
            self.release_environments()

        except ApiException as exception:
            Utility.print_exception(exception)

    def check_bucket_configuration_path(self):
        """This method will check whether bucket configuration path present."""
        configuration_bucket_path, file_name = os.path.split(MncConstats.FILE_BUCKET_NAME)
        if not os.path.exists(configuration_bucket_path):
            try:
                os.makedirs(configuration_bucket_path)
            except OSError as exception:
                print("Failed to create directory ", configuration_bucket_path)
                return False

    def create_configuration_bucket_file(self, configuration_bucket):
        """This method will create configuration file locally."""
        if not os.path.isfile(MncConstats.FILE_BUCKET_NAME):
            configuration_bucket_file_data = dict(configuration_bucket_name=configuration_bucket)
            try:
                with open(MncConstats.FILE_BUCKET_NAME, 'w') as configuration_file:
                    yaml.dump(configuration_bucket_file_data, configuration_file, default_flow_style=False)
            except yaml.YAMLError as exception:
                print("Failed to create bucket_configuration file at path", MncConstats.FILE_BUCKET_NAME)
                return False

    def create_and_store_configuration_file_data(self, configuration_bucket, deploy_group, master_provider, artifactory_bucket, master_acc_no, master_connection):
        """This method will create and store configuration file in s3."""

        path = os.path.expanduser('~')
        file_path = path + '/.' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '/' + PlatformConstants.PLATFORM_CONFIG_FILE_NAME + '.yaml'
        # file_path = os.path.expanduser("~/.reanplatform/reanplatform.yaml")
        with open(file_path, 'r') as configuration_file:
            try:
                data = yaml.load(configuration_file)
            except yaml.YAMLError as exception:
                print(exception)
        rean_deploy_endpoint = data['platform']['base_url']
        rean_deploy_api_key = data['platform']['username'].decode('ascii') + ":" + data['platform']['password'].decode('ascii')

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
            s3_resource = boto3.resource('s3')
            is_configuration_bucket_present = False
            for bucket in s3_resource.buckets.all():
                if bucket.name == configuration_bucket:
                    is_configuration_bucket_present = True
                    break
            if is_configuration_bucket_present is False:
                s3_resource.create_bucket(Bucket=configuration_bucket)
                print("Created configuration bucket ", configuration_bucket)
            else:
                print("Configuration bucket already exist!")
            s3_object = s3_resource.Object(configuration_bucket, 'config_bucket.yaml')
            s3_object.put(Body=yaml.dump(configuration_file_data, default_flow_style=False))
            print("Configuration file stored in s3 successfully!")
        except botocore.exceptions.ClientError as exception:
            print(exception)

    def get_blueprints_from_s3_and_unzip(self, artifactory_bucket):
        """ This method will download blueprints zip from S3 """
        try:
            if not os.path.exists(MncConstats.LOCAL_ARTIFACTS_ZIP_PATH):
                os.makedirs(MncConstats.LOCAL_ARTIFACTS_ZIP_PATH)

            prefix_version = self.get_lastest_build_version(artifactory_bucket)
            s3 = boto3.client('s3')
            response = s3.list_objects(Bucket=artifactory_bucket, Prefix=prefix_version)
            for file in response['Contents']:
                name = file['Key'].rsplit('/', 1)
                if name[1] and 'blueprint' in name[1]:
                    s3.download_file(artifactory_bucket, file['Key'], MncConstats.LOCAL_ARTIFACTS_ZIP_PATH + name[1])
                    zip_ref = zipfile.ZipFile(MncConstats.LOCAL_ARTIFACTS_ZIP_PATH + name[1], 'r')
                    zip_ref.extractall(MncConstats.LOCAL_ARTIFACTS_ZIP_PATH)
                    zip_ref.close()

        except botocore.exceptions.ClientError as exception:
            print(exception)

    def get_lastest_build_version(self, artifactory_bucket):
        """get_lastest_build_version."""
        startAfter = None
        prefix = "PROD/"
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(name=artifactory_bucket)
        folder_list = []
        for obj in bucket.objects.filter(Prefix=prefix):
            folder_list.append(obj.key.split('/')[1])
            folder_list = sorted(folder_list, reverse=True)
            self.__version = folder_list[0]
            startAfter = "PROD/" + folder_list[0] + "/"
        return startAfter

    def import_blueprints(self, master_provider, master_connection, local_artifacts_path):
        """ This method will be used to import the blueprints """
        deploy_api_response = None
        master_account_provider_id = ""
        master_account_connection_id = ""
        try:
            os.chdir(local_artifacts_path)
        except OSError as exception:
            print(exception)

        number_of_rules = len([name for name in os.listdir(local_artifacts_path) if name.endswith('.reandeploy') and os.path.isfile(os.path.join(local_artifacts_path, name))])
        print("\nTotal Rule Count : ", number_of_rules)

        master_account_provider_id = self.get_provider_id(master_provider)
        master_account_connection_id = self.get_connection_id(master_connection)

        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
        list_of_existing_env = self.list_of_env(api_instance)

        for file_name in os.listdir(local_artifacts_path):
            environment_name_list = []
            if file_name.endswith('.reandeploy'):
                blueprint_all_env = None
                try:
                    blueprint_all_env = api_instance.prepare_import_blueprint(file=local_artifacts_path + '/' + file_name)
                    index = 0
                    to_del = []
                    for one_env in blueprint_all_env.environment_imports:
                        if one_env.import_config.name in list_of_existing_env:
                            to_del.append(index)
                        else:
                            blueprint_all_env.environment_imports[index].import_config.connection_id = master_account_connection_id
                            blueprint_all_env.environment_imports[index].import_config.provider_id = master_account_provider_id
                            blueprint_all_env.environment_imports[index].import_config.env_version = self.get_release_version()
                        index = index + 1

                    # Skip already imported
                    for already_imported in reversed(to_del):
                        del (blueprint_all_env.environment_imports[already_imported])

                    if blueprint_all_env.environment_imports:
                        api_instance.import_blueprint(body=blueprint_all_env)
                        print("Rule imported :: ", file_name)
                    else:
                        print("Already imported", file_name)

                except ApiException as exception:
                    Utility.print_exception(exception)

    def list_of_env(self, api_instance):
        """list_of_env."""
        already_exist = []
        all_env = api_instance.get_all_environments()
        for one_env in all_env:
            already_exist.append(one_env.name)
        return already_exist

    def get_provider_id(self, master_provider):
        """ This method will return provider-id based on provider-name """
        instance = deploy_sdk_client.ProviderApi()
        provider_api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
        providers_list = provider_api_instance.get_all_providers()
        provider_id = ""
        for provider in providers_list:
            if provider.name == master_provider:
                provider_id = provider.id
                break
        return provider_id

    def get_connection_id(self, master_connection):
        """ This method will return connection-id based on connection-name """
        instance = deploy_sdk_client.ConnectionApi()
        connection_api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
        connection_list = connection_api_instance.get_all_vm_connections()
        for connection in connection_list:
            if connection.name == master_connection:
                connection_id = connection.id
                break
        return connection_id

    def get_release_version(self):
        """ This method will return the current MNC version """
        release_version = self.__version.replace('v', '')
        return release_version

    def share_blueprints(self, deploy_group):
        """ This method will share the blueprints """
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
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
        api_instance_auth = set_header_parameter(instance, Utility.get_url(AunthnzConstants.AUTHNZ_URL))
        api_response = api_instance_auth.get_group_with_name_using_get(deploy_group)
        group_id = api_response.id

        for environment_id in environment_ids_list:
            group_dto_instance = deploy_sdk_client.GroupDto(id=group_id, name=deploy_group)
            action_list = ['VIEW', 'CREATE', 'DELETE', 'EDIT', 'EXPORT', 'DEPLOY', 'DESTROY', 'IMPORT']
            share_group_permission_instance = deploy_sdk_client.ShareGroupPermission(group_dto_instance, action_list)
            environment_policy_instance = deploy_sdk_client.EnvironmentPolicy(environment_id, [share_group_permission_instance])
            api_instance.share_environment(environment_id, body=environment_policy_instance)

        print("Shared all the blueprints!")

    def release_environments(self):
        """ This method will release environments """
        is_released_environments = False
        instance = deploy_sdk_client.EnvironmentApi()
        api_instance = set_header_parameter(instance, Utility.get_url(DeployConstants.DEPLOY_URL))
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
            elif environment['released'] is True:
                continue

            provider = environment['provider']
            provider_object = deploy_sdk_client.Provider(created_by=provider['created_by'], id=provider['id'], modified_by=provider['modified_by'], name=provider['name'], type=provider['type'])
            environment_object = deploy_sdk_client.Environment(id=environment['id'], created_by=environment['created_by'], modified_by=environment['modified_by'], name=environment['name'], description=environment['description'], provider=provider_object, connection_id=environment['connection_id'], env_version=version, released=True)
            modified_on = int(datetime.datetime.now().strftime("%s")) * 1000
            response = api_instance.update_environment(header_env_id=environment['id'], modified_on=modified_on, body=environment_object)
            is_released_environments = True
            print("Released environment ", environment['name'])
        if not is_released_environments:
            print("All environments are already released!")
