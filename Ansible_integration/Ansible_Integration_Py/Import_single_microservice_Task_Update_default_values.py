import re
import sys
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.repository import Repository
from msa_sdk import constants


dev_var = Variables()
context = Variables.task_call(dev_var)

#Initial Repository object.
repository = Repository()

workflow_name = context['execute_workflow']
response = repository.get_workflow_definition(workflow_name)
if 'wo_status' in response:
    if response['wo_status'] == 'FAIL':
        ret = MSA_API.process_content(constants.FAILED, 'Failed to get workflow definition with name "' + workflow_name + '".', context, True)
        print(ret)
        sys.exists()

workflow_details = response

value_name = explode(".", context['microservice_file_name'])[0]
  
result = preg_match('|^(\S+?)([^/]+?\.yml)|', context['playbook'], matches)
value_display = matches[2]
  
new_value_array = dict(displayValue=value_display,displayValue_de="",displayValue_en="",displayValue_es="",displayValue_fr="",displayValue_ja="",actualValue=value_name)

foreach (workflow_details['variables']['variable'] as var=&var_details) {
  if (var_details['name'] == 'params.ansible_microservice') {
    if (!var_details['values']) {
      var_details['values'] = array()
    array_push(var_details['values'], new_value_array)

response = _repository_change_workflow_definition(workflow_name, json_encode(workflow_details))


#Clean up context
context['variables_line'] = ''
context['microservice_create_line'] = ''
context['playbook_variables'] = array()
context['microservice_name'] = ''

#Finish the task.
ret = MSA_API.process_content(constants.ENDED, 'Success. Deployment settings profile has been updated successfully.', context, True)
print(ret)