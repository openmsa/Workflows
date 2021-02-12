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
#synchronise device all microservices
timeout = 60
obmf.command_synchronize(timeout)

#get microservices instance by microservice object ID.
object_name = 'interfaces_status'
object_id = str(context.get('interface_name'))
obmf.command_objects_instances_by_id(object_name, object_id)
response = json.loads(obmf.content)
context.update(obmf_inter_status_resp=response)

#ensure the object inputs are in the response.
is_status_down = False
ret_interface_status = '?'
if response:
    if object_id in response.get(object_name):
        ret_service_policy_dict = response.get(object_name).get(object_id) # {"direction": "input","object_id": "GigabitEthernet2","status": "down"}
        if 'status' in ret_service_policy_dict:
            ret_interface_status = ret_service_policy_dict.get('status')
            if ret_interface_status == 'down':
                is_status_down = True

#Store interface status in the context to used it later
context.update(interface_is_status_down=is_status_down)


#the status should be down
if is_status_down == False:
    #ret = MSA_API.process_content(constants.FAILED, 'The interface status is "'+ret_interface_status+'" for "' + object_id + '", the status should be down', context, True)
    ret = MSA_API.process_content(constants.ENDED, 'Good, the interface status is "' + is_status_down + '" for "' + object_id + '" on the device.', context, True)
    print(ret)

ret = MSA_API.process_content(constants.ENDED, 'Good, the interface status is "down" for "' + object_id + '" on the device.', context, True)
print(ret)
