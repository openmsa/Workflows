import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup
from msa_sdk.device import Device

dev_var = Variables()
dev_var.add('subtenant', var_type='Customer')
dev_var.add('user_namespace', var_type='String')
dev_var.add('service_namespace', var_type='String')
dev_var.add('pkt_size', var_type='Integer')
dev_var.add('pkt_count', var_type='Integer')
dev_var.add('app_name', var_type='String')
dev_var.add('port', var_type='Integer')
dev_var.add('target_port', var_type='Integer')
dev_var.add('node_port', var_type='Integer')
dev_var.add('label', var_type='String')
context = Variables.task_call(dev_var)

if __name__ == "__main__":

    device_id_list = []
    device_ip_list = []

    search = Lookup()
    # search.look_list_device_by_customer_ref(context['subtenant'])
    search.look_list_device_by_customer_ref('TyrellCorp')
    device_list = search.content
    device_list = json.loads(device_list)

    for device in device_list:
        device_id_list.append(device['id'])
        device_ip_list.append(Device(device_id=device['id']).management_address)

    context['device_ip_list'] = device_ip_list
    context['device_id_list'] = device_id_list

    ret = MSA_API.process_content('ENDED',
                                  f'Workflow Instance Created. Data retrieved.',
                                  context, True)
    print(ret)