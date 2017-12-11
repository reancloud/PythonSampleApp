import logging
from . import config
from . import rest 
from cliff.command import Command

import swagger_client
from swagger_client.rest import ApiException
import json
from pprint import pprint
from ast import literal_eval


class GetProperties(Command):
    "All actions in the TestNowUtility API"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetProperties, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        apiInstance = swagger_client.TestNowUtilityApi()
        try:
                api_response = apiInstance.get_properties()   
                return  str(api_response)
            
        except ApiException as e:
            self.log.error("Exception when calling TestNowUtilityApi->: %s \n %s\n" % parsed_args.action  % e)



        # rest.RestClient.getSwaggerClient('testnowutility')
        # try:
        #     if parsed_args.action == "get_properties":
        #         api_response = apiInstance.get_properties()   
        #         # self.log.debug(api_response) 
        #         # self.app.stdout.write(api_response)
        #         # self.app.stdout.write('\n')
        #         # print json.dumps(api_response, sort_keys=True, indent=2, separators=(',', ': '))
        #         # result = json.loads(api_response,encoding='ut-8')
        #         # print api_response.decode("utf-8", "strict")
        #         print literal_eval(json.dumps(api_response))
        #         # print json.dumps(u"ברי צקלה", ensure_ascii=False).encode('utf8')
        #         # print json.dumps(api_response, ensure_ascii=True).encode('utf8')
        #         mydict = {k: unicode(v).encode("utf-8") for k,v in api_response.iteritems()}
        #         print mydict
        #         # print json.dumps(api_response, indent=4)
        #         # return  str(api_response)
        #     else:
        #         return "The Action is not yet implemented"
            
        # except ApiException as e:
        #     self.log.error("Exception when calling TestNowUtilityApi->: %s \n %s\n" % parsed_args.action  % e)

class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
