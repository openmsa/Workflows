'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''
import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

#excel files : 
#Flag	Interface name	Direction	Policy name
#ADD	Vlan3002      	input     PM_600104
#
#    "ServicePolicy": [ {
#            "": "",
#            "flag": "ADD",
#            "interface_name": "Vlan3002",
#            "direction": "input",
#            "policy_map": "PM_600104"
#        } ],
 

dev_var = Variables()
dev_var.add('service_policy.0.interface_name', var_type='String')
dev_var.add('service_policy.0.direction', var_type='String')
dev_var.add('service_policy.0.policy_map', var_type='String')

context = Variables.task_call(dev_var)


def is_order_op_success(response):
    # check if response if not empty
    if response:
        if 'wo_status' in response:
            #if status equals ENDED operation is success otherwise FAILED
            if response.get('wo_status') == constants.ENDED:
                return True  
    return False

#get device_id from context
device_id = context['device_id'][3:]

#Initiate Order object with the device_id
obmf = Order(device_id)

#Execute ADD method of StaticRouting Microservice to add route in the device
command = 'CREATE' # MS method corresponding on ADD Static route operation

service_policies = context.get('service_policy')

#build MS the dictionary input object 
config = dict(service_policies=service_policies)
  
obj = {"":config} #object = {'':{'object_id':'Service_pol', 'direction':'in', 'policy_map':'POLAAA-555'}}
#MS XML file name
#ms_xml_filename = 'service_policy'

params = dict(service_policy=obj)
context['ms_params'] = params

#Store service Policy action
context.update(service_policy_action='ADD_SERVICE_POLICY')

is_policy_map_matched = context.get('is_policy_map_matched')
if is_policy_map_matched == True:
    MSA_API.task_success('Skipped, Service Policy already exist.', context, True)


obmf.command_execute(command, params, timeout = 300) #execute the MS ADD static route operation
response = json.loads(obmf.content)

if response.get('wo_status') == constants.FAILED:
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
    MSA_API.task_error('Failure details: ' + detials, context, True)

#store OBMF command execution response in context
context['response'] = response.get('wo_newparams')

MSA_API.task_success('Add Service Policy operation is done successfully.', context, True)
