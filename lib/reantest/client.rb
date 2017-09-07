# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved

module REANTest
  class Client < REANPlatformTools::RestClient
    include Util
    
    private
    
    # Connection to REANDeploy
    def create_conn
      @conn = Faraday.new url: config['reantest']['base_url']
      @conn.headers['Authorization'] = config['reantest'].values_at('username', 'password').map{|v| URI.escape(v)}.join(':')
      @conn.headers['Accepts'] = 'application/json'
      @conn
    end
  end
end