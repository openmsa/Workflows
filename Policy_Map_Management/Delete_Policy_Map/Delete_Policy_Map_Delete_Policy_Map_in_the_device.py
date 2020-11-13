'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''

from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('policy_map_name', var_type='String')

context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]

#Initiate Order object with the device_id
obmf = Order(device_id)

command = 'DELETE'

object_id = context.get('policy_map_name')

config = dict(object_id=object_id)
obj = {"":config}

prams = dict(policy_map=obj)
context['ms_params'] = params

response = obmf.command_execute(command, params, timeout=60) #execute the MS ADD static route operation

if response.get('wo_status') == 'FAIL':
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
        ret = MSA_API.process_content('FAILED', 'Failure details: ' + detials, context, True)
        print(ret)

context['response'] = response.get('wo_newparams')

ret = MSA_API.process_content('ENDED', 'Delete policy map operation is done successfully.', context, True)
print(ret)

