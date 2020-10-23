import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup
from msa_sdk.device import Device

dev_var = Variables()
dev_var.add('subtenant', var_type='Customer')
dev_var.add('namespace', var_type='String')
dev_var.add('packet_size', var_type='Integer')
dev_var.add('packet_count', var_type='Integer')
dev_var.add('user_app', var_type='String')
dev_var.add('user_ns', var_type='String')
context = Variables.task_call(dev_var)

device_id_list = []
device_ip_list = []

search = Lookup()
search.look_list_device_by_customer_ref(context['subtenant'])
device_list = search.content.decode()
device_list = json.loads(device_list)

for device in device_list:
    device_id_list.append(device['id'])
    device_ip_list.append(Device(device_id=device['id']).management_address)
    
context['device_ip_list'] = device_ip_list
context['device_id_list'] = device_id_list

ret = MSA_API.process_content('ENDED', f'workflow initialised {context["device_ip_list"]}', context, True)
print(ret)