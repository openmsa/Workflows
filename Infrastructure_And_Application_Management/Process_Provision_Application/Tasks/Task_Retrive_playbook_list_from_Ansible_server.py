import json
import time
import sys
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('ansible_me', var_type='Device')
dev_var.add('ansible_playbook', var_type='String')
dev_var.add('do_import_hosts', var_type='Boolean')
dev_var.add('playbook_path', var_type='String')
dev_var.add('microservice_skeleton', var_type='String')
dev_var.add('microservice_dir', var_type='String')
dev_var.add('execute_workflow', var_type='String')
context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################

'''
Retrieve process instance by service instance ID.

@param orch:
    Ochestration class object reference.
@param service_id:
    Baseline workflow service instance ID.
@param timeout:
    loop duration before to break.
@param interval:
    loop time interval.
@return:
    Response of the get process instance execution.
'''
def get_process_instance(orch, process_id, timeout=60, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #get service instance execution status.
        orch.get_process_instance(process_id)
        response = json.loads(orch.content)
        status = response.get('status').get('status')
        #context.update(get_process_instance=status)
        if status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)

    return response
####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Get device id from context (e.g: UBI2455).
device_ref = context['ansible_me']
device_id = device_ref[3:]

#Initiate orchestration object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

#ansible_integration Management WF service name constant variable.
SERVICE_NAME = 'Process/Ansible_integration/Ansible_Integration/Ansible_integration'
CREATE_PROCESS_NAME = 'Process/Ansible_integration/Ansible_Integration/Connect_to_Ansible_host'
service_id = ''
service_ext_ref = ''

# #Instantiate new ansible_integration Management WF dedicated for the device_id.
if not 'ansible_integration_service_instance' in context:
    #import hosts by default.
    data = dict(device_id=context['ansible_me'], playbook_path=context['playbook_path'], do_import_hosts=True, microservice_skeleton=context['microservice_skeleton'], microservice_dir=context['microservice_dir'], execute_workflow=context['execute_workflow'])
    orch.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
    response = json.loads(orch.content)
    context['response'] = response
    #get service process details.
    process_id = response.get('processId').get('id')
    response = get_process_instance(orch, process_id)
    details = response.get('status').get('details')
    status = response.get('status').get('status')
    if status == constants.ENDED:
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #Store service_instance_id of ansible_integration_Service_Mangement WF in context.
            context['ansible_integration_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
        else:
            ret = MSA_API.process_content(constants.FAILED, 'Missing service id return by orchestration operation.', context, True)
            print(ret)
            sys.exit()
    else:
        ret = MSA_API.process_content(constants.FAILED, 'Execute service operation failed:' + details + ' (#' + str(service_id) + ')', context, True)
        print(ret)
        sys.exit()
ret = MSA_API.process_content('ENDED', 'Ansible playbook list is retrieved successfully.', context, True)
print(ret)
sys.exit()