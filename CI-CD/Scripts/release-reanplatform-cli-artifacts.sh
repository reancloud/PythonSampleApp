#!/bin/bash

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

VIRTUALENV='reancli_artifacts'
PYTHON_CMD='/usr/local/bin/python3'
PIP_CMD='/usr/local/bin/pip3'
S3_BUCKET='reanplatform-cli'

echo "Creating Virtual Env"
virtualenv $VIRTUALENV --python=${PYTHON_CMD} 
source $VIRTUALENV/bin/activate 


echo "Checking latest tag"
git fetch --tags
LatestTag=$(git describe --tags `git rev-list --tags --max-count=1`)
git checkout $LatestTag

echo "Installing py-lambda-packer Dependencies ..."
pip install py-lambda-packer
cd REANPlatform/
ARTIFACT_VERSION=$(awk -v FS="VERSION =" 'NF>1{print $2}' setup.py | cut -d"'" -f2)
py-lambda-packer --requirement requirements.txt --package . --python python3.5 --include setup.py
REANPLATFORM_CLI_ARTIFACT=$(find reanplatform_cli.zip)
if [[ $REANPLATFORM_CLI_ARTIFACT == reanplatform_cli.zip ]];
then
    echo "CLI artifact formed"
    mv reanplatform_cli.zip reanplatform_cli_${ARTIFACT_VERSION}.zip
    aws s3 cp reanplatform_cli_${ARTIFACT_VERSION}.zip s3://${S3_BUCKET}/${ARTIFACT_VERSION}/
else
    echo "CLI artifact not formed"
    exit 1
fi
