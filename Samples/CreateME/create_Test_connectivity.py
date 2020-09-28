from msa_sdk.device import Device
from msa_sdk.variables import Variables

context = Variables.task_call()

new_device = Device(device_id=context['device_id'])
new_device.read()
new_device.ping(new_device.management_address)

print(new_device.process_content('ENDED', 'Pinging IP: ' + new_device.management_address + ' successfully', context, True))