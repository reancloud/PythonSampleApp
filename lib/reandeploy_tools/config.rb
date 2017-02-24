require 'yaml'

module REANDeployTools
  module Config
    class << self
      include Util
      
      attr_writer :config_file
      
      def config_file
        @config_file ||= File.join(ENV['HOME'] || '.', '.reandeploy-tools')
      end
      
      def config
        @config ||= YAML.load(File.read(config_file))
      rescue SystemCallError => e
        die "reading config file: #{e.message}"
      end
    end

    def config
      ::REANDeployTools::Config.config
    end
  end
end
