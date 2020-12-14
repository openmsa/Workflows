import json
import time
import re
from msa_sdk import constants
from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from Check_Qos_Is_Not_Apply_To_Device import *

dev_var = Variables()
context = Variables.task_call(dev_var)
input_policy_name = context.get('policy_name')

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
device = Device(device_id=device_id)

#extract vlan_id from interface_name
vlan_id = extract_vlan_id_from_interface_name(context)
context.update(vlan_id=vlan_id)

#check QoS cancellation if vlan_id exits
qos_application_pattern = r'\[In\] Policy map is ' + input_policy_name
matchObj = is_qos_applied_or_not_to_device_vlan_iface(context, vlan_id, qos_application_pattern)

return_message = ''
if 'device_push_conf_end_reponse' in context:
    return_message = context.get('device_push_conf_end_reponse').get('message')

if vlan_id:
    if matchObj != False:
        ret = MSA_API.process_content(constants.ENDED, 'OK Qos applied for vlan : '+vlan_id+' : '+return_message, context, True)
        print(ret)
    else:
        ret = MSA_API.process_content(constants.FAILED, 'NOK, Qos Policy map '+input_policy_name+' not found : '+return_message, context, True)
        print(ret)

ret = MSA_API.process_content(constants.ENDED, 'SKIPPED, VLAN-ID is missing from interface_name input: '+input_policy_name, context, True)
print(ret)

