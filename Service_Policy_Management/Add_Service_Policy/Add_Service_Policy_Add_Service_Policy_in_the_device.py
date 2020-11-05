'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''

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
#            "policy_name": "PM_600104"
#        } ],
 

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
command = 'CREATE' # MS method corresponding on ADD Static route operation

object_id = context['interface_name'] #MS input variable value
direction = context['direction'] #MS input variable value
policy_name = context['policy_name'] #MS input variable value

#build MS the dictionary input object 
config = dict(object_id=object_id, direction=direction, policy_name=policy_name)
  
obj = {"":config} #object = {'':{'object_id':'Service_pol', 'direction':'in', 'policy_name':'POLAAA-555'}}
#MS XML file name
ms_xml_filename = 'service_policy'
params = dict(service_policy=obj)
context['ms_params'] = params

response = obmf.command_execute(command, params, timeout=60) #execute the MS ADD static route operation

if response.get('wo_status') == 'FAIL':
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
    ret = MSA_API.process_content('FAILED', 'Failure details: ' + detials, context, True)
    print(ret)

#store OBMF command execution response in context
context['response'] = response.get('wo_newparams')

ret = MSA_API.process_content('ENDED', 'Add Service Policy operation is done successfully.', context, True)
print(ret)