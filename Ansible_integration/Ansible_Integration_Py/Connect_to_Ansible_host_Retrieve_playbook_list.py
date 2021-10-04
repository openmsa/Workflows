import os
import sys
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('playbook_path', var_type='String')
dev_var.add('microservice_skeleton', var_type='String')
dev_var.add('microservice_dir', var_type='String')
dev_var.add('do_import_hosts', var_type='Boolean')
context = Variables.task_call(dev_var)


Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])


if __name__ == "__main__":
    
    #Grab variable from context.
    device_id = context['device_id'][3:]
    
    #Instantiate Order object.
    order = Order(device_id)

    Orchestration.update_asynchronous_task_details(*async_update_list, f'Modyfing microservice to read playbook list... OK')
    
    '''
    $microservice_file is path to microservice that dynamically updated based on
    directory where Ansible playbooks located are. The microservice is proposed to extract
    avaliable playbooks.
    '''
    microservice_file = context['retrieve_playbook_files']
    
    #Define playbook dir inside microservice.
    rewrite_string = '<operation>for file in ' + context["playbook_path"] + '/*.yml; do md5sum \$file; done</operation>'
    
    #Modify microservice with new playbook directory.
    sed_command = 'sed -i "s|<operation.*|' + rewrite_string + '|" ' + microservice_file
    result = os.system(sed_command)
    
    if result != 0:
        ret = MSA_API.process_content(constants.FAILED, 'Failed. Modyfing microservice to read playbook list... NOK.', context, True)
        print(ret)
        sys.exit()
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Modyfing microservice to read playbook list... OK')
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Syncing Ansible host... ')
    
    #Sync out ansible ME to grab avaliable playbooks.
    timeout = 60
    order.command_synchronize(timeout)
#     response = json.loads(order.content)
#     
#     if response.get('wo_status') == constants.FAILED:
#         detials = ''
#         if 'wo_newparams' in response:
#             detials = response.get('wo_newparams')
#             ret = MSA_API.process_content(constants.FAILED, 'Failed. Failure details: ' + detials, context, True)
#             print(ret)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Syncing Ansible host... OK')
    
    #Finish the task
    ret = MSA_API.process_content(constants.ENDED, 'Success. The microservice to gather avaliable playbooks has been modified.', context, True)
    print(ret)