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
#synchronise device microservices
timeout = 300
obmf.command_synchronize(timeout)

#get microservices instance by microservice object ID.
object_name = 'service_policy'
object_id = str(context.get('interface_name'))
obmf.command_objects_instances_by_id(object_name, object_id)
response = json.loads(obmf.content)
context.update(obmf_sync_resp=response)
#if response equals empty dictionary it means class map object is not exist in the device yet.
is_policy_name_matched = False
input_policy_name = context.get('policy_name')
interface_is_status_down = context.get('interface_is_status_down')
service_policy_action = context.get('service_policy_action')   # 'DELETE_SERVICE_POLICY' / 'ADD_SERVICE_POLICY' 

if response:
    if object_id in response.get(object_name):
        ret_service_policy_dict = response.get(object_name).get(object_id) # {"direction": "input","object_id": "GigabitEthernet2","param": {"_order": "2000"},"policy_map": "PM_600104"}
        if 'policy_map' in ret_service_policy_dict:
            ret_policy_name = ret_service_policy_dict.get('policy_map')
            if ret_policy_name == input_policy_name:
                is_policy_name_matched = True
            else:
                if interface_is_status_down == True:
                   #Interface DOWN and other policy
                   if service_policy_action == 'DELETE_SERVICE_POLICY' :
                       ret = MSA_API.process_content(constants.ENDED, 'Interface Down, Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)
                   else:
                       ret = MSA_API.process_content(constants.ENDED, 'Interface Down, Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)
                else:
                   #Interface UP and other policy
                   ret = MSA_API.process_content(constants.FAILED, 'Interface UP and Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)
                print(ret)

context.update(is_policy_name_matched=is_policy_name_matched)

#if is_policy_name_matched equals True it means Service Policy object doesn't exist in the device yet.
if is_policy_name_matched == True:
    if interface_is_status_down == True:
      #Interface DOWN and matche
      if service_policy_action == 'DELETE_SERVICE_POLICY' :
          ret = MSA_API.process_content(constants.FAILED, 'On interface Down "' + object_id + '", the Service Policy "'+input_policy_name+'" always exists in the device.', context, True)
      else:
          ret = MSA_API.process_content(constants.FAILED, 'On interface Down "' + object_id + '", the Service Policy "'+input_policy_name+'" already exists in the device.', context, True)
    else:
      #Interface UP and matche
      if service_policy_action == 'DELETE_SERVICE_POLICY' :
          ret = MSA_API.process_content(constants.FAILED, 'On interface UP "' + object_id + '", the Service Policy "'+input_policy_name+'" always exists in the device.', context, True)
      else:
          ret = MSA_API.process_content(constants.ENDED, 'On interface UP "' + object_id + '", the Service Policy "'+input_policy_name+'" already exists in the device.', context, True)
    print(ret)

ret = MSA_API.process_content(constants.ENDED, 'On interface "' + object_id + '", the Service Policy  "'+input_policy_name+'" does not exist in the device yet.', context, True)

print(ret)