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
import xmltodict
import sys
import os


"""
NEW
The proposals of the task are:
   - Identify site ASN
   - Identify site prefixes and IP addresses
   - Identify PE and CE devices

"""


#New Variables object
TaskVariables = Variables()

#Add new variables
TaskVariables.add('site', var_type = 'String')

#Add vars to context
context = Variables.task_call(TaskVariables)

process_id                   = context['SERVICEINSTANCEID']
ipam_device_id               = context['ipam_device_id']
customer_vrf                 = context['customer_details']['vrf']
customer_name                = context['customer_name']
site                         = context['site']

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



#Identify ASN for the site and save to context
Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieve AS number for the site... ')  
site_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_site, site)[ms_ipam_site][site]
context['site_asn'] = site_object['asn']
Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieve AS number for the site... OK')
time.sleep(3)



#Identify IPv4 subnets for the site and save to context
Orchestration.update_asynchronous_task_details(*async_update_list, 'Find out a IPv4 block for the site... ')
context['site_prefixes_list'] = list()
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_prefix)


for object in objects_list:
    prefix_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_prefix, 
                                                                    object)[ms_ipam_prefix][object]
    try:
        if prefix_object['tenant'] == customer_name and prefix_object['site'] == site:
            context['site_prefixes_list'].append(prefix_object)
    except:
        pass

Orchestration.update_asynchronous_task_details(*async_update_list, 'Find out a IPv4 block for the site... OK')
time.sleep(3)


#Identify IPv4 addresses for the site and save to context
Orchestration.update_asynchronous_task_details(*async_update_list, 'Find out a IPv4 addrsses for the site... ')
context['site_address_list'] = list()
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_address)

util.log_to_process_file(process_id, 'DEBUG: {}'.format(objects_list))
#Find customer IPv4 block (assume that customer has big IPv4 block with 'container' status)
for object in objects_list:
    prefix_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_address, 
                                                                    object)[ms_ipam_address][object]
    try:
        for number, tag in prefix_object['tags'].items():
            if prefix_object['tenant'] == customer_name and tag['tag'] == 'site:{}'.format(site):
                context['site_address_list'].append(prefix_object)
    except:
        pass

Orchestration.update_asynchronous_task_details(*async_update_list, 'Find out a IPv4 addrsses for the site... OK')
time.sleep(3)


objects_list = IpamOrderObject.command_objects_instances(ms_ipam_device)

#Retrieve information about CE device what is located on the site
counter = 0
ce_device_id = None
ce_device_name = None

#Find CE device name
Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieve information about CE device on the site... ')
while ce_device_name is None or counter < len(objects_list):
    util.log_to_process_file(process_id, 'DEBUG: {}'.format(IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, objects_list[counter])))
    device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                    objects_list[counter])[ms_ipam_device][objects_list[counter]]
    if device_object['role'] == 'CE' and device_object['site'] == site:
        ce_device_name = device_object['object_id']
    counter += 1

#Find device ID value
MsaLookup = lookup.Lookup()
MsaLookup.look_list_device_ids()

devices = json.loads(MsaLookup.content)

counter = 0
while ce_device_id is None or counter < len(devices):
    if devices[counter]['name'] == ce_device_name:
        ce_device_id = devices[counter]['id']
    counter += 1

Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieve information about CE device on the site... OK')
time.sleep(3)


#Retrieve info about connected device
Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieve info about connected device... ')
ce_connections = dict()
objects_list = IpamOrderObject.command_objects_instances(ms_interface_connection)
for connection in objects_list:
    connection_object = IpamOrderObject.command_objects_instances_by_id(ms_interface_connection, 
                                                                        connection)[ms_interface_connection][connection]
    if connection_object['iface_a_device'] == ce_device_name:
        ce_connections[connection_object['iface_a_port']] = {'neighbour':  {
                                                                            'device':     connection_object['iface_b_device'],
                                                                            'device_id':  None,
                                                                            'interface':  connection_object['iface_b_port'],
                                                                            }
                                                            }
            
    if connection_object['iface_b_device'] == ce_device_name:
        ce_connections[connection_object['iface_b_port']] = {'neighbour':  {
                                                                            'device':     connection_object['iface_a_device'],
                                                                            'device_id':  None,
                                                                            'interface':  connection_object['iface_a_port'],
                                                                           }
                                                            }


#Identify what device is PE
for interface, connection in ce_connections.items():
    device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                    connection['neighbour']['device'])[ms_ipam_device][connection['neighbour']['device'].replace('.', '_')]
    if device_object['role'] != 'PE':
        ce_connections.pop(interface)

#For pretty formated task comment in GUI
pe_list = list()
for interface, connection in ce_connections.items():
    pe_list.append(connection['neighbour']['device'])

Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieve info about connected device... OK. Connected PE are {}'.format(' '.join(pe_list)))
time.sleep(3)


#Find out device_id for all PE what the CE connected to
MsaLookup.look_list_device_ids()
devices = json.loads(MsaLookup.content)
for interface, connection in ce_connections.items():
    counter = 0
    while connection['neighbour']['device_id'] is None and counter < len(devices):
        if devices[counter]['name'] == connection['neighbour']['device']:
            connection['neighbour']['device_id'] = devices[counter]['id']
        counter += 1


#Grab internal interface of the CE device
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_interface)

counter = 0
ce_internal_interface_name = None
while ce_internal_interface_name is None or counter < len(objects_list):
    interface_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_interface, 
                                                                    objects_list[counter])[ms_ipam_interface][objects_list[counter]]
    if  interface_object['device'] == ce_device_name:
        if 'tags' in interface_object:
            for number, tag in interface_object['tags'].items():
                if tag['tag'] == 'internal':
                    ce_internal_interface_name = interface_object['name']
    counter += 1
    
#Because bug
_ce_connections = dict()
for interface, connection in ce_connections.items():
    _ce_connections[interface.replace('.', 'DOT')] = connection

context['ce_connections'] = _ce_connections


context['ce_device_details'] = dict()
context['ce_device_details']['device_id'] = ce_device_id
context['ce_device_details']['name'] = ce_device_name
context['ce_device_details']['internal_interface_name'] = ce_internal_interface_name


success_comment = f'IP plan information for {site} has been prepared successfully.'
print(IpamOrderObject.process_content('ENDED', success_comment, context, True))
