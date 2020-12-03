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

# stub find prim master id -'k8s-node-1'
cust_ref = context["UBIQUBEID"]
search = Lookup()
search.look_list_device_by_customer_ref(cust_ref)
device_list = search.content
device_list = json.loads(device_list)

worker_id_list = []
master = context['vm_name'] + '-1'
backup = context['vm_name'] + '-2'

# add all vms that are not k8s masters to the list 
for me in device_list:
    if me['name'] != (master and backup):
         worker_id_list.append(me['id'])

# (4) kubeadm loop on workers
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
        

ret = MSA_API.process_content('ENDED', 'K8S cluster ready - Enjoy!', context, True)
print(ret)