'''
Guide used for developing this task script: https://msa2.ubiqube.com/msa_sdk/order.html#msa_sdk.order.Order.command_execute

'''
import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('class_map_list.0.class_map_name', var_type='String')
dev_var.add('class_map_list.0.method', var_type='String')
dev_var.add('class_map_list.0.acl_name', var_type='String')

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

class_map_list = context.get('class_map_list')

config = dict(class_map_list=class_map_list)
obj = {"":config} #object = {'':{'object_id':'192.168.1.2', 'gateway':'192.168.1.254'}}
params = dict(class_map=obj)
context['ms_params'] = params

obmf.command_execute(command, params, timeout = 300) #execute the MS ADD static route operation
response = json.loads(obmf.content)

if response.get('wo_status') == constants.FAILED:
    detials = ''
    if 'wo_newparams' in response:
        detials = response.get('wo_newparams')
    MSA_API.task_error('Failure details: ' + detials, context, True)
context['response'] = response.get('wo_newparams')

MSA_API.task_success('Add class map operation is done successfully.', context, True)