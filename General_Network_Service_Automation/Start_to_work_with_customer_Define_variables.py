from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import json
import re

"""
The prposals of the task are:
  - Retrive variables from customer;
  - Retrieve microservice variables from file
  - Put the variables to context

"""


#New Variables object
TaskVariables = Variables()

#Add new variables
TaskVariables.add('customer_name', var_type = 'String')
TaskVariables.add('ipam_device_id', var_type = 'Device')

#Add vars to context
context = Variables.task_call(TaskVariables)
context['ipam_device_id'] = re.match('^\D+?(\d+?)$', context['ipam_device_id']).group(1)


#Import microservice alias list
with open('/opt/fmc_repository/Process/General_network_service_automation/microservices_list.json', 'r') as alias_file:
  	context['ipam_ms_aliases'] = json.load(alias_file)


#Finish the task correctlly
result = MSA_API.process_content('ENDED', 'All variables have been defined successfully', context, True)
print(result)
