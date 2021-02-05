from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

ret = MSA_API.process_content('ENDED', 'Instance deleted', context, True)
print(ret)

[root@462c84081ed5 Password_Change]# cat ./Process_DELETE/Tasks/Task_delete_instance.py
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

ret = MSA_API.process_content('ENDED', 'Instance deleted', context, True)
print(ret)

