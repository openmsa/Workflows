from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('device_id', var_type='Device')
    dev_var.add('mano_user', var_type='String')
    dev_var.add('mano_pass', var_type='Password')
    dev_var.add('mano_port', var_type='String')
    context = Variables.task_call(dev_var)
    
    ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
    print(ret)
