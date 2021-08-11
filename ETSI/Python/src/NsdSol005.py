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

    def ns_descriptors_nsd_info_id_delete(self, _nsdinfoid):
        _url     = self.NSD_URL + "/" + _nsdinfoid
        response = self.do_delete(_url)
        return response
