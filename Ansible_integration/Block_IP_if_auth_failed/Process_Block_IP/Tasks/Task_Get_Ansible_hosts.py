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

#Add new variables
TaskVariables.add('ansible_device_id', var_type = 'Device')
TaskVariables.add('ansible_microservice', var_type = 'String')

#Add vars to context
context = Variables.task_call(TaskVariables)
context['ansible_device_id'] = re.match('^\D*?(\d+?)$', context['ansible_device_id']).group(1)
context['ansible_microservice'] = 'ANSIBLE_MS__based_on_grenoble_server_firewall_'

ms_ansible_host = 'Read_hosts_file'
                  
#Create site router Order object
AnsibleOrderObject = Order(context['ansible_device_id'])
AnsibleOrderObject.command_synchronize(300)

server_list = list()
#Find device ID value
MsaLookup = lookup.Lookup()
MsaLookup.look_list_device_ids()
devices = json.loads(MsaLookup.content)

objects_list = AnsibleOrderObject.command_objects_instances(ms_ansible_host)
for ansible_group in objects_list:
    ansible_group_object = AnsibleOrderObject.command_objects_instances_by_id(ms_ansible_host, 
                                                                    ansible_group)[ms_ansible_host][ansible_group]
    for device in devices:
        if re.search(ansible_group_object['object_id'], device['name']):
            server_list.append(device['id'])
context['server_list'] = server_list

#Finish the task correctlly
result = MSA_API.process_content('ENDED', 'All variables have been defined successfully', context, True)
print(result)
