from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from datetime import datetime
from msa_sdk import constants
from msa_sdk import lookup
from msa_sdk import util
import ipaddress
import time
import re
import json
import sys
import os

"""
The proposals of the task are:


"""


#New Variables object
TaskVariables = Variables()

#Add vars to context
context = Variables.task_call(TaskVariables)

ms_auth_fail = 'auth_failure'

fail_ip_dict = dict()
for device_id in context['server_list']:
  CurrentDeviceOrderObject = Order(device_id)
  CurrentDeviceOrderObject.command_synchronize(300)
  objects_list = CurrentDeviceOrderObject.command_objects_instances(ms_auth_fail)
  for fail_event in objects_list:
    fail_object = CurrentDeviceOrderObject.command_objects_instances_by_id(ms_auth_fail, 
                                                                           fail_event)[ms_auth_fail][fail_event]
    if fail_object['rhost'] not in fail_ip_dict.keys():
      fail_ip_dict[fail_object['rhost']] = 0
      
    fail_ip_dict[fail_object['rhost']] += 1

context['block_ip_list'] = list()
#Prepare blocking list
for ip, number in fail_ip_dict.items():
  if number > 5:
    context['block_ip_list'].append(ip)

#Finish the task correctlly
result = MSA_API.process_content('ENDED', 'Auth fail events have been analysed', context, True)
print(result)
