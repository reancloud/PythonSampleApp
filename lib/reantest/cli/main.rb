module REANTest
  module Cli
    class Main < Base
      desc "job SUBCOMMAND ...ARGS", "Manage cross-browser testing jobs"
      subcommand "job", Job
    end
  end
end
