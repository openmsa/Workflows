from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfLcmOpOccsSol003 import VnfLcmOpOccsSol003


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    vnfLcmOpOccs = VnfLcmOpOccsSol003(context["mano_ip"], context["mano_port"])
    vnfLcmOpOccs.set_parameters(context['mano_user'], context['mano_pass'])

    r = vnfLcmOpOccs.vnf_lcm_op_occs_operation_status_get(context["vnf_lcm_op_occ_id"])

    # context["vnfServerId"] = r.json()['resourceChanges']['affectedVnfcs'][0]['vnfdId']
    context["vnfServerId"] = r.json()

    MSA_API.task_success('Got VNF server Id', context, True)
