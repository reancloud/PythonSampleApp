$LOAD_PATH.unshift File.expand_path("../lib", __FILE__)

require "reandeploy_tools/version"

file 'tmp/jolt' do
  mkdir_p 'tmp'
  Dir.chdir 'tmp' do
    sh "git clone https://github.com/bazaarvoice/jolt.git"
  end
end

file 'vendor/jolt/jolt-cli.jar' => 'tmp/jolt' do
  #Dir.chdir 'tmp/jolt' do
  #  sh "mvn clean package"
  #end
  mkdir_p "vendor/jolt"
  sh "cp -va tmp/jolt/cli/target/jolt-cli-*-SNAPSHOTt.jar vendor/jolt/jolt-cli.jar"
end

task :clean  do
  rm_rf "*.gem"
  rm_rf "pkg"
  rm_rf "vendor/jolt"
  rm_rf "tmp"
end

task :build => 'vendor/jolt/jolt-cli.jar' do
  system "gem build reandeploy-tools.gemspec"
end

task :default => :build