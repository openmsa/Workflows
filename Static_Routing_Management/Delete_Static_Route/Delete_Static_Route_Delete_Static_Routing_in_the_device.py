'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''
import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('static_routing.0.source_address', var_type='IPAddress')
dev_var.add('static_routing.0.subnet_mask', var_type='IPMask')
dev_var.add('static_routing.0.vlan_id', var_type='String')
dev_var.add('static_routing.0.nexthop', var_type='IPAddress')
dev_var.add('static_routing.0.distance', var_type='Interger')
context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]

#Initiate Order object with the device_id
obmf = Order(device_id)

#Execute ADD method of StaticRouting Microservice to add route in the device
command = 'DELETE' # MS method corresponding on ADD Static route operation

static_routing = context.get('static_routing')

if static_routing:
  #build MS the dictionary input object 
  config = dict(static_routing=static_routing)

  obj = {"":config} #object = {'':{'object_id':'192.168.1.2', 'gateway':'192.168.1.254'}}
  params = dict(static_route=obj)

  obmf.command_execute(command, params, timeout = 300) #execute the MS ADD static route operation
  response = json.loads(obmf.content)

  if response.get('wo_status') == constants.FAILED:
      detials = ''
      if 'wo_newparams' in response:
          detials = response.get('wo_newparams')
      MSA_API.task_error('Failure details: ' + detials, context, True)

  #store OBMF command execution response in context
  context['response'] = response.get('wo_newparams')

  MSA_API.task_success('Delete static route operation is done successfully.', context, True)
else:
  MSA_API.task_success('OK no static rule to delete', context, True)
