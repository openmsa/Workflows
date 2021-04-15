from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.repository import Repository
from msa_sdk.orchestration import Orchestration
from datetime import datetime
from msa_sdk import constants
from msa_sdk import lookup
from msa_sdk import util
import json
import sys
import time
import re


"""
The proposals of the tasks are:

"""

#New Variables object
TaskVariables = Variables()

#Add new variables
TaskVariables.add('ansible_device_id', var_type = 'Device')
TaskVariables.add('ansible_microservice', var_type = 'String')

#Add vars to context
context = Variables.task_call(TaskVariables)
context['ansible_device_id'] = re.match('^\D+?(\d+?)$', context['ansible_device_id']).group(1)

process_id = context['SERVICEINSTANCEID']

#Udate exchange file
with open(context['exchange_file'], 'r') as exchange_file:
    exchange_dict = json.load(exchange_file)

process_id                   = context['SERVICEINSTANCEID']
site_ip_plan			 	 = exchange_dict['site_ip_plan']

#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

#Create Ansible order object
RepositoryObject = Repository()
AnsibleOrderObject = Order(context['ansible_device_id'])
AnsibleOrderObject.command_synchronize(300)

#Get default values for microservice
deployment_settings_id = AnsibleOrderObject.command_get_deployment_settings_id()
microservice_path = RepositoryObject.get_microservice_path_by_name(context['ansible_microservice'], deployment_settings_id)
microservice_variables = RepositoryObject.get_microservice_variables_default_value(microservice_path)

#Get list of IP addresses to configure on servers
ip_list = list()
for device, details in site_ip_plan.items():
  if re.match('srv', device):
    ip_list.append(details)
    

ms_dict = {context['ansible_microservice']: {'': {'object_id': '',
                                                  'playbook_path': microservice_variables['playbook_path'],
                                                  'server_1_iface': ip_list[0]['interface'],
                                                  'server_1_ip_address': ip_list[0]['ip_address'].split('/')[0],
                                                  'server_1_prefix_len':ip_list[0]['ip_address'].split('/')[1],
                                                  'server_2_iface': ip_list[1]['interface'],
                                                  'server_2_ip_address': ip_list[1]['ip_address'].split('/')[0],
                                                  'server_2_prefix_len':ip_list[1]['ip_address'].split('/')[1]
                                                 }
                                            }
          }
AnsibleOrderObject.command_execute('CREATE', ms_dict)

success_comment = 'IP addresses have been configured on host interfaces'

#Finish the task correctlly
print(MSA_API.process_content('ENDED', success_comment , context, True))