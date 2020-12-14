import json
import time
import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from msa_sdk.variables import Variables
from msa_sdk.device import Device
from msa_sdk.order import Order
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

class MSAConnect():

    def __init__(self, hostname, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://" + hostname + "/ubi-api-rest"
        self.token = self.get_token()

    def get_token(self):

        url = self.base_url + "/auth/token"

        payload = {"username": self.username,
                   "password": self.password
                   }

        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", url, headers=headers,
                                    data=json.dumps(payload), verify=False)

        if 'token' in response.json():
            return response.json()['token']
        else:
            # return (response, response.json())
            return (response, payload)

    def get_device_asset(self, device_id):

        url = self.base_url + \
              "/assetManagement/v1/device-asset/device/id/" + \
              device_id

        payload = {}

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.token
                   }

        response = requests.request("GET", url, headers=headers,
                                    data=payload, verify=False)

        return response.json()
      
    def set_params(self, device_id, key, value):

        url = self.base_url + \
              "/variables/" + \
              device_id + \
              "/" + key + \
              "?value=" + value + \
              "&type=&comment=NA"

        payload = {}

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.token
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=payload, verify=False)

        return response
      
if __name__ == "__main__":
  
    try:
        one = MSAConnect(context['msa_fqdn'],
                         context['msa_user'],
                         context['msa_pass'])
        if isinstance(one.token, tuple):
            ret = MSA_API.process_content('WARNING',
                                          f'Can\'t get MSA token {one.token[1]}',
                                          context, True)
            print(ret)
            exit()
    except HTTPError as http_err:
        ret = MSA_API.process_content('WARNING',
                                      f'HTTP error occured: {http_err}',
                                      context, True)
        print(ret)
        exit()      

    entity = Device(device_id=context['k8s_device'][3:])

    try:
        one.set_params(str(entity.device_id), 'KUBE_TOKEN', context["k8s_token"])
        one.set_params(str(entity.device_id), 'KUBE_AUTH_METHOD', 'KUBERNETES')
        one.set_params(str(entity.device_id), 'KUBE_HTTP_PROTOCOL', 'https')
        one.set_params(str(entity.device_id), 'KUBE_PORT', context["k8s_port"])
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t set custom params {context["k8s_device"]} : {str(e)}',
                                      context, True)
        print(ret)
        exit()

    ret = MSA_API.process_content('ENDED', f'K8S VARIABLES UPDATED {str(entity.device_id)}', context, True)
    print(ret)