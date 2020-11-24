'''
Create new service instance dedicated for one device.
INPUT: device_id
'''
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('device_id', var_type='Device')

context = Variables.task_call(dev_var)

device_id = context['device_id'] 

ret = MSA_API.process_content(constants.ENDED, 'Service instantiated for device: ' + device_id + '.', context, True)
print(ret)

