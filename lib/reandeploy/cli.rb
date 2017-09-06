# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved
require 'thor'
require 'json'
require 'pp'

module REANDeploy
  module Cli
    def self.client
      @client ||= ::REANDeploy::Client.new
    end
  
    class Base < Thor
      include Util
      include Thor::Actions
      
      def self.inherited(base)
        base.instance_eval do
          class_option :config, default: REANPlatformTools::Config.config_file, desc: "location of the reanplatform-tools config file"
        end unless base.name =~ /::Main$/
      end
      
      private
      
      # FIXME: There should be a *documented* way to get notified by Thor about class options.
      def options=(_options)
        REANPlatformTools::Config.config_file = _options['config'] if _options.include? 'config'
        super
      end
      
      def client
        ::REANDeploy::Cli.client
      end
    end
  end
end