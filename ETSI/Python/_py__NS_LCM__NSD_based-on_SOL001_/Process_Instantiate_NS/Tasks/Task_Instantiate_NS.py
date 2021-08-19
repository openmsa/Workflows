from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NsLcmSol005 import NsLcmSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('ns_package_id', var_type='String')
    context = Variables.task_call(dev_var)
    
    nsLcm = NsLcmSol005(context["mano_ip"], context["mano_port"])
    nsLcm.set_parameters(context["mano_user"], context["mano_pass"])
    
    ns_instance_id = context["ns_instance"]["id"]

    r = nsLcm.ns_lcm_instantiate_ns(ns_instance_id)
    
    location = r.headers["Location"]

    context["ns_lcm_op_occ_id"] = location.split("/")[-1]

    ret = MSA_API.process_content('ENDED', f'{context["ns_lcm_op_occ_id"]}',
                                  context, True)
    print(ret)