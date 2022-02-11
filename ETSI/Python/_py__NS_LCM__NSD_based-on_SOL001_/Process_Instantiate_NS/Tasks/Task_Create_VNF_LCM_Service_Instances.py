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
def _create_service_instance(vnf_lcm_services_list, SERVICE_NAME, VNF_LCM_CREATE_PROCESS_NAME, data):
    orch.execute_service(SERVICE_NAME, VNF_LCM_CREATE_PROCESS_NAME, data)
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
            #Store service_instance_id of VNF_LCM_workflow in context.
            service_data = {'vnf_instance_id': vnf_instance_id, 'service_id': str(service_id), 'service_ext_ref': service_ext_ref}
            vnf_lcm_services_list.append(service_data.copy())
            
            return service_ext_ref
        else:
            MSA_API.task_error('Missing service id return by orchestration operation.', context, True) 
    else:
        MSA_API.task_error('Execute service operation is failed: ' + details + ' (#' + str(service_id) + ')', context, True)
 
'''
'''
def _execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, VNF_LCM_INSTANTIATE_PROCESS_NAME, data):
    orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, VNF_LCM_INSTANTIATE_PROCESS_NAME, data)
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

'''
'''
def _is_vnflcm_service_instance_exist(vnf_instance_id, vnf_lcm_services_list):
    for index, vnf_lcm_services_dict in enumerate(vnf_lcm_services_list):
        if vnf_instance_id == vnf_lcm_services_dict.get('vnf_instance_id'):
            return True
    return False
        
if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)
    
    #Initiate orchestraction object.
    ubiqube_id = context['UBIQUBEID']
    orch = Orchestration(ubiqube_id)
    
    #Static Routing Management WF service name constant variable.
    SERVICE_NAME = 'Process/Telekom_Malaysia/_py__VNF_LCM__VNFD_based-on_SOL001_/_py__VNF_LCM__VNFD_based-on_SOL001_'
    VNF_LCM_CREATE_PROCESS_NAME = 'Process/Telekom_Malaysia/_py__VNF_LCM__VNFD_based-on_SOL001_/Process_Create_VNF_Instance'
    VNF_LCM_INSTANTIATE_PROCESS_NAME = 'Process/Telekom_Malaysia/_py__VNF_LCM__VNFD_based-on_SOL001_/Process_Instantiate_VNF'
    
    #Get NS Instance details.
    nsLcm = NsLcmSol005(context["mano_ip"], context["mano_port"])
    nsLcm.set_parameters(context["mano_user"], context["mano_pass"])
    
    #ns_instance_id = context["ns_instance"]["id"]
    ns_instance_id = context["ns_instance_id"]
    
    r = nsLcm.ns_lcm_get_ns_instance_details(context["ns_instance_id"])
    
    context.update(ns_instance_details=r.json())
    
    ns_instance_details = r.json()
    context.update(ns_instance_DEBUGn = r.json())
    vnfInstance_list = ns_instance_details["vnfInstance"]
    
    context.update(vnfInstance_list=vnfInstance_list)
    
    #Service external ref init.
    service_ext_ref = ''
    
    #List of VNF LCM service instances.
    vnf_lcm_services_list = list()
    if 'vnf_lcm_services_list' in context:
        vnf_lcm_services_list = context.get('vnf_lcm_services_list')
    else:
        context['vnf_lcm_services_list'] = vnf_lcm_services_list
    
    #For each VNF part of the NS Instance, create VNF LCM service instance.
    for index, vnfInstance in enumerate(vnfInstance_list):
        ns_service_instance_ref = context['SERVICEINSTANCEREFERENCE']
        vnfm_device = context['vnfm_device']
        nfvo_device = context['nfvo_device']
        
        #retrieve from NS Instance response (GET).
        vnf_instance_id = vnfInstance['id']
        vnf_pkg_id = vnfInstance['vnfPkgId']
        
        #check if vnf_instance corresponding VNF LCM service instance exists, if not create it.
        is_vnflcm_service_instance = _is_vnflcm_service_instance_exist(vnf_instance_id, vnf_lcm_services_list)
        if is_vnflcm_service_instance == False:
            #VNF LCM service instance creation inputs data.
            data = dict(nfvo_device=nfvo_device, vnfm_device=vnfm_device, vnf_pkg_id=vnf_pkg_id, vnf_instance_id=vnf_instance_id, ns_service_instance_ref=ns_service_instance_ref, is_vnf_instance_exist=True)
            #Create VNF LCM service instance.
            service_ext_ref = _create_service_instance(vnf_lcm_services_list, SERVICE_NAME, VNF_LCM_CREATE_PROCESS_NAME, data)
    	
        #Execute VNF Instantiate (as existing VNFi) process of VNF LCM workflow.
        data = dict()
        _execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, VNF_LCM_INSTANTIATE_PROCESS_NAME, data)
        
    MSA_API.task_success( 'VNF LCM service instances are created successfully.', context, True)