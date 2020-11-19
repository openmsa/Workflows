import time
import json
from msa_sdk.variables import Variables
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from msa_sdk.lookup import Lookup
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

# stub find prim master id -'k8s-node-1'
cust_ref = context["UBIQUBEID"]
search = Lookup()
search.look_list_device_by_customer_ref(cust_ref)
device_list = search.content
device_list = json.loads(device_list)

for me in device_list:
    if me['name'] == context['vm_name'] + '-1':
        master_id = me['id']
    elif me['name'] == context['vm_name'] + '-2':
        backup_id = me['id']

# (1) kubeadm init on master first
# stub here - actually k8s master nodes should be selected according to the user input
k8s_kubeadm_init_data = {"object_id": "123",
                         "lb_ip": list(context['vms'][2].values())[0]['internal'],
                         "lb_port": "6443",
                        }
k8s_kubeadm_init_ms = {"k8s_kubeadm_init": {"123": k8s_kubeadm_init_data}}
Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'k8s-node-1: Provisioning')

try:
    order = Order(str(master_id))
    order.command_execute('CREATE', k8s_kubeadm_init_ms, timeout=400)
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Master Initiated: k8s-node-1')

# (2) get params from master first
# k8s_get_token
k8s_get_token = {'k8s_get_token': {'':{'object_id': 'kubeamd'}}}
try:
    order = Order(str(master_id))
    order.command_execute('IMPORT', k8s_get_token)
    data_1 = json.loads(order.content)
    data_1 = json.loads(data_1['message'])
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'k8s-node-1: Token retrieved')

# k8s_get_key
k8s_get_key = {'k8s_get_key': {'':{'object_id': ''}}}
try:
    order = Order(str(master_id))
    order.command_execute('IMPORT', k8s_get_key)
    data_2 = json.loads(order.content)
    data_2 = json.loads(data_2['message'])
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'k8s-node-1: Key retrieved')
time.sleep(2)

# stripping unnecessary headers
data_3 = data_1['k8s_get_token']['kubeadm']
data_4 = data_2['k8s_get_key']

# (3) kubeadm inin on master second
k8s_join_master_data = {"object_id": "123",
                        "proxy_ip": data_3['ip_addr'],
                        "proxy_port": data_3['port'],
						"token": data_3['token'],
						"hash": data_3['hash'],
						"key": list(data_4.keys())[0]
                        }
k8s_join_master = {"k8s_join_master": {"123": k8s_join_master_data}}

# (3.1) prepare microservice data for workers
k8s_join_worker_data = {"object_id": "123",
                        "proxy_ip": data_3['ip_addr'],
                        "proxy_port": data_3['port'],
                        "token": data_3['token'],
                        "hash": data_3['hash']
                       }
k8s_join_worker = {"k8s_join_worker": {"123": k8s_join_worker_data}}

context['k8s_join_worker'] = k8s_join_worker

# (4) provision second master
Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'k8s-node-2: Provisioning')
try:
    order = Order(str(backup_id))
    order.command_execute('CREATE', k8s_join_master, timeout=300)
    ddd = order.response.content
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Master Initiated: k8s-node-2')

# (5) apply k8s configuration
Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Post installation configuration: CLI control...')
k8s_cli_control_data = {"object_id": '123'}
k8s_cli_control = {"k8s_cli_control": {"123": k8s_cli_control_data}}
try:
    order = Order(str(master_id))
    order.command_execute('CREATE', k8s_cli_control, timeout=300)
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)
    
# (5.1) k8s_create_service_account (CREATE) and get token (IMPORT)
Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Post installation configuration: API control...')
k8s_create_service_account_1 = {'k8s_create_service_account': {'':{'object_id': ''}}}

try:
    order = Order(str(master_id))
    order.command_execute('CREATE', k8s_create_service_account_1, timeout=300)
    ret = order.response.content
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Post installation configuration: API token...')

# do the same in API task:
context['master_id'] = master_id

Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Post installation configuration completed.')

time.sleep(2)
# (6) install cni plugin
Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Network Plugin: Installation...')

k8s_cni_install_data = {"object_id": '123'}
k8s_cni_install = {"k8s_cni_install": {"123": k8s_cni_install_data}}
try:
    order = Order(str(master_id))
    order.command_execute('CREATE', k8s_cni_install, timeout=300)
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

Orchestration.update_asynchronous_task_details(*async_update_list,
                                               f'Network Plugin: Installed')

ret = MSA_API.process_content('ENDED',
                              f'k8s-node-1, k8s-node-2 configured as k8s masters.',
                              context, True)
print(ret)