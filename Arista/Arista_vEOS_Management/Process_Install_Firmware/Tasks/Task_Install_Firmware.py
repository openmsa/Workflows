import json
import time
import re
from msa_sdk import constants
from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration


dev_var = Variables()
dev_var.add('firmware_file', var_type='File')

context = Variables.task_call(dev_var)

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])



#get device_id from context
device_id = context['arista_eos_device'][3:]
# instantiate device object
device = Device(device_id=device_id)
context['device_id'] = device_id
params='FILE='+'/opt/fmc_repository/'+context['firmware_file']
context['params'] = params
res = device.update_firmware(params)
start_update_firmware =  json.loads(device.content)
context['start_update_firmware_res'] = str(res)
context['start_update_firmware'] = start_update_firmware 
if start_update_firmware.get('wo_status') and start_update_firmware['wo_status'] !=  "END" :
  MSA_API.task_error('Devices firmware updated failed  ' +  start_update_firmware['wo_newparams'], context, True) 

status = 'RUNNING'
loop   = 0
while status == 'RUNNING' and loop < 200:
  time.sleep(5)
  response = device.get_update_firmware_status()
  status = response.get('status')
  loop = loop + 1
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Firmware upgrade message '+response['message'])
  
context['update_firmware_status']  =   response  
if status !=  "ENDED" :
  MSA_API.task_error('Devices firmware updated failed with status '+ status+ ', response :' + str(response), context, True)
else:
  MSA_API.task_success('Firmware updated for device : ' + context['arista_eos_device'], context, True) 
