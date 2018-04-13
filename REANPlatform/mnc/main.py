import sys
import yaml
import os
import boto3
import botocore
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
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

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
        s3 = boto3.resource('s3')
        try:
            s3.meta.client.download_file(
                self.configuration_bucket, 'mnc_configuration.yml', '/tmp/mnc_configuration.yml')
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 403:
                self.LOG.debug('Bucket access denied, Error is %s', str(e))
                self.LOG.error('%s bucket access denied',
                               self.configuration_bucket)
            elif error_code == 404:
                self.LOG.debug(
                    'Failed to find managed cloud configuration file at %s', self.configuration_bucket)
                self.LOG.debug('Error is %s', str(e))



    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)

def main(argv=sys.argv[1:]):
    myapp = MNC()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
