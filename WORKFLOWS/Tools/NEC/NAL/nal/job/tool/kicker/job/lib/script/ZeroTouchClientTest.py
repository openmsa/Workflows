import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.script import zerotouch

client = zerotouch.ZeroTouchClient(config.JobConfig())

# A10_vThunder_provisioning
params = ['A', 'B']
output = client.a10_vthunder_provisioning(params)

print('A10_vThunder_provisioning')
print(type(output))
print(output)

print()

# BIGIP_provisioning
params = ['A', 'B']
output = client.bigip_provisioning(params)

print('BIGIP_provisioning')
print(type(output))
print(output)

print()

# fortiVM_provisioning
params = ['A', 'B']
output = client.fortivm_provisioning(params)

print('fortiVM_provisioning')
print(type(output))
print(output)

print()

# Paloalto_provisioning
params = ['A', 'B']
output = client.paloalto_provisioning(params)

print('Paloalto_provisioning')
print(type(output))
print(output)

print()

# vSRX_FF_provisioning
params = ['A', 'B']
output = client.vsrx_ff_provisioning(params)

print('vSRX_FF_provisioning')
print(type(output))
print(output)
