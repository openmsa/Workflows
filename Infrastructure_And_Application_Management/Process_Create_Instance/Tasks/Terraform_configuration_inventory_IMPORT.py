import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import constants

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('terraform_managed_entity', var_type='Device')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['terraform_managed_entity']

# extract the database ID
devicelongid = device_id[3:]

# call the CREATE for simple_firewall MS for each device
order = Order(devicelongid)
order.command_synchronize(60)

# convert dict object into json
content = json.loads(order.content)

# check if the response is OK
if order.response.ok:
    ret = MSA_API.process_content(constants.ENDED,
                                  f'Terreform MS objects were synchronized successfull.',
                                  context, True)
else:
    ret = MSA_API.process_content(constants.FAILED,
                                  f'Failed to synchronize Terreform MS objects.',
                                  context, True)


print(ret)

