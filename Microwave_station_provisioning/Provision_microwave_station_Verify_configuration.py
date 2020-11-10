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
 - Verify VLAN configuration
 - Verify trunk configuration
 - Verify QoS configuration (TBD)

"""


#New Variables object
TaskVariables = Variables()

#Add vars to context
context = Variables.task_call(TaskVariables)

process_id = context['SERVICEINSTANCEID']
ms_vlan = context['ms_aliases']['Station VLAN management']
ms_port_vlan = context['ms_aliases']['Station Ethernet port VLAN configuration']
ms_hostname = context['ms_aliases']['Station hostname']
ms_port_settings = context['ms_aliases']['Station Ethernet port settings']


#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

Orchestration.update_asynchronous_task_details(*async_update_list, 'Import current configuration... ') 

#Create Station device order object
StationOrderObject = Order(context['station_device_id'])
response = StationOrderObject.command_synchronize(300)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Import current configuration... OK') 
time.sleep(3)


#Check VLAN IDs
Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying VLANs... ') 
objects_list = StationOrderObject.command_objects_instances(ms_vlan)
do_vlans_exist = list()
for number, vlan in context['vlan_list'].items():
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying VLANs... ID {}... '.format(vlan['id']))
  for vlan_id in objects_list:
    vlan_object = StationOrderObject.command_objects_instances_by_id(ms_vlan, vlan_id)[ms_vlan][vlan_id]
    if vlan['id'] == vlan_object['object_id']:
      Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying VLANs... ID {}... OK'.format(vlan['id']))
      time.sleep(3)
      do_vlans_exist.append(True)
      break
  else:
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying VLANs... ID {}... FAILED'.format(vlan['id']))
    time.sleep(3)
    do_vlans_exist.append(False)
    
#Check trunk port status
Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying status of port {}... '.format(context['trunk_port'])) 
objects_list = StationOrderObject.command_objects_instances(ms_port_settings)
is_port_enable = False

for port_name in objects_list:
  if port_name == context['trunk_port']:
    port_object = StationOrderObject.command_objects_instances_by_id(ms_port_settings, port_name)[ms_port_settings][port_name]
    if port_object['status'] == 'enabled':
      is_port_enable = True
      Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying status of port {}... OK'.format(context['trunk_port']))
      time.sleep(3)
    else:
      Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying status of port {}... FAILED'.format(context['trunk_port']))
      time.sleep(3)
  
#Check trunk port VLAN membership
Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying VLAN membership for port {}... '.format(context['trunk_port'])) 
objects_list = StationOrderObject.command_objects_instances(ms_port_vlan)
are_vlans_member = list()

for number, vlan in context['vlan_list'].items():
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying VLAN membership for port {}... VLAN ID {}... '.format(context['trunk_port'], vlan['id']))
  for port_name in objects_list:
    if port_name == context['trunk_port']:
      port_object = StationOrderObject.command_objects_instances_by_id(ms_port_vlan, port_name)[ms_port_vlan][port_name]
      for member_number, member_vlan in port_object['vlan_list'].items():
        if member_vlan['id'] == vlan['id']:
          Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying VLAN membership for port {}... VLAN ID {}... OK'.format(context['trunk_port'], vlan['id']))
          time.sleep(3)
          are_vlans_member.append(True)
          break
      else:
        Orchestration.update_asynchronous_task_details(*async_update_list, 'Verifying VLAN membership for port {}... VLAN ID {}... FAILED'.format(context['trunk_port'], vlan['id']))
        time.sleep(3)
        are_vlans_member.append(False)

if all(do_vlans_exist):
  if is_port_enable:
    if all(are_vlans_member):
      success_comment = 'The station has been configured properlly'
      print(StationOrderObject.process_content('ENDED', success_comment, context, True))
    else:
      fail_comment = 'Not all required VLANs are memeber of {}'.format(context['trunk_port'])
      print(StationOrderObject.process_content('FAILED', fail_comment, context, True))
  else:
    fail_comment = 'Trunk port {} is not enabled'.format(context['trunk_port'])
    print(StationOrderObject.process_content('FAILED', fail_comment, context, True))
else:
    fail_comment = 'Not all required VLANs exist in database'
    print(StationOrderObject.process_content('FAILED', fail_comment, context, True))