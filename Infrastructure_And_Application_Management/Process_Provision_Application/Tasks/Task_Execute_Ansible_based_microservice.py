import json
import time
import sys
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('exchange_file', var_type='String')
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

#execute_ansible_playbook Management WF service name constant variable.
SERVICE_NAME = 'Process/Ansible_integration/DEMO/Execute_Ansible_based_microservice/Execute_Ansible_based_microservice'
EXECUTE_PROCESS_NAME = 'Process/Ansible_integration/DEMO/Execute_Ansible_based_microservice/Process_Execute_microservice'
service_id = ''
service_ext_ref = ''

# #Instantiate new execute_ansible_playbook Management WF dedicated for the device_id.
if not 'execute_ansible_playbook_service_instance' in context:
    #import hosts by default.
    data = dict(ansible_device_id=context['ansible_me'], ansible_microservice=context['playbook_ms_ref_name'], exchange_file=context['exchange_file'])
    orch.execute_service(SERVICE_NAME, EXECUTE_PROCESS_NAME, data)
    response = json.loads(orch.content)
    context['response'] = response
    #get service process details.
    process_id = response.get('processId').get('id')
    response = get_process_instance(orch, process_id, 600)
    details = response.get('status').get('details')
    status = response.get('status').get('status')
    if status == constants.ENDED:
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #Store service_instance_id of execute_ansible_playbook_Service_Mangement WF in context.
            context['execute_ansible_playbook_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
        else:
            ret = MSA_API.process_content(constants.FAILED, 'Missing service id return by orchestration operation.', context, True)
            print(ret)
            sys.exit()
    else:
        ret = MSA_API.process_content(constants.FAILED, 'Execute service operation failed:' + details + ' (#' + str(service_id) + ')', context, True)
        print(ret)
        sys.exit()
ret = MSA_API.process_content('ENDED', 'Ansible playbook is executed based-on microservice successfully.', context, True)
print(ret)
sys.exit()