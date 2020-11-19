import json
import time
import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from msa_sdk.variables import Variables
from msa_sdk.orchestration import Orchestration
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
# dev_var.add('vm_username', var_type='String')
# dev_var.add('vm_secret', var_type='Password')
context = Variables.task_call(dev_var)

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

        try:
            response = requests.request("POST", url, headers=headers,
                                        data=json.dumps(payload), verify=False)
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')

        return response.json()['token']

    def get_device_asset(self, device_id):

        url = self.base_url + \
              "/assetManagement/v1/device-asset/device/id/" + \
              device_id

        payload = {}

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.token
                   }

        try:
            response = requests.request("GET", url, headers=headers,
                                        data=payload, verify=False)
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')

        return response.json()
      
if __name__ == "__main__":

    # Next block creates ME
    # manufacturer/model = 14020601 > Linux/Generic
    
    cust_id = context["UBIQUBEID"][4:]
    
    vm_id_list = []
    for vm in context['vms']:
        entity = Device(customer_id=cust_id,
                        name=list(vm.keys())[0],
                        manufacturer_id="14020601",
                        model_id="19112020",
                        login=context['vm_username'],
                        password=context['vm_secret'],
                        password_admin=context['vm_secret'],
                        management_address=list(vm.values())[0]['external'])

        entity.create()
        time.sleep(2)
        vm_id_list.append(str(entity.device_id))
        # assign deployment setting
        entity.profile_switch(context['dpl_linux'], context['dpl_linux'])
        time.sleep(2)
        entity.activate()

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'MEs created - Activating...')
    
    # check if ME is ready to be configured by veryfing asset
    counter = 0
    
    try:
        two = MSAConnect(context['msa_fqdn'],
                         context['msa_user'],
                         context['msa_pass'])
        while len(vm_id_list) > 0:
            for me in vm_id_list:
                if len(two.get_device_asset(me)['serialNb']) > 1:
                    vm_id_list.remove(me)
                    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                                   f'ME id:{Device(device_id=me).name} = Ready')
            time.sleep(3)
            counter = counter + 3
            if counter == 300:
                break
    except HTTPError as http_err:
        ret = MSA_API.process_content('WARNING', f'MSA HTTP error: {http_err}', context, True)
        print(ret)
        exit()
        
    ret = MSA_API.process_content('ENDED', f'Next Managed Entities created: {context["vms"]}', context, True)
    print(ret)
