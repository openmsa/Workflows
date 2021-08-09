import json
import requests
import base64
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BaseApi():

    def __init__(self, hostname, port='80'):
        self.hostname = hostname
        self.port     = port
        self.base_url = "http://" + hostname + ":" + port + "/ubi-etsi-mano/"
    
    def do_get(self, _url):
        _url     = self.base_url + _url
        response = requests.request("GET", url=_url, headers=self.headers,
                                    data=self.payload, verify=False)
        return response
    
    def do_post(self, _url, _payload):
        _url     = self.base_url + _url
        _payload = json.dumps(_payload)
        response = requests.request("POST", url=_url, headers=self.headers,
                                    data=_payload, verify=False)
        return response
    
    def do_post_return_location():
        pass
    
    def do_patch():
        pass

    def do_put():
        pass
    
    def do_put_mp():
        pass
    
    def multipart_build_query():
        pass
    
    def do_delete(self, _url):
        _url     = self.base_url + _url
        response = requests.request("DELETE", url=_url, headers=self.headers,
                                    data={}, verify=False)
        return response

    def set_parameters(self, username, password, data={}):        
        userpass       = f"{username}:{password}"
        base64userpass = base64.b64encode(userpass.encode()).decode()
        self.headers   = {'Content-Type': 'application/json',
                          'Authorization': f'Basic {base64userpass}'
                          }
    
    def check_error():
        pass

