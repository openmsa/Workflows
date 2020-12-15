import json
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
device_ip_list = context["device_ip_list"]
ms_vars_dict_list = context["ms_vars_dict_list"]

# throw message
def info_message(text, timeout=1):
    Orchestration.update_asynchronous_task_details(*async_update_list, text)
    time.sleep(timeout)

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

if __name__ == "__main__":

    metrics = {}

    info_message('Collecting metrics from devices...')

    for device in device_id_list:
        d_name = Device(device_id=device).name
        info_message(f'Collecting metrics from devices: {d_name}...')
        device_metrics = []
        for ip in device_ip_list:
            order = Order(device)
            order.command_execute('IMPORT', get_logs_ms(ip.replace(".","-")))
            data = json.loads(order.content)
            # strip unnecessary fields
            # device_metrics.append(json.loads(data['message']))
            device_metrics.append(data)
        metrics[device] = device_metrics
        info_message(f'Collecting metrics from devices: {d_name} done.')

    ret = MSA_API.process_content('ENDED', f'Metrics collected.', context, True)
    print(ret)