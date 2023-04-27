import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('devices.0.id', var_type='String')
dev_var.add('devices.0.username', var_type='String')
dev_var.add('devices.0.password', var_type='String')
dev_var.add('devices.0.name', var_type='String')
dev_var.add('devices.0.ip', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)
for device in context['devices']:
	object_id=device['name']
	object_parameters = {}
	object_parameters['FortiManager_-_Devices']={}
	object_parameters['FortiManager_-_Devices'] [object_id]={}
	object_parameters['FortiManager_-_Devices'] [object_id]['object_id']=device['name']
	object_parameters['FortiManager_-_Devices'] [object_id]['user_name']=device['username']
	object_parameters['FortiManager_-_Devices'] [object_id]['user_password']=device['password']
	object_parameters['FortiManager_-_Devices'] [object_id]['ip_address']=device['ip']
	order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)

order.command_synchronize(300)	
MSA_API.task_success('DONE',context, True)