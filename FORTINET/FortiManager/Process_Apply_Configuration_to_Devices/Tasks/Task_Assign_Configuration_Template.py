import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
#dev_var.add('fmg_me', var_type='Device')
dev_var.add('device', var_type='String')
dev_var.add('template', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)


object_id="temp"
object_parameters = {}
object_parameters['Assign_SDWAN_Template']={}
object_parameters['Assign_SDWAN_Template'] [object_id]={}
object_parameters['Assign_SDWAN_Template'] [object_id]['object_id']="temp"
object_parameters['Assign_SDWAN_Template'] [object_id]['device_name']=context['device']
object_parameters['Assign_SDWAN_Template'] [object_id]['template_name']=context['template']

order.command_execute('CREATE', object_parameters)

# convert dict object into json
content = json.loads(order.content)

order.command_synchronize(300)	
MSA_API.task_success('DONE',context, True)