module REANTest
  module Cli
    class Main < Base
      desc "browser SUBCOMMAND ...ARGS", "Manage cross-browser testing jobs"
      subcommand "browser", Browser
      
      desc "infra SUBCOMMAND ...ARGS", "Manage infrastructure testing jobs"
      subcommand "infra", Infra
    end
  end
end
