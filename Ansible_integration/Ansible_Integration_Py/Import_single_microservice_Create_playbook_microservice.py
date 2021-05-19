from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants

dev_var = Variables()
context = Variables.task_call(dev_var)

#Gather vars from context
microservice_variables_array = context['microservice_variables']
playbook_variables_array = context['playbook_variables']
playbook = context['playbook']
variable_skeleton = context['variable_skeleton']

'''
Dynamically change playbook path. 
This is required to execute playbook on Ansible host
'''
microservice_variables_array['var_playbook_path'] = playbook
microservice_variables_array['var_ansible_hosts'] = context['ansible_hosts']

#Create a string that contains new variables to write to MS file
microservice_create_vars = ''
for var in playbook_variables_array:
    var_attributes = playbook_variables_array[var]
    #current_variable = sprintf(variable_skeleton, var_attributes['prompt'], var, var_attributes['default']) #TODO convert PHP --> Python
    microservice_variables_array[var] = current_variable
    microservice_create_vars += var + '={params.' + var +' '


#Create a string that is used as command for CREAT method
microservice_create_line = '<operation>ansible-playbook:params.playbook_path --extra-vars "' + microservice_create_vars + '"</operation>'
variable_line = '  <variables frozen="0">\n'

for var in microservice_variables_array:
    variable_line += var + '\n'

variable_line += '  </variables>\n'

#Preserve the strings for next task
context['variables_line'] = variable_line
context['microservice_create_line'] = microservice_create_line

#Finish the task
ret = MSA_API.process_content(constants.ENDED, 'Success. All parameters have been prepared to create microservice dynamically', context, True)
print(ret)