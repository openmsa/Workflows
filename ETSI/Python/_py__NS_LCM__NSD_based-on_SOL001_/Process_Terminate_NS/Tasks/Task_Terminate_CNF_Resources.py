import json
import time
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration

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
def get_process_instance(orch, process_id, timeout = 600, interval=5):
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

if __name__ == "__main__":
    dev_var = Variables()
    context = Variables.task_call(dev_var)
    
    #Initiate orchestraction object.
    ubiqube_id = context['UBIQUBEID']
    orch = Orchestration(ubiqube_id)
    
    #Static Routing Management WF service name constant variable.
    SERVICE_NAME = 'Process/ETSI-MANO/WORKFLOWS/ETSI-MANO/KUBERNETES/CNF_LCM_v3__Based-on_Kubernetes_Descriptor_/CNF_LCM_v3__Based-on_Kubernetes_Descriptor_'
    CNF_LCM_TERMINATE_PROCESS_NAME = '/opt/fmc_repository/Process/ETSI-MANO/WORKFLOWS/ETSI-MANO/KUBERNETES/CNF_LCM_v3__Based-on_Kubernetes_Descriptor_/Process_Terminate_CNF'
    
    is_cnf = context.get('is_cnf')
    
    if is_cnf == 'true':
        #Get from context CNF LCM service instances dict.
        service_ext_ref = context.get('cnf_lcm_service_ref')
        
        if not service_ext_ref:
            MSA_API.task_success('No CNF LCM services instances to be deleted.', context, True)
            
        elif service_ext_ref:
            #Execute CNF Instantiate (as existing CNFi) process of CNF LCM workflow.
            orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, CNF_LCM_TERMINATE_PROCESS_NAME, dict())
            response = json.loads(orch.content)
            context.update(nslcm_response=response)
            service_id = response.get('serviceId').get('id')
            process_id = response.get('processId').get('id')
            
            #get service process details.
            response = get_process_instance(orch, process_id)
            status = response.get('status').get('status')
            details = response.get('status').get('details')
            if status == constants.FAILED:
                MSA_API.task_error('Execute service operation is failed: ' + details + ' (#' + str(service_id) + ')', context, True)
            
    MSA_API.task_success('CNF LCM services instances are deleted.', context, True)
