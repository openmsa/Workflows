import json
import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi


class VnfLcmSol003(BaseApi):

    #NSLCM_BASE_URL = 'sol003/vnflcm/v1/vnf_instances'
    NSLCM_BASE_URL = 'vnflcm/v1/vnf_instances'

    def vnf_lcm_create_instance(self, _payload):
        response = self.do_post(self.NSLCM_BASE_URL, _payload)
        return response

    def vnf_lcm_instantiate_vnf(self, vnf_instance_id, _payload={}):
        _url = self.NSLCM_BASE_URL + "/" + vnf_instance_id + "/instantiate"
        response = self.do_post_return_location(_url, _payload)
        return response

    def vnf_lcm_terminate_vnf(self, vnf_instance_id, _payload={}):
        _url = self.NSLCM_BASE_URL + "/" + vnf_instance_id + "/terminate"
        response = self.do_post_return_location(_url, _payload)
        return response

    def vnf_lcm_delete_instance_of_vnf(self, vnf_instance_id):
        _url = self.NSLCM_BASE_URL + "/" + vnf_instance_id
        response = self.do_delete(_url)
        return response

    def vnf_lcm_scale_to_level_instance_vnf(self, vnf_instance_id, _payload):
        _url = self.NSLCM_BASE_URL + "/" + vnf_instance_id + "/scale_to_level"
        response = self.do_post_return_location(_url, _payload)
        return response

    def vnf_lcm_scale_instance_vnf(self, vnf_instance_id, _payload):
        _url = self.NSLCM_BASE_URL + "/" + vnf_instance_id + "/scale"
        response = self.do_post_return_location(_url, _payload)
        return response

    def vnf_lcm_operate_instance_vnf(self, vnf_instance_id, _payload):
        _url = self.NSLCM_BASE_URL + "/" + vnf_instance_id + "/operate"
        response = self.do_post_return_location(_url, _payload)
        return response
    def vnf_lcm_get_vnf_instance_details(self, vnf_instance_id):
        _url = self.NSLCM_BASE_URL + "/" + vnf_instance_id
        response = self.do_get(_url)
        return response
