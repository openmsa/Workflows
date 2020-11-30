import time
import json
import datetime
from msa_sdk.variables import Variables
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

device_id = context['k8s_api'][3:]

k8_pods_list = {'k8_pods_list': {'':{'object_id': ''}}}

try:
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'Sync in progress...')
    order = Order(str(device_id))
    order.command_synchronize(timeout=60)
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'Syncronized.')
    time.sleep(2)
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'Check in progress...')
    order.command_execute('IMPORT', k8_pods_list)
    data = json.loads(order.content)
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)
    
if 'message' in data.keys():
    container_list = json.loads(data['message'])['k8_pods_list'].keys()
else:
    container_list = []

if 'nginx' in container_list:
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'Undefined resource found: nginx')
    context['wf_name'] = 'WARNING'
    ret = MSA_API.process_content('WARNING',
                                  f'Undefined resource found - POD: nginx',
                                  context, True)
    print(ret)
else:
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'Test passed.')
    ret = MSA_API.process_content('ENDED',
                                  f'Test passed. No suspicious PODs found.',
                                  context, True)
    print(ret)
