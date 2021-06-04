import json
import time
import sys
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('playbook_ms_ref_name', var_type='String')
dev_var.add('playbook_filename', var_type='OBMFRef')
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

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

#ansible_integration Management WF service name constant variable.
SERVICE_NAME = 'Process/Ansible_integration/Ansible_Integration/Ansible_integration'
IMPORT_PLAYBOOK_PROCESS_NAME = 'Process/Ansible_integration/Ansible_Integration/Import_single_microservice'
service_id = ''
service_ext_ref = ''

#Execute ansible_integration_Management baseline service apply process
data = dict(playbook=context['playbook_filename'],microservice_name=context['playbook_ms_ref_name']) 
if isinstance(data, dict):
    #Get ansible_integration management service instance reference.
    service_ext_ref = context.get('ansible_integration_service_instance').get('external_ref')
    #execute ansible_integration apply WF process
    orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, IMPORT_PLAYBOOK_PROCESS_NAME, data)
    response = json.loads(orch.content)
    service_id = response.get('serviceId').get('id')
    process_id = response.get('processId').get('id')
    #get service process details.
    response = get_process_instance(orch, process_id, 300)
    status = response.get('status').get('status')
    details = response.get('status').get('details')
    if status == constants.FAILED:
        ret = MSA_API.process_content(constants.FAILED, 'Execute service operation is failed: ' + details + ' (#' + str(service_id) + ')', context, True)
        print(ret)
        sys.exit()
ret = MSA_API.process_content('ENDED', 'The ansible playbook is imported successfully.', context, True)
print(ret)
sys.exit()