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
context = Variables.task_call(TaskVariables)

#Import microservice alias list
with open('/opt/fmc_repository/Process/Ansible_integration/microservice_list.json', 'r') as alias_file:
  	context['ms_aliases'] = json.load(alias_file)

#Udate exchange file
with open(context['exchange_file'], 'r') as exchange_file:
    exchange_dict = json.load(exchange_file)
    
process_id = context['SERVICEINSTANCEID']
ms_router_lldp = context['ms_aliases']['Router LLDP neighbour details']    


#Wait when LLDP neighbours become available
time.sleep(30)
#Create site router Order object
RouterOrderObject = Order(exchange_dict['router_device_id'])
RouterOrderObject.command_synchronize(300)
time.sleep(3)
RouterOrderObject.command_synchronize(300)


#Find a router interface where a site server is connected to
objects_list = RouterOrderObject.command_objects_instances(ms_router_lldp)
util.log_to_process_file(process_id, objects_list)
counter = 0
router_interface = None
while router_interface is None and counter < len(objects_list):
    neighbour_object = RouterOrderObject.command_objects_instances_by_id(ms_router_lldp, objects_list[counter])[ms_router_lldp][objects_list[counter]]
    util.log_to_process_file(process_id, '{} {}'.format(neighbour_object['system_name'], exchange_dict['site']))
    if re.search(exchange_dict['site'].lower(), neighbour_object['system_name'].lower()):
      router_interface = neighbour_object['local_interface']
    counter += 1

#Find servers what should be configured to
objects_list = RouterOrderObject.command_objects_instances(ms_router_lldp)
server_list = list()
for neighbour in objects_list:
  neighbour_object = RouterOrderObject.command_objects_instances_by_id(ms_router_lldp, neighbour)[ms_router_lldp][neighbour]
  if re.search(exchange_dict['site'].lower(), neighbour_object['system_name'].lower()) and neighbour_object['local_interface'] == router_interface:
    server_list.append((neighbour_object['system_name'],neighbour_object['port_name']))

context['router_interface'] = router_interface
context['server_list'] = server_list
context['exchange_dict'] = exchange_dict

#Finish the task correctlly
if router_interface:
	result = MSA_API.process_content('ENDED', 'Router interface has been identified correctly', context, True)
else:
    result = MSA_API.process_content('FAIL', 'No router interface where servers are connected to', context, True)
print(result)
