#!/usr/bin/env ruby
#
# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved
#

# Fix output buffering if running in Jenkins.
$stdout.sync = true
$stderr.sync = true

# Fix invalid SSL certificate for DeployNow ELB.
require 'openssl'
OpenSSL::SSL.instance_eval{ remove_const :VERIFY_PEER }    # Hack to prevent warning (bundle exec preloads stuff)
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

require 'thor'
require 'timeout'
require 'uri'
require 'json'
require 'faraday'
require 'yaml'

SCRIPT_NAME = File.basename($0, '.rb')

# Initial configuration.
CONFIG = YAML.load(File.read(File.expand_path('../config.yml', __FILE__)))

class REANDeploy
  module Util
    
    protected
    
    # Logging output.
    def log(*items)
      $stderr.puts "#{SCRIPT_NAME}: #{items.join(' ')}"
    end

    # Fatal exit.
    def die(*items)
      log(*items)
      exit 1
    end
    
    # Connection to REANDeploy
    def conn
      unless defined? @conn
        @conn = Faraday.new url: CONFIG['dnow']['base_url']
        @conn.headers['Authorization'] = CONFIG['dnow'].values_at('username', 'password').map{|v| URI.escape(v)}.join(':')
        @conn.headers['Accepts'] = 'application/json'
      end
      @conn
    end
  
    # GET request to REANDeploy
    def dnow_get(path, *args)
      rp = conn.get(path, *args)
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status != 200
      JSON.parse rp.body
    end
      
    # POST request to REANDeploy
    def dnow_post(path, body, *args)
      rp = conn.post(path, *args) do |rq|
        rq.headers['Content-Type'] = 'application/json'
        rq.body = (String===body ? body : body.to_json)
      end
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status / 100 != 2
      JSON.parse rp.body
    end
    
    # DELETE request to REANDeploy
    def dnow_delete(path, *args)
      rp = conn.delete(path, *args)
      die "request failed #{rp.env.url} (#{rp.status})" if rp.status / 100 != 2
      JSON.parse rp.body
    end
      
  end
  
  class Env < Thor
    include Util
    
    option :inputs, desc: "JSON file describing input variables"
    option :outputs, desc: "filename to write outputs to, as JSON"
    option :deploy_config, desc: "JSON file describing deployment configuration"
    option :wait, default: true, type: :boolean, desc: "Wait for the operation to finish"
    desc "deploy <ID-or-NAME>", "Deploy an environment identified by ID or by NAME"
    def deploy id_or_name
      id = get_env_id(id_or_name)
      
      # Parse the deployment configuration as JSON, if it exists.
      if deploy_config = options[:deploy_config]
        die "unable to parse deployment config JSON: #{deploy_config.inspect}" unless File.exists?
        deploy_config = JSON.parse(File.read(deploy_config))
      end
      
      # Get the existing resources for this environment.
      resources = dnow_get("env/resources/#{id}")
      
      # Apply any input variables from a JSON file, if it exists.
      if vars = options[:inputs]
        die "unable to parse input vars JSON: #{vars.inspect}" unless File.exists? vars
        vars = JSON.parse(File.read(vars))
      
        # Only apply input variables if they have been defined.
        if input_resource = resources.find{|r| r['resourceName']=='Input Variables' }

          # Only set variables that are already defined and have scalar values.
          input_vars = input_resource['attributes'].find{|a| a['name']=='input_variables'}
          input_vars['validValue'].each_key do |key|
            input_vars['validValue'][key] = vars[key] if vars.include?(key) && !(Array===vars[key] || Hash===vars[key])
          end
          input_vars['value'] = input_vars['validValue'].to_json
            
          # Retrieve the environment, then save the input variables back.
          dnow_post "env/saveAll", environment: dnow_get("env/#{id}"), resourcesToSave: [input_resource]
        end
      end
      
      # Now we can deploy the environment.
      log "env deploy ##{id}"
      env = dnow_post "env/deploy/#{id}", deployConfig: deploy_config
      log "env deploy ##{id}: #{env['status']} #{env['name'].inspect} (#{env['tfRunId']})"
      
      # Optionally wait for the deployment to complete.
      if options[:wait]
        begin
          sleep 5
          envDeployment = dnow_get "env/deploy/deployment/#{env['tfRunId']}"
          log "env deploy ##{id}: #{envDeployment['status']} #{env['name'].inspect} (#{env['tfRunId']})"
        end while envDeployment['status'] == 'DEPLOYING'
        
        # Fail unless the deployment succeeded.
        exit 1 unless envDeployment['status'] == 'DEPLOYED'
          
        # If we have waited for the deployment to complete, then we can collect outputs.
        if envDeployment['status'] == 'DEPLOYED' and
              outputs = options[:outputs] and
              output_resource = resources.find{|r| r['resourceName']=='output' }
          resource_status = dnow_get "env/deploy/#{id}"
          if output_status = resource_status[output_resource['id'].to_s]
            File.write(outputs, output_status.find{|x| x['otherAttributes']}['otherAttributes'].to_json)
          end
        end
      end
    end
    
    option :wait, default: true, type: :boolean, desc: "Wait for the operation to finish"
    desc "destroy <ID-or-NAME>", "Destroy an environment identified by ID or by NAME"
    def destroy id_or_name
      id = get_env_id(id_or_name)
      
      # Now we can destroy the environment.
      log "env destroy ##{id}"
      env = dnow_delete "env/deploy/#{id}"
      log "env destroy ##{id}: #{env['status']} #{env['name'].inspect} (#{env['tfRunId']})"
      
      # Optionally wait for the destroy to complete.
      if options[:wait]
        begin
          sleep 5
          envDeployment = dnow_get "env/deploy/deployment/#{env['tfRunId']}"
          log "env destroy ##{id}: #{envDeployment['status']} #{env['name'].inspect} (#{env['tfRunId']})"
        end while envDeployment['status'] == 'DESTROYING'
        
        # Fail unless the destroy succeeded.
        exit 1 unless envDeployment['status'] == 'DESTROYEDj'
      end
    end
    
    protected
    
    def get_env_id(name)
      # Short-circuit in case we are called from somewhere other than the command-line.
      if Fixnum===name
        name
        
      # If a numeric ID was not passed, we need to get the environment by name.
      elsif name !~ /^\d+$/
        die "getting an environment by name is not yet supported"
        
      # Otherwise, just use the numeric ID.
      else
        name.to_i
      end
    end
  end

  class Tool < Thor
    desc "env SUBCOMMAND ...ARGS", "Manage an environment"
    subcommand "env", Env
  end
  
end

# Process the command
REANDeploy::Tool.start(ARGV)
