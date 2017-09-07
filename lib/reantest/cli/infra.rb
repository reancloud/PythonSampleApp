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
      option :job_name,                     desc: "job name"
      option :region,                       desc: "AWS region"
      option :aws_secret_access_key,        desc: "AWS secret access key"
      option :aws_access_key_id,            desc: "AWS access key id"
      option :input_param,                  desc: "filename to read input parameter from, as JSON"
      option :output_param,                 desc: "filename to read output parameter from, as JSON"
      desc "autotest", "Submits a REAN-defined infrastructure test job"
      def autotest
        input = {}
          
        # Allow parts of the configuration to be customized by other arguments.
        input['name'] = options[:job_name] if options[:job_name]
        input['region'] = options[:region] if options[:region]
        input['secreteKey'] = options[:aws_secret_acces_key] if options[:aws_secret_acces_key]
        input['accessKey'] = options[:aws_access_key_id] if options[:aws_access_key_id]
        input['input'] = File.read(options[:inputParam]) if options[:inputParam]
        input['output'] = File.read(options[:outputParam]) if options[:outputParam]
        
        # Execute the testing job.
        id = client.post "infratest/awspec", input
        die 'failed to run job' unless String===id && id.length > 0
        log "infra autotest: jobId #{id}"
        id
        
        # Collect job status, possibly waiting until execution completes.
        job = collect_status id, 'autotest'
        job['name'] = input['name']
        
        # Output job status.
        if output = options[:output]
          File.write(output, job.to_json)
        end

        # If we waited until the end, then fail if the job did not succeed.
        exit 1 if options[:wait] && job['status'] != 'SUCCESS' && job['status'] != 'UNSTABLE'
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
      
      # Collect job status and possibly wait until completion.
      def collect_status(id, cmd='status')
        job = client.get "infratest/jobDetails/#{id}"
        die 'failed to get job details' unless Hash===job
        job['status'] = parse_status(job)
        log "infra #{cmd} #{id}: #{job['status']}"
        
        if options[:wait]
          while job.length == 0
            sleep 5
            job = client.get "infratest/jobDetails/#{id}"
            die 'failed to get job details' unless Hash===job
            job['status'] = parse_status(job)
            log "infra #{cmd} #{id}: #{job['status']}"
          end
        end
        
        job
      end
      
      # REAN Test does not include Job status as part of job details API, so we must detect it
      def parse_status(details)
        if details.length == 0
          'RUNNING'
        elsif details['failed'] == 0
          'SUCCESS'
        elsif details['success'] == 0
          'FAILED'
        else
          options[:allow_unstable] ? 'UNSTABLE' : 'FAILED'
        end
      end
    end
  end
end