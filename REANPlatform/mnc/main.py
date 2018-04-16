import sys
import yaml
import os
import boto3
import botocore
import uuid
import logging
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pathlib import Path
from cliff.app import App
from cliff.commandmanager import CommandManager

class MNC(App):

    def __init__(self):
        super(MNC, self).__init__(
            description='CLI for REAN Managed Cloud.',
            version='0.1',
            command_manager=CommandManager('rean.mnc'),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        self.LOG.debug('main.Function :: initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('Prapare to run command %s', cmd.__class__.__name__)

        configuration_bucket_file_path = os.path.expanduser(
            '~/.mnc/config_bucket.yaml')
        self.LOG.debug('Trying to open managed cloud bucket details file %s',
                       configuration_bucket_file_path)

        self.configuration_bucket = None
        if Path(configuration_bucket_file_path).is_file():
            with open(configuration_bucket_file_path) as configuration_bucket_file_details:

                try:
                    configuration_bucket_file_content = yaml.safe_load(
                        configuration_bucket_file_details)
                    self.LOG.debug('Configuration bucket file content are %s',
                                   configuration_bucket_file_content)
                except yaml.YAMLError as e:
                    self.LOG.debug('Failed to open managed cloud bucket details file %s',
                                   configuration_bucket_file_path)
                    self.LOG.debug('Error is %s', str(e))

                try:
                    self.configuration_bucket = configuration_bucket_file_content[
                        'configuration_bucket_name']
                except KeyError as e:
                    self.configuration_bucket = None
                    self.LOG.debug(
                        'Failed to find %s key in configuration bucket file', 'configuration_bucket_name')
                    self.LOG.debug('Error is %s', str(e))

        else:
            self.configuration_bucket = None
            self.LOG.debug('Failed to find managed cloud bucket details file %s',
                           configuration_bucket_file_path)

        self.LOG.debug('configuration_bucket value is %s ',
                       self.configuration_bucket)

        self.s3 = boto3.resource('s3')
        try:
            local_configuration_file_name = uuid.uuid4().hex
            self.local_configuration_file_path = '/tmp/' + local_configuration_file_name
            self.LOG.debug('Local configuration file path is %s',
                           self.local_configuration_file_path)
            self.s3.meta.client.download_file(
                self.configuration_bucket, 'mnc_configuration.yml', self.local_configuration_file_path)

        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])

            if error_code == 403:
                self.LOG.debug('Bucket access denied, Error is %s', str(e))
                self.LOG.error('%s bucket access denied',
                               self.configuration_bucket)

                if cmd.__class__.__name__ != "Configure":
                    raise RuntimeError(e)

            elif error_code == 404:
                self.LOG.debug(
                    'Failed to find managed cloud configuration file at bucket %s', self.configuration_bucket)
                self.LOG.debug('Error is %s', str(e))

        if Path(self.local_configuration_file_path).is_file():
            with open(self.local_configuration_file_path) as local_configuration_file_details:

                try:
                    local_configuration_file_content = yaml.safe_load(
                        local_configuration_file_details)
                    self.LOG.debug('Local configuration file content are %s',
                                   local_configuration_file_content)
                except yaml.YAMLError as e:
                    self.LOG.debug('Failed to open local configuration file %s',
                                   local_configuration_file_content)
                    self.LOG.debug('Error is %s', str(e))

                try:
                    self.mnc_master_account_number = local_configuration_file_content[
                        'mnc_master_account_number']
                except KeyError as e:
                    self.mnc_master_account_number = None
                    self.LOG.debug(
                        'Failed to find mnc_master_account_number key in local configuration file %s', self.local_configuration_file_path)
                    self.LOG.debug('Error is %s', str(e))

                try:
                    self.rean_deploy_endpoint = local_configuration_file_content[
                        'rean_deploy_endpoint']
                except KeyError as e:
                    self.rean_deploy_endpoint = None
                    self.LOG.debug(
                        'Failed to find rean_deploy_endpoint key in local configuration file %s', self.local_configuration_file_path)
                    self.LOG.debug('Error is %s', str(e))

                try:
                    self.rean_deploy_api_key = local_configuration_file_content['rean_deploy_api_key']
                except KeyError as e:
                    self.rean_deploy_api_key = None
                    self.LOG.debug(
                        'Failed to find rean_deploy_api_key key in local configuration file %s', self.local_configuration_file_path)
                    self.LOG.debug('Error is %s', str(e))

                try:
                    self.rean_deploy_mnc_master_provider = local_configuration_file_content[
                        'rean_deploy_mnc_master_provider']
                except KeyError as e:
                    self.rean_deploy_mnc_master_provider = None
                    self.LOG.debug(
                        'Failed to find rean_deploy_mnc_master_provider key in local configuration file %s', self.local_configuration_file_path)
                    self.LOG.debug('Error is %s', str(e))

                try:
                    self.rean_deploy_mnc_group = local_configuration_file_content[
                        'rean_deploy_mnc_group']
                except KeyError as e:
                    self.rean_deploy_mnc_group = None
                    self.LOG.debug(
                        'Failed to find rean_deploy_mnc_group key in local configuration file %s', self.local_configuration_file_path)
                    self.LOG.debug('Error is %s', str(e))

                try:
                    self.mnc_artifact_bucket = local_configuration_file_content['mnc_artifact_bucket']
                except KeyError as e:
                    self.mnc_artifact_bucket = None
                    self.LOG.debug(
                        'Failed to find mnc_artifact_bucket key in local configuration file %s', self.local_configuration_file_path)
                    self.LOG.debug('Error is %s', str(e))

        else:
            self.mnc_master_account_number = None
            self.rean_deploy_endpoint = None
            self.rean_deploy_api_key = None
            self.rean_deploy_mnc_master_provider = None
            self.rean_deploy_mnc_group = None
            self.mnc_artifact_bucket = None
            self.LOG.debug('Failed to find managed cloud bucket details file %s',
                           configuration_bucket_file_path)

        self.LOG.debug('mnc_master_account_number value is %s',
                       self.mnc_master_account_number)
        self.LOG.debug('rean_deploy_endpoint value is %s',
                       self.rean_deploy_endpoint)
        self.LOG.debug('rean_deploy_api_key value is %s',
                       self.rean_deploy_api_key)
        self.LOG.debug('rean_deploy_mnc_master_provider value is %s',
                       self.rean_deploy_mnc_master_provider)
        self.LOG.debug('rean_deploy_mnc_group value is %s',
                       self.rean_deploy_mnc_group)
        self.LOG.debug('mnc_artifact_bucket value is %s',
                       self.mnc_artifact_bucket)

        if cmd.__class__.__name__ != "Configure":

            if self.configuration_bucket is None:
                raise RuntimeError(
                    'The following arguments is required for initial configuration: --configuration-bucket')

            if self.mnc_artifact_bucket is None:
                raise RuntimeError(
                    'The following arguments is required for initial configuration: --artifactory-bucket')

            if self.rean_deploy_api_key is None:
                raise RuntimeError(
                    'The following arguments is required for initial configuration: --deploy-api-key')

            if self.rean_deploy_endpoint is None:
                raise RuntimeError(
                    'The following arguments is required for initial configuration: --deploy-endpoint')

            if self.rean_deploy_mnc_group is None:
                raise RuntimeError(
                    'The following arguments is required for initial configuration: --deploy-group')

            if self.mnc_master_account_number is None:
                raise RuntimeError(
                    'The following arguments is required for initial configuration: --master-acc-no')

            if self.rean_deploy_mnc_master_provider is None:
                raise RuntimeError(
                    'The following arguments is required for initial configuration: --master-provider')

            self.deploy_api_instance = deploy_sdk_client.ConnectionApi()
            self.deploy_api_instance.api_client.host = self.rean_deploy_endpoint
            self.LOG.debug('Created REANDeploy API Instance')

    def clean_up(self, cmd, result, err):
        self.LOG.debug('Inside Cleanup %s', cmd.__class__.__name__)

        if Path(self.local_configuration_file_path).is_file():
            try:
                os.remove(self.local_configuration_file_path)
                self.LOG.debug('Successfuly removed file %s',
                               self.local_configuration_file_path)
            except OSError as e:
                self.LOG.error('Failed to remove file %s',
                                   self.local_configuration_file_path)
                self.LOG.debug('Error is %s', str(e))
                return False


def main(argv=sys.argv[1:]):
    myapp = MNC()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
