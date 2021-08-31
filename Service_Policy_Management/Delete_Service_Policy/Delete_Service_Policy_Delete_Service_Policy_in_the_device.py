'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''
import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('service_policy.0.interface_name', var_type='String')
dev_var.add('service_policy.0.direction', var_type='String')
dev_var.add('service_policy.0.policy_name', var_type='String')

context = Variables.task_call(dev_var)


#get device_id from context
device_id = context['device_id'][3:]

#Initiate Order object with the device_id
obmf = Order(device_id)


#Execute ADD method of StaticRouting Microservice to add route in the device
command = 'DELETE' # MS method corresponding on ADD Static route operation

#Store service Policy action
context.update(service_policy_action='DELETE_SERVICE_POLICY')

service_policies = context.get('service_policy')

#build MS the dictionary input object 
config = dict(service_policies=service_policies)
config['object_id']= "object_id"   #add mandatory field object_id, put only one default value

obj = {"":config} #object = {'':{'object_id':'Service_pol', 'direction':'in', 'policy_name':'POLAAA-555'}}
#MS XML file name
#ms_xml_filename = 'service_policy'

params = dict(service_policy=obj)
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

MSA_API.task_success('Delete Service Policy  operation is done successfully.', context, True)
