import sys
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfLcmOpOccsSol003 import VnfLcmOpOccsSol003


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)
    
    if context.get('is_vnf_instance_exist') != True:
        vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
        vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
        
        content = {'flavourId': 'flavor'}

        r = vnfLcm.vnf_lcm_instantiate_vnf(context["vnf_instance_id"], content)
    
        location = r.headers['Location']
        
        context["vnf_lcm_op_occ_id"] = location.split("/")[-1]
        
        ret = MSA_API.process_content(vnfLcm.state, f'{r}', context, True)
        print(ret)
        sys.exit()
    else:
        vnfLcmOpOccs = VnfLcmOpOccsSol003(context["mano_ip"], context["mano_port"])
        vnfLcmOpOccs.set_parameters(context['mano_user'], context['mano_pass'])
        
        vnf_instance_id = context['vnf_instance_id']
        
        vnf_lcm_op_occ_id = vnfLcmOpOccs.vnf_lcm_op_occs_get_id(vnf_instance_id)
        context["vnf_lcm_op_occ_id"] = vnf_lcm_op_occ_id
        
        #MSA_API.task_error('The VNF managed entities are created.' + vnf_lcm_op_occ_id, context)
    
    ret = MSA_API.process_content(vnfLcmOpOccs.state, f'VNF Instance context is stored.', context, True)
    print(ret)
    sys.exit()