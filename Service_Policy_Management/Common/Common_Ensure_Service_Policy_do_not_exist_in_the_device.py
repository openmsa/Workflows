import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('service_policy.0.interface_name', var_type='String')
dev_var.add('service_policy.0.direction', var_type='String')
dev_var.add('service_policy.0.policy_map', var_type='String')

context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)
#synchronise device microservices
timeout = 300
obmf.command_synchronize(timeout)

#get microservices instance by microservice object ID.
object_name = 'service_policy'


 
service_policy = context['service_policy']
bad_values = dict()
good_values = dict()
interfaces_is_status_down = context['interfaces_is_status_down']

if service_policy:
  for rule in service_policy:
    interface_name =  str(rule.get('interface_name'))
    if good_values.get(interface_name) == None and bad_values.get(interface_name) == None :
      #don't need to check twice the same interface

      object_id = interface_name
      obmf.command_objects_instances_by_id(object_name, object_id)
      response = json.loads(obmf.content)
      context.update(obmf_sync_resp=response) 
      #if response equals empty dictionary it means class map object is not exist in the device yet.
      is_policy_map_matched = False
      input_policy_map = rule.get('policy_map')
      interface_is_status_down = interfaces_is_status_down.get(interface_name)
      service_policy_action = context.get('service_policy_action')   # 'DELETE_SERVICE_POLICY' / 'ADD_SERVICE_POLICY' 

      if response:
          #response: { "service_policy": {  "GigabitEthernet2": {  "direction": "input", "object_id": "GigabitEthernet2", "param": {  "_order": "2000" },  "policy_map": "PM_600104" }
          if object_id in response.get(object_name):
              ret_service_policy_dict = response.get(object_name).get(object_id) # {"direction": "input","object_id": "GigabitEthernet2","param": {"_order": "2000"},"policy_map": "PM_600104"}
              if 'policy_map' in ret_service_policy_dict:
                  ret_policy_map = ret_service_policy_dict.get('policy_map')
                  if ret_policy_map == input_policy_map:
                      is_policy_map_matched = True
                  else:
                      if interface_is_status_down == True:
                         #Interface DOWN and other policy
                         if service_policy_action == 'DELETE_SERVICE_POLICY' :
                             #MSA_API.task_success('Interface Down, Found one other Service Policy "'+ret_policy_map+'" for interface "' + object_id + '" on the device.', context, True)
                             good_values[interface_name]= 1                        
                         else:
                             #MSA_API.task_success('Interface Down, Found one other Service Policy "'+ret_policy_map+'" for interface "' + object_id + '" on the device.', context, True)
                             good_values[interface_name]= 1                        
                      else:
                         #Interface UP and other policy
                         MSA_API.task_error('Interface UP and Found one other Service Policy "'+ret_policy_map+'" for interface "' + object_id + '" on the device.', context, True)
              else:
                  good_values[interface_name]= 1                        
      if (context.get('all_is_policy_map_matched') == None):
         all_is_policy_map_matched = dict()
      else:
         all_is_policy_map_matched = context['all_is_policy_map_matched']
      all_is_policy_map_matched[interface_name] = is_policy_map_matched
      context.update(all_is_policy_map_matched  = all_is_policy_map_matched)

      #if is_policy_map_matched equals True it means Service Policy object doesn't exist in the device yet.
      if is_policy_map_matched == True:
          if interface_is_status_down == True:
            #Interface DOWN and matche
            if service_policy_action == 'DELETE_SERVICE_POLICY' :
                MSA_API.task_error('On interface Down "' + object_id + '", the Service Policy "'+input_policy_map+'" always exists in the device.', context, True)
            else:
                MSA_API.task_error('On interface Down "' + object_id + '", the Service Policy "'+input_policy_map+'" already exists in the device.', context, True)
          else:
            #Interface UP and matche
            if service_policy_action == 'DELETE_SERVICE_POLICY' :
                MSA_API.task_error('On interface UP "' + object_id + '", the Service Policy "'+input_policy_map+'" always exists in the device.', context, True)
            else:
                #MSA_API.task_success('On interface UP "' + object_id + '", the Service Policy "'+input_policy_map+'" already exists in the device.', context, True)
                good_values[interface_name]= 1                        

if (len(good_values)):
  good_values_string =  ", ".join(good_values.keys())
else: 
  good_values_string =  ""

#MSA_API.task_success('On interface "' + object_id + '", the Service Policy  "'+input_policy_map+'" does not exist in the device yet.', context, True)
MSA_API.task_success('Good, Interfaces ('+good_values_string+'), all given Service Policies no exist in the device yet', context, True)

