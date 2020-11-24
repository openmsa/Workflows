'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''
import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('object_id', var_type='String')
dev_var.add('method', var_type='String')
dev_var.add('acl', var_type='String')

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

command = 'CREATE'

class_map_name = context['object_id'] #MS input variable value
method = context['method'] #MS input variable value
acl_name = context['acl'] #MS input variable value

config = dict(object_id=class_map_name, method=method, acl=acl_name)
obj = {"":config} #object = {'':{'object_id':'192.168.1.2', 'gateway':'192.168.1.254'}}
params = dict(class_map=obj)
context['ms_params'] = params

obmf.command_execute(command, params, timeout=60) #execute the MS ADD static route operation
response = json.loads(obmf.content)

if response.get('wo_status') == constants.FAILED:
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
    ret = MSA_API.process_content(constants.FAILED, 'Failure details: ' + detials, context, True)
    print(ret)

context['response'] = response.get('wo_newparams')

ret = MSA_API.process_content(constants.ENDED, 'Add class map operation is done successfully.', context, True)
print(ret)
