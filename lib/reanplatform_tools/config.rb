# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved
require 'yaml'

module REANPlatformTools
  module Config
    class << self
      include Util
      
      attr_accessor :script_name
      attr_writer :config_file
      
      def config_file
        @config_file ||= File.join(ENV['HOME'] || '.', '.reanplatform-tools')
      end
      
      def config
        @config ||= YAML.load(File.read(config_file))
      rescue SystemCallError => e
        die "reading config file: #{e.message}"
      end
    end

    def config
      ::REANPlatformTools::Config.config
    end
  end
end
