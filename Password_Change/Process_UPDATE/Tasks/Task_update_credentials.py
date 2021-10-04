import json
import time
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

    def get_manager_id(self, manager):

        url = self.base_url + \
              "/user/login/" + \
              manager

        payload = {}

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.token
                   }

        response = requests.request("GET", url, headers=headers,
                                    data=payload, verify=False)

        return response.json()['id']

    def update_manager_with_password(self, manager_id, password):

        url = self.base_url + \
              "/user/manager_password/" + \
              manager_id + "/" + \
              "?password=" + \
              password

        payload = {}

        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + self.token
                   }

        response = requests.request("PUT", url, headers=headers,
                                    data=payload, verify=False)

        return response


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('msa_fqdn', var_type='String')
    dev_var.add('msa_user', var_type='String')
    dev_var.add('msa_pass', var_type='Password')
    dev_var.add('target_username', var_type='String')
    dev_var.add('target_password', var_type='Password')
    context = Variables.task_call(dev_var)

    # (1) GET MSActivator TOKEN
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

    # (2) Get user(manager) ID
    try:
        manager_id = msa_call.get_manager_id(context["target_username"])
        context['manager_id'] = str(manager_id)
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t get user id : check {str(e)}',
                                      context, True)
        print(ret)
        exit()

    # (3) Update manager with password
    try:
        status = msa_call.update_manager_with_password(context["manager_id"],
                                                       context["target_password"])
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t update password : check {str(e)}',
                                      context, True)
        print(ret)
        exit()

    ret = MSA_API.process_content('ENDED',
                                  f'Credentials updated for {context["target_username"]}, status: {status}',
                                  context, True)
    print(ret)

