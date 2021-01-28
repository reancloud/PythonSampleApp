# frozen_string_literal: true

load 'pipeline-tasks/rake/artifact/python.rake'

#after 'release:finish', 'document:generate'
namespace :document do
    task 'generate' do
    run 'sh doc_release_script.sh'
    end
end

