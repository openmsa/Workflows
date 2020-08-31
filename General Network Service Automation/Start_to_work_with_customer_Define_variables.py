from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import json

#New Variables object
task_variables = Variables()

#Add new variables
task_variables.add('customer_name', var_type = 'String')
task_variables.add('ipam_device_id', var_type = 'Device')

#Add vars to context
context = Variables.task_call(task_variables)

#Import microservice alias list
with open('/opt/fmc_repository/Process/General_network_service_automation/microservices_list.json', 'r') as alias_file:
  	context['ipam_ms_aliases'] = json.load(alias_file)


#Finish the task correctlly
result = MSA_API.process_content('ENDED', 'All variables have been defined successfully', context, True)
print(result)
