from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import json
import re

"""
The proposals of the task are:


"""


#New Variables object
TaskVariables = Variables()

#Add new variables
TaskVariables.add('tenant', var_type = 'String')
TaskVariables.add('site', var_type = 'String')
TaskVariables.add('ipam_device_id', var_type = 'Device')

#Add vars to context
context = Variables.task_call(TaskVariables)
context['ipam_device_id'] = re.match('^\D+?(\d+?)$', context['ipam_device_id']).group(1)

#Import microservice alias list
with open('/opt/fmc_repository/Process/Ansible_integration/microservice_list.json', 'r') as alias_file:
  	context['ipam_ms_aliases'] = json.load(alias_file)


#Finish the task correctlly
result = MSA_API.process_content('ENDED', 'All variables have been defined successfully', context, True)
print(result)
