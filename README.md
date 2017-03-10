# reandeploy

This tool supports the following commands

* `env deploy`: Deploy an environment.  Supports setting input variables and collecting terraform outputs.
* `env destroy`: Destroy an environment.

## Installation

### Installing as a local gem

You can check out the code from git, and then install the gem with a command similar to:

`gem build reandeploy-tools.gemspec && gem install reandeploy-tools-1.2.3.gem`

### Running from source

Run bundler from your project's base directory to fetch and install any gems required by your project:  `bundle install`

Bundler will create a `Gemfile.lock` describing the current set of dependencies.

**Do not edit your Gemfile.lock**

After doing this, you can run the tool using `bundle exec bin/reandeploy` as the command name instead of `reandeploy`.

## Usage - Environment Commands

### Commands Help

```
$ reandeploy help env
Commands:
  reandeploy env deploy <ID-or-NAME>   # Deploy an environment identified by ID or by NAME
  reandeploy env destroy <ID-or-NAME>  # Destroy an environment identified by ID or by NAME
  reandeploy env help [COMMAND]        # Describe subcommands or one specific subcommand

Options:
  [--config=CONFIG]  # location of the reandeploy-tools config file
                     # Default: ~/.reandeploy-tools

```


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

`reandeploy env deploy 123 --config config.json`

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

Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved

[Bundler]: http://bundler.io/
