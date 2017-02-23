module REANDeployTools
  module Util
    protected
    
    # Logging output.
    def log(*items)
      $stderr.puts "#{SCRIPT_NAME}: #{items.join(' ')}"
    end

    # Fatal exit.
    def die(*items)
      log(*items)
      exit 1
    end
  end
end
