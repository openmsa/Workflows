from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.customer import Customer
from msa_sdk.repository import Repository
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
 - Remove default values for ansible-based microservice name in 
 the workflow what executes  ansible-based microservices

"""

#New Variables object
TaskVariables = Variables()


#Add vars to context
context = Variables.task_call(TaskVariables)


#Udate exchange file
with open(context['exchange_file'], 'r') as exchange_file:
    exchange_dict = json.load(exchange_file)

process_id = context['SERVICEINSTANCEID']

#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

customer_id = re.match('^\D+?(\d+?)$',context['UBIQUBEID']).group(1)
CustomerObject = Customer()
RepositoryObject = Repository()
deployment_settings_list = CustomerObject.get_deployment_settings_by_customer_id(customer_id)
ansible_profile = dict()
counter = 0
while not ansible_profile and counter < len(deployment_settings_list):
  if int(context['ansible_device_id']) in deployment_settings_list[counter]['attachedManagedEntities']:
    ansible_profile = deployment_settings_list[counter]
  counter += 1
ms_list = list()
for microservice_uri, microservice_details in ansible_profile['microserviceUris'].items():
  if 'Ansible-based' in microservice_details['groups']:
    ms_list.append(microservice_uri)
RepositoryObject.detach_microserviceis_from_configuration_profile(ansible_profile['id'], ms_list)

for microservice_uri in ms_list:
  RepositoryObject.delete_repository_resource(microservice_uri)

workflow_details = RepositoryObject.get_workflow_definition(context['ansible_execute_wf'])

for variable, details in enumerate(workflow_details['variables']['variable']):
  if details['name'] == 'params.ansible_microservice':
    details['values'] = list()
    

RepositoryObject.change_workflow_definition(context['ansible_execute_wf'], workflow_details)

result = MSA_API.process_content('ENDED', 'Ansible-based microservices have been removed', context, True)
print(result)

