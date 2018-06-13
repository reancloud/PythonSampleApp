import logging
import os
import yaml
import botocore
import boto3
import deploy_sdk_client
import json
import zipfile
import shutil
import glob
import ast
import inflection
from deploy_sdk_client.rest import ApiException
from pathlib import Path
from cliff.command import Command

def change_keys_to_camel_case(obj):
    """
    Recursively goes through the dictionary obj and chane keys to Camel Case.
    """
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
    log = logging.getLogger(__name__)

    "Configure"

    def get_parser(self, prog_name):
        parser = super(Configure, self).get_parser(prog_name)

        parser.add_argument(
            '--configuration-bucket', help='Managed Cloud CLI configuration bucket', action="store", required=False)
        parser.add_argument(
            '--deploy-group', help='REANDeploy group for Managed Cloud', action="store", required=False)
        parser.add_argument(
            '--master-provider', help='REANDeploy provider for Managed Cloud AWS master account', action="store", required=False)
        parser.add_argument(
            '--artifactory-bucket', help='Managed Cloud artifactory S3 bucket', action="store", required=False)
        parser.add_argument(
            '--master-acc-no', help='Managed Cloud AWS master account number', action="store", required=False)
        parser.add_argument(
            '--master-connection', help='REANDeploy connection for Managed Cloud AWS master account', action="store", required=False)
        return parser

    def convert_json(self, d, convert):
        new_dict = {}
        for k, v in d.iteritems():
            new_dict[convert(k)] = self.convert_json(
                v, convert) if isinstance(v, dict) else v
        return new_dict

    def take_action(self, parsed_args):
        self.app.LOG.debug('Inside %s', self.__class__.__name__)

        parsed_args = vars(parsed_args)
        self.app.LOG.debug('Parsed arguments are %s', str(parsed_args))

        if not parsed_args['configuration_bucket']:
            configuration_bucket = self.app.configuration_bucket
        else:
            configuration_bucket = parsed_args['configuration_bucket']

        if not parsed_args['artifactory_bucket']:
            mnc_artifact_bucket = self.app.mnc_artifact_bucket
        else:
            mnc_artifact_bucket = parsed_args['artifactory_bucket']

        if not parsed_args['deploy_group']:
            rean_deploy_mnc_group = self.app.rean_deploy_mnc_group
        else:
            rean_deploy_mnc_group = parsed_args['deploy_group']

        if not parsed_args['master_acc_no']:
            mnc_master_account_number = self.app.mnc_master_account_number
        else:
            mnc_master_account_number = parsed_args['master_acc_no']

        if not parsed_args['master_provider']:
            rean_deploy_mnc_master_provider = self.app.rean_deploy_mnc_master_provider
        else:
            rean_deploy_mnc_master_provider = parsed_args['master_provider']

        if not parsed_args['master_connection']:
            rean_deploy_mnc_master_connection = self.app.rean_deploy_mnc_master_connection
        else:
            rean_deploy_mnc_master_connection = parsed_args['master_connection']

        if configuration_bucket is None:
            self.app.LOG.error(
                'The following arguments is required for initial configuration: --configuration-bucket')
            return False
        else:
            self.app.LOG.debug(
                'Value of configuration_bucket is %s', configuration_bucket)

        if mnc_artifact_bucket is None:
            self.app.LOG.error(
                'The following arguments is required for initial configuration: --artifactory-bucket')
            return False
        else:
            self.app.LOG.debug(
                'Value of mnc_artifact_bucket is %s', mnc_artifact_bucket)

        if rean_deploy_mnc_group is None:
            self.app.LOG.error(
                'The following arguments is required for initial configuration: --deploy-group')
            return False
        else:
            self.app.LOG.debug(
                'Value of rean_deploy_mnc_group is %s', rean_deploy_mnc_group)

        if mnc_master_account_number is None:
            self.app.LOG.error(
                'The following arguments is required for initial configuration: --master-acc-no')
            return False
        else:
            self.app.LOG.debug(
                'Value of mnc_master_account_number is %s', mnc_master_account_number)

        if rean_deploy_mnc_master_provider is None:
            self.app.LOG.error(
                'The following arguments is required for initial configuration: --master-provider')
            return False
        else:
            self.app.LOG.debug(
                'Value of rean_deploy_mnc_master_provider is %s', rean_deploy_mnc_master_provider)

        if rean_deploy_mnc_master_connection is None:
            self.app.LOG.error(
                'The following arguments is required for initial configuration: --master-connection')
            return False
        else:
            self.app.LOG.debug(
                'Value of rean_deploy_mnc_master_connection is %s', rean_deploy_mnc_master_connection)

        bucket_configuration_directory_path = os.path.expanduser('~/.mnc')
        if not Path(bucket_configuration_directory_path).is_dir():
            try:
                os.makedirs(bucket_configuration_directory_path)
                self.app.LOG.debug('Created directory %s',
                                   bucket_configuration_directory_path)
            except OSError as e:
                self.app.LOG.error('Failed to create directory %s',
                                   bucket_configuration_directory_path)
                self.app.LOG.debug('Error is %s', str(e))
                return False
        else:
            self.app.LOG.debug('Directory %s already exists', bucket_configuration_directory_path)

        bucket_configuration_file_data = dict(
            configuration_bucket_name=configuration_bucket
        )
        bucket_configuration_file_path = os.path.join(
            bucket_configuration_directory_path, 'config_bucket.yaml')

        try:
            with open(bucket_configuration_file_path, 'w') as bucket_configuration_file:
                yaml.dump(bucket_configuration_file_data, bucket_configuration_file,
                          default_flow_style=False)
            self.app.LOG.debug(
                'Successfuly created file %s', bucket_configuration_file_path)
        except yaml.YAMLError as e:
            self.app.LOG.error(
                'Failed to create bucket_configuration file at path %s', bucket_configuration_file_path)
            self.app.LOG.debug('Error is %s', str(e))
            return False

        configuration_file_data = dict(
            mnc_master_account_number=mnc_master_account_number,
            rean_deploy_mnc_master_provider=rean_deploy_mnc_master_provider,
            rean_deploy_mnc_master_connection=rean_deploy_mnc_master_connection,
            rean_deploy_mnc_group=rean_deploy_mnc_group,
            mnc_artifact_bucket=mnc_artifact_bucket
        )

        try:
            with open(self.app.local_configuration_file_path, 'w') as local_configuration_file:
                yaml.dump(configuration_file_data, local_configuration_file,
                          default_flow_style=False)
            self.app.LOG.debug(
                'Successfuly created local configuration file %s', self.app.local_configuration_file_path)
        except yaml.YAMLError as e:
            self.app.LOG.error(
                'Failed to create local configuration file at path %s', self.app.local_configuration_file_path)
            self.app.LOG.debug('Error is %s', str(e))
            return False

        try:
            self.app.s3.meta.client.upload_file(
                self.app.local_configuration_file_path,
                configuration_bucket,
                'mnc_configuration.yml'
            )
            self.app.LOG.debug(
                'Successfuly uploaded configuration file at %s', configuration_bucket)
        except botocore.exceptions.ClientError as e:
            self.app.LOG.error('Failed to upload configuration file at %s',
                               configuration_bucket)
            self.app.LOG.debug('Error is %s', str(e))
            return False


        local_artifacts_zip_path = '/tmp/mnc_artifacts.zip'
        try:
            self.app.s3.meta.client.download_file(
                mnc_artifact_bucket,
                'PROD/v1.0.06/rean_mnc_blueprints_v1.0.06.zip',
                local_artifacts_zip_path
            )
            self.app.LOG.debug(
                'Downloaded blueprints artifacts at location %s', local_artifacts_zip_path)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])

            if error_code == 403:
                self.app.LOG.error('%s bucket access denied',
                               mnc_artifact_bucket)


            elif error_code == 404:
                self.app.LOG.error(
                    'Failed to find managed cloud blueprint artifacts at bucket %s', mnc_artifact_bucket)

            self.app.LOG.debug('Error is %s', str(e))
            return False

        local_artifacts_path = "/tmp/mnc_artifacts"

        if not Path(local_artifacts_path).is_dir():
            try:
                os.makedirs(local_artifacts_path)
                self.app.LOG.debug('Created directory %s',
                                   local_artifacts_path)
            except OSError as e:
                self.app.LOG.error('Failed to create directory %s',
                                   local_artifacts_path)
                self.app.LOG.debug('Error is %s', str(e))
                return False
        else:
            self.app.LOG.debug('Directory %s already exists',
                               local_artifacts_path)
            self.app.LOG.debug('Deleting content inside %s directory',
                               local_artifacts_path)
            for the_file in os.listdir(local_artifacts_path):
                file_path = os.path.join(local_artifacts_path, the_file)
                self.app.LOG.debug('Deleting %s ',
                                   file_path)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    self.app.LOG.debug('Failed to delete %s',
                                       file_path)
                    self.app.LOG.debug('Error is %s', str(e))

        try:
            with zipfile.ZipFile(local_artifacts_zip_path, "r") as artifacts_zip:
                artifacts_zip.extractall(local_artifacts_path)
                self.app.LOG.debug(
                    'Extracted blueprint artifacts at location %s', local_artifacts_path)

        except zipfile.BadZipFile as e:
            self.app.LOG.error('failed to extract %s zip file', local_artifacts_zip_path)
            self.app.LOG.debug('Error is %s', str(e))
            return False

        deploy_environment_api = deploy_sdk_client.EnvironmentApi()
        deploy_environment_api.api_client.set_default_header(
            'Authorization',
            rean_deploy_api_key
        )
        deploy_environment_api.api_client.host = rean_deploy_endpoint

        deploy_provider_api = deploy_sdk_client.ProviderApi()
        deploy_provider_api.api_client.set_default_header(
            'Authorization',
            rean_deploy_api_key
        )
        deploy_provider_api.api_client.host = rean_deploy_endpoint

        deploy_connection_api = deploy_sdk_client.ConnectionApi()
        deploy_connection_api.api_client.set_default_header(
            'Authorization',
            rean_deploy_api_key
        )
        deploy_connection_api.api_client.host = rean_deploy_endpoint


        try:
            deploy_providers = deploy_provider_api.get_all_providers()
            deploy_providers_dict = ast.literal_eval(str(deploy_providers))
            self.app.LOG.debug('Available providers are %s',
                               str(deploy_providers_dict))
        except ApiException as e:
            self.app.LOG.error('Failed to get all Deploy Providers')
            self.app.LOG.debug('Error is %s', str(e))
            return False

        rean_deploy_mnc_master_provider_id = None
        for provider in deploy_providers_dict:
            if provider['name'] == rean_deploy_mnc_master_provider:
                rean_deploy_mnc_master_provider_id = provider['id']
                self.app.LOG.debug('Required Provider ID is %s',
                                   rean_deploy_mnc_master_provider_id)
                break

        if rean_deploy_mnc_master_provider_id is None:
            self.app.LOG.error('Failed to find provider %s',
                               rean_deploy_mnc_master_provider)
            return False

        try:
            deploy_connections = deploy_connection_api.get_all_vm_connections()
            deploy_connections_dict = ast.literal_eval(str(deploy_connections))
            self.app.LOG.debug('Available connections are %s',
                               str(deploy_connections_dict))
        except ApiException as e:
            self.app.LOG.error('Failed to get all Deploy Connections')
            self.app.LOG.debug('Error is %s', str(e))
            return False

        rean_deploy_mnc_master_connection_id = None
        for connection in deploy_connections_dict:
            if connection['name'] == rean_deploy_mnc_master_connection:
                rean_deploy_mnc_master_connection_id = connection['id']
                self.app.LOG.debug('Required Connection ID is %s',
                                   rean_deploy_mnc_master_connection_id)
                break

        if rean_deploy_mnc_master_connection_id is None:
            self.app.LOG.error('Failed to find connection %s',
                               rean_deploy_mnc_master_connection)
            return False


        for file in glob.glob(local_artifacts_path + '/rules/*.reandeploy'):

            try:
                self.app.LOG.debug('Preparing blueprint %s for import', file)
                deploy_api_response = deploy_environment_api.prepare_import_blueprint(
                    file=file)

            except ApiException as e:
                self.app.LOG.error('Failed to prepare %s blueprint for import', file)
                self.app.LOG.debug('Error is %s', str(e))
                continue


            deploy_api_response_dict = deploy_api_response.to_dict()
            deploy_api_response_dict_new = []
            deploy_env_details = {}

            for total_env in range(len(deploy_api_response_dict['environment_imports'])):
                self.app.LOG.debug('Found environment %s', deploy_api_response_dict['environment_imports'][total_env]['import_config']['name'])

                if deploy_api_response_dict['environment_imports'][total_env]['import_config']['name'] == "mnc_rule_processor_lambda_setup":
                    self.app.LOG.debug('Not importhig enviroment')
                    continue
                if deploy_api_response_dict['environment_imports'][total_env]['import_config']['name'] == "mnc_rule_processor_lambda_permission":
                    self.app.LOG.debug('Not importhig enviroment')
                    continue

                self.app.LOG.debug('Setting up connection and provider values for envrionment')
                deploy_api_response_dict['environment_imports'][total_env]['import_config']['connection_id'] = rean_deploy_mnc_master_connection_id
                deploy_api_response_dict['environment_imports'][total_env]['import_config']['provider_id'] = rean_deploy_mnc_master_provider_id

                deploy_api_response_dict_new.append(deploy_api_response_dict['environment_imports'][total_env])
                deploy_env_details[deploy_api_response_dict['environment_imports'][total_env]['import_config']['name']] = deploy_api_response_dict['environment_imports'][total_env]['import_config']['env_version']

            try:
                self.app.LOG.debug(
                    'Checking if blueprint already exists')
                api_responce = deploy_environment_api.check_environment_import_for_name_and_version(
                    body=deploy_env_details)

            except ApiException as e:
                self.app.LOG.error(
                    'Failed to check if %s blueprint exists', file)
                self.app.LOG.debug('Error is %s', str(e))
                continue

            if len(api_responce) != 0:
                self.app.LOG.info('%s is already exists', file)
                continue

            blueprint_body_to_import = deploy_sdk_client.BlueprintImport(environment_imports=deploy_api_response_dict_new)
            blueprint_body_to_import = change_keys_to_camel_case(
                blueprint_body_to_import.to_dict())

            self.app.LOG.debug('Created BlueprintImport object for blueprint')

            try:
                deploy_environment_api.import_blueprint(
                    body=blueprint_body_to_import)
                self.app.LOG.info('%s is successfuly imported', file)

            except ApiException as e:
                self.app.LOG.error(
                    'Failed to import %s blueprint', file)
                self.app.LOG.debug('Error is %s', str(e))
                continue

