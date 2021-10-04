import time
import json
from msa_sdk.lookup import Lookup
from msa_sdk.device import Device
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

# (1) prepare data for k8s_pre_requirements microservice
k8s_pre_requirements_data = {"object_id": "123"}
k8s_pre_requirements_ms = {"k8s_pre_requirements": {"123": k8s_pre_requirements_data}}

# prepare device list, by id
cust_ref = context["UBIQUBEID"]
search = Lookup()
search.look_list_device_by_customer_ref(cust_ref)
device_list = search.content
device_list = json.loads(device_list)

# deploy required packages
for me in device_list:
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'k8s software installation: \
                                                   {Device(device_id=me["id"]).name}')
    try:
        order = Order(me['id'])
        order.command_execute('CREATE', k8s_pre_requirements_ms, timeout=300)
    except Exception as e:
        ret = MSA_API.process_content('FAILED',
                                      f'ERROR: {str(e)}',
                                      context, True)
        print(ret)

ret = MSA_API.process_content('ENDED', f'K8S software installed.', context, True)
print(ret)