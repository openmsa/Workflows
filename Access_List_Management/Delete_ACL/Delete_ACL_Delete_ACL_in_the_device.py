import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('access_lists.0.acl_name', var_type='String')

context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]

#Initiate Order object with the device_id
obmf = Order(device_id)

#Execute DELETE method of StaticRouting Microservice to add route in the device
command = 'DELETE' # MS method corresponding on DELETE Static route operation

#build MS the dictionary input object
access_lists = context.get('access_lists')

config = dict(access_lists=access_lists)
obj = {"":config} #object = {'':{'object_id':'192.168.1.2', 'gateway':'192.168.1.254'}}
params = dict(access_lists=obj)
context['ms_params'] = params

obmf.command_execute(command, params, timeout = 300) #execute the MS ADD static route operation
response = json.loads(obmf.content)

if response.get('wo_status') == constants.FAILED:
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
    MSA_API.task_error('Failure details: ' + detials, context, True)

#store OBMF command execution response in context
context['response'] = response.get('wo_newparams')

MSA_API.task_success('Delete ACL operation is done successfully.', context, True)