import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('object_id', var_type='String')
dev_var.add('method', var_type='String')
dev_var.add('acl', var_type='String')
context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)
#synchronise device microservices
timeout = 300
obmf.command_synchronize(timeout)

#get microservices instance by microservice object ID.
object_name = 'class_map'
object_id = context.get('object_id')
obmf.command_objects_instances_by_id(object_name, object_id)
response = json.loads(obmf.content)
context.update(obmf_sync_resp=response)
#if response equals empty dictionary it means class map object is not exist in the device yet.
if response:
    ret = MSA_API.process_content(constants.FAILED, 'Class Map with id="' + object_id + '" is already exists in the device.', context, True)
    print(ret)
ret = MSA_API.process_content(constants.ENDED, 'Class Map with id="' + object_id + '" does not exist in the device.', context, True)
print(ret)
