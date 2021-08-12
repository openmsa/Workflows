from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NsLcmSol005 import NsLcmSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('ns_package_id', var_type='String')
    context = Variables.task_call(dev_var)
    
    ns_lcm = NsLcmSol005('10.31.1.245', '8080')
    ns_lcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    data = {"nsdId": context['ns_package_id']}

    r = ns_lcm.ns_lcm_create_instance(data)

    context['ns_instance'] = r
    context['url']         = r

    ret = MSA_API.process_content('ENDED', f'{r}', context, True)
    print(ret)