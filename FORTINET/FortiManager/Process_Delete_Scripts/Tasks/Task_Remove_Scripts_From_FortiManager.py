import json
import uuid
import time
import os
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('devices.0.registeredScripts', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
for dev in context['devices']:
	object_id=dev['registeredScripts']
	object_parameters = {}
	object_parameters['FortiManager_-_Scripts'] = {}
	object_parameters['FortiManager_-_Scripts'] [object_id]={}
	object_parameters['FortiManager_-_Scripts'] [object_id]['object_id']= object_id

	order = Order(devicelongid)
	order.command_execute('DELETE', object_parameters)
# convert dict object into json
	content = json.loads(order.content)

order.command_synchronize(300)		
MSA_API.task_success('DONE',context, True)