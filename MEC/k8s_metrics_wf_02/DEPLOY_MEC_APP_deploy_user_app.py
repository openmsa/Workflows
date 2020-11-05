import json
import random
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order

context = Variables.task_call()

device_id_list = context["device_id_list"]

def rand_int():
    return ''.join(random.choice('0123456789') for i in range(8))

cost_summary = {}

########################################################################################################
#                                         MATH ALGORITHM                                               #
########################################################################################################

for device in device_id_list.values():
    cost_summary[device] = float()
    order = Order(device)
    order.command_objects_instances('k8s_log')

    for ms_item in json.loads(order.content.decode()):
        order.command_objects_instances_by_id('k8s_log', ms_item)
        cost = json.loads(order.content.decode())['k8s_log'][ms_item]['min']
        cost_summary[device] += float(cost)        


target_device_id = min(cost_summary, key=cost_summary.get)
target_device_name = Device(device_id=target_device_id).name
context['target_device_id'] = target_device_id
context['target_device_name'] = target_device_name

########################################################################################################
#                                        DEPLOY USER APP                                               #
########################################################################################################
'''
Generate data in format.
ms_vars_dict = {"namespace": ,
                "pod_name": ,
                "container_name": ,
                "remote_ip":
                }
'''

oid = rand_int()

ms_vars_dict = {"object_id": oid,
                "namespace": context['user_ns'],
                "user_app": context['user_app']
                }

Order(target_device_id).command_execute('CREATE', {'k8s_user_app': {oid: ms_vars_dict}})


ret = MSA_API.process_content('ENDED', f'App {context["user_app"]} Deployed on {context["target_device_name"]}', context, True)
print(ret)