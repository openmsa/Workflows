import os
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('playbook', var_type='OBMFRef')
dev_var.add('microservice_name', var_type='String')
context = Variables.task_call(dev_var)

#check_mandatory_param('playbook')
#check_mandatory_param('microservice_name')

if __name__ == "__main__":

    microservice_skeleton = context['microservice_skeleton']
    device_id = context['device_id']
    playbook = context['playbook']
    
    '''microservice_file is path to microservice that will be modified dynamically
    to read a playbook file content 
    '''
    microservice_file = context['read_playbook_file']
    #The string that contain chosen playbook path
    rewrite_string = '<operation>cat '+playbook+' '
    
    #Modify microservice file
    sed_command = 'sed -i \'s@<operation>cat [^ ]* @'+rewrite_string+'@\' '+microservice_file
    result = os.system(sed_command)
    
    #Finish task
    ret = MSA_API.process_content(constants.ENDED, 'Success. The microservice to read playbook file content has been modified.', context, True)
    print(ret)