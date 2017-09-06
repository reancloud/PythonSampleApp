require 'thor'
require 'json'
require 'tempfile'
require 'shellwords'

module REANTest
  module Cli
    class Job < Base

      option :output, required: true, desc: "filename to write output to, as JSON"
      desc "status <ID>", "Get job status by ID"
      def status id
        job = client.get "RunTest/jobStatus/#{id}"
        case job
        when String
          # Until TES-672 is closed, REAN Test jobs won't return JSON even when we use the right Accepts header.
          job = {'status' => job}
        end
        
        log "job status #{id}: #{job['status']} #{job['name'] || '(Unknown job name)'}"

        # Fail if the job does not give any status
        exit 1 unless job['status'] == 'SUCCESS'

        # If the environment is deployed, then we can collect outputs.
        if output = options[:output]
          File.write(output, output.to_json)
        end
      end
    end
  end
end