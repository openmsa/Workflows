import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('BGP_config.0.BGP_temp_name', var_type='String')
dev_var.add('BGP_config.0.object_id', var_type='String')
dev_var.add('BGP_config.0.AS_no', var_type='String')
dev_var.add('BGP_config.0.routerid', var_type='String')
dev_var.add('BGP_config.0.neighip1', var_type='IpAddress')
dev_var.add('BGP_config.0.remote_AS_no1', var_type='String')
dev_var.add('BGP_config.0.route_map_in', var_type='String')
dev_var.add('BGP_config.0.route_map_out1', var_type='String')
dev_var.add('BGP_config.0.neighip2', var_type='IpAddress')
dev_var.add('BGP_config.0.remote_AS_no2', var_type='String')
dev_var.add('BGP_config.0.route_map_out2', var_type='String')
dev_var.add('BGP_config.0.neighip3', var_type='IpAddress')
dev_var.add('BGP_config.0.remote_AS_no3', var_type='String')
dev_var.add('BGP_config.0.route_map_out3', var_type='String')
dev_var.add('BGP_config.0.network_no1', var_type='String')
dev_var.add('BGP_config.0.network_ip1', var_type='IpAddress')
dev_var.add('BGP_config.0.network_subnetmask1', var_type='String')
dev_var.add('BGP_config.0.network_no2', var_type='String')
dev_var.add('BGP_config.0.network_ip2', var_type='IpAddress')
dev_var.add('BGP_config.0.network_subnetmask2', var_type='String')
dev_var.add('BGP_config.0.network_no3', var_type='String')
dev_var.add('BGP_config.0.network_ip3', var_type='IpAddress')
dev_var.add('BGP_config.0.network_no4', var_type='String')
dev_var.add('BGP_config.0.network_ip4', var_type='IpAddress')
dev_var.add('BGP_config.0.network_no5', var_type='String')
dev_var.add('BGP_config.0.network_ip5', var_type='IpAddress')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

context['object_id']='bgptest'
object_id=context['object_id']

for bgp in context['BGP_config']:
	object_parameters = {}
	object_parameters['BGP_Config']={}
	object_parameters['BGP_Config'][object_id]={}
	for key, value in bgp.items():
		object_parameters['BGP_Config'][object_id][key]={}
		object_parameters['BGP_Config'][object_id][key]=value
		
	order.command_execute('CREATE', object_parameters)
# convert dict object into json
	content = json.loads(order.content)

order.command_synchronize(300)
MSA_API.task_success('DONE',context, True)