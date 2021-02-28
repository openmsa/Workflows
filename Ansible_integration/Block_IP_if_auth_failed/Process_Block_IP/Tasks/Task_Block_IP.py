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


#Add vars to context
context = Variables.task_call(TaskVariables)

process_id = context['SERVICEINSTANCEID']

process_id                   = context['SERVICEINSTANCEID']

#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

AnsibleOrderObject = Order(context['ansible_device_id'])
AnsibleOrderObject.command_synchronize(300)

RepositoryObject = Repository()

#Get default values for microservice
deployment_settings_id = AnsibleOrderObject.command_get_deployment_settings_id()
util.log_to_process_file(process_id, 'PROFILE ID {}'.format(deployment_settings_id))
microservice_path = RepositoryObject.get_microservice_path_by_name(context['ansible_microservice'], deployment_settings_id)
microservice_variables = RepositoryObject.get_microservice_variables_default_value(microservice_path)
    

for ip in context['block_ip_list']:
    ms_dict = {context['ansible_microservice']: {'': {'object_id': '',
                                                      'playbook_path': microservice_variables['playbook_path'],
                                                      'dport': '22',
                                                      'sip': ip
                                                     }
                                                }
              }
    AnsibleOrderObject.command_execute('CREATE', ms_dict)
if context['block_ip_list']:
    success_comment = 'All IP addresses have been blocked'
else:
    success_comment = 'There is no IP addresses to block'

#Finish the task correctlly
print(MSA_API.process_content('ENDED', success_comment , context, True))