from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NsLcmOpOccsSol005 import NsLcmOpOccsSol005


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    nsLcmOpOccsInfo = NsLcmOpOccsSol005(context["mano_ip"], context["mano_port"])
    nsLcmOpOccsInfo.set_parameters(context['mano_user'], context['mano_pass'])

    r = nsLcmOpOccsInfo.ns_lcm_op_occs_completion_wait(context["ns_lcm_op_occ_id"])
    
    context["ns_lcm_op_occs"] = r.json()
    operationState = context["ns_lcm_op_occs"]["operationState"]

    ret = MSA_API.process_content('ENDED', f'{operationState}', context, True)
    print(ret)