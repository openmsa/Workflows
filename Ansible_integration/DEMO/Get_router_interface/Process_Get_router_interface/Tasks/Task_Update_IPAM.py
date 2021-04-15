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
 - Update IPAM by new IPv4 addresses


"""

#New Variables object
TaskVariables = Variables()

#Add new variables
TaskVariables.add('site', var_type = 'String')

#Add vars to context
context = Variables.task_call(TaskVariables)

process_id                   = context['SERVICEINSTANCEID']
ipam_device_id               = context['exchange_dict']['ipam_device_id']
customer_name                = context['exchange_dict']['tenant']
site                         = context['exchange_dict']['site']
subnet						 = context['exchange_dict']['site_prefix']
server_list					 = context['server_list']
site_ip_plan 				 = context['site_ip_plan'] 

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

for host_name, details in site_ip_plan.items():
    ms_dict = {ms_ipam_address: 
                               {details['ip_address']: {'object_id': details['ip_address'],
                                                     'status':    'active',
                                                     'tenant':    customer_name,
                                                     'vrf':       '',
                                                     'interface': '',
                                                     'tags':      ''
                                                     }
                                }
                }
    IpamOrderObject.command_execute('CREATE', ms_dict)
    
exchange_dict = context['exchange_dict']
exchange_dict['site_ip_plan'] = site_ip_plan

#Udate exchange file
with open(context['exchange_file'], 'w') as exchange_file:
    json.dump(exchange_dict, exchange_file)

result = MSA_API.process_content('ENDED', 'IPAM has been updated', context, True)
print(result)

