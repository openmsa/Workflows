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
 - Configure station's hostname
 - Configure VLANs
 - Enable trunk interface
 - Configure VLAN memberships for trunk interface
 - Configure QoS (TBD)
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

#Configure hostname
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configure hostname... ') 
ms_dict = {ms_hostname: {context['hostname']: {'object_id': context['hostname']}}}
StationOrderObject.command_execute('CREATE', ms_dict)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configure hostname... OK') 

#Configure VLANs
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configure VLAN... ') 
for number,vlan in context['vlan_list'].items():
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Configure VLAN... {}... '.format(vlan['name'])) 
  ms_dict = {ms_vlan: {vlan['id']: {'object_id': vlan['id'],
								    'name': vlan['name']
								   }
					  }

		    }
  StationOrderObject.command_execute('CREATE', ms_dict)
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Configure VLAN... {}... OK '.format(vlan['name'])) 


#Enable trunk interface
Orchestration.update_asynchronous_task_details(*async_update_list, 'Enable port {}... '.format(context['trunk_port'])) 
ms_dict = {ms_port_settings: {context['trunk_port']: {'object_id': context['trunk_port'], 
                                                      'status': 'enable'
                                                     }
                             }
          }
StationOrderObject.command_execute('UPDATE', ms_dict)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Enable port {}... OK'.format(context['trunk_port'])) 


#Configure VLANs on trunk port
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configure port {} as trunk... '.format(context['trunk_port'])) 
ms_dict = {ms_port_vlan: {context['trunk_port']: {'object_id': context['trunk_port'], 
                                                  'type': 'trunk',
                                                  'vlan_list': list()
                                                  }
                          }
          }
for number,vlan in context['vlan_list'].items():
  ms_dict[ms_port_vlan][context['trunk_port']]['vlan_list'].append({'id': vlan['id']})
  
StationOrderObject.command_execute('UPDATE', ms_dict)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configure port {} as trunk... OK'.format(context['trunk_port'])) 

success_comment = 'Station has been provisioned successfully.'
print(StationOrderObject.process_content('ENDED', success_comment, context, True))
  
  