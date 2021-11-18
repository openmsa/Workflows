import uuid
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.NfviVim import NfviVim


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('vim_type', var_type='String')
    dev_var.add('interface_info', var_type='String')
    dev_var.add('username', var_type='String')
    dev_var.add('password', var_type='Password')
    dev_var.add('project_id', var_type='String')
    dev_var.add('project_domain', var_type='String')
    dev_var.add('user_domain', var_type='String')
    dev_var.add('vim_project', var_type='String')
    context = Variables.task_call(dev_var)
    
    nfviVim = NfviVim('10.31.1.245', '8080')
    nfviVim.set_parameters(context['mano_user'], context['mano_pass'])

    content = {
               "vimId": str(uuid.uuid4()),
               "vimType": context["vim_type"],
               "interfaceInfo": {
                   "endpoint": context["interface_info"]
                   },
               "accessInfo": {
                   "username": context["username"],
                   "password": context["password"],
                   "projectId": context["project_id"],
                   "projectDomain": context["project_domain"],
                   "userDomain": context["user_domain"],
                   "vim_project": context["vim_project"],
                   "device_id": context["device_id"]
                   },
               "geoloc": {
                   "lng": 45.75801,
                   "lat": 4.8001016
                   }
               }

    r = nfviVim.nfvi_vim_register(content)
    
    # context['vim_id'] = r.json()['id']
    
    ret = MSA_API.process_content('ENDED', f'{r}', context, True)
    print(ret)