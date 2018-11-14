## Packaging automation script


This script is used to create packages for reanplatform-cli along with all SDK's packages
which we get push to local Artifactory to work it in offline mode. 


## Steps to upload packages to Artifactory,  


1. Update environment variable in ReanPlatform_CLI_Env_Export.sh
2. Execute ```Source ReanPlatform_CLI_Env_Export.sh```
3. Update .pypirc file (You can find more details in Set Me Up tab of local Articatory)
4. Execute ```sh REANPlatform_CLI.sh```


## Package creation details

* REANPLatform-cli package will get created from reanplatform-cli's developed branched.

* Authnz SDK: We fetch swagger.json from S3 bucket because Swagger API for authnz is not exposed to the public.

* Deploy SDK: we fetch swagger.json from running production environment.

* Test SDK: Currently swagger.json is fetched from S3. 
			Code to expose swagger API is already merged on the developed branch but it's not available on production.
			we will update it on swagger API exposed on production.

* Generating SDK from swagger.json requires Swagger code generation jar which we are fetching from production's maven Artifactory.


## Environment Variables details

- GIT_USERNAME		: required to clone reanplatform-cli develop branch
- GIT_PASSWORD		: required to clone reanplatform-cli develop branch
- SDK_VERSION		: XX.XX.XX 
- ARTIFACTORY_USERNAME: required to upload packages to local Artifactory
- ARTIFACTORY_PASSWORD: required to upload packages to local Artifactory


