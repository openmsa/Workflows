import json
from msa_sdk.variables import Variables
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup

'''
dev_var = Variables()
dev_var.add('proxy_host', var_type='Device')
dev_var.add('proxy_type', var_type='String')
dev_var.add('k8s_master.0.host', var_type='Device')
context = Variables.task_call(dev_var)

# Ex. for list var [{'host': 'UBI1365'}, {'host': 'UBI1366'}]
# Replace ME names according to provided schema:

i = 0
for me in context["k8s_master"]:
    i += 1
    Device(device_id=me['host'][-4:]).name = "k8s-master-0" + str(i)
Device(device_id=context['proxy_host'][-4:]).name += "[proxy]"
'''

dev_var = Variables()
context = Variables.task_call()

cust_ref = context["UBIQUBEID"]

# prepare configuration where to install loadbalancer
search = Lookup()
search.look_list_device_by_customer_ref(cust_ref)
device_list = search.content
device_list = json.loads(device_list)

# stub for load-balancer node num.3
for me in device_list:
    if me['name'] == context['vm_name'] + '-3':
        context['proxy_host'] = me['externalReference']
        break

context['proxy_type'] = 'haproxy'

ret = MSA_API.process_content('ENDED',
                              f'Haproxy package to install on {context["vm_name"]}-3',
                              context, True)
print(ret)