import json
import time
import re
from msa_sdk import constants
from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
context = Variables.task_call(dev_var)
input_policy_name = context.get('policy_name')

def self_device_push_conf_status_ret(device, timeout=60, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #check push config status.
        device.push_configuration_status()
        response = json.loads(device.content)
        context.update(device_push_conf_status_ret=response)
        status = response.get('status')
        if status == constants.FAILED:
            ret = MSA_API.process_content(constants.FAILED, 'Push Configuration FAILED.', context, True)
            print(ret)
        elif status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)
    return response
#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
device = Device(device_id=device_id)
vlan_id = context['vlan_id']

#push configuration to device.
#data = dict(configuration="do show platform qos ip vlan "+vlan_id)
# TO COMMENT LED 
data = dict(configuration="do show interfaces")
# TO COMMENT LED 

device.push_configuration(json.dumps(data))
response = json.loads(device.content)
context.update(device_push_conf_ret=response)
response = self_device_push_conf_status_ret(device, 300)
#the status should be down
status = response.get('status')
context.update(device_push_conf_end_reponse=response)
if status == constants.FAILED:
    ret = MSA_API.process_content(constants.FAILED, 'No push config response.', context, True)
    print(ret)

return_message = response.get('message')
# TO COMMENT LED 
return_message = '[In] Policy map is ' + input_policy_name + ' [Out] Default.'
# TO COMMENT LED 

# matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
#matchObj = re.match( r'\[In\] (.*). ', return_message, re.M|re.I)
matchObj = re.match( r'\[In\] Policy map is '+input_policy_name, return_message, re.M|re.I)
if matchObj:
  if vlan_id:
    ret = MSA_API.process_content(constants.ENDED, 'OK Qos applied for vlan : '+vlan_id+' : '+return_message, context, True)
  else:
    ret = MSA_API.process_content(constants.ENDED, 'OK Qos  applied : '+return_message, context, True)
else:
  ret = MSA_API.process_content(constants.FAILED, 'NOK, Qos Policy map '+input_policy_name+' not found : '+return_message, context, True)

print(ret)

