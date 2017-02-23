require 'thor'
require 'json'

module REANDeployTools
  module Cli
    def self.client
      @client ||= ::REANDeployTools::Client.new
    end
  
    class Base < Thor
      include Util
      
      private
      
      def client
        ::REANDeployTools::Cli.client
      end
    end
  end
end