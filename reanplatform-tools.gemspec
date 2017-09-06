# Copyright (c) 2016-2017 REAN Cloud (https://www.reancloud.com) All rights reserved
require File.expand_path('../lib/reanplatform_tools/version', __FILE__)

Gem::Specification.new do |gem|
  gem.authors       = ['Joseph Khoobyar']
  gem.email         = 'joseph.khoobyar@reancloud.com'
  gem.summary       = 'Tools for use with REAN Platform'
  gem.description   = 'Tools for use with REAN Platform, written in Ruby'
  gem.licenses      = %w(Nonstandard)
  gem.homepage      = 'https://github.com/reancloud/reanplatform-tools'
  gem.files         = `git ls-files bin lib README.md Gemfile Gemfile.lock`.split($\) +
                      %w(lib/jolt-cf2tf/transform.json lib/jolt-cf2tf/notes.txt
													vendor/jolt/jolt-cli.jar)
  gem.executables   = `git ls-files bin`.split($\).map{ |f| File.basename(f) }
  gem.name          = 'reanplatform-tools'
  gem.test_files    = `git ls-files spec`.split($\)
  gem.version       = REANPlatformTools::VERSION
  
  gem.required_ruby_version = '>= 2.3.0'
  
  gem.add_development_dependency 'bundler', '~> 1.0'
  
  gem.add_dependency 'thor', '~> 0.19.1'
  gem.add_dependency 'faraday', '~> 0.9.2'
end
