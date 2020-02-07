#!/bin/sh

VIRTUALENV='cli_doc_env'
PYTHON_CMD='python3'


ACTIVE_DIR=$(pwd)

# Create and active virtualenv
cd ACTIVE_DIR
echo "------------ Creating VirtualEnv for release ------------"
virtualenv $VIRTUALENV --python=${PYTHON_CMD}
source $VIRTUALENV/bin/activate
echo "------------ VirtualEnv created ------------"


# Install latest available CLI from QA setup
echo "------------ Installing cli from QA artifactory ------------"
pip install --no-cache-dir reanplatform-cli --index-url https://${ARTIFACTORY_USERNAME}:${ARTIFACTORY_API_KEY}@artifactory.prod.platform.reancloud.com/artifactory/api/pypi/virtual-qa-pypi/simple

pip uninstall reanplatform-cli -y
cd reanplatform-cli/REANPlatform
python setup.py build
python setup.py install
echo "------------ CLI installed------------"

cd doc/

echo "------------ Installing requirement.txt for doc generation ------------"
pip install -r requirement.txt
echo "------------ Installation completed ------------"

echo "------------ Generating auto documentation ------------"
make html
echo "------------ Documentation Generated ------------"
cd _build/html
zip -r reanplatform-cli-doc.zip .

echo "------------ Uploading zip to artifactory ------------"
curl -H 'X-JFrog-Art-Api:'$ARTIFACTORY_API_KEY -T reanplatform-cli-doc.zip "https://artifactory.prod.platform.reancloud.com/artifactory/local-release-misc-reantest/reanplatform-cli-doc.zip"
echo "------------  Zip uploaded to artifactory ------------"
