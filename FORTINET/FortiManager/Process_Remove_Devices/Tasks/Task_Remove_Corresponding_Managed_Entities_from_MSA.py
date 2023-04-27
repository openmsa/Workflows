import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order

dev_var = Variables()

context = Variables.task_call(dev_var)

MSA_API.task_success('OK' , context, True)
for device in context['devices']:
	device = Device(device_id=device['id'])
	device.delete()
	
MSA_API.task_success('Fortigate Managed Entities have been deleted' , context, True)