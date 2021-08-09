from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.BaseApi import BaseApi


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('vnf_package_name', var_type='String')
    context = Variables.task_call(dev_var)
    
    conn = BaseApi('10.31.1.245', '8080')
    conn.set_parameters(context['mano_user'], context['mano_pass'])
    r = conn.do_get('sol005/vnfpkgm/v1/vnf_packages')
    
    ret = MSA_API.process_content('ENDED', f'{r}', context, True)
    print(ret)

