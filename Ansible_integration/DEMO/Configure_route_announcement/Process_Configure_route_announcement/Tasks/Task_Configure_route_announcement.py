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
 - Configure server subnet announcment via OSPF


"""

#New Variables object
TaskVariables = Variables()


#Add vars to context
context = Variables.task_call(TaskVariables)

#Import microservice alias list
with open('/opt/fmc_repository/Process/Ansible_integration/DEMO/Get_router_interface/microservice_list.json', 'r') as alias_file:
  	context['ms_aliases'] = json.load(alias_file)

#Udate exchange file
with open(context['exchange_file'], 'r') as exchange_file:
    exchange_dict = json.load(exchange_file)

process_id                   = context['SERVICEINSTANCEID']
subnet						 = exchange_dict['site_prefix']
site_ip_plan			 	 = exchange_dict['site_ip_plan']
site_prefix					 = exchange_dict['site_prefix']
ms_router_ospf_config		 = context['ms_aliases']['Router OSPF configuration']
ms_router_interface		     = context['ms_aliases']['Router Interface']


#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])


#Create site router Order object
RouterOrderObject = Order(exchange_dict['router_device_id'])
RouterOrderObject.command_synchronize(300)

objects_list = RouterOrderObject.command_objects_instances(ms_router_ospf_config)
ospf_process_object = RouterOrderObject.command_objects_instances_by_id(ms_router_ospf_config, objects_list[0])[ms_router_ospf_config][objects_list[0]]

#Add new network to announce
ospf_process_object_interfaces = list(ospf_process_object['interface'].keys())
for index, value in enumerate(ospf_process_object_interfaces):
  ospf_process_object_interfaces[index] = int(value)

new_index = str(sorted(ospf_process_object_interfaces)[-1]+1)
NetObject = ipaddress.ip_network(site_prefix)
ospf_process_object['interface'][new_index] = {'area': '0',
                                               'network_address': str(NetObject.network_address),
                                               'network_mask': str(NetObject.hostmask)
                                              }

#Configure OSPF
ms_dict = {ms_router_ospf_config: {ospf_process_object['object_id']: ospf_process_object}}
RouterOrderObject.command_execute('UPDATE', ms_dict)


result = MSA_API.process_content('ENDED', 'Route has been announced', context, True)
print(result)

