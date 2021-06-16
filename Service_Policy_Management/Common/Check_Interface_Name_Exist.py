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
#synchronise device all microservices
timeout = 300
obmf.command_synchronize(timeout)

#get microservices instance by microservice object ID.
object_name = 'interfaces_status'


service_policy = context['service_policy']
bad_values = dict()
good_values = dict()

if service_policy:
  for rule in service_policy:
    interface_name =  str(rule.get('interface_name'))
    if good_values.get(interface_name) == None and bad_values.get(interface_name) == None :
      #don't need to check twice the same interface
      obmf.command_objects_instances_by_id(object_name, interface_name)
      response = json.loads(obmf.content)
      context.update(obmf_inter_status_resp=response)

      #ensure the object inputs are in the response.
      found_interface_name = False
      if response:
        if interface_name in response.get(object_name):
          ret_service_policy_dict = response.get(object_name).get(interface_name) # {"direction": "input","interface_name": "GigabitEthernet2","status": "down"}
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



