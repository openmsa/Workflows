import requests
import json
import re
import socket
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

dev_var = Variables()
dev_var.add('k8s_base_url', var_type='String')
dev_var.add('k8s_api_token', var_type='Password')
dev_var.add('msa_fqdn', var_type='String')
dev_var.add('msa_user', var_type='String')
dev_var.add('msa_pass', var_type='Password')
context = Variables.task_call(dev_var)

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

try:
    proto = re.findall('(\w+)://', context['k8s_base_url'])
    host = re.findall('://(\S+):', context['k8s_base_url'])
    port = re.findall(':(\d+)', context['k8s_base_url'])
    if proto and not port:
        if proto[0] == 'http':
            port = '80'
        elif proto[0] == 'https':
            port = '443'
        context['k8s_proto'] = proto[0]
        context['k8s_port'] = port
    if proto:
        proto = proto[0]
        context['k8s_proto'] = proto
    if port:
        port = port[0]
        context['k8s_port'] = port
    if host:
        k8s_ip = socket.gethostbyname(host[0])
        context['k8s_ip'] = k8s_ip
        context['k8s_host'] = host[0]
except Exception as e:
    ret = MSA_API.process_content('WARNING',
                                  f'CHECK BASE URL: {str(e)}',
                                  context, True)

def check_status(base_url, token):

    url = base_url.strip('/') + "/api/v1"

    payload = {}

    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
              }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    return response.status_code

if __name__ == "__main__":

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'K8S PARAMETERS SET...')

    try:
        status = check_status(context['k8s_base_url'], context['k8s_api_token'])
        if status == 200:
            context['k8s_status'] = status
            ret = MSA_API.process_content('ENDED',
                                          f'CONNECTION ESTABLISHED {context["k8s_ip"]}:{context["k8s_port"]}',
                                          context, True)
        else:
            context['k8s_status'] = status
            ret = MSA_API.process_content('WARNING', f'HTTP STATUS CODE: {status}. CHECK CONNECTION.',
                                          context, True)

    except Exception as e:
        context['k8s_status'] = 522
        ret = MSA_API.process_content('WARNING',
                                      f'WARNING: {str(e)}',
                                      context, True)
        print(ret)
        
    print(ret)

