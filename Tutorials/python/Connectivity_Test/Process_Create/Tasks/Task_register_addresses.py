from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import util
import json

# this task can be used either in a CREATE or an UPDATE process

dev_var = Variables()
dev_var.add('addresses.0.ip')
dev_var.add('addresses.0.status')
context = Variables.task_call(dev_var)

# get the current process id, useful for logging message to the process log file
process_id = context['SERVICEINSTANCEID']

# create a new variable Device to use the sdk function msa_sdk/device.html#msa_sdk.device.Device.ping 
device = Device()

# get the list of IP addresses registered in the UI
addresses = context['addresses']

# for each IP addresses
i=0
for address in addresses:
  ip = address['ip']
  
  # call the ping function with the IP
  ping_result = device.ping(ip)
  
  # log the result in the log file process-xx.log
  util.log_to_process_file(process_id, ping_result)
  
  # get the JSON result as a Python object
  ping_result_json = json.loads(ping_result)
  
  # update the addresses with the ping status
  num = len(context['addresses'])
  context['addresses'][i] = {}
  context['addresses'][i]['ip'] = ip
  context['addresses'][i]['status'] = ping_result_json['status']
  i += 1

  
ret = MSA_API.process_content('ENDED', 'IP addresses tested', context, True)
print(ret)
