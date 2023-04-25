import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('Static_routes.0.object_id', var_type='String')
dev_var.add('Static_routes.0.route_no1', var_type='String')
dev_var.add('Static_routes.0.gateway_1', 'IpAddress');
dev_var.add('Static_routes.0.distance', var_type='String')
dev_var.add('Static_routes.0.portname1', var_type='String')
dev_var.add('Static_routes.0.route_no2', var_type='String')
dev_var.add('Static_routes.0.dst_ip_1', 'IpAddress');
dev_var.add('Static_routes.0.dst_subnetmask', var_type='String')
dev_var.add('Static_routes.0.portname2', var_type='String')
dev_var.add('Static_routes.0.route_no3', var_type='String')
dev_var.add('Static_routes.0.dst_ip_2', var_type='String')
dev_var.add('Static_routes.0.portname3', var_type='String')
dev_var.add('Static_routes.0.route_no4', var_type='String')
dev_var.add('Static_routes.0.dst_ip_3', 'IpAddress');
dev_var.add('Static_routes.0.gateway_2', 'IpAddress');
dev_var.add('Static_routes.0.portname4', var_type='String')
dev_var.add('Static_routes.0.static_temp_name', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

context['object_id']='IPSEC'
object_id=context['object_id']

for bgp in context['Static_routes']:
	object_parameters = {}
	object_parameters['Static_Route']={}
	object_parameters['Static_Route'][object_id]={}
	for key, value in bgp.items():
		object_parameters['Static_Route'][object_id][key]={}
		object_parameters['Static_Route'][object_id][key]=value
		
	order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)
order.command_synchronize(300)
MSA_API.task_success('DONE',context, True)