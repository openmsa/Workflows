import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005

'''
Check if VNFC resource is exist in the context.
'''
def is_vnfc_resource_exist(vnfc_resource_id, vnf_me_list):
    for index, vnfc_resource_dict in enumerate(vnf_me_list):
        if vnfc_resource_id == vnfc_resource_dict.get('vnf_resource_id'):
            return True
    return False

dev_var = Variables()
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']

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
    if 'vnf_me_list' in context:
        vnf_me_list = context.get('vnf_me_list')
    else:
        context['vnf_me_list'] = vnf_me_list
    
    #For each VNFC-VDU create corresponding ME's.
    for index, vnfc_dict in enumerate(vnf_me_list):
        #openstack server instance ID.
        vnf_resource_id = vnfc_dict.get('vnf_resource_id')
        device_ref = vnfc_dict.get('device_ext_ref')
        
        #check if the VNFC ME is already created.
        is_vnfc_me_exist = is_vnfc_resource_exist(vnf_resource_id, vnfResourcesList)
        
        if is_vnfc_me_exist == False:
            device_id = device_ref[3:]
            #initialize Device object based-on the device id.
            device = Device(device_id=device_id)
            try:
                #remove managed entity.
                device.delete(device_ref)
            except:
                continue
        #Remove vnfc resource object from list.
        vnf_me_list.remove(vnfc_dict)
        
    MSA_API.task_success('The VNF managed entities are deleted.', context)