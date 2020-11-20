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

# build the Microservice JSON params for IMPORT
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}

gateway = {"Gateway":"0"}

# call the CREATE for simple_firewall MS for each device
order = Order(devicelongid)
order.command_execute('IMPORT', gateway)

# convert dict object into json
content = json.loads(order.content)

# check if the response is OK
if order.response.ok:
    ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                    MESSAGE: {profile} activated on {object_id}',
                                  context, True)
else:
    ret = MSA_API.process_content('FAILED',
                                  f'Import failed \
                                  - {order.content}',
                                  context, True)


print(ret)
