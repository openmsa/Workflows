from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device


dev_var = Variables()
dev_var.add('id', var_type='integer')
dev_var.add('site_left', var_type='Device')
dev_var.add('site_right', var_type='Device')
dev_var.add('leftsubnet', var_type='string')
dev_var.add('rightsubnet', var_type='string')
dev_var.add('secret', var_type='string')
context = Variables.task_call(dev_var)

left_device_id = context['site_left'][-3:]
right_device_id = context['site_right'][-3:]

left_device = Device(device_id=left_device_id)
right_device = Device(device_id=right_device_id)

context['left_device_id'] = left_device_id
context['right_device_id'] = right_device_id
context['left_device_ip'] = left_device.management_address
context['right_device_ip'] = right_device.management_address

ret = MSA_API.process_content('ENDED',
                              f'IPsec data retrieved \
                               site-A: {context}, \
                               site-Z: {context}',
                              context, True)

print(ret)
