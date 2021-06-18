import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('policy_map_name', var_type='String')
dev_var.add('policy.0.class_map', var_type='String')
dev_var.add('policy.0.cir_before', var_type='String')
dev_var.add('policy.0.cir_after', var_type='String')
dev_var.add('policy.0.bc_before', var_type='String')
dev_var.add('policy.0.bc_after', var_type='String')
dev_var.add('policy.0.be_before', var_type='String')
dev_var.add('policy.0.be_after', var_type='String')
dev_var.add('policy.0.conform_action', var_type='String')
dev_var.add('policy.0.exceed_action', var_type='String')
dev_var.add('policy.0.violate_action', var_type='String')
dev_var = Variables()

context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################
'''
Compare the policy-map configuration from device running-config to the input configuration parameters.

@param device_policy_dict: Dict
    Policy-map classes dictionary from the device running-config.
@param input_policy_dict: Dict
    Policy-map classes dictionary from the process input parameters.
@return: Boolean
    True or False if the Policy-map classes comparison matched or not.

'''
def is_policy_map_matched(device_policy_dict, input_policy_dict):
    #loop in the input policy dictionary parameter.
    #if isinstance(device_policy_dict, dict) and isinstance(input_policy_dict, dict): 
    for i_policy in input_policy_dict:
        input_class_map = i_policy.get('class_map')
        #loop in device (configuration) policy-map dictionary.
        for key, d_policy  in device_policy_dict.items():
            device_class_map = d_policy.get('class_map')
            if device_class_map == input_class_map and device_class_map != 'CM_DISCARD':
                return True

    return False           
####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################
#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)

object_name = 'policy_map'

command = 'IMPORT'
params = dict()
params[object_name] = "0"
#synchronise the given device microservice
obmf.command_call(command, 0, params) # put 0 to not update the db

#get microservices instance by microservice object ID.
object_id = context.get('policy_map_name')
response = json.loads(obmf.content)
context.update(obmf_sync_resp=response)
#ensure the object inputs are in the response.
is_p_map_matched = False
#ensure that all acl rules from context['acl'] dict are in response['acl']

#response={'entity': {'commandId': 0, 'status': 'OK', 'message': '{"policy_map":{"policy_auto":{"object_id":"policy_auto","policy":{"0":{"class_map":"TestAuto"},"1":{"class_map":"CM_DISCARD"}}},"CM_600104-6003G012":{"object_id":"CM_600104-6003G012","policy":{"0":{"class_map":"CM_DISCARD"}}},"CM_600104-6003G011":{"object_id":"CM_600104-6003G011"},"PM_600104":{"object_id":"PM_600104","policy":{"0":{"class_map":"CM_DISCARD"}}},"PM_600105":{"object_id":"PM_600105","policy":{"0":{"class_map":"CM_DISCARD"}}},"P":{"object_id":"P"},"MyTest":{"object_id":"MyTest","policy":{"0":{"class_map":"TestAuto"},"1":{"class_map":"CM_DISCARD"}}},"PM_QA":{"object_id":"PM_QA"},...

message = response.get('entity').get('message')

if message:
    #Convert message into array
    message = json.loads(message)
    if message.get(object_name) and object_id  in message.get(object_name):
        ret_policy_map_dict = message.get(object_name).get(object_id)
        if 'policy' in ret_policy_map_dict:
            device_policy_dict = ret_policy_map_dict.get('policy')
            context.update(main_device_policy_dict=device_policy_dict)
            input_policy_dict = context.get('policy')
            is_p_map_matched = is_policy_map_matched(device_policy_dict, input_policy_dict)

#if response equals empty dictionary it means class map object is not exist in the device yet.
if is_p_map_matched != False:
    MSA_API.task_error('Policy-map with id="' + object_id + ', one class at least exits in the device.', context, True)
MSA_API.task_success('Policy-map with id="' + object_id + '", no class exists in the device yet.', context, True)
