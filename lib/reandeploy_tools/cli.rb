require 'thor'
require 'json'
require 'pp'

module REANDeployTools
  module Cli
    def self.client
      @client ||= ::REANDeployTools::Client.new
    end
  
    class Base < Thor
      include Util
      include Thor::Actions
      
      def self.inherited(base)
        base.instance_eval do
          class_option :config, default: REANDeployTools::Config.config_file, desc: "location of the reandeploy-tools config file"
        end unless base.name =~ /::Main$/
      end
      
      private
      
      # FIXME: There should be a *documented* way to get notified by Thor about class options.
      def options=(_options)
        REANDeployTools::Config.config_file = _options['config'] if _options.include? 'config'
        super
      end
      
      def client
        ::REANDeployTools::Cli.client
      end
    end
  end
end