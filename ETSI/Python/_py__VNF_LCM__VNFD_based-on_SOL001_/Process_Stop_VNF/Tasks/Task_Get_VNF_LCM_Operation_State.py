from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants

from custom.ETSI.VnfLcmOpOccsSol003 import VnfLcmOpOccsSol003


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)
    
    if context.get('is_vnf_instance_exist') == True:
        MSA_API.task_success('Task execution is completed.', context)

    vnfLcmOpOccs = VnfLcmOpOccsSol003(context["mano_ip"], context["mano_port"], context['mano_base_url'])
    vnfLcmOpOccs.set_parameters(context['mano_user'], context['mano_pass'])
    
    vnf_lcm_op_occ_id = context.get('vnf_lcm_op_occ_id')
    operation_state = ''
    
    if 'vnf_lcm_op_occ_id' in context and vnf_lcm_op_occ_id:
        r = vnfLcmOpOccs.vnf_lcm_op_occs_completion_wait(vnf_lcm_op_occ_id)
        
        operation_state = r.json()['operationState']
        context["operation_state"] = operation_state
        
    if operation_state == "FAILED":
        MSA_API.task_error('The VNF stop operation is ' + operation_state + '.', context, True)
    
    ret = MSA_API.process_content(vnfLcmOpOccs.state, f'{operation_state}', context, True)
    print(ret)
