# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved
require 'thor'
require 'json'
require 'tempfile'
require 'shellwords'

module REANTest
  module Cli
    class Job < Base

      option :job_config,  required: true,  desc: "filename to read input from, as JSON"
      option :output,      required: true,  desc: "filename to write output to, as JSON"
      option :wait,        default: true, type: :boolean, desc: "Wait for the test execution to complete"
      option :reuse_vm,    type: :boolean,  desc: "reuse VM     (overrides \"executionStrategy\" in --job-config)"
      option :job_name,                     desc: "job name     (overrides \"appName\" in --job-config)"
      option :test_url,                     desc: "test URL     (overrides \"testURL\" in --job-config)"
      option :git_user,                     desc: "git user     (overrides \"gitUser\" in --job-config)"
      option :git_pass,                     desc: "git password (overrides \"gitPass\" in --job-config)"
      option :git_url,                      desc: "git URL      (overrides \"gitURL\" in --job-config)"
      option :git_branch,                   desc: "git branch   (overrides \"branchName\" in --job-config)"
      desc "runTest <TYPE>", "Run a cross-browser test job of the specified TYPE: functionaltest | urltest"
      def runTest(type)
        raise "invalid test type: #{type}" unless type=='functionaltest' || type=='urltest'
        
        # Get the base job configuration, as JSON.
        input = JSON.parse(File.read(options[:job_config]))
          
        # Allow parts of the configuration to be customized by other arguments.
        input['type'] = type
        input['appName'] = options[:job_name] if options[:job_name]
        input['testURL'] = options[:test_url] if options[:test_url]
        input['gitUser'] = options[:git_user] if options[:git_user]
        input['gitPass'] = options[:git_pass] if options[:git_pass]
        input['gitURL'] = options[:git_url] if options[:git_url]
        input['branchName'] = options[:git_branch] if options[:git_branch]
        case options[:reuse_vm]
        when FalseClass
          input['executionStrategy'] = 'boost'
        when TrueClass
          input['executionStrategy'] = 'vmReuse'
        else
          input['executionStrategy'] ||= 'boost'
        end
        
        # Execute the testing job.
        id = client.post "RunTest", input
        die 'failed to run job' unless String===id && id.length > 0
        
        # Collect job status, possibly waiting until execution completes.
        job = collect_status(id, 'functionaltest')
        job['name'] = input['appName']
        
        # Output job status.
        if output = options[:output]
          File.write(output, job.to_json)
        end

        # If we waited until the end, then fail if the job did not succeed.
        exit 1 if options[:wait] && job['status'] != 'SUCCESS'
      end

      option :output, required: true, desc: "filename to write output to, as JSON"
      option :wait,   default: false, type: :boolean, desc: "Wait for the test execution to complete"
      desc "status <ID>", "Get cross-browser test job status by ID"
      def status id
        # Collect job status, possibly waiting until execution completes.
        job = collect_status(id)

        # Output job status.
        if output = options[:output]
          File.write(output, job.to_json)
        end

        # Fail if the job did not succeed.
        exit 1 unless job['status'] == 'SUCCESS'
      end
      
      private
      
      # Collect job status and possibly wait until completion.
      def collect_status(id, cmd='status')
        job = client.get "RunTest/jobStatus/#{id}"
        die 'failed to get job status' unless String===job && job.length > 0
        log "job #{cmd} #{id}: #{job}"
        
        if options[:wait]
          while job == 'SUBMITTED' || job == 'RUNNING'
            sleep 5
            job = client.get "RunTest/jobStatus/#{id}"
            die 'failed to get job status' unless String===job && job.length > 0
            log "job #{cmd} #{id}: #{job}"
          end
        end
        
        job = {'id' => id, 'status' => job}
      end
    end
  end
end