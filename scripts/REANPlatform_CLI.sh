#!/bin/sh

CWD=$(pwd)

# Validate Git username password

if [ -z "${GIT_USERNAME}" ]; then
   echo "Provide valid git username "
   exit
fi

if [ -z "${GIT_PASSWORD}" ]; then
   echo "Provide valid git  password"
   exit
fi

# Validate SDK_VERSION

if [ -z "${SDK_VERSION}" ]; then
   echo "Provide valild SDK Version"
   exit
fi

# Validate Articatory credentials

if [ -z "${ARTIFACTORY_USERNAME}" ]; then
   echo "Provide valild ARTIFACTORY_USERNAME"
   exit
fi

if [ -z "${ARTIFACTORY_PASSWORD}" ]; then
   echo "Provide valild ARTIFACTORY_PASSWORD"
   exit
fi

mkdir $CWD/packages
ZIP_PATH=$CWD/packages/

virtualenv -p python3.5 env
. env/bin/activate

# Generate tarball for REANPLatform CLI

git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/reancloud/reanplatform-cli
cd reanplatform-cli/REANPlatform/
python setup.py sdist upload -r local
cp dist/REANPlatform-$(python setup.py --version).tar.gz $ZIP_PATH

cd $CWD

# Download swagger-code-generation.jar

curl -u ${ARTIFACTORY_USERNAME}:${ARTIFACTORY_PASSWORD} https://artifactory.prod.platform.reancloud.com/artifactory/virtual-mavenlibs-reanplatform/io/swagger/swagger-codegen-cli/2.2.3/swagger-codegen-cli-2.2.3.jar --output swagger-codegen-cli-2.2.3.jar

# Generate tarball for Deploy SDK
mkdir $CWD/DeploySDK
cd DeploySDK
touch config.json
echo "{\"packageName\": \"deploy_sdk_client\", \"projectName\": \"deploy_sdk_client\",\"packageVersion\": \"${SDK_VERSION}\"}" >  config.json
java -jar ../swagger-codegen-cli-2.2.3.jar generate -i https://rean-platform.reancloud.com/swagger-api/DeployNow/rest/swagger.json -l python -o deploy-sdk-client -c config.json
cd deploy-sdk-client
python setup.py sdist upload -r local
cp dist/deploy_sdk_client-${SDK_VERSION}.tar.gz $ZIP_PATH

# Generate tarball for Test SDK
cd $CWD
mkdir $CWD/TestSDK
cd TestSDK

curl https://s3.amazonaws.com/reancli-artifacts/test/swagger.json --output swagger.json

touch config.json
echo "{\"packageName\": \"test_sdk_client\", \"projectName\": \"test_sdk_client\",\"packageVersion\": \"${SDK_VERSION}\"}" >  config.json
java -jar ../swagger-codegen-cli-2.2.3.jar generate -i swagger.json -l python -o test-sdk-client -c config.json
cd test-sdk-client
python setup.py sdist upload -r local
cp dist/test_sdk_client-${SDK_VERSION}.tar.gz $ZIP_PATH


# Generate tarball for Authnz SDK
cd $CWD
mkdir $CWD/AuthnzSDK
cd AuthnzSDK

curl https://s3.amazonaws.com/reancli-artifacts/auth/swagger.json --output swagger.json

touch config.json
echo "{\"packageName\": \"authnz_sdk_client\", \"projectName\": \"authnz_sdk_client\",\"packageVersion\": \"${SDK_VERSION}\"}" >  config.json
java -jar ../swagger-codegen-cli-2.2.3.jar generate -i https://rean-platform.reancloud.com/swagger-api/DeployNow/rest/swagger.json -l python -o auth-sdk-client -c config.json
cd auth-sdk-client
python setup.py sdist upload -r local
cp dist/authnz_sdk_client-${SDK_VERSION}.tar.gz $ZIP_PATH





