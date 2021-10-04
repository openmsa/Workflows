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


time.sleep(5)

#New Variables object
TaskVariables = Variables()

context = Variables.task_call(TaskVariables)
process_id = context['SERVICEINSTANCEID']

Orchestration = Orchestration(context['UBIQUBEID'])
response = Orchestration.list_service_instances()
service_list = json.loads(Orchestration.content)

for service in service_list:
  if service['state'] == 'ACTIVE':
    if service['name'] in ('Process/IP_CONTROLLER/Fulfilment_Handler/Fulfilment_Handler',
                           'Process/IP_CONTROLLER/Fulfilment_Dispatcher/Fulfilment_Dispatcher',
                           'Process/IP_CONTROLLER/Cleaner/Cleaner'):
      is_finished = True
      response = Orchestration.list_process_instances_by_service(service['id'])
      for process in json.loads(Orchestration.content):
        if process['status']['status'] != 'ENDED':
          is_finished = False
          
      if is_finished:
        Orchestration.delete_service(service['id'])      
    
#Finish the task correctlly
result = MSA_API.process_content('ENDED', 'Cleaner has been finished' , context, True)
print(result)
