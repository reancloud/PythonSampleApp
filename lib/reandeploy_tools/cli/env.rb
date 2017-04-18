require 'thor'
require 'json'
require 'tempfile'
require 'shellwords'

module REANDeployTools
  module Cli
    class Env < Base

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
        resources = client.get("env/resources/#{id}")

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
            client.post "env/saveAll", environment: client.get("env/#{id}"), resourcesToSave: [input_resource]
          end
        end

        # Now we can deploy the environment.
        log "env deploy ##{id}"
        env = client.post "env/deploy/#{id}", deployConfig: deploy_config
        log "env deploy ##{id}: #{env['status']} #{env['name'].inspect} (#{env['tfRunId']})"

        # Optionally wait for the deployment to complete.
        if options[:wait]
          begin
            sleep 5
            envDeployment = client.get "env/deploy/deployment/#{env['tfRunId']}"
            log "env deploy ##{id}: #{envDeployment['status']} #{env['name'].inspect} (#{env['tfRunId']})"
          end while envDeployment['status'] == 'DEPLOYING'

          # Fail unless the deployment succeeded.
          exit 1 unless envDeployment['status'] == 'DEPLOYED'

          # If we have waited for the deployment to complete, then we can collect outputs.
          if envDeployment['status'] == 'DEPLOYED' and
          outputs = options[:outputs] and
          output_resource = resources.find{|r| r['resourceName']=='output' }
            resource_status = client.get "env/deploy/#{id}"
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
        env = client.delete "env/deploy/#{id}"
        log "env destroy ##{id}: #{env['status']} #{env['name'].inspect} (#{env['tfRunId']})"

        # Optionally wait for the destroy to complete.
        if options[:wait]
          begin
            sleep 5
            envDeployment = client.get "env/deploy/deployment/#{env['tfRunId']}"
            log "env destroy ##{id}: #{envDeployment['status']} #{env['name'].inspect} (#{env['tfRunId']})"
          end while envDeployment['status'] == 'DESTROYING'

          # Fail unless the destroy succeeded.
          exit 1 unless envDeployment['status'] == 'DESTROYED'
        end
      end

      option :format, enum: %w(json blueprint tf cf), required: true, desc: "Export format: json, blueprint, tf, cf"
      option :output, required: true, desc: "Output file for json or blueprint formats, output directory for tf and cf formats"
      
      JOLT_TRANSFORM = File.expand_path('../../../jolt-cf2tf/transform.json', __FILE__).shellescape
      JOLT_NOTES = File.expand_path('../../../jolt-cf2tf/notes.txt', __FILE__)
      
      desc "export <ID-or-NAME>", "Export an environment identified by ID or by NAME"
      def export id_or_name
        id = get_env_id(id_or_name)
        self.destination_root = options[:output]
        
        case format = options[:format]
        when 'tf', 'cf'
          tarball = client.get "env/download/terraform/#{id}"
          log "env export ##{id} (#{format}) => #{tarball.filename} (#{tarball.length})"
          
          create_file tarball.filename, tarball.content
          empty_directory 'terraform'
          inside 'terraform' do
            run "tar xzf ../#{tarball.filename.shellescape}"
          end
            
          if format == 'cf'
            failures = []
              
            empty_directory 'CloudFormation'
            inside 'CloudFormation' do
              Dir['../terraform/*.tf.json'].each do |tffile|
                
                # Attempt to convert this file.  
                cfjson = run("jolt transform #{JOLT_TRANSFORM} #{tffile.shellescape}", capture: true) || ''
                case cfjson
                when '', '[]', '{}', 'null'
                  failures << File.basename(tffile)
                  say "WARNING: Could not to convert #{File.basename(tffile)} to CloudFormation"
                else
                  cffile = File.basename(tffile,'.tf.json') + '.cf.json'
                  create_file cffile, cfjson
                end
              end
            end
           
            say <<NOTES
WARNING: CloudFormation conversion support is very limited and requires manual intervention.
         See the following notes about this conversion process.
         
NOTES
            say File.read(JOLT_NOTES)
          end
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
  end
end