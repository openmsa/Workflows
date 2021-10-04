from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('terraform_managed_entity', var_type='Device')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', 'New service instance is created successfully!', context, True)
print(ret)

