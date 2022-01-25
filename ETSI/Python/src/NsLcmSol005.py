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

    def ns_lcm_instantiate_ns(self, ns_instance_id, _payload={}):
        _url = self.NSLCM_URL + "/" + ns_instance_id + "/instantiate"
        response = self.do_post_return_location(_url, _payload)
        return response

    def ns_lcm_scale_ns(self, ns_instance_id, _payload={}):
        _url = self.NSLCM_URL + "/" + ns_instance_id + "/scale"
        response = self.do_post_return_location(_url, _payload)
        return response

    def ns_lcm_terminate_ns(self, ns_instance_id, _payload={}):
        _url = self.NSLCM_URL + "/" + ns_instance_id + "/terminate"
        response = self.do_post_return_location(_url, _payload)
        return response

    def ns_lcm_delete_instance_of_ns(self, ns_instance_id):
        _url = self.NSLCM_URL + "/" + ns_instance_id
        response = self.do_delete(_url)
        return response

    def ns_lcm_get_ns_instance_details(self, ns_instance_id):
        _url = self.NSLCM_URL + "/" + ns_instance_id
        response = self.do_get(_url)
        return response

