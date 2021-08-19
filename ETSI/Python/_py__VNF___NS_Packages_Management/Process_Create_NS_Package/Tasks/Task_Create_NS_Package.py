from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NsdSol005 import NsdSol005


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call()
    
    nsdApi = NsdSol005(context["mano_ip"], context["mano_port"])
    nsdApi.set_parameters(context['mano_user'], context['mano_pass'])
    
    data = {"userDefinedData": {}}

    r = nsdApi.nsd_descriptors_post(data)

    ret = MSA_API.process_content('ENDED', f'{r}', context, True)
    print(ret)