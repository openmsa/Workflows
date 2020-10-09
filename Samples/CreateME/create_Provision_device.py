from msa_sdk.device import Device
from msa_sdk.variables import Variables

context = Variables.task_call()

new_device = Device(device_id=context['device_id'])
new_device.initial_provisioning()

print(new_device.process_content('ENDED', 'Device: ' + str(new_device.device_id) + ' provisioned successfully', context, True))