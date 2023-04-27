import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('devices.0.registeredDevices', var_type='String')
dev_var.add('devices.0.registeredScripts', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

for dev in context['devices']:
	object_id="temp"
	object_parameters = {}
	object_parameters['FortiManager_-_Run_Scripts']={}
	object_parameters['FortiManager_-_Run_Scripts'][object_id]={}
	object_parameters['FortiManager_-_Run_Scripts'][object_id]['object_id']="temp"
	object_parameters['FortiManager_-_Run_Scripts'][object_id]['device_name']=dev['registeredDevices']
	object_parameters['FortiManager_-_Run_Scripts'][object_id]['script_name']=dev['registeredScripts']

	order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)


order.command_synchronize(300)	
MSA_API.task_success('DONE',context, True)