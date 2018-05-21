A REANPlatform CLI
=======================

> This is the REANPlatform CLI.

Requirements
1. python version <= 3
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
 rean-platform rean-configure --username <USERNAME> --platform_url <PLATFORM_URL>

 rean-deploy provider list -f <table>/<json>
 rean-deploy delete-provider --name <NAME> --id <ID>
 rean-deploy create-provider --name <NAME> --type <TYPE> --provider_details <PROVIDER_DETAILS>

 rean-deploy list-connections -f <table>/<json>
 rean-deploy list-connections  --type <TYPE> --name <NAME> --user <USER> --password <PASSWORD> --securekeypath <SECUREKEYPATH>
```
