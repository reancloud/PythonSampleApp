# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved
require 'openssl'

# Workaround for invalid SSL certificates at DeployNow ELB.
# FIXME: Make this configuration driven
OpenSSL::SSL.instance_eval do
  remove_const :VERIFY_PEER if const_defined? :VERIFY_PEER # Hack to prevent warning (bundle exec preloads stuff)
end
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

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
      @conn ||= create_conn
    end
    
    def create_conn
      raise 'not implemented'
    end
  end
end