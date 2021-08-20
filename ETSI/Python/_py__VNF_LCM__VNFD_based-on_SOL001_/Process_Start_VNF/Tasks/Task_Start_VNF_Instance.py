from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    content = {
               "additionalParams": {},
               "changeStateTo": "STARTED",
               "gracefulStopTimeout": 0,
               "stopType": "FORCEFUL"
               }
    
    r = vnfLcm.vnf_lcm_operate_instance_vnf(context["vnf_instance_id"], content)
    
    location = r.headers['Location']
    
    context["vnf_lcm_op_occ_id"] = location.split("/")[-1]
    
    ret = MSA_API.process_content(vnfLcm.state, f'{r}', context, True)
    print(ret)