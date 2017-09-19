# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved
require 'openssl'
require 'timeout'
require 'uri'
require 'json'
require 'faraday'

module REANPlatformTools
  class RestClient
    include Config
    
    # Utility class for handling attachments.
    class Attachment < Struct.new(:filename, :length, :content_type, :content)
    end

    class << self

      # Global SSL configuration.      
      def configure_ssl!(config)
        configure_verify_ssl! config
      end
      
      # Workaround for invalid SSL certificates in deployments.  Opt-in only.
      def configure_verify_ssl!(config)
        if config.key?('verify_ssl') && (FalseClass === config['verify_ssl'] || config['verify_ssl'] == 'false')
        
          # FIXME: Make this configuration driven
          OpenSSL::SSL.instance_eval do
            remove_const :VERIFY_PEER if const_defined? :VERIFY_PEER # Hack to prevent warning (bundle exec preloads stuff)
            const_set :VERIFY_PEER, const_get(:VERIFY_NONE)
          end
        end
        
        # Make sure that this hack only runs once.
        instance_eval 'def configure_ssl!(config); end'
      end
    end    
  
    # GET request
    def get(path, *args, &block)
      rp = conn.get(path, *args, &block)
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status != 200
      unwrap_body rp, args
    end
      
    # POST request
    def post(path, body, *args, &block)
      rp = conn.post(path, *args) do |rq|
        rq.headers['Content-Type'] = 'application/json'
        rq.body = (String===body ? body : body.to_json)
        block.call(rq) if block
      end
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status / 100 != 2
      unwrap_body rp, args
    end
    
    # DELETE request
    def delete(path, *args, &block)
      rp = conn.delete(path, *args, &block)
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status / 100 != 2
      unwrap_body rp, args
    end
    
    private
    
    def unwrap_body(rp, args)
      if Hash===args.last
        case args.last[:result]
        when :body then return rp.body
        when :response then return rp
        end
      end
      
      case content_type = rp['Content-Type']
      when 'application/json', 'text/json'
        JSON.parse(rp.body)
      when 'text/plain'
        rp.body
      else
        if /^attachment; filename="([^"]+)"/ === rp['Content-Disposition']
          Attachment.new(File.basename($1), (rp['Content-Length'].to_i rescue nil), content_type, rp.body)
        else
          die "unable to automatically parse response body"
        end
      end
    end
    
    # Connection
    def conn
      @conn ||= begin
        configure_ssl!
        create_conn
      end
    end
    
    def create_conn
      raise 'not implemented'
    end
    
    # Workaround for SSL certificate handling issue
    def configure_ssl!
      ::REANPlatformTools::RestClient.configure_ssl! config
      if OpenSSL::SSL::VERIFY_PEER == OpenSSL::SSL::VERIFY_NONE
        out "reanplatform: INSECURE WARNING: SSL certificate validation is disabled"
      end
    end
  end
end