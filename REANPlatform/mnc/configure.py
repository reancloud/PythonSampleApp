import logging
import os
import yaml
import botocore
from pathlib import Path
from cliff.command import Command


class Configure(Command):
    log = logging.getLogger(__name__)

    "Configure"

    def get_parser(self, prog_name):
        parser = super(Configure, self).get_parser(prog_name)

        parser.add_argument(
            '--configuration-bucket', help='Managed Cloud CLI configuration bucket', action="store", required=False)
        parser.add_argument(
            '--deploy-endpoint', help='REANDeploy endpoint', action="store", required=False)
        parser.add_argument(
            '--deploy-api-key', help='REANDeploy API key', action="store", required=False)
        parser.add_argument(
            '--deploy-group', help='REANDeploy group for Managed Cloud', action="store", required=False)
        parser.add_argument(
            '--master-provider', help='REANDeploy provider for Managed Cloud AWS master account', action="store", required=False)
        parser.add_argument(
            '--artifactory-bucket', help='Managed Cloud artifactory S3 bucket', action="store", required=False)
        parser.add_argument(
            '--master-acc-no', help='Managed Cloud AWS master account number', action="store", required=False)

        return parser

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

        if not parsed_args['deploy_api_key']:
            rean_deploy_api_key = self.app.rean_deploy_api_key
        else:
            rean_deploy_api_key = parsed_args['deploy_api_key']

        if not parsed_args['deploy_endpoint']:
            rean_deploy_endpoint = self.app.rean_deploy_endpoint
        else:
            rean_deploy_endpoint = parsed_args['deploy_endpoint']

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

        if rean_deploy_api_key is None:
            self.app.LOG.error(
                'The following arguments is required for initial configuration: --deploy-api-key')
            return False
        else:
            self.app.LOG.debug(
                'Value of rean_deploy_api_key is %s', rean_deploy_api_key)

        if rean_deploy_endpoint is None:
            self.app.LOG.error(
                'The following arguments is required for initial configuration: --deploy-endpoint')
            return False
        else:
            self.app.LOG.debug(
                'Value of rean_deploy_endpoint is %s', rean_deploy_endpoint)

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
                'Value of mnc_master_account_number is %s', rean_deploy_mnc_master_provider)

        bucket_configuration_directory_path = os.path.expanduser(
            '~/.mnc')

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
            rean_deploy_endpoint=rean_deploy_endpoint,
            rean_deploy_api_key=rean_deploy_api_key,
            rean_deploy_mnc_master_provider=rean_deploy_mnc_master_provider,
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
