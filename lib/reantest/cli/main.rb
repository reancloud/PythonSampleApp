module REANTest
  module Cli
    class Main < Base
      desc "job SUBCOMMAND ...ARGS", "Manage cross-browser testing jobs"
      subcommand "job", Job
      
      desc "infra SUBCOMMAND ...ARGS", "Manage infrastructure testing jobs"
      subcommand "infra", Infra
    end
  end
end
