import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('scripts.0.name', var_type='String')
dev_var.add('scripts.0.type', var_type='String')
dev_var.add('scripts.0.content', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

for script in context['scripts']:
	object_id=script['name']
	object_parameters = {}
	object_parameters['FortiManager_-_Scripts']={}
	object_parameters['FortiManager_-_Scripts'] [object_id]={}
	object_parameters['FortiManager_-_Scripts'] [object_id]['object_id']=script['name']
	object_parameters['FortiManager_-_Scripts'] [object_id]['type']=script['type']
	object_parameters['FortiManager_-_Scripts'] [object_id]['content']=script['content']
	order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)
	order.command_synchronize(300)
	
MSA_API.task_success('DONE',context, True)