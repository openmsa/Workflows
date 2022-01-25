import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005

dev_var = Variables()
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']
vnf_service_instance_ref = context.get('SERVICEINSTANCEREFERENCE')

if __name__ == "__main__":
    
    ## Get list of VNFC vdu.
    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    r = vnfLcm.vnf_lcm_get_vnf_instance_details(context["vnf_instance_id"])
    
    #MSA_API.task_error('DEBUG = ' + json.dumps(r.json()), context)
    
    context.update(vnf_instance_details=r.json())
        
    vnfResourcesList = r.json()["instantiatedVnfInfo"]["vnfcResourceInfo"]
    
    context.update(vnfResourcesList=vnfResourcesList)
    
    #VNF Managed Entities.
    vnf_me_list = list()
    
    #For each VNFC-VDU create corresponding ME's.
    for index, item in enumerate(vnfResourcesList):
        #openstack server instance ID.
        vnfResourceId = vnfResourcesList[index]["computeResource"]["resourceId"]
    
        ## get VDU details (@IP, Hostname).
        #TODO: create VIM SDK to call Openstack API servers resources.
        
        #Customer ID
        customer_id = subtenant_ext_ref[4:]
        #Kubernetes_generic manufacturer_id
        manufacturer_id='20060101'
        #Kubernetes_generic model_id
        model_id='20060101'
        #default IP address
        management_address='1.1.1.1'
        #Kubernetes adaptor does not use the password and login of ME.
        password = 'fake38passwOrd'
        management_port='22'
        name = vnf_service_instance_ref + '_VNFC_' + vnfResourceId
        #Create Device
        device = Device(customer_id=customer_id, name=name, manufacturer_id=manufacturer_id, model_id=model_id, login='admin', password=password, password_admin=password, management_address=management_address, management_port=management_port, device_external="", log_enabled=True, log_more_enabled=True, mail_alerting=False, reporting=True, snmp_community='ubiqube', device_id="")
        response = device.create()
        context.update(device=response)
        #get device external reference
        device_ext_ref = response.get('externalReference')
        
        #Add device_ext_ref to the VNF ME list.
        vnf_me_list.append(device_ext_ref)
        
        #get device external reference
        device_id = response.get('id')
        context.update(vnf_me_id=device_id)
    
        #add ns_service_instance_ref as VNF ME variable configuration.
        if 'ns_service_instance_ref' in context:
            ns_service_instance_ref = context.get('ns_service_instance_ref')
            if ns_service_instance_ref:
                device.create_configuration_variable('nslcm_wf_service_instance_ref', ns_service_instance_ref)
                
        #add VNF LCM service instance REF:
        device.create_configuration_variable('vnflcm_wf_service_instance_ref', vnf_service_instance_ref)
        
    #Store vnf_me_list in the context.
    context.update(vnf_me_list=vnf_me_list)

    MSA_API.task_success('The VNF managed entities are created.', context)

