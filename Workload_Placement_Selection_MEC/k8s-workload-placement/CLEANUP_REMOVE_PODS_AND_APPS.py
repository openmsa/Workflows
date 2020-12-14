import json
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

device_id_list = context["device_id_list"]
target_device_name = context['target_device_name']
target_device_id = context['target_device_id']

# throw message
def info_message(text, timeout=1):
    Orchestration.update_asynchronous_task_details(*async_update_list, text)
    time.sleep(timeout)

def get_pod_ns(pod_name):
    order.command_objects_instances_by_id('k8_pods_list', pod_name)
    response = json.loads(order.content)
    return response['k8_pods_list'][pod_name]['namespace']

if __name__ == "__main__":
    
    # remove metrics pods
    info_message('Removing service pods...')
    for device in device_id_list:
        d_name = Device(device_id=device).name
        info_message(f'Removing service pods: {d_name}...')
        order = Order(device)
        # syncronize first
        k8_pods_list = {'k8_pods_list': {'':{ }}}
        order.command_execute('IMPORT', k8_pods_list)
        order.command_objects_instances('k8_pods_list')
        pods_list = json.loads(order.content)
        for pod in pods_list:
            if get_pod_ns(pod) == context['service_namespace']:
                info_message(f'Removing service pods: {d_name} {pod}...')
                order.command_execute('DELETE', {'k8_pods_list': pod})
            
    # remove all applications from user_namespace
    info_message(f'Removing user apps: {target_device_name}...')
    order = Order(target_device_id)
    # syncronize first
    k8_pods_list = {'k8_pods_list': {'':{ }}}
    order.command_execute('IMPORT', k8_pods_list)
    order.command_objects_instances('k8_pods_list')
    ms_instances = json.loads(order.content)
    pods_list = json.loads(order.content)
    for pod in pods_list:
        if get_pod_ns(pod) == context['user_namespace']:
            info_message(f'Removing service pods: {target_device_name} {pod}...')
            order.command_execute('DELETE', {'k8_pods_list': pod})

    ret = MSA_API.process_content('ENDED', f'Service PODs removed, User APPs removed.', context, True)
    print(ret)