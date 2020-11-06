'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''

from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('object_id', var_type='String')
dev_var.add('class_map', var_type='String')
dev_var.add('cir', var_type='String')
dev_var.add('bc', var_type='String')
dev_var.add('be', var_type='String')
dev_var.add('conform', var_type='String')
dev_var.add('exceed', var_type='String')
dev_var.add('violate', var_type='String')

context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]

#Initiate Order object with the device_id
obmf = Order(device_id)

command = 'DELETE'

policy_map_name = context['object_id']
class_name = context['class_map']
cir_after = context['cir']
bc_after = context['bc']
be_after = context['be']
conform_action = context['conform']
exceed_action = context['exceed']
violate_action = context['violate']

object_id = policy_map_name
config = dict(object_id=policy_map_name, class_map=class_name, cir=cir_after, bc=bc_after, be=be_after, conform=conform_action, exceed=exceed_action, violate=violate_action)
obj = dict(object_id=config)
params = dict(policy_map=obj)
params = dict(policy_map=obj)

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
