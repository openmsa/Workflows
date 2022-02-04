import json
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('aspectId', var_type='String')
    dev_var.add('numberOfSteps', var_type='String')
    context = Variables.task_call(dev_var)

    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    aspectId = context.get('aspectId')
    if not aspectId:
    	aspectId = 'aspect'
    
    numberOfSteps = context.get('numberOfSteps')
    if not numberOfSteps:
    	numberOfSteps = '1'
    
    content = {
               "type": "SCALE_OUT",
               "aspectId": aspectId,
               "numberOfSteps": numberOfSteps,
               "additionalParams": {}
               }
    
    r = vnfLcm.vnf_lcm_scale_instance_vnf(context["vnf_instance_id"], content)
    
    location = ''
    try:
        location = r.headers['Location']
    except:
        MSA_API.task_error('Stop VNF Instance message: ' + json.dumps(r.json()), context)
    
    context["vnf_lcm_op_occ_id"] = location.split("/")[-1]
    
    ret = MSA_API.process_content(vnfLcm.state, f'{r}', context, True)
    print(ret)