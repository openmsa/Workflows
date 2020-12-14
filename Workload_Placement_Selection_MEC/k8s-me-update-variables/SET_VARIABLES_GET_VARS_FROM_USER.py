from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('msa_fqdn', var_type='String')
dev_var.add('msa_user', var_type='String')
dev_var.add('msa_pass', var_type='Password')
dev_var.add('k8s_device', var_type='Device')
dev_var.add('k8s_port', var_type='String')
dev_var.add('k8s_token', var_type='Password')
context = Variables.task_call(dev_var)

if __name__ == "__main__":

    ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
    print(ret)