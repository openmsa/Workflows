import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('profile', var_type='String')
#dev_var.add('gateway', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device']
object_id = context['gateway']
profile = context['profile']

# extract the database ID
devicelongid = device_id[-3:]

ret = MSA_API.process_content('ENDED',
                              f'STATUS: OK, MESSAGE: Profile {profile}',
                              context, True)

print(ret)
