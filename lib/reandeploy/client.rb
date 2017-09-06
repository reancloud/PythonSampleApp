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

module REANDeploy
  class Client
    include Util
    include Config
    
    # Utility class for handling attachments.
    class Attachment < Struct.new(:filename, :length, :content_type, :content)
    end
  
    # GET request to REANDeploy
    def get(path, *args, &block)
      rp = conn.get(path, *args, &block)
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status != 200
      unwrap_body rp, args
    end
      
    # POST request to REANDeploy
    def post(path, body, *args, &block)
      rp = conn.post(path, *args) do |rq|
        rq.headers['Content-Type'] = 'application/json'
        rq.body = (String===body ? body : body.to_json)
        block.call(rq) if block
      end
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status / 100 != 2
      unwrap_body rp, args
    end
    
    # DELETE request to REANDeploy
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
      else
        if /^attachment; filename="([^"]+)"/ === rp['Content-Disposition']
          Attachment.new(File.basename($1), (rp['Content-Length'].to_i rescue nil), content_type, rp.body)
        end
      end
    end
    
    # Connection to REANDeploy
    def conn
      unless defined? @conn
        @conn = Faraday.new url: config['dnow']['base_url']
        @conn.headers['Authorization'] = config['dnow'].values_at('username', 'password').map{|v| URI.escape(v)}.join(':')
        @conn.headers['Accepts'] = 'application/json'
      end
      @conn
    end
  end
end