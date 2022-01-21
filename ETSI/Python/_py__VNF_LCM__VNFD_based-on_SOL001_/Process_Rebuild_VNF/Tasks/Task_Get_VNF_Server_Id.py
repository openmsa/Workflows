from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])

    r = vnfLcm.vnf_lcm_get_vnf_instance_details(context["vnf_instance_id"])

    vnfResourcesList = r.json()["instantiatedVnfInfo"]["vnfcResourceInfo"]
    context["vnfResourceId"] = vnfResourcesList[0]["computeResource"]["resourceId"]

    MSA_API.task_success('Got VNF server Id', context, True)
