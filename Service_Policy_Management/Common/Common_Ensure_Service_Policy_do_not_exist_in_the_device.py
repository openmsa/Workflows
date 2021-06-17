import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('interface_name', var_type='String')
dev_var.add('direction', var_type='String')
dev_var.add('policy_name', var_type='String')

context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)

object_name = 'service_policy'

command = 'IMPORT'
params = dict()
params[object_name] = "0"
#synchronise the given device microservice
obmf.command_call(command, 0, params) # put 0 to not update the db

#get microservices instance by microservice object ID.
object_id = str(context.get('interface_name'))
response = json.loads(obmf.content)
context.update(obmf_sync_resp=response)
#if response equals empty dictionary it means class map object is not exist in the device yet.
is_policy_name_matched = False
input_policy_name = context.get('policy_name')
interface_is_status_down = context.get('interface_is_status_down')
service_policy_action = context.get('service_policy_action')   # 'DELETE_SERVICE_POLICY' / 'ADD_SERVICE_POLICY' 

#response={'entity': {'commandId': 0, 'status': 'OK', 'message': '{"service_policy":{"GigabitEthernet1":{"object_id":"GigabitEthernet1"},"GigabitEthernet2":{"object_id":"GigabitEthernet2"},"GigabitEthernet3":{"object_id":"GigabitEthernet3","direction":"input","policy_map":"PM_600105"}}}'}, 'variant': {'language': None, 'mediaType': {'type': 'application', 'subtype': 'json', 'parameters': {}, 'wildcardType': False, 'wildcardSubtype': False}, 'encoding': None, 'languageString': None}, 'annotations': [], 'mediaType': {'type': 'application', 'subtype': 'json', 'parameters': {}, 'wildcardType': False, 'wildcardSubtype': False}, 'language': None, 'encoding': None} 
message = response.get('entity').get('message')
#MSA_API.task_error('Test, response='+str(response), context, True)

if message:
    #Convert message into array
    message = json.loads(message)

    if object_id in message.get(object_name):
        ret_service_policy_dict = message.get(object_name).get(object_id) # {"direction": "input","object_id": "GigabitEthernet2","param": {"_order": "2000"},"policy_map": "PM_600104"}
        if 'policy_map' in ret_service_policy_dict:
            ret_policy_name = ret_service_policy_dict.get('policy_map')
            if ret_policy_name == input_policy_name:
                is_policy_name_matched = True
            else:
                if interface_is_status_down == True:
                   #Interface DOWN and other policy
                   if service_policy_action == 'DELETE_SERVICE_POLICY' :
                       MSA_API.task_success('Interface Down, Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)
                   else:
                       MSA_API.task_success('Interface Down, Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)
                else:
                   #Interface UP and other policy
                   MSA_API.task_error('Interface UP and Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)

context.update(is_policy_name_matched=is_policy_name_matched)

#if is_policy_name_matched equals True it means Service Policy object doesn't exist in the device yet.
if is_policy_name_matched == True:
    if interface_is_status_down == True:
      #Interface DOWN and matche
      if service_policy_action == 'DELETE_SERVICE_POLICY' :
          MSA_API.task_error('On interface Down "' + object_id + '", the Service Policy "'+input_policy_name+'" always exists in the device.', context, True)
      else:
          MSA_API.task_error('On interface Down "' + object_id + '", the Service Policy "'+input_policy_name+'" already exists in the device.', context, True)
    else:
      #Interface UP and matche
      if service_policy_action == 'DELETE_SERVICE_POLICY' :
          MSA_API.task_error('On interface UP "' + object_id + '", the Service Policy "'+input_policy_name+'" always exists in the device.', context, True)
      else:
          MSA_API.task_success('On interface UP "' + object_id + '", the Service Policy "'+input_policy_name+'" already exists in the device.', context, True)

MSA_API.task_success('On interface "' + object_id + '", the Service Policy  "'+input_policy_name+'" does not exist in the device yet.', context, True)

