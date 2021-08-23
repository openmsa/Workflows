import json
import requests
import base64
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi


class NsdSol005(BaseApi):

    NSD_URL = "sol005/nsd/v1/ns_descriptors"

    def nsd_descriptors_post(self, _payload):
        response = self.do_post(self.NSD_URL, _payload)
        return response

    def nsd_descriptors_get(self, _nsdinfoid):
        _url     = self.NSD_URL + "/" + _nsdinfoid
        response = self.do_get(_url)
        return response

    def ns_descriptors_nsd_info_id_delete(self, _nsdinfoid):
        _url     = self.NSD_URL + "/" + _nsdinfoid
        response = self.do_delete(_url)
        return response

    # def ns_descriptors_nsdinfoid_nsd_content_put(self, _nsdinfoid, _content):
    #     _url     = self.NSD_URL + "/" + _nsdInfoId + "/nsd_content"
    #     response = self.do_put_mp(_url, _content)
    #     return response

    def ns_descriptors_nsdinfoid_nsd_file_put(self, _nsdinfoid, _filename):
        _url     = self.NSD_URL + "/" + _nsdinfoid + "/nsd_content"
        response = self.do_put(_url, _filename)
        return response

    def set_operational_state(self, _nsdinfoid, _state):
        _content = {"nsdOperationalState": "DISABLED"}
        if _state == True:
            _content = {"nsdOperationalState": "ENABLED"}
        return self.ns_descriptors_nsdinfoid_patch(_nsdinfoid, _content)

    def ns_descriptors_nsdinfoid_patch(self, _nsdinfoid, _payload):
        _url     = self.NSD_URL + "/" + _nsdinfoid
        response = self.do_patch(_url, _payload)
        return response
