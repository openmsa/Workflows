import json
import time
import re
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('interface_name', var_type='String')
dev_var.add('direction', var_type='String')
dev_var.add('policy_name', var_type='String')
context = Variables.task_call(dev_var)

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
            ret = MSA_API.process_content(constants.FAILED, 'Push Configuration FAILED.', context, True)
            print(ret)
        elif status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)
    return response

'''
Check interface is in 'shutdown' status.

@param context: Dict
    Service Instance context (database).
@param ifce_name: String
    Device interface name.
@param ifce_status_pattern: String
    Regular expression pattern allows to confirme interface status is shotdown or not.
@return: Boolean
    True or False to confirme interface status is shotdown or not.

'''
def is_interface_shutdown(context, device, ifce_name, ifce_status_pattern):
    is_shutdown = False
    if ifce_name:
        #push configuration to device.
        data = dict(configuration="do show run interface " + ifce_name)

        device.push_configuration(json.dumps(data))
        response = json.loads(device.content)

        #get asynchronous push config status
        context.update(device_push_conf_ret=response)
        response = self_device_push_conf_status_ret(device, 300)

        #the status should be down
        status = response.get('status')
        context.update(device_push_conf_end_reponse=response)
        if status == constants.FAILED:
            ret = MSA_API.process_content(constants.FAILED, 'No push config response.', context, True)
            print(ret)

        return_message = response.get('message')

        if return_message != None:
            matchObj = return_message.find(ifce_status_pattern)
            if matchObj != -1:
                is_shutdown = True
    return is_shutdown

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#get device_id from context
device_ref = context['device_id']
device_id = context['device_id'][3:]

#initiate Device object
device = Device(device_id=device_id)

#get interface name
interface_name = context.get('interface_name')

return_message = ''

#check interface status from the device running-configuration.
ifce_status_pattern = 'shutdown'
is_status_shutdown = is_interface_shutdown(context, device, interface_name, ifce_status_pattern)

#Store interface status in the context to used it later
context.update(interface_is_status_down=is_status_shutdown)

if is_status_shutdown == True:
    ret = MSA_API.process_content(constants.ENDED, 'The interface status is "SHUTDOWN" for "' + interface_name + '" on the device.', context, True)
    print(ret)

ret = MSA_API.process_content(constants.ENDED, 'The interface status is "NOT SHUTDOWN" for "' + interface_name + '" on the device.', context, True)
print(ret)
