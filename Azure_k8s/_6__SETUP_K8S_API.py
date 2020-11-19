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
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

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
        three = MSAConnect(context['msa_fqdn'],
                           context['msa_user'],
                           context['msa_pass'])
        if isinstance(three.token, tuple):
            ret = MSA_API.process_content('WARNING',
                                          f'Can\'t get MSA token {three.token[1]}',
                                          context, True)
            print(ret)
            exit()
    except HTTPError as http_err:
        ret = MSA_API.process_content('WARNING',
                                      f'HTTP error occured: {http_err}',
                                      context, True)
        print(ret)
        exit()      

    k8s_create_service_account_2 = {'k8s_create_service_account': {'0':{'object_id': 'token'}}}
    try:
        order = Order(str(context['master_id']))
        order.command_synchronize(timeout=60)
        time.sleep(2)
        order.command_execute('IMPORT', k8s_create_service_account_2)
        data_5 = json.loads(order.content)
        data_5 = json.loads(data_5['message'])
    except Exception as e:
        ret = MSA_API.process_content('FAILED',
                                      f'ERROR: {str(e)}',
                                      context, True)
        print(ret)

    if 'token' in data_5['k8s_create_service_account'].keys():
        k8s_token = data_5['k8s_create_service_account']['token']['token']
    else:
        ret = MSA_API.process_content('WARNING',
                                      f'Token not found: {k8s_token}',
                                      context, True)
        print(ret)
        exit()

    me_id = context['proxy_host'][3:]
    # same ip address as haproxy ip address
    try:
        k8s_api_ip = Device(device_id=me_id).management_address
        cust_id = context["UBIQUBEID"][4:]

        entity = Device(customer_id=cust_id,
                        name="k8s-api",
                        manufacturer_id="20060101",
                        model_id="20060101",
                        login="admin",
                        password="admin",
                        password_admin="admin",
                        management_address=k8s_api_ip)

        entity.create()
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t call device {me_id} : {str(e)}',
                                      context, True)
        print(ret)
        exit()
        
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'K8S API ME CREATED...')
    
    time.sleep(2)
    # set k8s specific parameters
    try:
        three.set_params(str(entity.device_id), 'KUBE_TOKEN', k8s_token)
        three.set_params(str(entity.device_id), 'KUBE_AUTH_METHOD', 'KUBERNETES')
        three.set_params(str(entity.device_id), 'KUBE_HTTP_PROTOCOL', 'https')
        three.set_params(str(entity.device_id), 'KUBE_PORT', '6443')
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t set custom params {me_id} : {str(e)}',
                                      context, True)
        print(ret)
        exit()
    
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'K8S PARAMETERS SET...')
    # assign deployment setting
    try:
        entity.profile_switch(context['dpl_k8s'], context['dpl_k8s'])
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t assign dpl {me_id} : {str(e)}',
                                      context, True)
        print(ret)
        exit()

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'K8S PROFILE UPDATED')
    time.sleep(2)
    try:
        entity.activate()
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t activate {me_id} : {str(e)}',
                                      context, True)
        print(ret)
        exit()

    ret = MSA_API.process_content('ENDED', f'K8S API REGISTERED {str(entity.device_id)}', context, True)
    print(ret)