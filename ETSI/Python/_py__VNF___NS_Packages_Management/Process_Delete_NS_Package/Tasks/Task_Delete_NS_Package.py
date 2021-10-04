from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NsdSol005 import NsdSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('ns_package_id', var_type='String')
    context = Variables.task_call(dev_var)
    
    nsdApi = NsdSol005(context["mano_ip"], context["mano_port"])
    nsdApi.set_parameters(context['mano_user'], context['mano_pass'])
    
    r = nsdApi.ns_descriptors_nsd_info_id_delete(context["ns_package_id"])

    ret = MSA_API.process_content(nsdApi.state, f'{r}', context, True)
    print(ret)