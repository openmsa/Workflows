import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('acl_name', var_type='String')
dev_var.add('acl.0.condition', var_type='String')
dev_var.add('acl.0.protocol', var_type='String')
dev_var.add('acl.0.src_address', var_type='String')
dev_var.add('acl.0.src_wildcard', var_type='String')
dev_var.add('acl.0.src_port', var_type='String')
dev_var.add('acl.0.dst_address', var_type='String')
dev_var.add('acl.0.dst_wildcard', var_type='String')
dev_var.add('acl.0.dst_port', var_type='String')
context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)

object_name = 'access_lists'

command = 'IMPORT'
params = dict()
params[object_name] = "0"
#synchronise the given device microservice
obmf.command_call(command, 0, params) # put 0 to not update the db

#get microservices instance by microservice object ID.
object_id = context.get('acl_name')
response = json.loads(obmf.content)
context.update(obmf_sync_resp=response)

#response={'entity': {'commandId': 0, 'status': 'OK', 'message': '{"access_lists":{"A":{"object_id":"A"},"IP-Adm-V4-Int-ACL-global":{"object_id":"IP-Adm-V4-Int-ACL-global","acl":{"10":{"index":"10","condition":"permit","protocol":"tcp","any_src":"any","src_address_host":"","src_address":"","src_wildcard":"","src_op":"","src_port":"","any_dst":"any","dst_address_host":"","dst_address":"","dst_wildcard":"","dst_op":"eq","dst_port":"www","opt":""},"20":{"index":"20","condition":"permit","protocol":"tcp","any_src":"any","src_address_host":"","src_address":"","src_wildcard":"","src_op":"","src_port":"","any_dst":"any","dst_address_host":"","dst_address":"","dst_wildcard":"","dst_op":"eq","dst_port":"443","opt":""}}},"acl-auto":{"object_id":"acl-auto","acl":{"10":{"index":"10","condition":"permit","protocol":"ip","any_src":"","src_address_host":"","src_address":"10.166.174.16","src_wildcard":"0.0.0.15","src_op":"","src_port":"","...
message = response.get('entity').get('message')

if message:
    #Convert message into array
    message = json.loads(message)
    if message.get(object_name) and object_id  in message.get(object_name):
      #if response equals empty dictionary it means class map object is not exist in the device yet.
      MSA_API.task_error('ACL with id="' + object_id + '" is already exists in the device.', context, True) 
MSA_API.task_success('ACL Map with id="' + object_id + '" does not exist in the device yet.', context, True)