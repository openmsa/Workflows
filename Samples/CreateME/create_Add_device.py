from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()

dev_var.add('customer_id', var_type='Integer')
dev_var.add('managed_device_name')
dev_var.add('manufacturer_id', var_type='Integer')
dev_var.add('model_id', var_type='Integer')
dev_var.add('device_ip_address', var_type='IP Address', def_value='10.30.19.41')
dev_var.add('login')
dev_var.add('password', var_type='Password')
dev_var.add('password_admin', var_type='Password')

context = Variables.task_call(dev_var)

new_device = Device(context['customer_id'], context['managed_device_name'], context['manufacturer_id'],context['model_id'], context['login'], context['password'], context['password_admin'],context['device_ip_address'])
new_device.create()
context['device_id'] = new_device.device_id

print(new_device.process_content('ENDED', 'Task OK', context, True))