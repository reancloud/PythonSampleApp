#!/usr/bin/env ruby
require 'optparse'
require 'timeout'
require 'uri'
require 'json'
require 'faraday'
require 'yaml'

SCRIPT_NAME=File.basename($0, '.rb')

# Fix invalid SSL certificate for DeployNow ELB.
require 'openssl'
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

# Fix output buffering if running in Jenkins.
$stdout.sync = true
$stderr.sync = true

# Logging output.
def log(*items)
	$stderr.puts "#{SCRIPT_NAME}: #{items.join(' ')}"
end

# Fatal exit.
def die(*items)
	log(*items)
	exit 1
end

# Read config.
@config = YAML.load(File.read(File.expand_path('../config.yml', __FILE__)))

# Set up connection to DNow.
@conn = Faraday.new url: @config['dnow']['base_url']
@conn.headers['Authorization'] = @config['dnow'].values_at('username', 'password').map{|v| URI.escape(v)}.join(':')
@conn.headers['Accepts'] = 'application/json'
  
def dnow_get(path, *args)
  rp = @conn.get(path, *args)
  die "request failed #{rp.env.url} (#{rp.status})" if rp.status != 200
  JSON.parse rp.body
end
  
def dnow_post(path, body, *args)
  rp = @conn.post(path, *args) do |rq|
    rq.headers['Content-Type'] = 'application/json'
    rq.body = (String===body ? body : body.to_json)
  end
  die "request failed #{rp.env.url} (#{rp.status})" if rp.status / 100 != 2
  JSON.parse rp.body
end
