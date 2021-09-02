import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from builtins import isinstance

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
    All given class map should be present on the device

'''
def is_policy_map_matched(policy_map, device_policy_dict, input_policy_dict):
    #loop in the input policy dictionary parameter.
    #"input_policy_dict": "[{'bc_after': 5000000, 'bc_before': '', 'be_after': 5000000, 'be_before': '', 'cir_after': 20000000, 'cir_before': '', 'class_map': 'CM_600104-6003G011', 'conform_action': 'set-prec-transmit 5', 'exceed_action': 'drop', 'violate_action': 'drop'}, {'bc_after': 8000, 'bc_before': '', 'be_after': 8000, 'be_before': '', 'cir_after': 32000, 'cir_before': '', 'class_map': 'CM_600104-6003G012', 'conform_action': 'drop', 'exceed_action': 'drop', 'violate_action': 'drop'}]",
    #"device_policy_dict": "{'0': {'class_map': 'CM_600104-6003G011'}, '1': {'class_map': 'CM_600104-6003G012'}, '2': {'class_map': 'CM_DISCARD'}}"

    # We should check what all given class map in excel file (cf input_policy_dict) are present on the device (in device_policy_dict)
    class_map_found_on_device = []
    class_map_not_found_on_device = []
    if not input_policy_dict:
       return True,'For policy "' + policy_map + '", no class map to check'
    if isinstance(device_policy_dict, dict) and isinstance(input_policy_dict, list): 
        for i_policy in input_policy_dict:
            found_class_map_in_device = False
            input_class_map = i_policy.get('class_map')
            #loop in device (configuration) policy-map dictionary.
            for key, d_policy  in device_policy_dict.items():
                device_class_map = d_policy.get('class_map')
                if device_class_map == input_class_map and device_class_map != "CM_DISCARD":
                   found_class_map_in_device = True
            if found_class_map_in_device == False:
                #Can not find the class map input_class_map on the device
                class_map_not_found_on_device.append(input_class_map)
            else:
               class_map_found_on_device.append(input_class_map)

     
    if class_map_not_found_on_device:
       #some class map are missing on the device:
       return False,'The class map "' + ", ".join(class_map_not_found_on_device) + '" are not attached on policy "' + policy_map + '" on the device'
    else:
       return True,'For policy "' + policy_map + '",  class maps "' + ", ".join(class_map_not_found_on_device) + '" are present on the device'


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
#Import the given device microservice from the device, the MS values in the UI will be not updated
obmf.command_call(command, 0, params)
 
policy_map_list = context['policy_map_list']
good_values = dict()

if policy_map_list:
  for rule in policy_map_list:
    object_id   = str(rule.get('policy_map_name'))
    policies    = rule.get('policy')
    response = json.loads(obmf.content)
    context.update(obmf_sync_resp=response)
    #ensure the object inputs are in the response.
    is_p_map_matched = False
    check_return = 'No class map associated on the device to policy "' + object_id +'"'
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
                input_policy_dict  = policies
                is_p_map_matched, check_return   = is_policy_map_matched(object_id, device_policy_dict, input_policy_dict)
            
    context.update(is_p_map_matched=is_p_map_matched)
    #if response equals empty dictionary it means class map object is not exist in the device yet.
    if is_p_map_matched == False:
        MSA_API.task_error(check_return, context, True)
    good_values[object_id]= 1                        


if (len(good_values)):
  good_values_string =  ", ".join(good_values.keys())
else: 
  good_values_string =  ""

MSA_API.task_success('Good, Policy-map with ids('+good_values_string+') are attached to all given class map in the device.', context, True)
