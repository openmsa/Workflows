import re
import json
import random
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration

context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

device_id_list = context["device_id_list"]

# throw message
def info_message(text, timeout=1):
    Orchestration.update_asynchronous_task_details(*async_update_list, text)
    time.sleep(timeout)

def rand_int():
    return ''.join(random.choice('0123456789') for i in range(8))
  
def check_pod_name(text):
    # ip address like pattern for container name
    # ex. 10_10_10_10, 192_168_0_100
    return bool(re.search('(\d{1,3}_){3}\d{1,3}', text))


if __name__ == "__main__":
       
    target_device_id = context['target_device_id']
    target_device_name = context['target_device_name']

    info_message(f'Creating service type NodePort {target_device_name}: tcp/{context["node_port"]}')

    oid = rand_int()

    ms_vars_dict = {"namespace": context['user_namespace'],
                    "app_name": context['app_name'],
                    "port": context['port'],
                    "target_port": context['target_port'],
                    "node_port": context['node_port'],
                    "label": context['label']
                    }

    Order(target_device_id).command_execute('CREATE',
                                            {'k8_services_list_nodeport_label': {oid: ms_vars_dict}})


    ret = MSA_API.process_content('ENDED',
                                  f'Service NodePort created \
                                  {target_device_name}: tcp/{context["node_port"]}', context, True)
    print(ret)