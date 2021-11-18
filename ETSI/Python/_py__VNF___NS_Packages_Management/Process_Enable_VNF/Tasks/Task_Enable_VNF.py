from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfPkgSol005 import VnfPkgSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('vnf_package_id', var_type='String')
    context = Variables.task_call(dev_var)
    
    _state = True

    vnfPkgApi = VnfPkgSol005(context["mano_ip"], context["mano_port"])
    vnfPkgApi.set_parameters(context['mano_user'], context['mano_pass'])
    r = vnfPkgApi.set_operational_state(context['vnf_package_id'],
                                        _state)

    ret = MSA_API.process_content(vnfPkgApi.state, f'{r}', context, True)
    print(ret)