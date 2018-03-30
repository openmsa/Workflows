import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import deviceconfigws


device_id = 'dev001'
object_file = 'obj_file'

try:
    client = deviceconfigws.DeviceConfigurationWs(config.JobConfig())

    # attach_files_to_device
    print('attach_files_to_device')
    output = client.attach_files_to_device(device_id, object_file)
    print(type(output))
    print(output)
    print()

    # detach_files_from_device
    print('detach_files_from_device')
    output = client.detach_files_from_device(device_id, object_file)
    print(type(output))
    print(output)

except:
    print('NG')
    print(traceback.format_exc())
