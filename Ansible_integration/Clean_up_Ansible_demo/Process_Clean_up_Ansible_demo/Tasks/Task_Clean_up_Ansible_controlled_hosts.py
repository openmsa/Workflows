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
 - Execute a playbook what cleans Linux host states:
  - Remove lldpd packet;
  - Flush Iptables;
  - Flush routes;
  - Flush interface config

"""

#New Variables object
TaskVariables = Variables()

#Add vars to context
context = Variables.task_call(TaskVariables)

#Define additional variables
process_id = context['SERVICEINSTANCEID']

#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

#Create Repository object
RepositoryObject = Repository()

#Create Order object for Ansible host
AnsibleOrderObject = Order(context['ansible_device_id'])
AnsibleOrderObject.command_synchronize(300)

#Get default values for microservice
deployment_settings_id = AnsibleOrderObject.command_get_deployment_settings_id()
microservice_path = RepositoryObject.get_microservice_path_by_name(context['ansible_rollback_ms'], deployment_settings_id)
microservice_variables = RepositoryObject.get_microservice_variables_default_value(microservice_path)

#Walk through the provided Ansible-based microservice variables. If the variable exists in exchange dict --> get the value.
#Else - empty string
object_dict = dict()
if microservice_variables:
	for variable in microservice_variables:
		if variable == 'playbook_path':
			object_dict[variable] = microservice_variables['playbook_path'] 
		else:
			object_dict[variable] = str()

	ms_dict = {context['ansible_rollback_ms']: {'': object_dict}}
	AnsibleOrderObject.command_execute('CREATE', ms_dict)

success_comment = 'Microservice {} has executed Ansible playbook successfully'.format(context['ansible_rollback_ms'])

#Finish the task correctlly
print(MSA_API.process_content('ENDED', success_comment , context, True))