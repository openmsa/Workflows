import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import devicews


customer_id = 'c001'
device_name = 'dev001'
login_user = 'usr'
password = 'pa"ss'
admin_password = 'ap\ass'
manufacture_id = 'm001'
model_id = 'model001'
ip_address = '10.0.0.1'
device_id = 'dev001'

try:
    client = devicews.DeviceWs(config.JobConfig())

    # create_managed_device
    print('create_managed_device')
    output = client.create_managed_device(
                            customer_id,
                            device_name,
                            login_user,
                            password,
                            admin_password,
                            manufacture_id,
                            model_id,
                            ip_address
    )
    print(type(output))
    print(output)
    print()

    # delete_device_by_id
    print('delete_device_by_id')
    output = client.delete_device_by_id(device_id)
    print(type(output))
    print(output)
    print()

    # do_provisioning_by_device_id
    print('do_provisioning_by_device_id')
    output = client.do_provisioning_by_device_id(device_id)
    print(type(output))
    print(output)

except:
    print('NG')
    print(traceback.format_exc())
