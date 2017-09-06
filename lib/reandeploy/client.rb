# Copyright (c) 2017 REAN Cloud (https://www.reancloud.com) All rights reserved

module REANDeploy
  class Client < REANPlatformTools::RestClient
    
    private
    
    # Connection to REANDeploy
    def create_conn
      @conn = Faraday.new url: config['dnow']['base_url']
      @conn.headers['Authorization'] = config['dnow'].values_at('username', 'password').map{|v| URI.escape(v)}.join(':')
      @conn.headers['Accepts'] = 'application/json'
      @conn
    end
  end
end