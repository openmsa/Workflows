from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
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
task_variables = Variables()

#Add new variables
task_variables.add('site', var_type = 'String')

#Add vars to context
context = Variables.task_call(task_variables)
process_id                   = context['SERVICEINSTANCEID']
_ce_connections              = context['ce_connections']

#Because bug
ce_connections = dict()
util.log_to_process_file(process_id, '_CE_CONNECTION {}'.format(_ce_connections))
for interface, connection in _ce_connections.items():
    ce_connections[interface.replace('DOT', '.')] = connection
util.log_to_process_file(process_id, 'CE_CONNECTION {}'.format(ce_connections))

ipam_device_id               = context['ipam_device_id']
ce_device_id                 = context['ce_device_details']['device_id']
ce_device_name               = context['ce_device_details']['name']
customer_vrf                 = context['customer_details']['vrf']
customer_name                = context['customer_name']
site                         = context['site']
site_asn                     = context['site_asn']
asn                          = '65042'

ms_file                  = '/opt/fmc_repository/CommandDefinition/microservices/Netbox___Avaliable_Prefix.xml'
ms_ipam_tenant           = context['ipam_ms_aliases']['IPAM Tenants']
ms_ipam_site             = context['ipam_ms_aliases']['IPAM Sites']
ms_ipam_device           = context['ipam_ms_aliases']['IPAM Devices']
ms_interface_connection  = context['ipam_ms_aliases']['IPAM Interface Connections']
ms_ipam_prefix           = context['ipam_ms_aliases']['IPAM IPv4 prefixes']
ms_ipam_avaliable_prefix = context['ipam_ms_aliases']['IPAM Available Prefixes']
ms_ipam_address          = context['ipam_ms_aliases']['IPAM IPv4 addresses']
ms_ipam_vrf              = context['ipam_ms_aliases']['IPAM VRFs']
ms_router_bgp_neighbor   = context['ipam_ms_aliases']['Router BGP neighbours']
ms_router_bgp_speaker    = context['ipam_ms_aliases']['Router BGP speaker']
ms_router_vrf            = context['ipam_ms_aliases']['Router VRF']
ms_router_interface      = context['ipam_ms_aliases']['Router interfaces']

fail_comment                 = str()
success_string               = str()
fail_string                  = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'


IpamOrderObject = Order(ipam_device_id)

#Create CE device irder object
CeOrderObject = Order(ce_device_id)
response = CeOrderObject.command_synchronize(300)
util.log_to_process_file(process_id, 'CE_CONNECTION {}'.format(ce_connections))
pe_order_list = list()
for interface, connection in ce_connections.items():
    util.log_to_process_file(process_id, 'CONNECTION {}'.format(connection))
    #Create oreder object for PE
    pe_order_list.append(Order(connection['neighbour']['device_id']))
    response = pe_order_list[-1].command_synchronize(300)

    #Configure IP address on CE link
    ms_dict = {ms_router_interface: 
                           {interface: {'object_id': interface,
                                        'ip_addr':   connection['ip_address'].split('/')[0],
                                        'ip_prefix': connection['ip_address'].split('/')[1]
                                        }
                            }
            }
    util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
    CeOrderObject.command_execute('UPDATE', ms_dict)
    CeOrderObject.command_synchronize(300)

    #Create BGP process on CE
    ms_dict = {ms_router_bgp_speaker: 
                           {site_asn: {'object_id': site_asn,
                                       'router_id': connection['ip_address'].split('/')[0]
                                        }
                            }
              }
    util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
    CeOrderObject.command_execute('CREATE', ms_dict)
    CeOrderObject.command_synchronize(300)
    
    #Create BGP neighbor on CE
    ms_dict = {ms_router_bgp_neighbor : 
                           {connection['neighbour']['ip_address'].split('/')[0].replace('.', '_'): {'object_id': connection['neighbour']['ip_address'].split('/')[0],
                                                                                                    'peer_group': customer_name.replace(' ', '_'),
                                                                                                    'asn': asn,
                                                                                                    'local_asn': site_asn,
                                                                                                    'address_family': {'0': {'afi': 'IPv4', 'safi': 'Unicast'}},
                                                                                                    'vrf': 'master'
                                                                                                     }
                            }
              }
    util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
    CeOrderObject.command_execute('CREATE', ms_dict)
    CeOrderObject.command_synchronize(300)

    #Check if customer VRF exists on PE
    does_customer_vrf_exist = False
    counter = 0
    objects_list = IpamOrderObject.command_objects_instances(ms_router_vrf)

    if len(objects_list) > 0:
      while not does_customer_vrf_exist or counter < len(objects_list):
        util.log_to_process_file(process_id, 'VRF LIST {}'.format(objects_list[counter]['object_id']))
        if objects_list[counter]['object_id'] == customer_vrf:
          does_customer_vrf_exist = True
        counter += 1

    if not does_customer_vrf_exist:
      #Create custromer VRF on PE
      #Grab RD from IPAM
      vrf_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_vrf, 
                                                                  customer_vrf)[ms_ipam_vrf][customer_vrf]


      ms_dict = {ms_router_vrf: 
                       {customer_vrf: {'object_id': customer_vrf,
                                      'interfaces': {'0': {'iface_name': connection['neighbour']['interface']}},
                                      'rd': vrf_object['rd'],
                                      'route_target_export': vrf_object['rd'],
                                      'route_target_import': vrf_object['rd']
                                       }
                        }
                }
      pe_order_list[-1].command_execute('CREATE', ms_dict)
      pe_order_list[-1].command_synchronize(300)

    
    #Configure IP address on PE link
    ms_dict = {ms_router_interface: 
                       {connection['neighbour']['interface']: {'object_id': connection['neighbour']['interface'],
                                                               'ip_addr':   connection['neighbour']['ip_address'].split('/')[0],
                                                               'ip_prefix': connection['neighbour']['ip_address'].split('/')[1]
                                                               }
                        }
        }
    util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
    pe_order_list[-1].command_execute('UPDATE', ms_dict)
    pe_order_list[-1].command_synchronize(300)

    #Create BGP neighbor on PE
    ms_dict = {ms_router_bgp_neighbor : 
                           {connection['ip_address'].split('/')[0].replace('.', '_'): {'object_id': connection['ip_address'].split('/')[0],
                                                                                       'peer_group': customer_name.replace(' ', '_'),
                                                                                       'asn': site_asn,
                                                                                       'local_asn': asn,
                                                                                       'address_family': {'0': {'afi': 'IPv4', 'safi': 'Unicast'}},
                                                                                       'vrf': customer_vrf
                                                                                      }
                            }
              }
    pe_order_list[-1].command_execute('CREATE', ms_dict)
    pe_order_list[-1].command_synchronize(300)



time.sleep(30)

#Verify connections
peering_list = list()
CeOrderObject.command_synchronize(300)
objects_list = CeOrderObject.command_objects_instances(ms_router_bgp_neighbor)
util.log_to_process_file(process_id, 'NEIGHBOUR LIST {}'.format(objects_list))
for neighbor in objects_list:
    neighbor_object = CeOrderObject.command_objects_instances_by_id(ms_router_bgp_neighbor, 
                                                                      neighbor)[ms_router_bgp_neighbor][neighbor]
    if neighbor_object['state'] == 'Established':
      peering_list.append(True)
    else:
      peering_list.append(False)


if len(peering_list) > 0:
  if all(peering_list):
    print(CeOrderObject.process_content('ENDED', 'All BGP sessions have been established', context, True))
  else:
    print(CeOrderObject.process_content('FAILED', 'One or more BGP sessions are not in Establshed stage', context, True))
else:
  print(CeOrderObject.process_content('FAILED', 'No BGP peer has been created', context, True))