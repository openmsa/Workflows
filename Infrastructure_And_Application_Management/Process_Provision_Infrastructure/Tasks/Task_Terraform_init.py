import json
import time
import sys
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('terraform_managed_entity', var_type='Device')
dev_var.add('terraform_configuration', var_type='OBMFRef')
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
device_ref = context['terraform_managed_entity']
device_id = device_ref[3:]

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

#Terraform Management WF service name constant variable.
SERVICE_NAME = 'Process/Terraform_Configuration_Management/Terraform_Configuration_Management'
CREATE_PROCESS_NAME = 'Process_New_Instance'
INIT_PROCESS_NAME = 'Process_Init'
service_id = ''
service_ext_ref = ''
# #Instantiate new Terraform Management WF dedicated for the device_id.
if not 'terraform_service_instance' in context:
    data = dict(device_id=context['terraform_managed_entity'])
    orch.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
    response = json.loads(orch.content)
    context['response'] = response
    status = response.get('status').get('status')
    if status == constants.ENDED:
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #store terraform configuration service instance ref.
            context.update(terraform_service_ext_ref=service_ext_ref)
            #Store service_instance_id of terraform_Service_Mangement WF in context.
            context['terraform_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
        else:
            ret = MSA_API.process_content(constants.FAILED, 'Missing service id return by orchestration operation.', context, True)
            print(ret)
            sys.exit()
    else:
        ret = MSA_API.process_content(constants.FAILED, 'Execute service operation failed.', context, True)
        print(ret)
        sys.exit()

#Execute terraform_Management baseline service apply process
data = dict(configuration_file=context['terraform_configuration']) 
if isinstance(data, dict):
    external_ref = context.get('terraform_service_instance').get('external_ref')
    #execute Terraform apply WF process
    context.update(SLE_DEBUG=ubiqube_id+'_'+external_ref+'_'+SERVICE_NAME+'_'+INIT_PROCESS_NAME+'_'+json.dumps(data))
    orch.execute_service_by_reference(ubiqube_id, external_ref, SERVICE_NAME, INIT_PROCESS_NAME, data)  
    response = json.loads(orch.content)
    service_id = response.get('serviceId').get('id')
    process_id = response.get('processId').get('id')
    #get service process details.
    response = get_process_instance(orch, process_id)
    status = response.get('status').get('status')
    details = response.get('status').get('details')
    if status == constants.FAILED:
        ret = MSA_API.process_content(constants.FAILED, 'Execute service operation is failed: ' + details + ' (#' + str(service_id) + ')', context, True)
        print(ret)
        sys.exit()
ret = MSA_API.process_content(constants.ENDED, 'Terraform init is executed successfully.', context, True)
print(ret)
sys.exit()