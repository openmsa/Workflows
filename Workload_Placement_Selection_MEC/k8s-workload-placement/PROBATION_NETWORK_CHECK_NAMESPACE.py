import random
import time
import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration

context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

device_id_list = context["device_id_list"]
service_ns_ms_data = {"namespace": context['service_namespace']}
user_ns_ms_data = {"namespace": context['user_namespace']}

# throw message
def info_message(text, timeout=1):
    Orchestration.update_asynchronous_task_details(*async_update_list, text)
    time.sleep(timeout)
    
def rand_int():
    return ''.join(random.choice('0123456789') for i in range(8))

if __name__ == "__main__":

    # create service and user namesapces if not exist
    info_message('Ckecking if the namespaces exist...')

    for device in device_id_list:
        d_name = Device(device_id=device).name
        info_message(f'Ckecking if the namespaces exist: {d_name}...')
        order = Order(device)
        namespaces = {'Namespaces': {'':{ }}}
        order.command_execute('IMPORT', namespaces)
        order.command_objects_instances('Namespaces')
        ns_list = json.loads(order.content)
        if context['service_namespace'] not in ns_list:
            info_message(f'Creating {context["service_namespace"]} on {d_name}...')
            order.command_execute('CREATE', {'Namespaces': {rand_int(): service_ns_ms_data}})
        if context['user_namespace'] not in ns_list:
            info_message(f'Creating {context["user_namespace"]} on {d_name}...')
            order.command_execute('CREATE', {'Namespaces': {rand_int(): user_ns_ms_data}})

    ret = MSA_API.process_content('ENDED', f'Namespaces prepared.', context, True)
    print(ret)