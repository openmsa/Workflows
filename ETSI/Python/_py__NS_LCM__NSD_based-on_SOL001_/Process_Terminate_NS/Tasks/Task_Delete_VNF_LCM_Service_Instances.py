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
    SERVICE_NAME = 'Process/Telekom_Malaysia/_py__VNF_LCM__VNFD_based-on_SOL001_/_py__VNF_LCM__VNFD_based-on_SOL001_'
    VNF_LCM_INSTANTIATE_PROCESS_NAME = 'Process/Telekom_Malaysia/_py__VNF_LCM__VNFD_based-on_SOL001_/Process_Delete_VNF_Instance'
    
    #Get from context VNF LCM service instances dict.
    vnf_lcm_services_list = context.get('vnf_lcm_services_list')
    
    if not isinstance(vnf_lcm_services_list, list):
        MSA_API.task_success('No VNF LCM services instances to be deleted.', context, True)
    
    for index, vnf_lcm_service in enumerate(vnf_lcm_services_list):
        
        service_id = vnf_lcm_service.get('service_id')
        service_ext_ref = vnf_lcm_service.get('service_ext_ref')
        instance_name = vnf_lcm_service.get('vnf_instance_id')
        
        if service_ext_ref:
            #Execute VNF Instantiate (as existing VNFi) process of VNF LCM workflow.
            orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, VNF_LCM_INSTANTIATE_PROCESS_NAME, dict())
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
        
    MSA_API.task_success('VNF LCM services instances are deleted.', context, True)
