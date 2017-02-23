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

module REANDeployTools
  class Client
    include Util
    include Config
  
    # GET request to REANDeploy
    def get(path, *args)
      rp = conn.get(path, *args)
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status != 200
      JSON.parse rp.body
    end
      
    # POST request to REANDeploy
    def post(path, body, *args)
      rp = conn.post(path, *args) do |rq|
        rq.headers['Content-Type'] = 'application/json'
        rq.body = (String===body ? body : body.to_json)
      end
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status / 100 != 2
      JSON.parse rp.body
    end
    
    # DELETE request to REANDeploy
    def delete(path, *args)
      rp = conn.delete(path, *args)
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status / 100 != 2
      JSON.parse rp.body
    end
    
    private
    
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