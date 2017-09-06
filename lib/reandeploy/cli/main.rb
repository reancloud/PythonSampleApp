module REANDeploy
  module Cli
    class Main < Base
      desc "env SUBCOMMAND ...ARGS", "Manage an environment"
      subcommand "env", Env
    end
  end
end
