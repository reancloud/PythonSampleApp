# Copyright (c) 2016-2017 REAN Cloud (https://www.reancloud.com) All rights reserved
$LOAD_PATH.unshift File.expand_path("../lib", __FILE__)

require "reandeploy_tools/version"

file 'tmp/jolt' do
  mkdir_p 'tmp'
  Dir.chdir 'tmp' do
    sh "git clone https://github.com/bazaarvoice/jolt.git"
  end
end

file 'tmp/jolt/cli/target/maven-archiver/pom.properties' => 'tmp/jolt' do
  Dir.chdir 'tmp/jolt' do
    sh "mvn clean package" unless File.exist? 'cli/target/maven-archiver/pom.properties'
  end
end

file 'vendor/jolt/jolt-cli.jar' => 'tmp/jolt/cli/target/maven-archiver/pom.properties' do
  mkdir_p "vendor/jolt"
  sh "cp -va tmp/jolt/cli/target/jolt-cli-*-SNAPSHOT.jar vendor/jolt/jolt-cli.jar && touch vendor/jolt/jolt-cli.jar"
end

task :clean  do
  rm_rf "*.gem"
  rm_rf "pkg"
  rm_rf "vendor/jolt"
  rm_rf "tmp"
end

task :build => 'vendor/jolt/jolt-cli.jar' do
  sh "gem build reanplatform-tools.gemspec"
end

task :install => 'vendor/jolt/jolt-cli.jar' do
  sh "gem install reanplatform-tools-#{REANPlatformTools::VERSION}.gem"
end

task :default => :build