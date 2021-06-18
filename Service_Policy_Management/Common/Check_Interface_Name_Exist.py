import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('service_policy.0.interface_name', var_type='String')
context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)

object_name = 'interfaces_status'

command = 'IMPORT'

params = dict()
params[object_name] = "0"
#synchronise the given device microservice
obmf.command_call(command, 0, params) # put 0 to not update the db

service_policy = context['service_policy']
bad_values = dict()
good_values = dict()

if service_policy:
  for rule in service_policy:
    interface_name =  str(rule.get('interface_name'))
    if good_values.get(interface_name) == None and bad_values.get(interface_name) == None :
      #don't need to check twice the same interface
      #LED obmf.command_objects_instances_by_id(object_name, interface_name)
      response = json.loads(obmf.content)
      context.update(obmf_inter_status_resp=response)

      #ensure the object inputs are in the response.
      found_interface_name = False
      if message:
          #Convert message into array
          message = json.loads(message)
          #message = {"interfaces_status":{"GigabitEthernet1":{"object_id":"GigabitEthernet1","status":"up"},"GigabitEthernet2":{"object_id":"GigabitEthernet2","status":"down"},"GigabitEthernet3":{"object_id":"GigabitEthernet3","status":"down"}}}
          if message.get(object_name) and interface_name  in message.get(object_name):
	 
            ret_service_policy_dict =  message.get(object_name).get(interface_name) # {"direction": "input","interface_name": "GigabitEthernet2","status": "down"}
            found_interface_name = True

      if found_interface_name == True:
        good_values[interface_name]= 1
      else:
        bad_values[interface_name]= 1
    


if (len(good_values)):
  good_values_string =  ", ".join(good_values.keys())
else: 
  good_values_string =  ""
good_values_string =  ", ".join(good_values.keys())

if (len(bad_values)):
  bad_values_string =  ", ".join(bad_values.keys())
  if (len(bad_values)):
    MSA_API.task_error('Can not find interfaces ('+bad_values_string+') on the device, but find interfaces ('+good_values_string+') ', context, True)
  else:
    MSA_API.task_error('Can not find all interfaces ('+bad_values_string+') on the device', context, True)
else: 
  MSA_API.task_success('Good, interfaces ('+good_values_string+') exists on the device ', context, True)



