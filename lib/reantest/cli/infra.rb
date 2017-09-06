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
        exit 1 unless job['status'] == 'SUCCESS' || (options[:allow_unstable] && job['status'] == 'UNSTABLE')
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