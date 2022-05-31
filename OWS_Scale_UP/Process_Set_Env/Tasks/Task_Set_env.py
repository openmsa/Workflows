from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


dev_var = Variables()
dev_var.add('Device', var_type='Device')
dev_var.add('VM_name', var_type='String')
dev_var.add('Image', var_type='OBMFRef')

context = Variables.task_call(dev_var)


ret = MSA_API.process_content('ENDED', 'Environnement OK', context, True)
print(ret)

