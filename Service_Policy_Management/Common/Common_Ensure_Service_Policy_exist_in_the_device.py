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
params = dict(object_name="0")
#synchronise the given device microservice
obmf.command_call(command, 1, params) # put 1 to update the DB

interface_is_status_down = context.get('interface_is_status_down')

#get microservices instance by microservice object ID.
object_id = str(context.get('interface_name'))
obmf.command_objects_instances_by_id(object_name, object_id)
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
input_policy_name = context.get('policy_name')
if response:
    if object_id in response.get(object_name):
        ret_service_policy_dict = response.get(object_name).get(object_id) # {"direction": "input","object_id": "GigabitEthernet2","param": {"_order": "2000"},"policy_map": "PM_600104"}
        if 'policy_map' in ret_service_policy_dict:
            ret_policy_name = ret_service_policy_dict.get('policy_map')
            if ret_policy_name == input_policy_name:
                is_policy_name_matched = True
            else:
                if interface_is_status_down == True:
                  MSA_API.task_error('Interface Down and Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)
                else:
                  MSA_API.task_success('Interface UP and Found one other Service Policy "'+ret_policy_name+'" for interface "' + object_id + '" on the device.', context, True)

context.update(is_policy_name_matched=is_policy_name_matched)
#if is_policy_name_matched equals False it means Service Policy object doesn't exist in the device yet.
if is_policy_name_matched == False:
    if interface_is_status_down == True:
         # IF Down and policy-map not applied
         MSA_API.task_error('Interface Down, but the Service Policy  "' + input_policy_name + '" does not exists in the interface  "' + object_id + '"', context, True)
    else:
         # IF UP and policy-map not applied
         MSA_API.task_success('Interface UP and Service Policy "'+input_policy_name+'" for interface "' + object_id + '" not found on the device.', context, True)
MSA_API.task_success('On interface "' + object_id + '", the Service Policy  "' + input_policy_name + '" exists in the device.', context, True)
