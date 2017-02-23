module REANDeployTools
  module Config
    class << self
      attr_accessor :config_file
      
      def config
        @config ||= YAML.load(File.read(config_file))
      end
    end

    def config
      ::REANDeployTools.config
    end
  end
end
