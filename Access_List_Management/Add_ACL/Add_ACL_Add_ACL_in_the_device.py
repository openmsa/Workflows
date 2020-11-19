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

#Initiate Order object with the device_id
obmf = Order(device_id)

#Execute ADD method of StaticRouting Microservice to add route in the device
command = 'CREATE' # MS method corresponding on ADD Static route operation

#acl name as object_id
object_id = context.get('acl_name')
#acl entry list
acl_list = context.get('acl')
#build MS the dictionary input object 
config = dict(object_id=object_id, acl=acl_list)
obj = {"":config} #object = {'':{'object_id':'192.168.1.2', 'gateway':'192.168.1.254'}}
params = dict(access_lists=obj)

context['ns_params_create'] = params

response = obmf.command_execute(command, params, timeout=60) #execute the MS ADD static route operation

if response.get('wo_status') == constants.FAILED:
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
    ret = MSA_API.process_content(constants.FAILED, 'Failure details: ' + detials, context, True)
    print(ret)

#store OBMF command execution response in context
context['response'] = response.get('wo_newparams')

ret = MSA_API.process_content(constants.ENDED, 'Add ACL operation is done successfully.', context, True)
print(ret)