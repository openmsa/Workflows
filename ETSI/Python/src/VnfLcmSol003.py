import json
import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi


class VnfLcmSol003(BaseApi):

    NSLCM_BASE_URL = 'sol003/vnflcm/v1/vnf_instances'

    def vnf_lcm_create_instance(self, _payload):
        response = self.do_post(self.NSLCM_BASE_URL, _payload)
        return response
