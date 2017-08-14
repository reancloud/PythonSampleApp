# reandeploy

This tool supports the following commands

* `env deploy`: Deploy an environment.  Supports setting input variables and collecting terraform outputs.
* `env destroy`: Destroy an environment.
* `env export`: Export an environment as JSON, Terraform or CloudFormation.

## Installation

### Installing as a local gem

You can check out the code from git, and then build and install the gem using:

`rake build install`

### Running from source

Run bundler from your project's base directory to fetch and install any gems required by your project:  `bundle install`

Bundler will create a `Gemfile.lock` describing the current set of dependencies.

**Do not edit your Gemfile.lock**

After doing this, you can run the tool using `bundle exec bin/reandeploy` as the command name instead of `reandeploy`.

## Usage - Environment Commands

### Config file

An example configuration file:

```yaml
dnow:
  base_url: http://localhost:8182/DeployNow/rest
  username: admin
  password: somePassW0rd
```

### Commands Help

```
$ reandeploy help env
Commands:
  reandeploy env deploy <ID-or-NAME>                                  # Deploy an environment identified by ID or by NAME
  reandeploy env destroy <ID-or-NAME>                                 # Destroy an environment identified by ID or by NAME
  reandeploy env export <ID-or-NAME> --format=FORMAT --output=OUTPUT  # Export an environment identified by ID or by NAME
  reandeploy env help [COMMAND]                                       # Describe subcommands or one specific subcommand

Options:
  [--config=CONFIG]  # location of the reandeploy-tools config file
                     # Default: ~/.reandeploy-tools

```

### reandeploy env get_outputs

`reandeploy env get_outputs ID-or-NAME [options]`

#### Help

```
$ reandeploy env help get_outputs
Usage:
  reandeploy get_outputs <ID-or-NAME> --outputs OUTPUTS

Options:
  --outputs=OUTPUTS                # filename to write outputs to, as JSON
  [--config=CONFIG]                # location of the reandeploy-tools config file
                                   # Default: ~/.reandeploy-tools

Get outputs for an environment identified by ID or by NAME
```

#### Examples

Get outputs for some environment with ID 123

`reandeploy env get_outputs 123 --outputs output.json`

### reandeploy env deploy

`reandeploy env deploy ID-or-NAME [options]`

#### Help

```
$ reandeploy env help deploy
Usage:
  reandeploy deploy <ID-or-NAME>

Options:
  [--inputs=INPUTS]                # JSON file describing input variables
  [--outputs=OUTPUTS]              # filename to write outputs to, as JSON
  [--deploy-config=DEPLOY_CONFIG]  # JSON file describing deployment configuration
  [--wait], [--no-wait]            # Wait for the operation to finish
                                   # Default: true
  [--config=CONFIG]                # location of the reandeploy-tools config file
                                   # Default: ~/.reandeploy-tools

Deploy an environment identified by ID or by NAME
```

#### Examples

Deploying some environment with ID 123

`reandeploy env deploy 123`

Deploying some environment with ID 123, passing a DeployConfig from a JSON file

`reandeploy env deploy 123 --deploy-config config.json`

Deploying some environment with ID 123, setting input variables from a JSON file

`reandeploy env deploy 123 --inputs vars.json`

Deploying some environment with ID 123, setting input variables from a JSON file, and writing outputs to a JSON file

`reandeploy env deploy 123 --inputs vars.json --outputs output.json`

### reandeploy env destroy

`reandeploy env destroy ID-or-NAME [options]`

#### Help

```
$ reandeploy env help destroy
Usage:
  reandeploy destroy <ID-or-NAME>

Options:
  [--wait], [--no-wait]  # Wait for the operation to finish
                         # Default: true
  [--config=CONFIG]      # location of the reandeploy-tools config file
                         # Default: ~/.reandeploy-tools

Destroy an environment identified by ID or by NAME
```

#### Examples

Destroying some environment with ID 123

`reandeploy env destroy 123`

### reandeploy env export

`reandeploy env export ID-or-NAME [options]`

#### Help

```
$ reandeploy env help export
Usage:
  reandeploy export <ID-or-NAME> --format=FORMAT --output=OUTPUT

Options:
  --format=FORMAT    # Export format
                     # Possible values: json, blueprint, tf, cf
  --output=OUTPUT    # Output file for json or blueprint formats, output directory for tf and cf formats
  [--config=CONFIG]  # location of the reandeploy-tools config file
                     # Default: ~/.reandeploy-tools

Export an environment identified by ID or by NAME
```

#### Examples

Exporting some environment with ID 123 as a blueprint

`reandeploy env export 123 --format=blueprint --output=env-123.blueprint.reandeploy`

Exporting some environment with ID 123 as Terraform

`reandeploy env export 123 --format=ff --output=env-123-directory`

Exporting some environment with ID 123 as CloudFormation

`reandeploy env export 123 --format=cf --output=env-123-directory`

Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved

[Bundler]: http://bundler.io/
