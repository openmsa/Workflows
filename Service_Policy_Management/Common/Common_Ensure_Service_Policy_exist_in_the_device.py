import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('service_policy.0.interface_name', var_type='String')
dev_var.add('service_policy.0.direction', var_type='String')
dev_var.add('service_policy.0.policy_name', var_type='String')
context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)

object_name = 'service_policy'
 
command = 'IMPORT'
params = dict()
params[object_name] = "0"
#Import the given device microservice, the MS values in the UI will be not updated
obmf.command_call(command, 0, params)

service_policies = context['service_policy']
bad_values = dict()
good_values = dict()
interfaces_is_status_down = context['interfaces_is_status_down']

if service_policies:
  for rule in service_policies:
    interface_name =  str(rule.get('interface_name'))
    if good_values.get(interface_name) == None and bad_values.get(interface_name) == None :
      #don't need to check twice the same interface
      object_id = interface_name
      interface_is_status_down = interfaces_is_status_down.get(interface_name)

      #LED obmf.command_objects_instances_by_id(object_name, object_id)
      response = json.loads(obmf.content)
      context.update(obmf_sync_resp=response)
      #   "obmf_sync_resp": {
      #       "service_policy": {
      #            "GigabitEthernet1": {
      #                "object_id": "GigabitEthernet1",
      #                "param": {
      #                    "_order": "1000"
      #                }
      #            }
      #        }
      #    }

      #ensure the object inputs are in the response.
      is_policy_name_matched = False
      input_policy_name = rule.get('policy_name')

      message = response.get('entity').get('message')

      if message:
          #Convert message into array
          message = json.loads(message)
          if message.get(object_name) and object_id  in message.get(object_name):

              ret_service_policy_dict =  message.get(object_name).get(object_id) # {"direction": "input","object_id": "GigabitEthernet2","param": {"_order": "2000"},"policy_name": "PM_600104"}
              if 'policy_name' in ret_service_policy_dict:
                  ret_policy_name = ret_service_policy_dict.get('policy_name')
                  if ret_policy_name == input_policy_name:
                      is_policy_name_matched = True
                      good_values[interface_name]= 1  
                  else:
                      if interface_is_status_down == True:
                        MSA_API.task_error('Interface Down and Found one other Service Policy "'+str(ret_policy_name)+'" for interface "' + object_id + '" on the device, instead of "'+str(input_policy_name)+'"', context, True)
                      else:
                        #MSA_API.task_success('Interface UP and Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)
                        good_values[interface_name]= 1  

      context.update(is_policy_name_matched=is_policy_name_matched)
      #if is_policy_name_matched equals False it means Service Policy object doesn't exist in the device yet.
      if is_policy_name_matched == False:
          if interface_is_status_down == True:
               # IF Down and policy-map not applied
               MSA_API.task_error('Interface Down, but the Service Policy  "' + input_policy_name + '" does not exists in the interface  "' + object_id + '"', context, True)
          else:
               # IF UP and policy-map not applied
               #MSA_API.task_success('Interface UP and Service Policy "'+input_policy_name+'" for interface "' + object_id + '" not found on the device.', context, True)
               good_values[interface_name]= 1  

if (len(good_values)):
  good_values_string =  ", ".join(good_values.keys())
else: 
  good_values_string =  ""

MSA_API.task_success('For all interfaces (' +good_values_string + '), the Service Policy  exists in the device.', context, True)
