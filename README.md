A REANPlatform CLI
=======================

> This is the REANPlatform CLI.

Requirements
1. python version >= 3 (Update python version https://github.com/pyenv/pyenv)
2. git
3. python-pip

## Usages

Work-in-progress

    1. rean-platforml --help
    2. rean-deploy --help
  
## Development Steps

```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev
 easy_install deploy_sdk_client-1.0.6-py3.5.egg
 easy_install REANPlatform-0.1-py3.5.egg
 ```

## Test

For help

```
 rean-platform --help
 rean-platform configure --username <USERNAME> --platform_url <PLATFORM_URL>

 rean-deploy provider list -f <table>/<json>
 rean-deploy delete-provider --name <NAME> --id <ID>
 rean-deploy create-provider --name <NAME> --type <TYPE> --provider_details <PROVIDER_DETAILS>

 rean-deploy list-connections -f <table>/<json>
 rean-deploy list-connections  --type <TYPE> --name <NAME> --user <USER> --password <PASSWORD> --securekeypath <SECUREKEYPATH>
```
## Installation

Install the zip package using pip command.
```
 pip install https://s3.amazonaws.com/bucket_name/package.zip
```

## Package CLI
Requirements
1. Install py-lambda-packer
```
 pip install py-lambda-packer
```
Packaging CLI

1. Change directory to REANPlatform
```
 cd REANPlatform/
```

2. Run following command to generate REANPlatformCLI package
```
py-lambda-packer --requirement requirements.txt --package . --python python3.6 --include setup.py
```

3. Upload the artifact to s3 bucket

## Bucket Policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucket_name/*",
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": ip_address
                }
            }
        }
    ]
}
```