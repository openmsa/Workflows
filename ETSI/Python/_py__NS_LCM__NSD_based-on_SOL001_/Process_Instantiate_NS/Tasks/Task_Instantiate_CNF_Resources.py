import json
import time
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

from custom.ETSI.NsLcmSol005 import NsLcmSol005

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

'''

'''
def _create_service_instance(SERVICE_NAME, CNF_LCM_CREATE_PROCESS_NAME, data):
    orch.execute_service(SERVICE_NAME, CNF_LCM_CREATE_PROCESS_NAME, data)
    response = json.loads(orch.content)
    context['response'] = response
    process_id = response.get('processId').get('id')
    #get service process details.
    response = get_process_instance(orch, process_id)
    status = response.get('status').get('status')
    details = response.get('status').get('details')
    
    if status == constants.ENDED:
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #Store service_instance_ref of CNF_LCM_workflow in context.
            context.update(cnf_lcm_service_ref=service_ext_ref)
            
            return service_ext_ref
        else:
            MSA_API.task_error('Missing service id return by orchestration operation.', context, True) 
    else:
        MSA_API.task_error('Execute service operation is failed: ' + details + ' (#' + str(service_id) + ')', context, True)
 
'''
'''
def _execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, CNF_LCM_INSTANTIATE_PROCESS_NAME, data):
    orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, CNF_LCM_INSTANTIATE_PROCESS_NAME, data)
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

        
if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('is_cnf', var_type='String')
    dev_var.add('k8s_me_ref', var_type='Device')
    dev_var.add('service_file', var_type='String')
    dev_var.add('deployments_file', var_type='String')
    context = Variables.task_call(dev_var)
    
    #Initiate orchestraction object.
    ubiqube_id = context['UBIQUBEID']
    orch = Orchestration(ubiqube_id)
    
    #Is Multiple CNFM
    is_cnf = context.get('is_cnf')
    
    #Static Routing Management WF service name constant variable.
    SERVICE_NAME = 'Process/ETSI-MANO/WORKFLOWS/ETSI-MANO/KUBERNETES/CNF_LCM_v3__Based-on_Kubernetes_Descriptor_/CNF_LCM_v3__Based-on_Kubernetes_Descriptor_'
    CNF_LCM_CREATE_PROCESS_NAME = '/opt/fmc_repository/Process/ETSI-MANO/WORKFLOWS/ETSI-MANO/KUBERNETES/CNF_LCM_v3__Based-on_Kubernetes_Descriptor_/Process_Create_Instance'
    CNF_LCM_INSTANTIATE_PROCESS_NAME = '/opt/fmc_repository/Process/ETSI-MANO/WORKFLOWS/ETSI-MANO/KUBERNETES/CNF_LCM_v3__Based-on_Kubernetes_Descriptor_/Process_Apply'
    
    if is_cnf == 'true':
        
        #Get KUBERNETES ME configuration vars.
        k8s_me_ref = context["k8s_me_ref"]
        k8s_me_id = k8s_me_ref[3:]
        k8s_var   = Device(device_id=k8s_me_id).get_configuration_variable("KUBE_TOKEN")
        k8s_token  = k8s_var.get("value")

        #Service external ref init.
        service_ext_ref = ''
        
        #List of CNF LCM service instances.
        if 'cnf_lcm_service_ref' in context:
            service_ext_ref = context.get('cnf_lcm_service_ref')
        else:
            #Create CNF LCM service instance.
            service_ext_ref = _create_service_instance(SERVICE_NAME, CNF_LCM_CREATE_PROCESS_NAME, {})
            
        # CNF dployments configuration.
        deployments_file = context.get('deployments_file')
        if deployments_file:
            #Execute CNF Instantiate (as existing CNFi) process of CNF LCM workflow.
            data = dict(deviceid=k8s_me_ref, auth_method='KUBERNETES', kube_token=k8s_token, namespace='default', resource='deployments', file=deployments_file)
            _execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, CNF_LCM_INSTANTIATE_PROCESS_NAME, data)
            
        # CNF service configuration.
        service_file = context.get('service_file')
        if service_file:
            #Execute CNF Instantiate (as existing CNFi) process of CNF LCM workflow.
            data = dict(deviceid=k8s_me_ref, auth_method='KUBERNETES', kube_token=k8s_token, namespace='default', resource='services', file=service_file)
            _execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, CNF_LCM_INSTANTIATE_PROCESS_NAME, data)
        
        MSA_API.task_success( 'CNF resources are instantiated.', context, True)
        
    MSA_API.task_success( 'Skip CNF LCM service instances creation.', context, True)