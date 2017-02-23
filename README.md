# reandeploy

This tool supports the following commands

* `env deploy`: Deploy an environment.  Supports setting input variables and collecting terraform outputs.
* `env destroy`: Destroy an environment.

## Installation

This tool has not been packaged into a ruby gem yet, so there is no installation procedure.

It must be run from source, using bundler.

### Running [Bundler][Bundler] for the first time

Run bundler from your project's base directory to fetch and install any gems required by your project:  `bundle install`

Bundler will create a `Gemfile.lock` describing the current set of dependencies.

**Do not edit your Gemfile.lock**

## Usage

### reandeploy env deploy

`bundle exec ./reandeploy.rb env deploy ID-or-NAME [options]`

#### Help description

```
$ be ./reandeploy.rb env help deploy
Usage:
  reandeploy.rb deploy <ID-or-NAME>

Options:
  [--inputs=INPUTS]                # JSON file describing input variables
  [--outputs=OUTPUTS]              # filename to write outputs to, as JSON
  [--deploy-config=DEPLOY_CONFIG]  # JSON file describing deployment configuration
  [--wait], [--no-wait]            # Wait for the operation to finish
                                   # Default: true

Deploy an environment identified by ID or by NAME
```

#### Examples

Deploying some environment with ID 123

`bundle exec ./reandeploy.rb env deploy 123`

Deploying some environment with ID 123, passing a DeployConfig from a JSON file

`bundle exec ./reandeploy.rb env deploy 123 --config config.json`

Deploying some environment with ID 123, setting input variables from a JSON file

`bundle exec ./reandeploy.rb env deploy 123 --inputs vars.json`

Deploying some environment with ID 123, setting input variables from a JSON file, and writing outputs to a JSON file

`bundle exec ./reandeploy.rb env deploy 123 --inputs vars.json --outputs output.json`

### reandeploy env destroy

`bundle exec ./reandeploy.rb env destroy ID-or-NAME [options]`

#### Help description

```
$ be ./reandeploy.rb env help destroy
Usage:
  reandeploy.rb destroy <ID-or-NAME>

Options:
  [--wait], [--no-wait]  # Wait for the operation to finish
                         # Default: true

Destroy an environment identified by ID or by NAME
```

#### Examples

Destroying some environment with ID 123

`bundle exec ./reandeploy.rb env destroy 123`

Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved

[Bundler]: http://bundler.io/