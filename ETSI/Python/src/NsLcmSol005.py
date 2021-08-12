import json
import requests
import base64
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi


class NsLcmSol005(BaseApi):

    NSLCM_URL = "sol005/nslcm/v1/ns_instances"

    def ns_lcm_create_instance(self, _payload):
        response = self.do_post(self.NSLCM_URL, _payload)
        return response

    def ns_lcm_instantiate_ns(ns_instance_id, _body={}):
        pass
