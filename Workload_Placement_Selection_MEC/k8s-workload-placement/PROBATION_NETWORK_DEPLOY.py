import random
import time
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
ms_vars_dict_list = context["ms_vars_dict_list"]

# throw message
def info_message(text, timeout=1):
    Orchestration.update_asynchronous_task_details(*async_update_list, text)
    time.sleep(timeout)

def rand_int():
    return ''.join(random.choice('0123456789') for i in range(8))

  
if __name__ == "__main__":

    info_message('Deploying service PODs...')
    for device in device_id_list:
        d_name = Device(device_id=device).name
        info_message(f'Deploying service PODs on: {d_name}...')
        for ms_var_dict in ms_vars_dict_list:
            Order(device).command_execute('CREATE', {'icmp_probes': {rand_int(): ms_var_dict}})
            info_message(f'Deploying service PODs on: {d_name} done.')
    
    # wait while ping is being executed
    counter = 3*int(context['pkt_count'])
    for i in range(counter):
        info_message(f'Packets counter: {counter-i}')

    ret = MSA_API.process_content('ENDED', f'Probation network deployed.', context, True)
    print(ret)