"""Configure module."""
import logging
from cliff.command import Command
import deploy_sdk_client
import json
import re
import boto3
from deploy_sdk_client.rest import ApiException
from reanplatform.set_header import set_header_parameter
from prettytable import PrettyTable
from reanplatform.utility import Utility
from deploy.destroydeployment import DestroyDeployment
import zipfile
import os, fnmatch


class Configure(Command):
    """Configure."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """get_parser."""
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
        parser.add_argument(
            '--master-connection', help='REANDeploy connection for Managed Cloud AWS master account', action="store", required=False)
        return parser

# aws s3 ls s3://mnc-rule-bucket/PROD/v1.1.2/
    def take_action(self, parsed_args):
        """take_action."""
        s3 = boto3.client('s3')
        #for bucket in s3.buckets.all():
        #    print(bucket.name)
        bucket = 'mnc-rule-bucket'
        startAfter = 'PROD/v1.1.2/'
        local_artifacts_zip_path = '/tmp/mnc/'
       #response = s3.list_objects(Bucket='mnc-rule-bucket')

        if not os.path.exists(local_artifacts_zip_path):
            os.makedirs(local_artifacts_zip_path) 


        response = s3.list_objects(
            Bucket = bucket,
            Prefix = startAfter
        )

         #s3.download_file(bucket, 'PROD/v1.0.06/rean_mnc_blueprints_v1.0.06.zip', '/tmp/rean_mnc_rule_processor_v1.1.2.zip')
        for file in response['Contents']:
            name = file['Key'].rsplit('/', 1)            
            if name[1] and 'blueprint' in name[1]:
                s3.download_file(bucket, file['Key'], local_artifacts_zip_path + name[1])
                print("File Downloaded :", local_artifacts_zip_path + name[1])

                #zip_ref = zipfile.ZipFile(local_artifacts_zip_path + name[1], 'r')
                #zip_ref.extractall(local_artifacts_zip_path)
                #zip_ref.close()
                self.import_blueprint(local_artifacts_zip_path + 'rules')

    def import_blueprint(self, path):

            listOfFiles = os.listdir(path)
            existing_env_list = []
            pattern = "*.blueprint.reandeploy"  
            api_env_instance = deploy_sdk_client.EnvironmentApi()
            env_instance = set_header_parameter(api_env_instance)
            all_env = env_instance.get_all_environments()

                    # Get all env and version from Rean-Deploy
            for one_env in all_env:
                existing_env_list.append(one_env.name)
            
            for blueprint_path in listOfFiles: 
                if fnmatch.fnmatch(blueprint_path, pattern):
                    print("env list::")
                    print(existing_env_list)
                    blueprint_all_env = env_instance.prepare_import_blueprint(file=path + '/' + blueprint_path)  
                    
                    print("=========blueprint_path===========")
                    print(blueprint_all_env)
                  #          
           
                  #  print("----------------------")
                    
            #api_env_instance = deploy_sdk_client.EnvironmentApi()
            #env_instance = set_header_parameter(api_env_instance)
            #blueprint_all_env = env_instance.prepare_import_blueprint(file=blueprint_path)


       
    
        #for object in my_bucket.objects.all():
        #    print("---------------")
        #    print(object)
        #print(response)

        #s3.meta.client.download_file('mybucket', 'hello.txt', '/tmp/hello.txt')
        
        #for key in list:
        #    s3.download_file('my_bucket_name', key['Key'], key['Key'])    
