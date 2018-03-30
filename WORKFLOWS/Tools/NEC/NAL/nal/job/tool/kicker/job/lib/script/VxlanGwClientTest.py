import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.script import vxlangw

client = vxlangw.VxlanGwClient(config.JobConfig())

# createVxlanGw
params = ['A"C', 'B']
output = client.create_vxlan_gw(params, ['A"C'])

print('createVxlanGw')
print(type(output))
print(output)

print()

# deleteVxlanGw
params = ['C', 'D']
output = client.delete_vxlan_gw(params)

print('deleteVxlanGw')
print(type(output))
print(output)
