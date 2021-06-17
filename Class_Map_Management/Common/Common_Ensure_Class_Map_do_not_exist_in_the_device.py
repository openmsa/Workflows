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

object_name = 'class_map'

command = 'IMPORT'
params = dict()
params[object_name] = "0"
#synchronise the given device microservice
obmf.command_call(command, 0, params) # put 0 to not update the db

#get microservices instance by microservice object ID.
object_id = context.get('object_id')
response = json.loads(obmf.content)
context.update(obmf_sync_resp=response)

#response={'entity': {'commandId': 0, 'status': 'OK', 'message': '{"class_map":{"TestAuto":{"method":"match-all","object_id":"TestAuto","access":{"0":{"acl":"acl-auto"}}},"CM_DISCARD":{"method":"match-all","object_id":"CM_DISCARD"},"class-default":{"method":"match-any","object_id":"class-default"}}}'}, 'variant': {'language': None, 'mediaType': {'type': 'application', 'subtype': 'json', 'parameters': {}, 'wildcardType': False, 'wildcardSubtype': False}, 'encoding': None, 'languageString': None}, 'annotations': [], 'mediaType': {'type': 'application', 'subtype': 'json', 'parameters': {}, 'wildcardType': False, 'wildcardSubtype': False}, 'language': None, 'encoding': None}

message = response.get('entity').get('message')

if message:
    #Convert message into array
    message = json.loads(message)
    if object_id in message.get(object_name):
      #if response equals empty dictionary it means class map object is not exist in the device yet.
      MSA_API.task_error( 'Class Map with id="' + object_id + '" is already exists in the device.', context, True)
MSA_API.task_success('Class Map with id="' + object_id + '" does not exist in the device.', context, True)
