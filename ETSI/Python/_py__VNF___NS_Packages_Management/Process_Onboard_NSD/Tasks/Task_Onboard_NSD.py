from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NsdSol005 import NsdSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('nsd_package_id', var_type='String')
    dev_var.add('nsd_pkg_content', var_type='String')
    context = Variables.task_call(dev_var)

    nsdApi = NsdSol005('10.31.1.245', '8080')
    nsdApi.set_parameters(context['mano_user'], context['mano_pass'])
    r = nsdApi.ns_descriptors_nsdinfoid_nsd_file_put(context['nsd_package_id'],
                                                     context['nsd_pkg_content'])

    ret = MSA_API.process_content('ENDED', f'{r}', context, True)
    print(ret)