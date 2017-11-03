import logging
from . import config
import swagger_client
from swagger_client.rest import ApiException
import validators

class Utility():
    "generate the swagger client in this class"

    log = logging.getLogger(__name__)
    
    @staticmethod
    def getUniqueSeq(seq): 
        # order preserving
        checked = list(set(seq))
        return checked

    @staticmethod
    def getBrowserDTO(params):

        log = logging.getLogger(__name__)
        log.debug(params)
        browser_list = swagger_client.BrowsersDto()

        if(params.firefox != None):
            firefox = Utility.getUniqueSeq(params.firefox.split(","))
            log.debug(firefox)
            browser_list.firefox = firefox
        if(params.chrome != None):
            chrome = Utility.getUniqueSeq(params.chrome.split(","))
            log.debug(chrome)
            browser_list.chrome = chrome
            
        
        log.debug(browser_list)
        return browser_list

    @staticmethod
    def validateInputs(self,params):
        # All the parameters validations goes in this function
        # log = logging.getLogger(__name__)
        # self.log.debug(params)
        message = ""

        # Validation for Test URL 
        if not validators.url(params.test_url):
            message = "Please enter valid Test URL."
        
        #Valodation for Browser list
        elif (params.firefox == None and 
                params.chrome == None and 
                params.ie == None and
                params.opera == None and
                params.safari == None and
                params.ios == None and
                params.ui_perf_analysis == None and
                params.device == None
                ):

            message = "Please Provide atleast one browser to Test."

        return message

    

        
