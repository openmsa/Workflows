from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

context = Variables.task_call()

ret = MSA_API.process_content('ENDED', f'workflow instance deleted', context, True)
print(ret)