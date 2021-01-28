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

    def create_dpl_set(self, customer_id, device_id, name):

        url = self.base_url + \
              "/conf-profile/v2/" + \
              customer_id

        payload = {
                      "id": 0,
                      "name": str(name),
                      "externalReference": "",
                      "comment": "",
                      "model": {
                          "id": 20060101,
                          "name": "Generic"
                      },
                      "vendor": {
                          "id": 20060101,
                          "name": "KUBERNETES"
                      },
                      "microserviceUris": [
                          "CommandDefinition/KUBERNETES/Generic/Nodes.xml",
                          "CommandDefinition/KUBERNETES/Generic/k8_pods_list.xml",
                          "CommandDefinition/KUBERNETES/Generic/k8_services_list.xml"
                      ],
                      "templateUris": [],
                      "attachedManagedEntities": [
                          int(device_id)
                      ]
                  }

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.token,
                   'Content-Type': 'application/json'
                  }

        response = requests.request("POST", url, headers=headers,
                                    data=json.dumps(payload),
                                    verify=False)

        return response


if __name__ == "__main__":

    if context['k8s_status'] != 200:
        ret = MSA_API.process_content('WARNING',
                                      f'CHECK CONNECTION. STATUS CODE: {context["k8s_status"]}',
                                      context, True)
        print(ret)
        exit()

    # (1) Create TOKEN
    try:
        msa_call = MSAConnect(context['msa_fqdn'],
                              context['msa_user'],
                              context['msa_pass'])
        if isinstance(msa_call.token, tuple):
            ret = MSA_API.process_content('WARNING',
                                          f'Can\'t get MSA token {msa_call.token[1]}',
                                          context, True)
            print(ret)
            exit()
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'HTTP error occured: {e}',
                                      context, True)
        print(ret)
        exit()

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'MSActivator token...')
    time.sleep(2)

    # (2) CREATE DPL
    try:
        r = msa_call.create_dpl_set(context['UBIQUBEID'][4:],
                                    context['entity_id'],
                                    "k8s_dpl_set")
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t create dpl_set for {context["entity_id"]} : check {str(e)}',
                                      context, True)
        print(ret)
        exit()

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'K8S DEPLOYMENT SET CREATED...')
    time.sleep(2)

    # (3) Syncronize
    order = Order(context['entity_id'])
    order.command_synchronize(timeout=60)
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'Entity Syncronized...')
    time.sleep(2)

    ret = MSA_API.process_content('ENDED', f'Please check K8S cluster now connected {r.text}', context, True)
    print(ret)

