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
 - Find out available IPv4 prefix for the provided site;
 - Create IPv4 prefix for the new server segment


"""

#New Variables object
TaskVariables = Variables()

#Add vars to context
context = Variables.task_call(TaskVariables)

process_id                   = context['SERVICEINSTANCEID']
ipam_device_id               = context['ipam_device_id']
customer_name                = context['tenant']
site                         = context['site']

ms_file                  = '/opt/fmc_repository/CommandDefinition/NETBOX/available_prefix.xml'
ms_ipam_tenant           = context['ipam_ms_aliases']['IPAM Tenants']
ms_ipam_site             = context['ipam_ms_aliases']['IPAM Sites']
ms_ipam_device           = context['ipam_ms_aliases']['IPAM Devices']
ms_interface_connection  = context['ipam_ms_aliases']['IPAM Interface Connections']
ms_ipam_prefix           = context['ipam_ms_aliases']['IPAM IPv4 prefixes']
ms_ipam_avaliable_prefix = context['ipam_ms_aliases']['IPAM Available Prefixes']
ms_ipam_address          = context['ipam_ms_aliases']['IPAM IPv4 addresses']
ms_ipam_interface        = context['ipam_ms_aliases']['IPAM Interfaces']

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


Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieve information about CE device on the site... ') 

objects_list = IpamOrderObject.command_objects_instances(ms_ipam_device)


#Pick up a subnet
Orchestration.update_asynchronous_task_details(*async_update_list, 'Find out a IPv4 block for the site... ')
customer_prefix = None
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_prefix)

#Find customer IPv4 block (assume that customer has big IPv4 block with 'container' status)
counter = 0
while (customer_prefix is None) or (counter < len(objects_list)):
    prefix_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_prefix, 
                                                                    objects_list[counter])[ms_ipam_prefix][objects_list[counter]]
    try:
        if prefix_object['tenant'] == customer_name and prefix_object['status'] == 'container' and prefix_object['site'] == context['site']:
            customer_prefix = prefix_object
    except:
        pass
    counter += 1

Orchestration.update_asynchronous_task_details(*async_update_list, 'Find out a IPv4 block for the site... OK. IPv4 block is {}'.format(customer_prefix['object_id']))
time.sleep(3)
#Modify microservice to grab avaliable prefix from cusotmer prefix
rewrite_string = '<xpath>/api/ipam/prefixes/{id}/available-prefixes/</xpath>'.format(id = customer_prefix['id'])
sed_command = 'sed -i \'s@<xpath>/api/ipam/prefixes/</xpath>@{rewrite_string}@\' {ms_file}'.format(rewrite_string = rewrite_string,
                                                                                                     ms_file = ms_file)
os.system(sed_command)

#Retrieve avaliable prefixes
Orchestration.update_asynchronous_task_details(*async_update_list, 'Create prefixes for the site... ')
response = IpamOrderObject.command_synchronize(300)
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_avaliable_prefix)


#Find avaliable /24 prefix
prefix_lenght_dict = dict()
for prefix in objects_list:
    prefix_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_avaliable_prefix, prefix)[ms_ipam_avaliable_prefix][prefix]
    prefix_lenght_dict[prefix] = prefix_object['prefix'].split('/')[1]
sorted_prefix = sorted(prefix_lenght_dict.items(), key=lambda x: x[1], reverse=True)

prefix = None
counter = 0
while (prefix is None) and counter < len(sorted_prefix):
    if int(sorted_prefix[counter][1]) <= 24:
        prefix = sorted_prefix[counter][0]
    counter += 1


#Derive site prefixes
site_base_prefix = ipaddress.ip_network(IpamOrderObject.command_objects_instances_by_id(ms_ipam_avaliable_prefix, 
                                                                                    prefix)[ms_ipam_avaliable_prefix][prefix]['prefix'])
site_base_prefix = list(site_base_prefix.subnets(new_prefix = 24))[0]
site_prefix_list = list()
site_prefix_list.append(('lan', list(site_base_prefix.subnets(new_prefix = 24))[0]))

#Modify microservice to original state back
rewrite_string = '<xpath>/api/ipam/prefixes/</xpath>'.format(id = customer_prefix['id'])
sed_command = 'sed -i \'s@<xpath>/api/ipam/prefixes/.*</xpath>@{rewrite_string}@\' {ms_file}'.format(rewrite_string = rewrite_string,
                                                                                                     ms_file = ms_file)
os.system(sed_command)

Orchestration.update_asynchronous_task_details(*async_update_list, 'Create prefixes for the site... OK')
time.sleep(3)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Update IPAM system with new prefixes and IP addresses... ')

#Update IPAM system with new prefixes
for prefix_tuple in site_prefix_list:
    object_id = prefix_tuple[1]
    tag = prefix_tuple[0]
    ms_dict = {ms_ipam_prefix: 
                               {str(object_id): {'object_id': str(object_id),
                                                 'status':    'active',
                                                 'site':      site,
                                                 'tenant':    customer_name,
                                                 'vrf':       '',
                                                 'tags':      {'0': {'tag': tag}}
                                                 }
                                }
                }
    IpamOrderObject.command_execute('CREATE', ms_dict)


Orchestration.update_asynchronous_task_details(*async_update_list, 'Update IPAM system with new prefixes and IP addresses... OK')
time.sleep(3)

exchange_dict = {"ipam_device_id":   context['ipam_device_id'],
                 "router_device_id": context['site_router'],
                 "tenant": context['tenant'],
                 "site": context['site'],
                 "site_prefix": str(site_prefix_list[0][1]),
                 "ansible_microservice_variables": dict()
                }

#Udate exchange file
with open(context['exchange_file'], 'w') as exchange_file:
    json.dump(exchange_dict, exchange_file)

success_comment = f'IPv4 address plan for site {site} has been prepared successfully. IPAM system has been updated.'
print(IpamOrderObject.process_content('ENDED', success_comment, context, True))
