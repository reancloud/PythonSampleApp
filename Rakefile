# frozen_string_literal: true

load 'pipeline-tasks/rake/artifact/python.rake'

after 'release:finish', 'document:generate'
# bundle
# bundle exec rake document:generate
namespace :document do
task 'generate' do
 run 'sh doc_release_script.sh'
  #run fetch(:artifactory_username), fetch(:artifactory_api_key), 
end
end

