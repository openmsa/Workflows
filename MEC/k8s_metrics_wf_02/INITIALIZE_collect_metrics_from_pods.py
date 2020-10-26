import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

context = Variables.task_call()

device_id_list = context["device_id_list"]
device_ip_list = context["device_ip_list"]
ms_vars_dict_list = context["ms_vars_dict_list"]

metrics = {}

for device in device_id_list.values():
    device_metrics = []
    for ip in device_ip_list.values():
        order = Order(device)
        order.command_execute('IMPORT', {'k8s_log': {'':{'pod_name':ip.replace(".","-")}}})
        data = json.loads(order.content.decode())
        # strip unnecessary fields
        device_metrics.append(json.loads(data['message']))
    metrics[device] = device_metrics

# context['metrics'] = metrics


ret = MSA_API.process_content('ENDED', f'Metrics collected', context, True)
print(ret)