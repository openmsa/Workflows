import json
import time
import re
from msa_sdk import constants
from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
#from Check_Qos_Is_Not_Apply_To_Device import *

dev_var = Variables()
context = Variables.task_call(dev_var)
input_policy_name = context.get('policy_name')

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################

def self_device_push_conf_status_ret(device, timeout = 300, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #check push config status.
        device.push_configuration_status()
        response = json.loads(device.content)
        context.update(device_push_conf_status_ret=response)
        status = response.get('status')
        if status == constants.FAILED:
            MSA_API.task_error('Push Configuration FAILED.', context, True)
        elif status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)
    return response

'''
Extract VLAN ID from interface name input variable of the service instance process.

@param context: Dict
    Service Instance context (database).
@return: String
    VLAN ID if it exitsor empty.
'''
def extract_vlan_id_from_interface_name(context):
    vlan_id = ''
    if 'interface_name' in context:
        interface_name = context.get('interface_name')
        vlan_id_parsing = re.search('vlan(\d+)', interface_name, re.IGNORECASE)
        if vlan_id_parsing:
            vlan_id = vlan_id_parsing.group(1)
    return vlan_id

'''
Check QoS application or cancellation to/from device interface VLAN.

@param context: Dict
    Service Instance context (database).
@param vlan_id: String
    Device interface VLAN ID.
@param qos_pattern: String
    Regular expression pattern allows to confirme QoS application or cancellation.
@return: Boolean
    True or False to confirm QoS application or cancellation.

'''
def is_qos_applied_or_not_to_device_vlan_iface(context, vlan_id, qos_pattern, status_timout=300):
    is_qos = False
    if vlan_id:
        #push configuration to device.
        data = dict(configuration="do show platform qos ip vlan "+vlan_id)

        device.push_configuration(json.dumps(data))
        response = json.loads(device.content)

        #get asynchronous push config status
        context.update(device_push_conf_ret=response)
        response = self_device_push_conf_status_ret(device, status_timout)

        #the status should be down
        status = response.get('status')
        context.update(device_push_conf_end_reponse=response)
        if status == constants.FAILED:
            MSA_API.task_error('No push config response.', context, True)

        return_message = response.get('message')

        matchObj = return_message.find(qos_pattern)
        context.update(matchObj_DEBUG=matchObj)
        if matchObj != -1:
            is_qos = True
    return is_qos

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
qos_application_pattern = '[In] Policy map is ' + input_policy_name
matchObj = is_qos_applied_or_not_to_device_vlan_iface(context, vlan_id, qos_application_pattern)

return_message = ''
if 'device_push_conf_end_reponse' in context:
    return_message = context.get('device_push_conf_end_reponse').get('message')

interface_is_status_down = context.get('interface_is_status_down')

if vlan_id:
    if matchObj != False:
        ret = MSA_API.process_content(constants.ENDED, 'OK Qos [In] applied for vlan : '+vlan_id+' : '+return_message, context, True)
        print(ret)
    else:
        if interface_is_status_down == True:
            #Check 'Interface Vlan-IF Number is disabled'
            matchObj = return_message.find('Interface Vlan-IF Number is disabled')
            if matchObj == -1:
                #condition: "Interface is shutdown AND "Interface Vlan-IF Number is disabled" is displayed
                MSA_API.task_success('NOK, Interface Down and "Interface Vlan-IF Number is disabled" is displayed: '+return_message, context, True)
            else:
                #Failure condition: "Interface is shutdown AND "Interface Vlan-IF Number is disabled" is NOT displayed
                MSA_API.task_error('NOK, Interface Down and "Interface Vlan-IF Number is disabled" is not displayed: '+return_message, context, True)
        else:
            MSA_API.task_error('NOK because Interface Up, but Qos [In] Policy map '+input_policy_name+' not found : '+return_message, context, True)

MSA_API.task_success('SKIPPED, VLAN-ID is missing from interface_name input: '+input_policy_name, context, True)

