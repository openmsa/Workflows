import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('FW_local_in_policy.0.object_id', var_type='String')
dev_var.add('FW_local_in_policy.0.rule_no1', var_type='String')
dev_var.add('FW_local_in_policy.0.intf_name', var_type='String')
dev_var.add('FW_local_in_policy.0.srcaddr1', var_type='String')
dev_var.add('FW_local_in_policy.0.dstaddr', var_type='String')
dev_var.add('FW_local_in_policy.0.action', var_type='String')
dev_var.add('FW_local_in_policy.0.schedule', var_type='String')
dev_var.add('FW_local_in_policy.0.service1', var_type='String')
dev_var.add('FW_local_in_policy.0.rule_no2', var_type='String')
dev_var.add('FW_local_in_policy.0.srcaddr2', var_type='String')
dev_var.add('FW_local_in_policy.0.service2', var_type='String')
dev_var.add('FW_local_in_policy.0.rule_no3', var_type='String')
dev_var.add('FW_local_in_policy.0.srcaddr3', var_type='String')
dev_var.add('FW_local_in_policy.0.service3', var_type='String')
dev_var.add('FW_local_in_policy.0.rule_no4', var_type='String')
dev_var.add('FW_local_in_policy.0.srcaddr4', var_type='String')
dev_var.add('FW_local_in_policy.0.service4', var_type='String')
dev_var.add('FW_local_in_policy.0.rule_no5', var_type='String')
dev_var.add('FW_local_in_policy.0.srcaddr5', var_type='String')
dev_var.add('FW_local_in_policy.0.service5', var_type='String')
dev_var.add('FW_local_in_policy.0.rule_no6', var_type='String')
dev_var.add('FW_local_in_policy.0.srcaddr6', var_type='String')
dev_var.add('FW_local_in_policy.0.service6', var_type='String')
dev_var.add('FW_local_in_policy.0.rule_no7', var_type='String')
dev_var.add('FW_local_in_policy.0.srcaddr7', var_type='String')
dev_var.add('FW_local_in_policy.0.service7', var_type='String')
dev_var.add('FW_local_in_policy.0.rule_no8', var_type='String')
dev_var.add('FW_local_in_policy.0.srcaddr8', var_type='String')
dev_var.add('FW_local_in_policy.0.service8', var_type='String')
dev_var.add('FW_local_in_policy.0.fw_local_template_name', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

context['object_id']='FW'
object_id=context['object_id']

for bgp in context['FW_local_in_policy']:
	object_parameters = {}
	object_parameters['FW_Local_In_Policy']={}
	object_parameters['FW_Local_In_Policy'][object_id]={}
	for key, value in bgp.items():
		object_parameters['FW_Local_In_Policy'][object_id][key]={}
		object_parameters['FW_Local_In_Policy'][object_id][key]=value
		
	order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)

order.command_synchronize(300)
MSA_API.task_success('DONE',context, True)