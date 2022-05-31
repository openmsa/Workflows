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

if __name__ == "__main__":
    
    #Get VNF Managed Entities list.
    vnf_me_list = context.get('vnf_me_list')
    
    #For each VNFC-VDU create corresponding ME's.
    if isinstance(vnf_me_list, list):
	    for index, vnfc_dict in enumerate(vnf_me_list):
	        device_ref = vnfc_dict.get('device_ext_ref')
	        device_id = device_ref[3:]
	        #initialize Device object based-on the device id.
	        device = Device(device_id=device_id)
	        try:
	            #remove managed entity.
	            device.delete(device_ref)
	        except:
	            continue
            
    MSA_API.task_success('The VNF managed entities are deleted.', context)

