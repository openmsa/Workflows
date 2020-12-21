from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('k8s_api', var_type='Device')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', 'SERVICE INSTANCE CREATED', context, True)
print(ret)