'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import util
import json
'''
dev_var = Variables()
dev_var.add('var_name', var_type='String')
dev_var.add('var_name2', var_type='Integer')
context = Variables.task_call(dev_var)
context['var_name2'] = int(context['var_name2']) + 1
'''

dev_var = Variables()
dev_var.add('addresses.0.ip')
dev_var.add('addresses.0.status')
dev_var.add('addresses.1.ip')
dev_var.add('addresses.1.status')
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']
device = Device()
addresses = context['addresses']

i=0
for address in addresses:
  ip = address['ip']

  ping_result = device.ping(ip)
  util.log_to_process_file(process_id, ping_result)
  ping_result_json = json.loads(ping_result)
  num = len(context['addresses'])
  context['addresses'][i] = {}
  context['addresses'][i]['ip'] = ip
  context['addresses'][i]['status'] = ping_result_json['status']
  i += 1


ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

