require 'thor'
require 'json'
require 'tempfile'
require 'shellwords'

module REANDeployTools
  module Cli
    class Env < Base

      option :outputs, required: true, desc: "filename to write outputs to, as JSON"
      desc "get_outputs <ID-or-NAME>", "Get outputs for an environment identified by ID or by NAME"
      def get_outputs id_or_name
        id = get_env_id(id_or_name)
         
        envDeployment = client.get "env/deploy/deployment/#{env['tfRunId']}"
        log "env get_outputs ##{id}: #{envDeployment['status']} #{env['name'].inspect} (#{env['tfRunId']})"

        # Fail if the environment is not deployed.
        exit 1 unless envDeployment['status'] == 'DEPLOYED'

        # If the environment is deployed, then we can collect outputs.
        if outputs = options[:outputs] and output_resource = resources.find{|r| r['resourceName']=='output' }
          resource_status = client.get "env/deploy/#{id}"
          if output_status = resource_status[output_resource['id'].to_s]
            File.write(outputs, output_status.find{|x| x['otherAttributes']}['otherAttributes'].to_json)
          end
        end
      end

      option :output, required: true, desc: "filename to write output to, as JSON"
      desc "get_validation_params <ID-or-NAME>", "Get validation params for an environment identified by ID or by NAME"
      def get_validation_params id_or_name
        id = get_env_id(id_or_name)
         
        validation_params = client.get "env/validation/param/#{id}"
        log "env get_validation_params ##{id}"

        if output = options[:output]
          File.write(output, validation_params.to_json)
        end
      end

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
            client.post("env/saveAll", environment: client.get("env/#{id}"), resourcesToSave: [input_resource]) do |rq|
              rq.headers['headerEnvId'] = id.to_s
              rq.headers['modifiedOn'] = (Time.new.utc.to_i * 1000).to_s
            end
          end
        end

        # Now we can deploy the environment.
        log "env deploy ##{id}"
        env = client.post("env/deploy/#{id}", deployConfig: deploy_config) do |rq|
          rq.headers['headerEnvId'] = id.to_s
          rq.headers['modifiedOn'] = (Time.new.utc.to_i * 1000).to_s
        end
        tfRunId = env['tfRunId']
        envStatus = env['status']
        log "env deploy ##{id}: #{envStatus} #{env['name'].inspect} (#{tfRunId})"

        # Optionally wait for the deployment to complete.
        if options[:wait]
          begin
            sleep 5
            
            # Workaround for DEP-4951: use Environment level status instead of EnvDeployment
            env = client.get "env/#{id}"
            envStatus = env['status']
            #envDeployment = client.get "env/deploy/deployment/#{tfRunId}"
            #envStatus = envDeployment['status']
            log "env deploy ##{id}: #{envStatus} #{env['name'].inspect} (#{tfRunId})"
          end while envStatus == 'DEPLOYING'

          # Fail unless the deployment succeeded.
          exit 1 unless envStatus == 'DEPLOYED'

          # If we have waited for the deployment to complete, then we can collect outputs.
          if outputs = options[:outputs] and output_resource = resources.find{|r| r['resourceName']=='output' }
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
        env = client.delete("env/deploy/#{id}") do |rq|
          rq.headers['headerEnvId'] = id.to_s
          rq.headers['modifiedOn'] = (Time.new.utc.to_i * 1000).to_s
        end
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

      option :format, enum: %w(json blueprint tf cf), required: true, desc: "Export format"
      option :output, required: true, desc: "Output file for json or blueprint formats.  Output directory for tf and cf formats."
      
      JOLT_TRANSFORM = File.expand_path('../../../jolt-cf2tf/transform.json', __FILE__).shellescape
      JOLT_NOTES = File.expand_path('../../../jolt-cf2tf/notes.txt', __FILE__)
      
      desc "export <ID-or-NAME>", "Export an environment identified by ID or by NAME"
      def export id_or_name
        id = get_env_id(id_or_name)
        self.destination_root = options[:output]
        
        case format = options[:format]
        when 'json'
          json = client.get "env/export/#{id}", result: :body
          file = options[:output]
          File.write file, json
          log "env export ##{id} (#{format}) => #{file} (#{json.length} bytes)"
          
        when 'blueprint'
          json = client.get "env/export/blueprint/#{id}", result: :body
          file = options[:output]
          File.write file, json
          log "env export ##{id} (#{format}) => #{file} (#{json.length} bytes)"
          
        when 'tf', 'cf'
          # Download the Terraform source code and save it in the output directory.
          tarball = client.get "env/download/terraform/#{id}"
          create_file tarball.filename, tarball.content
          
          # Unpack all of the Terraform source code.
          empty_directory 'terraform'
          inside 'terraform' do
            run "tar xzf ../#{tarball.filename.shellescape}"
          end
          
          # Optionally convert Terraform to CloudFormation 
          if format == 'cf'
            failures = []
              
            empty_directory 'CloudFormation'
            inside 'CloudFormation' do
              Dir['../terraform/*.tf.json'].each do |tffile|
                
                # Attempt to convert this file.  
                cfjson = jolt_transform tffile
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
           
            # Make sure that people are warned about the alpha nature of this conversion.
            say <<NOTES
WARNING: CloudFormation conversion support is very limited and requires manual intervention.
         See the following notes about this conversion process.
         
NOTES
            say File.read(JOLT_NOTES)
            say <<NOTES

WARNING: Please carefully read the above notes and then manually complete the conversion process.
NOTES
          end
          
          log "env export ##{id} (#{format}) => #{options[:output]} (directory)"
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
      
      private
      
      def jolt_transform(tffile)
        @jolt_cmd ||= begin
          jolt_cli_jar = File.expand_path('../../../../vendor/jolt/jolt-cli.jar', __FILE__)
          if File.exist? jolt_cli_jar
            "java -jar #{jolt_cli_jar.shellescape}"
          else
            "jolt"
          end
        end
        run("#{@jolt_cmd} transform #{JOLT_TRANSFORM} #{tffile.shellescape}", capture: true) || ''
      end
    end
  end
end