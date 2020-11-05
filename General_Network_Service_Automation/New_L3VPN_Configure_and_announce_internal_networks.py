from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from datetime import datetime
from msa_sdk import constants
from msa_sdk import util
import ipaddress
import time
import re
import json
import xmltodict
import sys
import os

#New Variables object
TaskVariables = Variables()

#Add vars to context
context = Variables.task_call(TaskVariables)
process_id                   = context['SERVICEINSTANCEID']
_ce_connections              = context['ce_connections']

#Because bug
ce_connections = dict()
for interface, connection in _ce_connections.items():
    ce_connections[interface.replace('DOT', '.')] = connection

ipam_device_id               = context['ipam_device_id']
ce_device_id                 = context['ce_device_details']['device_id']
ce_device_name               = context['ce_device_details']['name']
ce_internal_interface_name 	 = context['ce_device_details']['internal_interface_name']
ce_internal_interface_ip 	 = context['ce_device_details']['internal_interface_ip']
ce_internal_prefix 			 = context['ce_device_details']['internal_prefix']
ce_device_local_context 	 = context['ce_device_details']['local_context_data']
customer_vrf                 = context['customer_details']['vrf']
customer_name                = context['customer_name']
site                         = context['site']
site_asn                     = context['site_asn']
asn                          = '65042'

ms_file                  = '/opt/fmc_repository/CommandDefinition/NETBOX/available_prefix.xml'
ms_ipam_tenant           = context['ipam_ms_aliases']['IPAM Tenants']
ms_ipam_site             = context['ipam_ms_aliases']['IPAM Sites']
ms_ipam_device           = context['ipam_ms_aliases']['IPAM Devices']
ms_interface_connection  = context['ipam_ms_aliases']['IPAM Interface Connections']
ms_ipam_prefix           = context['ipam_ms_aliases']['IPAM IPv4 prefixes']
ms_ipam_avaliable_prefix = context['ipam_ms_aliases']['IPAM Available Prefixes']
ms_ipam_address          = context['ipam_ms_aliases']['IPAM IPv4 addresses']
ms_ipam_vrf              = context['ipam_ms_aliases']['IPAM VRFs']
ms_ipam_interface		 = context['ipam_ms_aliases']['IPAM Interfaces']
ms_router_bgp_neighbor   = context['ipam_ms_aliases']['Router BGP neighbours']
ms_router_bgp_speaker    = context['ipam_ms_aliases']['Router BGP speaker']
ms_router_vrf            = context['ipam_ms_aliases']['Router VRF']
ms_router_interface      = context['ipam_ms_aliases']['Router interfaces']
ms_router_prefix_filter  = context['ipam_ms_aliases']['Router Prefix Filter']
ms_router_import_to_bgp  = context['ipam_ms_aliases']['Router Import Connected to BGP']
ms_router_advert_by_bgp  = context['ipam_ms_aliases']['Router Import advertised routes by BGP']

#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

#Create CE device order object
CeOrderObject = Order(ce_device_id)
response = CeOrderObject.command_synchronize(300)

#Create IPAM order object
IpamOrderObject = Order(ipam_device_id)
response = IpamOrderObject.command_synchronize(300)

Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring IP address on CE device internal link... ') 
#Configure IP address on CE internal interface
ms_dict = {ms_router_interface: 
                       {ce_internal_interface_name: {'object_id': ce_internal_interface_name,
                                    				 'ip_addr':   ce_internal_interface_ip.split('/')[0],
                                    				 'ip_prefix': ce_internal_interface_ip.split('/')[1]
                                    				 }
                        }
        }
CeOrderObject.command_execute('UPDATE', ms_dict)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring IP address on CE device internal link... OK') 
CeOrderObject.command_synchronize(300)


#Configure route filter
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring route filter for internal prefix... ') 
ms_dict = {ms_router_prefix_filter: 
                       {'route_filter_internal_networks': {'object_id': 'route_filter_internal_networks',
                       								  	   'rules_list': {'0': {'action': 'permit',
                       								  					        'number': '10',
                       								  					        'prefix': ce_internal_prefix,
                       								  					        }
                       								  				      }
                                    				      }
                       }
        }
CeOrderObject.command_execute('CREATE', ms_dict)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring route filter for internal prefix... OK')
CeOrderObject.command_synchronize(300)

#Configure import connected routes to BGP
Orchestration.update_asynchronous_task_details(*async_update_list, 'Import internal prefix to BGP... ')
ms_dict = {ms_router_import_to_bgp: 
                       {'10': {'object_id': '10',
                       		   'local_asn': site_asn,
                       		   'prefix_filter': 'route_filter_internal_networks'
                               }
                        }
           }
CeOrderObject.command_execute('CREATE', ms_dict)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Import internal prefix to BGP... OK')
CeOrderObject.command_synchronize(300)


#Verify that site lan prefix is announced via BGP to PE
Orchestration.update_asynchronous_task_details(*async_update_list, 'Verify that internal prefix announced to PE device... ')

#Identify MS file path to import advertised prefixes
ms_advertised_prefix_file_path = '{}/{}.xml'.format(ce_device_local_context['msa_specific']['ms_dir'], ms_router_advert_by_bgp)
is_site_prefix_announced_to_all_peers = list()
for interface, connection in ce_connections.items():
	sed_command = 'sed -i \'s@{original_string}@{rewrite_string}@\' {ms_file}'.format(original_string = '1.1.1.1',
																				      rewrite_string = connection['neighbour']['ip_address'].split('/')[0],
																				      ms_file = ms_advertised_prefix_file_path)
	os.system(sed_command)

	with open(ms_advertised_prefix_file_path) as temp_ms_file:
		temp_ms_file_content = temp_ms_file.read()



	CeOrderObject.command_synchronize(300)
	time.sleep(10)

	objects_list = CeOrderObject.command_objects_instances(ms_router_advert_by_bgp)

	is_site_prefix_announced = False
	counter = 0

	while is_site_prefix_announced is False and counter < len(objects_list):
		prefix_object = CeOrderObject.command_objects_instances_by_id(ms_router_advert_by_bgp, 
                                                                  	   objects_list[counter])[ms_router_advert_by_bgp][objects_list[counter]]
		if prefix_object['object_id'] == ce_internal_prefix:
			is_site_prefix_announced = True
			is_site_prefix_announced_to_all_peers.append(is_site_prefix_announced)
		counter += 1

	sed_command = 'sed -i \'s@{original_string}@{rewrite_string}@\' {ms_file}'.format(original_string = connection['neighbour']['ip_address'].split('/')[0],
																				      rewrite_string = '1.1.1.1',
																				      ms_file = ms_advertised_prefix_file_path)
	os.system(sed_command)

	Orchestration.update_asynchronous_task_details(*async_update_list, 'Verify that internal prefix announced to PE device... OK')

if len(is_site_prefix_announced_to_all_peers) > 0 and all(is_site_prefix_announced_to_all_peers):
	context.pop('ce_connections')
	context.pop('ce_device_details')
	print(CeOrderObject.process_content('ENDED', 'Internal networks have been announced successfully to all peers', context, True))
else:
	print(CeOrderObject.process_content('FAILED', 'Internal networks have not been announced successfully to all peers', context, True))
