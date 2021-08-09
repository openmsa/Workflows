from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

# from custom.ETSI.BaseApi import BaseApi
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('vnf_package_name', var_type='String')
    context = Variables.task_call(dev_var)
    
    vnfPkgApi = VnfPkgSol005('10.31.1.245', '8080')
    vnfPkgApi.set_parameters(context['mano_user'], context['mano_pass'])
    pkg = {"userDefinedData": {"name": context['vnf_package_name']}}
    r = vnfPkgApi.vnf_packages_post(pkg)
    
    ret = MSA_API.process_content('ENDED', f'{r}', context, True)
    print(ret)

