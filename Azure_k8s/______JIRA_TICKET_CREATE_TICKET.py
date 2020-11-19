import json
import requests
import base64
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

class JiraConnection():

    def __init__(self, jira_fqdn, username, password, project_id):
        self.base64value = base64.b64encode(f'{username}:{password}'.
                                            encode('utf-8')
                                            ).decode("ascii")
        self.base_url = 'http://' + jira_fqdn + '/rest/api/2/issue'
        self.project_id = project_id

    def open_ticket(self, message):

        url = self.base_url

        payload = {
                    "fields": {
                        "project": {
                            "id": self.project_id
                        },
                        "summary": "KUBERNETES CLUSTER",
                        "priority": {
                            "id": "1"
                        },
                        "issuetype": {
                            "id": 10003
                        },
                        "description": message
                    }
                }

        headers = {
                   'Accept': 'application/json',
                   'Authorization': 'Basic ' + self.base64value,
                   'Content-Type': 'application/json'
                   }

        response = requests.request("POST", url, headers=headers,
                                    data=json.dumps(payload))

        if 'key' in response.json():
            return response.json()['key']
        else:
            return response.json()
          
          
if __name__ == "__main__":
  
    try:
        four = JiraConnection(context['jira_fqdn'],
                              context['jira_user'],
                              context['jira_pass'],
                              context['jira_project_id'])
        ticket_id = four.open_ticket(f'Check WF Instancem, \
                                     PROCESS ID: {context["PROCESSINSTANCEID"]}')
    except ConnectionError:
        ret = MSA_API.process_content('WARNING',
                                      f'Connection Error - Check Internet',
                                      context, True)
        print(ret)
        exit()
    except HTTPError:
        ret = MSA_API.process_content('WARNING',
                                      f'HTTP Error - Check API',
                                      context, True)
        print(ret)
        exit()

    ret = MSA_API.process_content('ENDED', f'{ticket_id} created.', context, True)
    print(ret)