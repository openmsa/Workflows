import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

context = Variables.task_call()

device_id_list = context["device_id_list"]
device_ip_list = context["device_ip_list"]
ms_vars_dict_list = context["ms_vars_dict_list"]


# url ex.: namespaces/network-metrics/pods/10-31-1-64/log
def get_logs_ms(pod_name):
    
    logs_ms_data = {'logs':
                       {'':
                            {'url': 'namespaces' + \
                                    '/' + \
                                    context['service_namespace'] + \
                                    '/' + \
                                    'pods' + \
                                    '/' + \
                                    pod_name + \
                                    '/' + \
                                    'log'
                            }
                       }
                   }
    
    return logs_ms_data

metrics = {}

for device in device_id_list:
    device_metrics = []
    for ip in device_ip_list:
        order = Order(device)
        order.command_execute('IMPORT', get_logs_ms(ip.replace(".","-")))
        data = json.loads(order.content)
        # strip unnecessary fields
        # device_metrics.append(json.loads(data['message']))
        device_metrics.append(data)
    metrics[device] = device_metrics


ret = MSA_API.process_content('ENDED', f'Metrics collected {metrics}', context, True)
print(ret)