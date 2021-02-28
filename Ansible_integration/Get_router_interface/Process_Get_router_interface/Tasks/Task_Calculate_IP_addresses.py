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
TaskVariables.add('site', var_type = 'String')

#Add vars to context
context = Variables.task_call(TaskVariables)

process_id                   = context['SERVICEINSTANCEID']
router_device_id             = context['exchange_dict']['router_device_id']
customer_name                = context['exchange_dict']['tenant']
site                         = context['exchange_dict']['site']
subnet						 = context['exchange_dict']['site_prefix']
server_list					 = context['server_list']
router_interface			 = context['router_interface']

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

#Get site router name
RouterDevice = Device(customer_id = re.match('^\D+?(\d+?)$',context['UBIQUBEID']).group(1),
                      device_id = router_device_id
                     )
RouterDevice.read()
router_name = RouterDevice.name


#Get IP addresses
NetObject = ipaddress.ip_network(subnet)
site_ip_plan = dict()
ip_address_list = list(NetObject.hosts())
site_ip_plan[router_name] = {'ip_address':'{}/{}'.format(ip_address_list[0], NetObject.prefixlen),
                             'interface': router_interface}
context['exchange_dict']['ansible_microservice_variables']['next_hop'] = str(ip_address_list[0])
context['exchange_dict']['ansible_microservice_variables']['network'] = '11.0.0.0/8'

counter = 10
server_number_counter = 1
for server in server_list:
  site_ip_plan[server[0]] = {'ip_address':'{}/{}'.format(ip_address_list[counter], NetObject.prefixlen),
                             'interface': server[1]}
  context['exchange_dict']['ansible_microservice_variables']['server_{}_ip_address'.format(server_number_counter)] = str(ip_address_list[counter])
  context['exchange_dict']['ansible_microservice_variables']['server_{}_prefix_len'.format(server_number_counter)] = str(NetObject.prefixlen)
  context['exchange_dict']['ansible_microservice_variables']['server_{}_iface'.format(server_number_counter)]      = str(server[1])
  counter += 1
  server_number_counter += 1
  
context['site_ip_plan'] = site_ip_plan
result = MSA_API.process_content('ENDED', 'Site IP plan is ready', context, True)
print(result)