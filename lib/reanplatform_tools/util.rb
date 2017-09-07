module REANPlatformTools
  module Util
    protected
    
    # Safely read a text file, dying on errors.
    def read_text(*args)
      File.read(*args)
    rescue SystemCallError => e
      die "reading file: #{e.message}"
    end
    
    # Safely read JSON, dying on errors.
    def read_json(*args)
      JSON.parse(File.read(*args))
    rescue SystemCallError => e
      die "reading JSON file: #{e.message}"
    end
    
    # Logging output.
    def log(*items)
      $stderr.puts "#{script_name}: #{items.join(' ')}"
    end

    # Fatal exit.
    def die(*items)
      log(*items)
      exit 1
    end
  end
end
