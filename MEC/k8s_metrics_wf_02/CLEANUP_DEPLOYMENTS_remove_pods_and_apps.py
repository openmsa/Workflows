import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
context = Variables.task_call()

device_id_list = context["device_id_list"]
target_device_id = context['target_device_id']

# remove metrics pods
for device in device_id_list.values():
    order = Order(device)
    order.command_objects_instances('k8s_pods')
    ms_instances = json.loads(order.content.decode())
    for instance in ms_instances:
        Order(device).command_execute('DELETE', {'k8s_pods': instance})
        
# remove user app
order = Order(target_device_id)
order.command_objects_instances('k8s_user_app')
ms_instances = json.loads(order.content.decode())
for instance in ms_instances:
    Order(target_device_id).command_execute('DELETE', {'k8s_user_app': instance})


ret = MSA_API.process_content('ENDED', f'pods cleared, app removed', context, True)
print(ret)