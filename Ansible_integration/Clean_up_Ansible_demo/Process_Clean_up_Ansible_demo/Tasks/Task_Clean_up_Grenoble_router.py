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
 - Remove IPv4 address from router interface
 - Remove IPv4 network from OSPF announcment

"""

#New Variables object
TaskVariables = Variables()


#Add vars to context
context = Variables.task_call(TaskVariables)


#Udate exchange file
with open(context['exchange_file'], 'r') as exchange_file:
    exchange_dict = json.load(exchange_file)

process_id                   = context['SERVICEINSTANCEID']
router_device_id             = exchange_dict['router_device_id']
subnet						 = exchange_dict['site_prefix']
site_ip_plan			 	 = exchange_dict['site_ip_plan']
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

#Get site router name
RouterDevice = Device(customer_id = re.match('^\D+?(\d+?)$',context['UBIQUBEID']).group(1),
                      device_id = router_device_id
                     )
RouterDevice.read()
router_name = RouterDevice.name

#Create site router Order object
RouterOrderObject = Order(exchange_dict['router_device_id'])
RouterOrderObject.command_synchronize(300)

#Configure IP address on CE link
ms_dict = {ms_router_interface: 
                       {site_ip_plan[router_name]['interface']: {'object_id': site_ip_plan[router_name]['interface'],
                                           'ip_addr': str(),
                                           'ip_prefix': str()
                                           }
                        }
        }
RouterOrderObject.command_execute('CREATE', ms_dict)


#Clean up route announcment
objects_list = RouterOrderObject.command_objects_instances(ms_router_ospf_config)
ospf_process_object = RouterOrderObject.command_objects_instances_by_id(ms_router_ospf_config, objects_list[0])[ms_router_ospf_config][objects_list[0]]

#Remove new network to announce
index_to_remove = None
for index, value in ospf_process_object['interface'].items():
  if value['network_address'] == exchange_dict['site_prefix'].split('/')[0]:
    index_to_remove = index
    break
if index_to_remove is not None:
    del ospf_process_object['interface'][index_to_remove]

#Configure OSPF
ms_dict = {ms_router_ospf_config: {ospf_process_object['object_id']: ospf_process_object}}
RouterOrderObject.command_execute('UPDATE', ms_dict)



result = MSA_API.process_content('ENDED', 'Router interface and OSPF configuration has been updated', context, True)
print(result)

