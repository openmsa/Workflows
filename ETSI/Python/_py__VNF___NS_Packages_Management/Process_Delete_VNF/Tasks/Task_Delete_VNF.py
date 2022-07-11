import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfPkgSol005 import VnfPkgSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('vnf_package_id', var_type='String')
    context = Variables.task_call(dev_var)
    
    #Get SOL00X version from context.
    sol_version = context.get('sol005_version')
    
    vnfPkgApi = VnfPkgSol005(context["mano_ip"], context["mano_port"], sol_version)
    vnfPkgApi.set_parameters(context['mano_user'], context['mano_pass'])

    r = vnfPkgApi.vnf_packages_vnfpkgid_delete(context['vnf_package_id'])
    
    r_details = r.json().get('detail')
    ret = MSA_API.process_content(vnfPkgApi.state, f'{r}' + ': ' + r_details, context, True)
    print(ret)
