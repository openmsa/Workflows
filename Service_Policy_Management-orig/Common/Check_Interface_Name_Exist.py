import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('interface_name', var_type='String')
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
object_id = str(context.get('interface_name'))
obmf.command_objects_instances_by_id(object_name, object_id)
response = json.loads(obmf.content)
context.update(obmf_inter_status_resp=response)

#ensure the object inputs are in the response.
found_interface_name = False
if response:
    if object_id in response.get(object_name):
        ret_service_policy_dict = response.get(object_name).get(object_id) # {"direction": "input","object_id": "GigabitEthernet2","status": "donw"}
        found_interface_name = True

if found_interface_name == False:
    MSA_API.task_error('Can not find the interface "'+object_id+'" on the device', context, True)
MSA_API.task_success('Good, the interface "'+object_id+'" exists on the device ', context, True)
