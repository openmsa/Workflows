import json
import requests
import base64
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi


class VnfPkgSol005(BaseApi):

    VNF_PKG_URL = "sol005/vnfpkgm/v1/vnf_packages"
    
    def vnf_packages_post(self, _payload):
        response = self.do_post(self.VNF_PKG_URL, _payload)
        return response
    
    def vnf_packages_vnf_pkgid_patch(_vnfpkgid, _payload):
        pass
    
    def vnf_packages_vnfpkgid_delete(self, _vnfpkgid):
        _url     = self.VNF_PKG_URL + "/" + _vnfpkgid 
        response = self.do_delete(_url)
        return response
    
    def vnf_packages_vnfpkgid_package_content_put(_vnfpkgid, _content):
        pass
    
    def vnf_packages_vnfpkgid_package_file_put(_vnfpkgid, _filename):
        pass
    
    def set_operational_state(_vnfpkgid, _state):
        pass
    
    def expose_document(_document_type, _id):
        pass

