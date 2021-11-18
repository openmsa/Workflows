import uuid
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NfviVim import NfviVim


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add("vim_id", var_type="OBMFRef")
    context = Variables.task_call(dev_var)
    
    nfviVim = NfviVim(context['mano_ip'], context['mano_port'])
    nfviVim.set_parameters(context['mano_user'], context['mano_pass'])
    
    r = nfviVim.nfvi_vim_delete(context["vim_id"])
    
    ret = MSA_API.process_content(nfviVim.state, f'{r}', context, True)
    print(ret)
