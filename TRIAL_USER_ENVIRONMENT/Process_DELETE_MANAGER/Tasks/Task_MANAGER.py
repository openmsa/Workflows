import json
import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


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
                   'Authorization': 'Bearer ' + self.token
                  }

        response = requests.request("POST", url, headers=headers,
                                    data=payload, verify=False)

        return response

    def create_user(self, email, username, password, operator):

        url = self.base_url + "/user/v1/manager/"

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.token,
                   'Content-Type': 'application/json'
                   }

        payload = {
                   "baseRole": {
                                "id": 3
                                },
                   "login": username,
                   "name": email,
                   "operatorPrefix": operator,
                   "pwd": password
                   }

        response = requests.request("POST", url, headers=headers,
                                    data=json.dumps(payload), verify=False)

        return response
      
    def delete_user(self, user_id):

        url = self.base_url + \
              "/user/id/" + \
              user_id

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.token,
                   }

        payload = {}

        response = requests.request("DELETE", url, headers=headers,
                                    data=payload, verify=False)

        return response


# This Process uses API not SDK
if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call()

    # (1) Get MSA Token
    try:
        call_msa = MSAConnect(context['msa_fqdn'],
                              context['msa_user'],
                              context['msa_pass'])
        if isinstance(call_msa.token, tuple):
            ret = MSA_API.process_content('WARNING',
                                          f'CAN\'T GET MSA TOKEN {call_msa.token[1]}',
                                          context, True)
            print(ret)
            exit()
    except HTTPError as http_err:
        ret = MSA_API.process_content('WARNING',
                                      f'HTTP ERROR OCCURRED: {http_err}',
                                      context, True)
        print(ret)
        exit()          

    # (2) Delete Manager
    try:
        call_msa.delete_user(str(context['user_id']))
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'CAN\'T DELETE MANAGER, SEE: {str(e)}',
                                      context, True)
        print(ret)
        exit()       

    ret = MSA_API.process_content('ENDED',
                                  f'MANAGER DELETED. \
                                  NAME: {context["email"]} \
                                  ID: {context["user_id"]}',
                                  context, True)
    print(ret)