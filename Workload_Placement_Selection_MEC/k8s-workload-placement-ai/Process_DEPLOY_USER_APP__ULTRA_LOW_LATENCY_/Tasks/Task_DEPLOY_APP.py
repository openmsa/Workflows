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
########################################################################################################
#                                         MATH ALGORITHM                                               #
########################################################################################################

    info_message('Processing metrics...')
    cost_summary = {}

    for device in device_id_list:
        d_name = Device(device_id=device).name
        info_message(f'Processing metrics from: {d_name}...')
        cost_summary[device] = float()
        order = Order(device)
        order.command_objects_instances('logs')

        for ms_item in json.loads(order.content):
            if check_pod_name(ms_item):
                order.command_objects_instances_by_id('logs', ms_item)
                cost = json.loads(order.content)['logs'][ms_item]['min']
                cost_summary[device] += float(cost)        


    target_device_id = min(cost_summary, key=cost_summary.get)
    target_device_name = Device(device_id=target_device_id).name

    info_message(f'Best offer from: {target_device_name}.', 5)

    context['target_device_id'] = target_device_id
    context['target_device_name'] = target_device_name

########################################################################################################
#                                        DEPLOY USER APP                                               #
########################################################################################################

    info_message(f'Deploying {context["app_name"]} on {target_device_name}')

    oid = rand_int()

    ms_vars_dict = {"object_id": oid,
                    "namespace": context['user_namespace'],
                    "app_name": context['app_name'],
                    "label": context['label']
                    }

    Order(target_device_id).command_execute('CREATE', {'k8_pods_list_label': {oid: ms_vars_dict}})


    ret = MSA_API.process_content('ENDED',
                                  f'App {context["app_name"]} \
                                  Deployed on {context["target_device_name"]}', context, True)
    print(ret)