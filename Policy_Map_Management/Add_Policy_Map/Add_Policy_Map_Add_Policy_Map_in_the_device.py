'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''
import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('policy_map_list.0.policy_map_name', var_type='String')
dev_var.add('policy_map_list.0.policy.0.class_map', var_type='String')
dev_var.add('policy_map_list.0.policy.0.cir_before', var_type='String')
dev_var.add('policy_map_list.0.policy.0.cir_after', var_type='String')
dev_var.add('policy_map_list.0.policy.0.bc_before', var_type='String')
dev_var.add('policy_map_list.0.policy.0.bc_after', var_type='String')
dev_var.add('policy_map_list.0.policy.0.be_before', var_type='String')
dev_var.add('policy_map_list.0.policy.0.be_after', var_type='String')
dev_var.add('policy_map_list.0.policy.0.conform_action', var_type='String')
dev_var.add('policy_map_list.0.policy.0.exceed_action', var_type='String')
dev_var.add('policy_map_list.0.policy.0.violate_action', var_type='String')

context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]

#Initiate Order object with the device_id
obmf = Order(device_id)

command = 'CREATE'


policy_map_list = context.get('policy_map_list')

config = dict(policy_map_list=policy_map_list)
obj = {"":config}

params = dict(policy_map=obj)
context['ms_params'] = params

obmf.command_execute(command, params, timeout = 300) #execute the MS ADD static route operation
response = json.loads(obmf.content)

if response.get('wo_status') == constants.FAILED:
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
        MSA_API.task_error('Failure details: ' + detials, context, True)

context['response'] = response.get('wo_newparams')

MSA_API.task_success('Add policy map operation is done successfully.', context, True)


