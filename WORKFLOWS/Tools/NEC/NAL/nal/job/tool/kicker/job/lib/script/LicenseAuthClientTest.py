import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.script import licenseauth


client = licenseauth.LicenseAuthClient(config.JobConfig())

# A10_vThunder_authentication
params = ['A', 'B']
output = client.a10_vthunder_authentication(params)

print('A10_vThunder_authentication')
print(type(output))
print(output)

print()

# Paloalto_authentication
params = ['A', 'B']
output = client.paloalto_authentication(params)

print('Paloalto_authentication')
print(type(output))
print(output)

print(type(True))
