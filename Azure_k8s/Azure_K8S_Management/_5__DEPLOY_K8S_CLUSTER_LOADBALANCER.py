import time
from msa_sdk.variables import Variables
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

# (1) prepare data for k8s_ha_proxy and k8s_package_management microservices
k8s_package_management_data = {"object_id": context['proxy_type']}
k8s_package_management_ms = {"k8s_package_management": {context['proxy_type']: k8s_package_management_data}}

# stub here - actually k8s master nodes should be selected according to the user input
k8s_ha_proxy_data = {"object_id": "123",
                     "k8s_m_1_ip": list(context['vms'][0].values())[0]['internal'],
                     "k8s_m_2_ip": list(context['vms'][1].values())[0]['internal'],
                    }
k8s_ha_proxy_ms = {"k8s_ha_proxy": {"123": k8s_ha_proxy_data}}

# (2) get short ME id
me_id = context['proxy_host'][3:]

# (3) install package on certain me
Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'haproxy installation: {Device(device_id=me_id).name}')
try:
    order = Order(me_id)
    order.command_execute('CREATE', k8s_package_management_ms, timeout=300)
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)
time.sleep(10)
# (4) configure and start proxy
try:
    order = Order(me_id)
    order.command_execute('CREATE', k8s_ha_proxy_ms)
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)


ret = MSA_API.process_content('ENDED', f'Loadbalancer prepared.', context, True)
print(ret)