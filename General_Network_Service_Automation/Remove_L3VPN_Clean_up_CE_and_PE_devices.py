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

"""
OLD
The proposals of the task are:
   - Remove BGP session on CE
   - Remove prefix filter on CE
   - Remove route map on CE
   - Remove interface IP settings and shutdown (LAN and WAN)
   - Remove BGP session on PE device
   - Remove VRF
   - Remove IP address and shutdown CE faced interface
"""


#New Variables object
TaskVariables = Variables()

#Add new variables
TaskVariables.add('site', var_type = 'String')

#Add vars to context
context = Variables.task_call(TaskVariables)
process_id                   = context['SERVICEINSTANCEID']
_ce_connections              = context['ce_connections']

#Because bug
ce_connections = dict()
for interface, connection in _ce_connections.items():
    ce_connections[interface.replace('DOT', '.')] = connection

site                         = context['site']
ipam_device_id               = context['ipam_device_id']
ce_device_id                 = context['ce_device_details']['device_id']
ce_device_name               = context['ce_device_details']['name']
ce_internal_interface_name   = context['ce_device_details']['internal_interface_name']
site_asn                     = context['site_asn']
customer_vrf                 = context['customer_details']['vrf']


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


IpamOrderObject = Order(ipam_device_id)

#Create CE device order object
CeOrderObject = Order(ce_device_id)
response = CeOrderObject.command_synchronize(300)
pe_order_list = list()

#Remove IP addresses from CE-PE links
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... ') 
for interface, connection in ce_connections.items():
      #Create oreder object for PE
    pe_order_list.append(Order(connection['neighbour']['device_id']))
    response = pe_order_list[-1].command_synchronize(300)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Clean up IP address on link toward {}... '.format(connection['neighbour']['device'])) 

    #Clean up IP address on CE link
    ms_dict = {ms_router_interface: 
                           {interface: {'object_id': interface
                                        }
                            }
            }
    CeOrderObject.command_execute('UPDATE', ms_dict)
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Clean up IP address on link toward {}... OK'.format(connection['neighbour']['device']))
    CeOrderObject.command_synchronize(300)

    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Clean up IP address on CE device internal link... ') 
    #Configure IP address on CE internal interface
    ms_dict = {ms_router_interface: 
                       {ce_internal_interface_name: {'object_id': ce_internal_interface_name
                                                    }
                        }
        }
    CeOrderObject.command_execute('UPDATE', ms_dict)
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Clean up IP address on CE device internal link... OK') 
    CeOrderObject.command_synchronize(300)

    #Remove route filter
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Remove route filter for internal prefix... ') 
    ms_dict = {ms_router_prefix_filter: 
                           {'route_filter_internal_networks': {'object_id': 'route_filter_internal_networks'
                                                              }
                           }
              }
    CeOrderObject.command_execute('DELETE', ms_dict)
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Remove route filter for internal prefix... OK')
    CeOrderObject.command_synchronize(300)

    #Remove import connected routes to BGP
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Remove import internal prefix to BGP... ')
    ms_dict = {ms_router_import_to_bgp: 
                           {'10': {'object_id': '10'}
                           }
               }
    CeOrderObject.command_execute('DELETE', ms_dict)
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Remove import internal prefix to BGP... OK')
    CeOrderObject.command_synchronize(300)


    CeOrderObject.command_synchronize(300)
    objects_list = CeOrderObject.command_objects_instances(ms_router_bgp_neighbor)

    for ip_address in context['site_address_list']:
      if ip_address['object_id'].split('/')[0].replace('.', '_') in objects_list:
    
        #Remove BGP neighbor on CE
        Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Remove BGP peer for {}... '.format(connection['neighbour']['device']))
        ms_dict = {ms_router_bgp_neighbor : 
                               {ip_address['object_id'].split('/')[0].replace('.', '_'): {'object_id': ip_address['object_id'].split('/')[0]}
                                }
                  }
        CeOrderObject.command_execute('DELETE', ms_dict)
        Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Remove BGP peer for {}... OK'.format(connection['neighbour']['device']))
        CeOrderObject.command_synchronize(300)

    #Delete BGP process on CE
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... Remove BGP process on {}... '.format(ce_device_name))
    ms_dict = {ms_router_bgp_speaker: 
                           {site_asn: {'object_id': site_asn
                                      }
                            }
              }
    CeOrderObject.command_execute('DELETE', ms_dict)
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring CE device... BGP process on {}... OK'.format(ce_device_name))
    CeOrderObject.command_synchronize(300)
    
    #Configure IP address on PE link
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring PE device... Clean up IP address on link toward {}... '.format(ce_device_name))
    ms_dict = {ms_router_interface: 
                       {connection['neighbour']['interface']: {'object_id': connection['neighbour']['interface']
                                                               }
                        }
        }
    pe_order_list[-1].command_execute('UPDATE', ms_dict)
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring PE device... Clean up IP address on link toward {}... OK'.format(ce_device_name))
    pe_order_list[-1].command_synchronize(300)

    objects_list = pe_order_list[-1].command_objects_instances(ms_router_bgp_neighbor)

    for ip_address in context['site_address_list']:
      if ip_address['object_id'].split('/')[0].replace('.', '_') in objects_list:
        #Create BGP neighbor on PE
        Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring PE device... Remove BGP peer for {}... '.format(ce_device_name))
        ms_dict = {ms_router_bgp_neighbor : 
                               {ip_address['object_id'].split('/')[0].replace('.', '_'): {'object_id': ip_address['object_id'].split('/')[0]}
                                }
                  }
        pe_order_list[-1].command_execute('DELETE', ms_dict)
        Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring PE device... Remove BGP peer for {}... OK'.format(ce_device_name))
        pe_order_list[-1].command_synchronize(300)


    #Check if customer VRF exists on PE
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring PE device... Remove VRF... ')
    ms_dict = {ms_router_vrf: 
                       {customer_vrf: {'object_id': customer_vrf}
                       }
                }
    pe_order_list[-1].command_execute('DELETE', ms_dict)
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuring PE device... Remove VRF... OK')
    pe_order_list[-1].command_synchronize(300)


print(CeOrderObject.process_content('ENDED', 'CE and PE devices have been cleaned successfully.', context, True))