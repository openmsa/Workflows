import json
import time
import re
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('service_policy.0.interface_name', var_type='String')
dev_var.add('service_policy.0.direction', var_type='String')
dev_var.add('service_policy.0.policy_map', var_type='String')
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
            MSA_API.task_error('Push Configuration FAILED.', context, True)
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
            MSA_API.task_error('No push config response.', context, True)

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

 
service_policy = context['service_policy']
bad_values = dict()
good_values = dict()

if service_policy:
  for rule in service_policy:
    interface_name =  str(rule.get('interface_name'))
    if good_values.get(interface_name) == None and bad_values.get(interface_name) == None :
      #don't need to check twice the same interface
      return_message = ''
      #check interface status from the device running-configuration.
      ifce_status_pattern = 'shutdown'
      #We can optimise the WF if we get the status for all insterfaces with one cli command
      is_status_shutdown = is_interface_shutdown(context, device, interface_name, ifce_status_pattern)

      #Store interface status in the context to used it later
      if (context.get('interfaces_is_status_down') == None):
        interfaces_is_status_down = dict()
      else:
        interfaces_is_status_down = context["interfaces_is_status_down"]
      interfaces_is_status_down[interface_name] = is_status_shutdown
      context.update(interfaces_is_status_down=interfaces_is_status_down)
      if is_status_shutdown == True:
        good_values[interface_name]= 1
      else:
        bad_values[interface_name]= 1


if (len(good_values)):
  good_values_string =  ", ".join(good_values.keys())
else: 
  good_values_string =  ""
good_values_string =  ", ".join(good_values.keys())

if (len(bad_values)):
  bad_values_string =  ", ".join(bad_values.keys())
  if (len(bad_values)):
    MSA_API.task_success('The interfaces ('+bad_values_string+') are "NOT SHUTDOWN" on the device, but interfaces ('+good_values_string+') are "SHUTDOWN"', context, True)
  else:
    MSA_API.task_success('The interfaces ('+ bad_values_string +') are "NOT SHUTDOWN" on the device', context, True)
else: 
  MSA_API.task_success('Good, Interfaces ('+good_values_string+') are all "SHUTDOWN" on the device ', context, True)

