import json
import requests
import base64
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi
from custom.ETSI.ManoProtocolsVersion import ManoProtocolsVersion


class VnfPkgSol005(BaseApi):

    NFV_API_PROTOCOL = "sol005"
    NFV_RESOURCE_FRAGMENT = "vnfpkgm"
    VNF_PKG_URL = NFV_API_PROTOCOL + "/" + NFV_RESOURCE_FRAGMENT + "/v1/vnf_packages"


    def __init__(self, hostname, port, sol_version):
       super().__init__(hostname, port, sol_version)
       
       _mano_proto_version_obj = ManoProtocolsVersion()
       data = _mano_proto_version_obj.get_fragment_versions(self.NFV_API_PROTOCOL, self.sol_version, self.NFV_RESOURCE_FRAGMENT)
       if 'fragment_version' in data:
           self.fragment_version = data.get('fragment_version')
           
       if 'header_version' in data:
           self.header_version = data.get('header_version')

       #update request header object by adding the header_version.
       self.headers.update(version=self.header_version)

       self.VNF_PKG_URL = self.NFV_API_PROTOCOL + "/" + self.NFV_RESOURCE_FRAGMENT + "/v" + self.fragment_version + "/vnf_packages"

    def vnf_packages_get_package(self, _vnfpkgid):
        _url     = self.VNF_PKG_URL + "/" + _vnfpkgid
        response = self.do_get(_url)
        return response
    
    def vnf_packages_post(self, _payload):
        response = self.do_post(self.VNF_PKG_URL, _payload)
        return response
    
    def vnf_packages_vnf_pkgid_patch(self, _vnfpkgid, _payload):
        _url     = self.VNF_PKG_URL + "/" + _vnfpkgid
        response = self.do_patch(_url, _payload) 
        return response
    
    def vnf_packages_vnfpkgid_delete(self, _vnfpkgid):
        _url     = self.VNF_PKG_URL + "/" + _vnfpkgid 
        response = self.do_delete(_url)
        return response
    
    def vnf_packages_vnfpkgid_package_content_put(_vnfpkgid, _content):
        pass
    
    def vnf_packages_vnfpkgid_package_file_put(self, _vnfpkgid, _filename):
        _url     = self.VNF_PKG_URL + "/" + _vnfpkgid + "/package_content"
        response = self.do_put(_url, _filename)
        return response
    
    def set_operational_state(self, _vnfpkgid, _state):
        _content = {"operationalState": "DISABLED"}
        if _state == True:
            _content = {"operationalState": "ENABLED"}
        return self.vnf_packages_vnf_pkgid_patch(_vnfpkgid, _content)
    
    def expose_document(_document_type, _id):
        pass

