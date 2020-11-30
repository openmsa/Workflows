import time
import json
from msa_sdk.variables import Variables
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from msa_sdk.lookup import Lookup
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if int(context["scale_lvl"]) <= 0:
    ret = MSA_API.process_content('ENDED', f'Scale-in completed. Skipping.',
                                  context, True)
    print(ret)
    exit()

# worker list hardcoded
worker_id_list = context['vm_id_list_new']
# kubeadm loop on workers
Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Worker nodes processing...')
for me in worker_id_list:
    try:
        order = Order(str(me))
        order.command_execute('CREATE', context['k8s_join_worker'], timeout=300)
    except Exception as e:
        ret = MSA_API.process_content('FAILED',
                                      f'ERROR: {str(e)}',
                                      context, True)
        print(ret)
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'Worker Initiated: {me}')
        

ret = MSA_API.process_content('ENDED', 'K8S cluster updated.', context, True)
print(ret)