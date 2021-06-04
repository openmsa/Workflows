'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''
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

#Initiate Order object with the device_id
obmf = Order(device_id)


#Execute ADD method of StaticRouting Microservice to add route in the device
command = 'DELETE' # MS method corresponding on ADD Static route operation

#Store service Policy action
context.update(service_policy_action='DELETE_SERVICE_POLICY')

interface_name = context['interface_name'] #MS input variable value
direction = context['direction'] #MS input variable value
policy_name = context['policy_name'] #MS input variable value

is_policy_name_matched=context['is_policy_name_matched']
if is_policy_name_matched == False:
    ret = MSA_API.process_content(constants.ENDED, 'Skipped, the service Policy  "' +   policy_name + '" does not exists in the device.', context, True)
    print(ret)

#build MS the dictionary input object 
object_id=interface_name
config = dict(object_id=interface_name, direction=direction, policy_map=policy_name)
  
obj = {object_id:config} #object = {'':{'object_id':'Service_pol', 'direction':'in', 'policy_name':'POLAAA-555'}}
#MS XML file name
#ms_xml_filename = 'service_policy'

params = dict(service_policy=obj)
context['ms_params'] = params

is_policy_name_matched = context.get('is_policy_name_matched')
if is_policy_name_matched == False:
    ret = MSA_API.process_content(constants.ENDED, 'Skipped , policy name was not found', context, True)
    print(ret)


obmf.command_execute(command, params, timeout = 300) #execute the MS ADD static route operation
response = json.loads(obmf.content)

if response.get('wo_status') == constants.FAILED:
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
    ret = MSA_API.process_content(constants.FAILED, 'Failure details: ' + detials, context, True)
    print(ret)

#store OBMF command execution response in context
context['response'] = response.get('wo_newparams')

ret = MSA_API.process_content(constants.ENDED, 'Delete Service Policy  operation is done successfully.', context, True)
print(ret)