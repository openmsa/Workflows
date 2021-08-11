import os
import json
import requests
import base64
import hashlib
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
 
    def do_patch(self, _url, _payload):
        _url     = self.base_url + _url
        _payload = json.dumps(_payload)
        response = requests.request("PATCH", url=_url, headers=self.headers,
                                    data=_payload, verify=False)
        return response

    # def do_put(self, _url, _filename):
    #     _url      = self.base_url + _url
    #     _username = self.username
    #     _password = self.password
    #
    #     dir_path = os.path.dirname(os.path.realpath(__file__))
    #     stream = os.popen(f'{dir_path}/onboard_vnf.sh {_username} {_password} {_url} {_filename}')
    #     plain_text = stream.read().strip("\n")
    #     return plain_text

    def do_put(self, _url, _filename):
        _url               = self.base_url + _url
        _headers           = self.headers
        del _headers['Content-Type']
        _headers['Accept'] = 'application/json'
        _name              = _filename.split('/')[-1] 
        _files             = {'file': ('_name', open(_filename, 'rb'))}
        response = requests.request("PUT", url=_url, headers=_headers,
                                    files=_files, verify=False)
        return response
    
    def do_put_mp(self, _url, _content):
        _boundary                = "----------" + hashlib.md5(str(time.time())).hexdigest()
        _headers                 = self.headers
        _headers['Content-Type'] = "multipart/form-data; boundary=" + _boundary
        _fields  = {'file': _content}
        _payload = self.multipart_build_query(_fields,_boundary)
        response = requests.request("PUT", url=_url, headers=_headers,
                                    data=_payload, verify=False)
        return response
        
    
    def multipart_build_query(self, _fields, _boundary):
        _retval = ''
        for k,v in _fields.items():
            _retval += f"--{_boundary}\r\nContent-Disposition: form-data; name=\"{key}\"; filename=\"filename\"\r\n\r\n{value}:\r\n"
            _retval += f"--{_boundary}--\r\n"
        return _retval
    
    def do_delete(self, _url):
        _url     = self.base_url + _url
        response = requests.request("DELETE", url=_url, headers=self.headers,
                                    data={}, verify=False)
        return response

    def set_parameters(self, username, password, data={}):
        self.username  = username
        self.password  = password        
        userpass       = f"{username}:{password}"
        base64userpass = base64.b64encode(userpass.encode()).decode()
        self.headers   = {'Content-Type': 'application/json',
                          'Authorization': f'Basic {base64userpass}'
                          }
    
    def check_error(response):
        _status = int(response.status)
        if (_status < 200) or (_status > 299):
            if _status == 0:
                print(f'Error: {response}, {response.content}')
            else:
                print(f'MANO Error: {response}, {response.content}')
