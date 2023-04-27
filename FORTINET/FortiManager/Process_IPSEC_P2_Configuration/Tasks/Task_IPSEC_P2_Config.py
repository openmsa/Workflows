import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()

dev_var.add('IPSEC_p2_config.0.object_id', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p2_name1', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p1_name1', var_type='String')
dev_var.add('IPSEC_p2_config.0.proposal_name1', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p2_name2', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p1_name2', var_type='String')
dev_var.add('IPSEC_p2_config.0.proposal_name2', var_type='String')
dev_var.add('IPSEC_p2_config.0.keylifeseconds', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p2_name3', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p1_name3', var_type='String')
dev_var.add('IPSEC_p2_config.0.keylifekbs', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p2_name4', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p1_name4', var_type='String')
dev_var.add('IPSEC_p2_config.0.IPSEC_p2_template_name', var_type='String')
context = Variables.task_call(dev_var)


# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

context['object_id']='IPSEC'
object_id=context['object_id']

for bgp in context['IPSEC_p2_config']:
	object_parameters = {}
	object_parameters['IPSEC_P2_Config']={}
	object_parameters['IPSEC_P2_Config'][object_id]={}
	for key, value in bgp.items():
		object_parameters['IPSEC_P2_Config'][object_id][key]={}
		object_parameters['IPSEC_P2_Config'][object_id][key]=value
		
	order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)
order.command_synchronize(300)
MSA_API.task_success('DONE',context, True)