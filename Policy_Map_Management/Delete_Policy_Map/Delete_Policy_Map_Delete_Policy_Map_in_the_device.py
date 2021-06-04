'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''
import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('policy_map_name', var_type='String')
dev_var.add('policy.0.class_map', var_type='String')

context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]

#Initiate Order object with the device_id
obmf = Order(device_id)

command = 'DELETE'

object_id = context.get('policy_map_name')
policy_list = context.get('policy')

config = dict(object_id=object_id, policy=policy_list)
obj = {"":config}

params = dict(policy_map=obj)
context['delete_ms_params'] = params

obmf.command_execute(command, params, timeout = 300) #execute the MS ADD static route operation
response = json.loads(obmf.content)

if response.get('wo_status') == constants.FAILED:
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
        ret = MSA_API.process_content(constants.FAILED, 'Failure details: ' + detials, context, True)
        print(ret)

context['response'] = response.get('wo_newparams')

ret = MSA_API.process_content(constants.ENDED, 'Delete policy map operation is done successfully.', context, True)
print(ret)

