import json
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"], context['mano_base_url'])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    content = {"gracefulTerminationTimeout": 0,
               "terminationType": "FORCEFUL",
               "additionalParams": {}
               }
    
    r = vnfLcm.vnf_lcm_terminate_vnf(context["vnf_instance_id"], content)
    
    location = ''
    try:
        location = r.headers['Location']
    except:
        MSA_API.task_error('Terminate VNF Instance message: ' + json.dumps(r.json()), context)
    
    context["vnf_lcm_op_occ_id"] = location.split("/")[-1]
    
    ret = MSA_API.process_content(vnfLcm.state, f'{r}', context, True)
    print(ret)