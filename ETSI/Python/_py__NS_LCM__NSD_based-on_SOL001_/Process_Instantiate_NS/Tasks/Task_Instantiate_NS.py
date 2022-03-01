from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
import json
from custom.ETSI.NsLcmSol005 import NsLcmSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('ns_package_id', var_type='String')
    dev_var.add('is_multiple_vnfm', var_type='Boolean')
    context = Variables.task_call(dev_var)
    
    nsLcm = NsLcmSol005(context["mano_ip"], context["mano_port"])
    nsLcm.set_parameters(context["mano_user"], context["mano_pass"])
    
    ns_instance_id = context.get("ns_instance_id")
    
    content = {'nsFlavourId': 'flavor'}

    r = nsLcm.ns_lcm_instantiate_ns(ns_instance_id, content)
    
    if nsLcm.state != "ENDED":
        ret = MSA_API.process_content(nsLcm.state, f'{context["ns_lcm_op_occ_id"]}',
                                      context, True)
        print(ret)
        exit()
    
    location = r.headers["Location"]

    context["ns_lcm_op_occ_id"] = location.split("/")[-1]

    ret = MSA_API.process_content(nsLcm.state, f'{context["ns_lcm_op_occ_id"]}',
                                  context, True)
    print(ret)