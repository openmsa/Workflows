from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
#dev_var.add('var_name', var_type='String')

context = Variables.task_call(dev_var)


ret = MSA_API.process_content(constants.ENDED, 'Task OK', context, True)
print(ret)