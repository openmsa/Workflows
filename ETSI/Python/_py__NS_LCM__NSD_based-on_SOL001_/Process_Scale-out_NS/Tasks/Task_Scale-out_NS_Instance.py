from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NsLcmSol005 import NsLcmSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('aspectId', var_type='String')
    dev_var.add('numberOfSteps', var_type='String')
    context = Variables.task_call(dev_var)
    
    nsLcm = NsLcmSol005(context["mano_ip"], context["mano_port"])
    nsLcm.set_parameters(context["mano_user"], context["mano_pass"])
    
    ns_instance_id = context["ns_instance_id"]
    
    #scale-out payload.
    payload = dict()
    
    numberOfSteps = int(context.get('numberOfSteps'))
    aspectId = context.get('aspectId')
    scaleNsByStepsData = dict(scalingDirection="SCALE_OUT", aspectId=aspectId, numberOfSteps=numberOfSteps)
    
    scaleNsData = dict()
    scaleNsData.update(scaleNsByStepsData=scaleNsByStepsData)
    
    scaleType = "SCALE_NS"
    payload.update(scaleType=scaleType, scaleNsData=scaleNsData)
    
    #Get NS package id.
    ns_instance_id = context.get('ns_instance_id')

    r = nsLcm.ns_lcm_scale_ns(ns_instance_id, payload)
    
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