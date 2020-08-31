from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
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

#New Variables object
task_variables = Variables()

#Add new variables
task_variables.add('site', var_type = 'String')

#Add vars to context
context = Variables.task_call(task_variables)

process_id                   = context['SERVICEINSTANCEID']
ipam_device_id               = context['ipam_device_id']
customer_vrf                 = context['customer_details']['vrf']
customer_name                = context['customer_name']
site                         = context['site']

ms_file                  = '/opt/fmc_repository/CommandDefinition/microservices/Netbox___Avaliable_Prefix.xml'
ms_ipam_tenant           = context['ipam_ms_aliases']['IPAM Tenants']
ms_ipam_site             = context['ipam_ms_aliases']['IPAM Sites']
ms_ipam_device           = context['ipam_ms_aliases']['IPAM Devices']
ms_interface_connection  = context['ipam_ms_aliases']['IPAM Interface Connections']
ms_ipam_prefix           = context['ipam_ms_aliases']['IPAM IPv4 prefixes']
ms_ipam_avaliable_prefix = context['ipam_ms_aliases']['IPAM Available Prefixes']
ms_ipam_address          = context['ipam_ms_aliases']['IPAM IPv4 addresses']
ms_ipam_interface        = context['ipam_ms_aliases']['IPAM Interfaces']

fail_comment                 = str()
success_string               = str()
fail_string                  = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'

#Create IPAM order object
IpamOrderObject = Order(ipam_device_id)
response = IpamOrderObject.command_synchronize(300)


objects_list = IpamOrderObject.command_objects_instances(ms_ipam_device)

#Retrieve information about CE device what is located on the site
counter = 0
ce_device_id = None
ce_device_name = None
while ce_device_name is None or counter < len(objects_list):
    device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                    objects_list[counter])[ms_ipam_device][objects_list[counter]]
    if device_object['role'] == 'CE' and device_object['site'] == site:
        ce_device_name = device_object['object_id']
    counter += 1


MsaLookup = lookup.Lookup()

MsaLookup.look_list_device_ids()

devices = json.loads(MsaLookup.response.text)
util.log_to_process_file(process_id, 'DEVICES {}'.format(devices))

counter = 0
while ce_device_id is None or counter < len(devices):
    if devices[counter]['name'] == ce_device_name:
        ce_device_id = devices[counter]['id']
    counter += 1



#Create CE device irder object
CeOrderObject = Order(ce_device_id)
response = CeOrderObject.command_synchronize(300)

#Gather ASN for the site
asn_list = list()
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_site)
for site_name in objects_list:
    try:
        site_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_site, 
                                                                      site_name)[ms_ipam_site][site_name]
        if site_object['tenant'] == customer_name:
            if site_object['asn']:
                asn_list.append(int(site_object['asn']))
    except:
        pass

if len(asn_list) > 0:
    asn_list.sort()
    site_asn = str(asn_list[-1] + 1)
else:
    site_asn = '65100';

context['site_asn'] = site_asn;


site_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_site, 
                                                              site)[ms_ipam_site][site]
#Update ASN for site in IPAM
ms_dict = {ms_ipam_site: 
                        {site: {'object_id': site,
                                'asn': site_asn,
                                'slug': site_object['slug'],
                                'status': site_object['status']
                                }
                         }
            }
util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
IpamOrderObject.command_execute('UPDATE', ms_dict)




#Retrieve info about connected device
ce_connections = dict()
objects_list = IpamOrderObject.command_objects_instances(ms_interface_connection)
for connection in objects_list:
    connection_object = IpamOrderObject.command_objects_instances_by_id(ms_interface_connection, 
                                                                        connection)[ms_interface_connection][connection]
    util.log_to_process_file(process_id, 'CONNECTION OBJECT {}'.format(connection_object))
    if connection_object['iface_a_device'] == ce_device_name:
        ce_connections[connection_object['iface_a_port']] = {'neighbour':  {
                                                                            'device':     connection_object['iface_b_device'],
                                                                            'device_id':  None,
                                                                            'interface':  connection_object['iface_b_port'],
                                                                            'ip_address': None
                                                                            },
                                                             'subnet':     None,
                                                             'ip_address': None
                                                            }
            
    if connection_object['iface_b_device'] == ce_device_name:
        ce_connections[connection_object['iface_b_port']] = {'neighbour':  {
                                                                            'device':     connection_object['iface_a_device'],
                                                                            'device_id':  None,
                                                                            'interface':  connection_object['iface_a_port'],
                                                                            'ip_address': None
                                                                           },
                                                             'subnet':     None,
                                                             'ip_address': None
                                                            }


#Identify what device is PE
for interface, connection in ce_connections.items():
    device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                    connection['neighbour']['device'])[ms_ipam_device][connection['neighbour']['device'].replace('.', '_')]
    util.log_to_process_file(process_id, 'DEVICE OBJECT {}'.format(device_object))
    util.log_to_process_file(process_id, 'CE CONNECTIONS {}'.format(ce_connections))
    if device_object['role'] != 'PE':
        ce_connections.pop(interface)


#Pick up a subnet
customer_prefix = None
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_prefix)
util.log_to_process_file(process_id, 'PREFIX LIST {}'.format(objects_list))

counter = 0
while (customer_prefix is None) or (counter < len(objects_list)):
    util.log_to_process_file(process_id, 'COUNTER {}'.format(counter))
    prefix_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_prefix, 
                                                                    objects_list[counter])[ms_ipam_prefix][objects_list[counter]]
    util.log_to_process_file(process_id, 'PREFIX OBJECT {}'.format(prefix_object))
    try:
        if prefix_object['tenant'] == customer_name and prefix_object['status'] == 'container':
            customer_prefix = prefix_object
    except:
        pass
    counter += 1

#Modify microservice to grab avaliable prefix from cusotmer prefix
rewrite_string = '<xpath>/api/ipam/prefixes/{id}/available-prefixes/</xpath>'.format(id = customer_prefix['id'])
sed_command = 'sed -i \'s@<xpath>/api/ipam/prefixes/.*</xpath>@{rewrite_string}@\' {ms_file}'.format(rewrite_string = rewrite_string,
                                                                                                     ms_file = ms_file)
os.system(sed_command)

#Retrieve avaliable prefixes
response = IpamOrderObject.command_synchronize(300)
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_avaliable_prefix)
util.log_to_process_file(process_id, 'AVALIABLE PREFIXES {}'.format(objects_list))


#Find avaliable /23 prefix
prefix_lenght_dict = dict()
for prefix in objects_list:
    prefix_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_avaliable_prefix, 
                                                                    prefix)[ms_ipam_avaliable_prefix][prefix]
    prefix_lenght_dict[prefix] = prefix_object['prefix'].split('/')[1]
    util.log_to_process_file(process_id, 'PREFIX LENGHT {}'.format(prefix_lenght_dict[prefix]))
sorted_prefix = sorted(prefix_lenght_dict.items(), key=lambda x: x[1], reverse=True)
util.log_to_process_file(process_id, 'SORTED LIST {}'.format(sorted_prefix))

prefix = None
counter = 0
while (prefix is None) and counter < len(sorted_prefix):
    if int(sorted_prefix[counter][1]) <= 23:
        prefix = sorted_prefix[counter][0]
    util.log_to_process_file(process_id, 'SITE BASE PREFIX IN LOOP {}'.format(prefix))
    counter += 1

util.log_to_process_file(process_id, 'SITE BASE PREFIX {}'.format(prefix))

#Derive site prefixes
site_base_prefix = ipaddress.ip_network(IpamOrderObject.command_objects_instances_by_id(ms_ipam_avaliable_prefix, 
                                                                                    prefix)[ms_ipam_avaliable_prefix][prefix]['prefix'])
site_base_prefix = list(site_base_prefix.subnets(new_prefix = 23))[0]
site_prefix_list = list()
site_prefix_list.append(('lan', list(site_base_prefix.subnets(new_prefix = 24))[0]))
site_prefix_list.append(('service', list(site_base_prefix.subnets(new_prefix = 24))[1]))
counter = 0
for interface, connection in ce_connections.items():
    counter -= 1
    site_prefix_list.append(('p2p', list(site_base_prefix.subnets(new_prefix = 30))[counter]))
    connection['subnet'] = str(site_prefix_list[-1][1])
    connection['neighbour']['ip_address'] = '{}/{}'.format(str(list(site_prefix_list[-1][1].hosts())[0]), site_prefix_list[-1][1].prefixlen)
    connection['ip_address'] = '{}/{}'.format(str(list(site_prefix_list[-1][1].hosts())[1]), site_prefix_list[-1][1].prefixlen)


util.log_to_process_file(process_id, 'SITE PREFIX LIST {}'.format(site_prefix_list))


#Update IPAM system with new prefixes
for prefix_tuple in site_prefix_list:
    object_id = prefix_tuple[1]
    tag = prefix_tuple[0]
    ms_dict = {ms_ipam_prefix: 
                               {str(object_id): {'object_id': str(object_id),
                                                 'status':    'active',
                                                 'site':      site,
                                                 'tenant':    customer_name,
                                                 'vrf':       customer_vrf,
                                                 'tags':      {'0': {'tag': tag}}
                                                 }
                                }
                }
    util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
    IpamOrderObject.command_execute('CREATE', ms_dict)

for interface, connection in ce_connections.items():
    interface_list = ((connection['ip_address'], interface), (connection['neighbour']['ip_address'], connection['neighbour']['interface']))
    for interface_tuple in interface_list:
        ms_dict = {ms_ipam_address: 
                                   {interface_tuple[0]: {'object_id': interface_tuple[0],
                                                         'status':    'active',
                                                         'tenant':    customer_name,
                                                         'vrf':       customer_vrf,
                                                         'interface': interface_tuple[1]
                                                         }
                                    }
                    }
        util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
        IpamOrderObject.command_execute('CREATE', ms_dict)

objects_list = IpamOrderObject.command_objects_instances(ms_ipam_interface)

#Grab internal interface of the CE device
counter = 0
ce_internal_interface_name = None
while ce_internal_interface_name is None or counter < len(objects_list):
    interface_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_interface, 
                                                                    objects_list[counter])[ms_ipam_interface][objects_list[counter]]
    util.log_to_process_file(process_id, 'INTERFACE OBJECT {}'.format(interface_object))
    if  interface_object['device'] == ce_device_name:
        if 'tags' in interface_object:
            for number, tag in interface_object['tags'].items():
                if tag['tag'] == 'internal':
                    ce_internal_interface_name = interface_object['name']
    counter += 1

for prefix_tuple in site_prefix_list:
    if prefix_tuple[0] == 'lan':
        ce_internal_interface_ip = '{}/{}'.format(str(list(prefix_tuple[1].hosts())[0]), prefix_tuple[1].prefixlen)
        ce_internal_prefix = str(prefix_tuple[1])
        ms_dict = {ms_ipam_address: 
                                {ce_internal_interface_ip: {'object_id': ce_internal_interface_ip,
                                                            'status':    'active',
                                                            'tenant':    customer_name,
                                                            'vrf':       customer_vrf,
                                                            'interface': ce_internal_interface_name
                                                            }
                                }
                }
    util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
    IpamOrderObject.command_execute('CREATE', ms_dict)




MsaLookup.look_list_device_ids()

devices = json.loads(MsaLookup.response.text)
util.log_to_process_file(process_id, 'DEVICES {}'.format(devices))

for interface, connection in ce_connections.items():
    counter = 0
    util.log_to_process_file(process_id, 'CONNECTION {}'.format(connection))
    while connection['neighbour']['device_id'] is None and counter < len(devices):
        util.log_to_process_file(process_id, 'DEVICE {}'.format(devices[counter]))
        if devices[counter]['name'] == connection['neighbour']['device']:
            connection['neighbour']['device_id'] = devices[counter]['id']
        counter += 1
    
#Because bug
_ce_connections = dict()
for interface, connection in ce_connections.items():
    _ce_connections[interface.replace('.', 'DOT')] = connection

context['ce_connections'] = _ce_connections
util.log_to_process_file(process_id, 'CE_CONNECTION IN PREPARE {}'.format(context['ce_connections']))

#Extract device local context data for future needs
ce_device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                   ce_device_name)[ms_ipam_device][ce_device_name.replace('.', '_')]
ce_device_local_context = json.loads(json.dumps(xmltodict.parse(ce_device_object['local_context_data'])))['local_context_data']


context['ce_device_details'] = dict()
context['ce_device_details']['device_id'] = ce_device_id
context['ce_device_details']['name'] = ce_device_name
context['ce_device_details']['internal_interface_name'] = ce_internal_interface_name
context['ce_device_details']['internal_interface_ip'] = ce_internal_interface_ip
context['ce_device_details']['internal_prefix'] = ce_internal_prefix
context['ce_device_details']['local_context_data'] = ce_device_local_context

print(CeOrderObject.process_content('ENDED', 'Task OK', context, True))
