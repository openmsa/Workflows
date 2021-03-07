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
TaskVariables.add('ipam_device_id', var_type = 'Device')
TaskVariables.add('ansible_device_id', var_type = 'Device')
TaskVariables.add('dns_server_device_id', var_type = 'Device')
TaskVariables.add('ansible_rollback_ms', var_type = 'String')
TaskVariables.add('exchange_file', var_type = 'String')

#Add vars to context
context = Variables.task_call(TaskVariables)
context['ipam_device_id'] = re.match('^\D+?(\d+?)$', context['ipam_device_id']).group(1)
context['ansible_device_id'] = re.match('^\D+?(\d+?)$', context['ansible_device_id']).group(1)
context['dns_server_device_id'] = re.match('^\D+?(\d+?)$', context['dns_server_device_id']).group(1)

#Udate exchange file
with open(context['exchange_file'], 'r') as exchange_file:
    exchange_dict = json.load(exchange_file)

#Import microservice alias list
with open('/opt/fmc_repository/Process/Ansible_integration/microservice_list.json', 'r') as alias_file:
  	context['ms_aliases'] = json.load(alias_file)

process_id               = context['SERVICEINSTANCEID']
ipam_device_id 			 = context['ipam_device_id']
ms_ipam_tenant           = context['ms_aliases']['IPAM Tenants']
ms_ipam_site             = context['ms_aliases']['IPAM Sites']
ms_ipam_device           = context['ms_aliases']['IPAM Devices']
ms_interface_connection  = context['ms_aliases']['IPAM Interface Connections']
ms_ipam_prefix           = context['ms_aliases']['IPAM IPv4 prefixes']
ms_ipam_avaliable_prefix = context['ms_aliases']['IPAM Available Prefixes']
ms_ipam_address          = context['ms_aliases']['IPAM IPv4 addresses']
ms_ipam_interface        = context['ms_aliases']['IPAM Interfaces']

#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

#Create IPAM order object
IpamOrderObject = Order(ipam_device_id)
IpamOrderObject.command_synchronize(300)

#A list of IP address what should be removed from IPAM
ip_address_list = list()
for host, host_detial in exchange_dict['site_ip_plan'].items():
  ip_address_list.append(host_detial['ip_address'])

objects_list = IpamOrderObject.command_objects_instances(ms_ipam_address)
counter = 0
while ip_address_list and (counter < len(objects_list)):
  object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_address, 
                                                           objects_list[counter])[ms_ipam_address][objects_list[counter]]
  if 'tenant' in list(object.keys()):
    if object['tenant'] == exchange_dict['tenant'] and object['object_id'] in ip_address_list:
      ms_dict = {ms_ipam_address: {object['object_id']: dict()}}
      IpamOrderObject.command_execute('DELETE', ms_dict)
      ip_address_list.remove(object['object_id'])
  counter += 1
  
    
#Clean up prefix
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_prefix)
counter = 0
is_removed = False
while not is_removed and (counter < len(objects_list)):
  object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_prefix, 
                                                           objects_list[counter])[ms_ipam_prefix][objects_list[counter]]
  if 'tenant' in list(object.keys()):
    if object['tenant'] == exchange_dict['tenant'] and exchange_dict['site_prefix'] == object['object_id']:
      ms_dict = {ms_ipam_prefix: {object['object_id']: dict()}}
      IpamOrderObject.command_execute('DELETE', ms_dict)
      is_removed = True
  counter += 1

result = MSA_API.process_content('ENDED', 'IPAM has been updated', context, True)
print(result)

