from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from msa_sdk.customer import Customer
from msa_sdk import util

from datetime import datetime
from msa_sdk import constants
import re
import json
import sys
import time

"""
The proposals of the task are:
 - Clean up processes

"""

time.sleep(5)

#New Variables object
TaskVariables = Variables()

context = Variables.task_call(TaskVariables)
process_id = context['SERVICEINSTANCEID']

Orchestration = Orchestration(context['UBIQUBEID'])
response = Orchestration.list_service_instances()
service_list = json.loads(Orchestration.content)


Orchestration.execute_service('Process/Ansible_integration/Ansible_Integration', 'Process/Ansible_integration/Ansible_Integration/Stop_playbook_monitoring', dict())
time.sleep(5)
Orchestration.execute_service('Process/Ansible_integration/Ansible_Integration', 'Process/Ansible_integration/Ansible_Integration/DELETE', dict())
time.sleep(5)
for service in service_list:
  if service['state'] == 'ACTIVE':
    if service['name'] in ('Process/Ansible_integration/DEMO/Configure_router_interface/Configure_router_interface',
'Process/Ansible_integration/DEMO/Configure_route_announcement/Configure_route_announcement',
'Process/Ansible_integration/DEMO/Update_DNS_records/Update_DNS_records',
'Process/Ansible_integration/DEMO/Get_router_interface/Get_router_interface',
'Process/Ansible_integration/DEMO/Import_from_IPAM/Import_from_IPAM',
'Process/Ansible_integration/Ansible_Integration',
'Process/Ansible_integration/DEMO/Execute_Ansible_based_microservice/Execute_Ansible_based_microservice',
'Process/Ansible_integration/DEMO/Clean_up_Ansible_demo/Clean_up_Ansible_demo'):
      is_finished = True
      response = Orchestration.list_process_instances_by_service(service['id'])
      for process in json.loads(Orchestration.content):
        if process['status']['status'] not in ('ENDED', 'FAILED'):
          is_finished = False
          
      if is_finished:
        Orchestration.delete_service(service['id'])      
    
#Finish the task correctlly
result = MSA_API.process_content('ENDED', 'Cleaner has been finished' , context, True)
print(result)