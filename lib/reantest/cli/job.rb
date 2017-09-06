# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved
require 'thor'
require 'json'
require 'tempfile'
require 'shellwords'

module REANTest
  module Cli
    class Job < Base
      DEFAULTS = {
        browsers:           '{"Chrome":["53"]}',
        run_crawl:          false,
        page_load_timeout:  60,
      }

      option :job_config,  required: true,  desc: "filename to read job config from, as JSON"
      option :output,      required: true,  desc: "filename to write job status to, as JSON"
      option :wait,        default: true, type: :boolean, desc: "Wait for the test execution to complete"
      option :reuse_vm,    type: :boolean,  desc: "reuse VM     (overrides \"executionStrategy\" in --job-config)"
      option :job_name,                     desc: "job name     (overrides \"appName\" in --job-config)"
      option :test_url,                     desc: "test URL     (overrides \"testURL\" in --job-config)"
      option :git_user,                     desc: "git user     (overrides \"gitUser\" in --job-config)"
      option :git_pass,                     desc: "git password (overrides \"gitPass\" in --job-config)"
      option :git_url,                      desc: "git URL      (overrides \"gitURL\" in --job-config)"
      option :git_branch,                   desc: "git branch   (overrides \"branchName\" in --job-config)"
      desc "functionaltest", "Submits a cross-browser functional test job"
      def functionaltest
        
        # Get the base job configuration, as JSON.
        input = options[:job_config] ? JSON.parse(File.read(options[:job_config])) : {}
        input['browsers'] ||= DEFAULTS[:browsers]
        input['executionStrategy'] ||= 'boost'
          
        # Submit the testing job.
        id = submit_job 'functionaltest', input
        
        # Collect job status, possibly waiting until execution completes.
        job = collect_status id, 'functionaltest'
        job['name'] = input['appName']
        
        # Output job status.
        if output = options[:output]
          File.write(output, job.to_json)
        end

        # If we waited until the end, then fail if the job did not succeed.
        exit 1 if options[:wait] && job['status'] != 'SUCCESS'
      end

      option :job_config,  required: false, desc: "filename to read job config from, as JSON"
      option :output,      required: true,  desc: "filename to write job status to, as JSON"
      option :wait,        default: true, type: :boolean, desc: "Wait for the test execution to complete"
      option :reuse_vm,    type: :boolean,        desc: "reuse VM           (overrides \"executionStrategy\" in --job-config)"
      option :job_name,                           desc: "job name           (overrides \"appName\" in --job-config)"
      option :test_url,                           desc: "test URL           (overrides \"testURL\" in --job-config)"
      option :browsers,                           desc: "browsers JSON      (overrides \"browsers\" in --job-config)"
      option :text_to_search,                     desc: "text to search     (overrides \"textToSearch\" in --job-config)"
      option :run_crawl,   type: :boolean,        desc: "run crawl          (overrides \"runCrawl\" in --job-config)"
      option :page_load_timeout, type: :numeric,  desc: "page load timeout  (overrides \"pageLoadTimeOut\" in --job-config)"
      desc "urltest", "Submits a cross-browser URL test job"
      def urltest
        
        # Get the base job configuration, as JSON.
        input = options[:job_config] ? JSON.parse(File.read(options[:job_config])) : {}
        input['executionStrategy'] ||= 'vmReuse'
        input['runCrawl'] ||= DEFAULTS[:run_crawl]
        input['browsers'] ||= DEFAULTS[:browsers]
        input['pageLoadTimeOut'] ||= DEFAULTS[:page_load_timeout]
          
        # Submit the testing job.
        id = submit_job 'urltest', input
        
        # Collect job status, possibly waiting until execution completes.
        job = collect_status id, 'urltest'
        job['name'] = input['appName']
        
        # Output job status.
        if output = options[:output]
          File.write(output, job.to_json)
        end

        # If we waited until the end, then fail if the job did not succeed.
        exit 1 if options[:wait] && job['status'] != 'SUCCESS'
      end

      option :output, required: false, desc: "filename to write output to, as JSON"
      option :wait,   default: false, type: :boolean, desc: "Wait for the test execution to complete"
      desc "status <ID>", "Get cross-browser test job status by ID"
      def status id
        
        # Collect job status, possibly waiting until execution completes.
        job = collect_status id

        # Output job status.
        if output = options[:output]
          File.write output, job.to_json
        end

        # Fail if the job did not succeed.
        exit 1 unless job['status'] == 'SUCCESS'
      end
      
      private
      
      # Submit a test to run and return a job ID.
      def submit_job(type, input)
        raise "invalid test type: #{type}" unless type=='functionaltest' || type=='urltest'
          
        # Allow parts of the configuration to be customized by other arguments.
        input['type'] = type
        input['appName'] = options[:job_name] if options[:job_name]
        input['testURL'] = options[:test_url] if options[:test_url]
        input['gitUser'] = options[:git_user] if options[:git_user]
        input['gitPass'] = options[:git_pass] if options[:git_pass]
        input['gitURL'] = options[:git_url] if options[:git_url]
        input['branchName'] = options[:git_branch] if options[:git_branch]
        input['browsers'] = options[:browsers] if options[:browsers]
        input['textToSearch'] = options[:text_to_search] if options[:text_to_search]
        input['runCrawl'] = options[:run_crawl] if options[:run_crawl]
        input['pageLoadTimeOut'] = options[:page_load_timeout] if options[:page_load_timeout]
        input['executionStrategy'] = (options[:reuse_vm] ? 'vmReuse' : 'boost') unless options[:reuse_vm].nil?
        
        # Execute the testing job.
        id = client.post "RunTest", input
        die 'failed to run job' unless String===id && id.length > 0
        log "job #{type}: jobId #{id}"
        id
      end
      
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
        
        {'id' => id, 'status' => job}
      end
    end
  end
end