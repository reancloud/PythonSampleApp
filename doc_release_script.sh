#!/bin/bash -l

VIRTUALENV='cli_doc_env'
PYTHON_CMD=$(which python3)
TARGET_ARTIFACTORY_NAME='local-release-documentation-reanplatform'


ACTIVE_DIR=$(pwd)

echo $ACTIVE_DIR

# Create and active virtualenv
cd $ACTIVE_DIR
echo "------------ Creating VirtualEnv for release ------------"
virtualenv $VIRTUALENV -p ${PYTHON_CMD}
source $VIRTUALENV/bin/activate
echo "------------ VirtualEnv created ------------"


# Install latest available CLI from QA setup
echo "------------ Installing Authnz SDK from released artifactory ------------"
pip install --no-cache-dir authnz-sdk-client --index-url https://${ARTIFACTORY_USERNAME}:${ARTIFACTORY_API_KEY}@artifactory.prod.platform.reancloud.com/artifactory/api/pypi/virtual-pypi/simple
echo "------------ Completed Authnz SDK installation ------------"

echo "------------ Installing Deploy SDK from released artifactory ------------"
pip install --no-cache-dir deploy-sdk-client --index-url https://${ARTIFACTORY_USERNAME}:${ARTIFACTORY_API_KEY}@artifactory.prod.platform.reancloud.com/artifactory/api/pypi/virtual-pypi/simple
echo "------------ Completed Deploy SDK installation ------------"

echo "------------ Installing Test SDK from released artifactory ------------"
pip install --no-cache-dir test-sdk-client --index-url https://${ARTIFACTORY_USERNAME}:${ARTIFACTORY_API_KEY}@artifactory.prod.platform.reancloud.com/artifactory/api/pypi/virtual-pypi/simple
echo "------------ Completed Test SDK installation ------------"


cd REANPlatform/
python setup.py build
python setup.py install
echo "------------ CLI installed------------"

echo "Platform Version : "$(rean-platform --version)
PLATFORM_VERSION=$(rean-platform --version | cut -d' ' -f2)

cd doc/

echo "------------ Installing requirement.txt for doc generation ------------"
pip install -r requirement.txt --index-url https://${ARTIFACTORY_USERNAME}:${ARTIFACTORY_API_KEY}@artifactory.prod.platform.reancloud.com/artifactory/api/pypi/virtual-pypi/simple
echo "------------ Installation completed ------------"

echo "------------ Generating auto documentation ------------"
make html
echo "------------ Documentation Generated ------------"
cd _build/html
zip -r reanplatform-cli-doc.zip .

echo "------------ Uploading zip to artifactory ------------"

echo "-------- Platform version --------------------"
echo $PLATFORM_VERSION
echo "----------------------------------------------"

echo "-------- Target artifactory URL --------------"
echo "https://artifactory.prod.platform.reancloud.com/artifactory/"$TARGET_ARTIFACTORY_NAME"/platform-cli-doc/"$PLATFORM_VERSION"/platform-cli-doc-"$PLATFORM_VERSION".zip"
echo "----------------------------------------------"


curl -H 'X-JFrog-Art-Api:'$ARTIFACTORY_API_KEY -T reanplatform-cli-doc.zip "https://artifactory.prod.platform.reancloud.com/artifactory/"$TARGET_ARTIFACTORY_NAME"/platform-cli-doc/"$PLATFORM_VERSION"/platform-cli-doc-"$PLATFORM_VERSION".zip"
echo "------------  Zip uploaded to artifactory ------------"

deactivate
cd $ACTIVE_DIR

rm -r $VIRTUALENV
