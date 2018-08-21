#!/bin/bash

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export RELEASE_VERSION
export GITHUB_AUTH_TOKEN

VIRTUALENV='reancli_artifacts'
PYTHON_CMD='/usr/local/bin/python3'
PIP_CMD='/usr/local/bin/pip3'
REAN_PLATFORM_CLI='reanplatform-cli'

cd DeployNow/
echo "Checking latest tag and Release for DeployNow"
git fetch --tags
DeployNowLatestTag=$(git describe --tags `git rev-list --tags --max-count=1`)
cd ..

cd test_sdk_client/
echo "Checking latest tag for TestSDKClient"
git fetch --tags
TestSDKClientTag=$(git describe --tags `git rev-list --tags --max-count=1`)
cd ..

cd authnz_sdk_client/
echo "Checking latest tag for AuthnzSDKClient"
git fetch --tags
AuthnzSDKClientTag=$(git describe --tags `git rev-list --tags --max-count=1`)
cd ..

cd reanplatform-cli/

echo "Creating Tag and Release for Rean Platform CLI"
git checkout develop
RELEASE_BODY="DeployNow version is $DeployNowLatestTag\n
TestSDKClient version is $TestSDKClientTag\n
AuthnzSDKClient version is $AuthnzSDKClientTag\n"
echo "{\"tag_name\": \"${RELEASE_VERSION}\",\"target_commitish\": \"develop\",\"name\": \"${RELEASE_VERSION}\",\"body\": \"${RELEASE_BODY}\",\"draft\": false,\"prerelease\": false}" > body.json
curl --data @body.json https://api.github.com/repos/reancloud/${REAN_PLATFORM_CLI}/releases\?access_token\=${GITHUB_AUTH_TOKEN}
rm body.json
git push --tags

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
REANPLATFORM_CLI_ARTIFACT=$(find reanplatform_cli_v${ARTIFACT_VERSION}.zip)
if [[ $REANPLATFORM_CLI_ARTIFACT == reanplatform_cli_v${ARTIFACT_VERSION}.zip ]];
then
    echo "CLI artifact formed"
    aws s3 cp reanplatform_cli_v${ARTIFACT_VERSION}.zip s3://reanplatform-cli/${ARTIFACT_VERSION}/
else
    echo "CLI artifact not formed"
    exit 1
fi
