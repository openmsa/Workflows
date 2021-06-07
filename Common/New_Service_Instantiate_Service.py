'''
Create new service instance dedicated for one device.
INPUT: device_id
'''
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('SO_service_instance_id', var_type='String')
dev_var.add('SO_service_external_ref', var_type='String')

context = Variables.task_call(dev_var)

device_id = context['device_id'] 

MSA_API.task_success('Service instantiated for device: ' + device_id + '.', context, True)
