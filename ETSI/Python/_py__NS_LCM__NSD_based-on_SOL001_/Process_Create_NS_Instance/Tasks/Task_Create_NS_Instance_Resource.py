from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NsLcmSol005 import NsLcmSol005
from custom.ETSI.NsdSol005 import NsdSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('mano_user', var_type='String')
    dev_var.add('mano_pass', var_type='Password')
    dev_var.add('nfvo_device', var_type='Device')
    dev_var.add('ns_package_id', var_type='String')
    context = Variables.task_call(dev_var)
    
    nsLcm = NsLcmSol005('10.31.1.245', '8080')
    nsLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    nsd = NsdSol005('10.31.1.245', '8080')
    nsd.set_parameters(context['mano_user'], context['mano_pass'])
    
    r1 = nsd.nsd_descriptors_get(context['ns_package_id'])
    
    context['ns_package_id'] = r1.json()["nsdId"]
    
    content = {"nsdId": context['ns_package_id']}

    r2 = nsLcm.ns_lcm_create_instance(content)
    
    context["ns_instance"] = r2.json()

    ret = MSA_API.process_content('ENDED', f'{r1}, {r2}', context, True)
    print(ret)