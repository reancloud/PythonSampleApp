"""Mnc Utility."""
import boto3
from mnc.parameters_constants import MncConstats


class MncUtility:       # noqa: D203
    """Manage Cloud common functionality."""

    @staticmethod
    def read_bucket_name():
        """read_bucket_name of mnc config."""
        with open(MncConstats.FILE_BUCKET_NAME, "r") as file_data:
            bucket_name = file_data.read().replace('\n', '')
            bucket_name = bucket_name.split(':')[-1]
            bucket_name = bucket_name.strip()
        return bucket_name

    @staticmethod
    def read_role_arn(role_name):
        """read_role_arn."""
        client = boto3.client('iam')
        notifier_lambda_role = client.get_role(RoleName=role_name)
        return notifier_lambda_role['Role']['Arn']

    @staticmethod
    def read_lambda_arn(lambda_name):
        """read_lambda_arn."""
        client = boto3.client('lambda')
        response = client.get_function(FunctionName=lambda_name)
        return response['Configuration']['FunctionArn']

    @staticmethod
    def provider_name_from_s3(bucket_name):
        """Read deploy provider_name_from_s3 of master account."""
        s3_client = boto3.client('s3')
        response = s3_client.list_objects(Bucket=bucket_name)
        for file in response['Contents']:
            obj = s3_client.get_object(Bucket=bucket_name, Key=file['Key'])
            file_s3_content = obj['Body'].read()

            for file_line in file_s3_content.decode('utf-8').split("\n"):
                if "rean_deploy_mnc_master_provider" in file_line:
                    provider_name = file_line.split(':')[-1]
                    provider_name = provider_name.strip()
        return provider_name    
