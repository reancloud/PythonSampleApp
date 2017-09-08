# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved
require 'thor'
require 'json'
require 'tempfile'
require 'shellwords'

module REANTest
  module Cli
    class Infra < Base
      DEFAULTS = {
      }
      
      option :output,      required: true,  desc: "filename to write job status to, as JSON"
      option :allow_unstable,  default: false, type: :boolean, desc: "Partial success (UNSTABLE) is acceptable"
      option :wait,        default: true, type: :boolean, desc: "Wait for the test execution to complete"
      option :job_name,                     required: true, desc: "job name"
      option :region,                       required: true, desc: "AWS region"
      option :aws_secret_access_key,        required: true, desc: "AWS secret access key"
      option :aws_access_key_id,            required: true, desc: "AWS access key id"
      option :reandeploy_env, type: :numeric, desc: "REAN Deploy environment ID to read both input and output parameters from"
      option :all_param,                    desc: "filename to read both input and output parameters from, as JSON"
      option :input_param,                  desc: "filename to read input parameter from, as JSON"
      option :output_param,                 desc: "filename to read output parameter from, as JSON"
      desc "autotest", "Submits a REAN-defined infrastructure test job"
      def autotest
        input = {}
          
        # REAN Deploy creates a single JSON file with both input and output, so we support it.
        if options[:reandeploy_env]
          die "cannot specify both --reandeploy-env and --all-param" if options[:all_param]
          all_params = read_reandeploy_env_validation_params(options[:reandeploy_env].to_i)
        elsif options[:all_param]
          all_params = read_json(options[:all_param])
        end
        if all_params
          input['input'] = all_params['input']
          input['output'] = all_params['output']
        end
        
        # Explicit input or output parameters can override the above.
        input['input'] = read_json(options[:input_param]) if options[:input_param]
        input['output'] = read_json(options[:output_param]) if options[:output_param]
          
        # Always require some input and output in order to execute.
        unless Hash===input['input'] && Hash===input['output']
          die 'infra autotest: no input/output parameters specified'
        end
          
        # Until TES-618 hits the master branch for REAN Test, we need to support the old API's bugs and format.
        input['name'] = options[:job_name]
        input['region'] = options[:region]
        input['secreteKey'] = options[:aws_secret_access_key]
        input['accessKey'] = options[:aws_access_key_id]
        input['input'].values.each{|o| o.delete('user_data') if Hash===o}
        input['input'] = input['input'].to_json
        input['output'] = input['output'].to_json
        
        # Execute the testing job.
        id = client.post "infratest/awspec", input
        die 'infra autotest: failed to run job' unless String===id && id.length > 0
        log "infra autotest: jobId #{id}"
        
        # Collect job status, possibly waiting until execution completes.
        job = collect_status id, 'autotest'
        job['name'] = input['name']
        
        # Output job status.
        if output = options[:output]
          File.write(output, job.to_json)
        end

        if options[:wait]
          # If we waited until the end, then output the reports URL.
          log "infra autotest: reports are available on #{reports_url(id)}"
          
          # If we waited until the end, then fail if the job did not succeed.
          exit 1 unless job['status'] == 'SUCCESS' || job['status'] == 'UNSTABLE'
        end
      end
      
      option :output, required: false, desc: "filename to write output to, as JSON"
      option :allow_unstable,  default: false, type: :boolean, desc: "Partial success (UNSTABLE) is acceptable"
      option :wait,   default: false, type: :boolean, desc: "Wait for the test execution to complete"
      desc "status <ID>", "Get infrastructure test job status by ID"
      def status id
        
        # Collect job status, possibly waiting until execution completes.
        job = collect_status id

        # Output job status.
        if output = options[:output]
          File.write output, job.to_json
        end

        # Fail if the job did not succeed.
        exit 1 unless job['status'] == 'SUCCESS' || job['status'] == 'UNSTABLE'
      end
      
      private
      
      def reports_url(id)
        "#{client.config['reantest']['reports_url']}/#{id}/Infra_Test/"
      end
      
      # Collect job status and possibly wait until completion.
      def collect_status(id, cmd='status')
        job = client.get "infratest/jobDetails/#{id}"
        die "infra #{cmd}: failed to get job details" unless Hash===job
        job = parse_details(id, job)
        log "infra #{cmd} #{id}: #{job['status']}"
        
        if options[:wait]
          while job.length <= 1
            sleep 5
            job = client.get "infratest/jobDetails/#{id}"
            die "infra #{cmd}: failed to get job details" unless Hash===job
            job = parse_details(id, job)
            log "infra #{cmd} #{id}: #{job['status']}"
          end
        end
        
        job
      end
      
      # REAN Test does not include Job status as part of job details API, so we must detect it
      def parse_details(id, details)
        if not Hash===details
          details = {'id' => id, 'status' => 'FAILED'}
        elsif details.length == 0
          details = {'id' => id, 'status' => 'RUNNING'}
        elsif details.length == 1
          details = details.values[0]
          details['id'] = id
          if details['failed'] == 0
            details['status'] = 'SUCCESS'
          elsif details['success'] == 0 || details.length == 0
            details['status'] = 'FAILED'
          elsif options[:allow_unstable]
            details['status'] = 'UNSTABLE'
          else
            details['status'] = 'FAILED'
          end
        end
        details
      end
      
      # Integration with REAN Deploy to read environment validation parameters
      def read_reandeploy_env_validation_params(id)
        require 'reandeploy'
        rd_client = ::REANDeploy::Cli.client
         
        validation_params = rd_client.get "env/validation/param/#{id}"
        out "reandeploy: env get_validation_params ##{id}"
        validation_params
      end
    end
  end
end