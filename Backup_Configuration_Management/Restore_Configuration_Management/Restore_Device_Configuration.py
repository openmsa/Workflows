import json
import time
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from builtins import isinstance

dev_var = Variables()
dev_var.add('revision_id', var_type='int')
context = Variables.task_call(dev_var)

def self_end_of_restore(device_obj, timeout= 300, interval=5):
    time.sleep(interval)
    #We check the end of the back
    #Get restore-config status from /conf-backup/v1/restore-status/{deviceId}  
    device_obj.action = 'Get restore-config status'
    device_obj.path = "/conf-backup/v1/restore-status/"+device_id
    global_timeout = time.time() + timeout
    while True:
      # We will wait the end of the device backup
      device_obj.call_get()
      response = json.loads(device_obj.content)
      # response: {"date" : "11-12-2020 16:19:37",  "message" : "BACKUP processed", "result" : null, "revisionId" : 12, "status" : "ENDED"
      context.update(device_restore_status=response)
      status = response.get('status')
      if status == constants.FAILED:
          MSA_API.task_error('Device Restore-config FAILED.', context, True)
      elif status != constants.RUNNING or time.time() > global_timeout:
          break
      time.sleep(interval)
    return response
  
#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
device_obj = Device(device_id=device_id)


#1) Run a new backup
device_obj.action = 'Backup Configuration Device'
backup_revisionId = context.get('backup_revisionId')
input_revision_id = context.get('revision_id')
if input_revision_id:
    backup_revisionId = input_revision_id

# API /conf-backup/v1/restore/{deviceId}/{revision} : Restore
device_obj.path = "/conf-backup/v1/restore/" + device_id + "/" + str(backup_revisionId)
device_obj.call_post()

response = json.loads(device_obj.content)
context.update(device_restore_obj_response=response)
# response: { "  "status" : "OK", "result" : "", "rawJSONResult" : "{\"sms_status\":\"OK\"}",  "rawSmsResult" : null, "code" : "OK",   "ok" : true,  "message" : "Successfully processed" },

if response:
  backup_start=''
  if 'status' in response:
    restore_status=response.get('status')
  if restore_status == "OK":
    response = self_end_of_restore(device_obj, 300)
    # response: {"date" : "11-12-2020 16:19:37",  "message" : "BACKUP processed", "result" : null, "revisionId" : 12, "status" : "ENDED"
    status = response.get('status')
    context.update(device_restore_status_end=response)
    if status == constants.FAILED:
      MSA_API.task_error( 'Device restore failed. ', context, True)

    MSA_API.task_success('Device "' +  context['device_id'] + '" RESTORE done', context, True)

MSA_API.task_success('Restore configuration failed on device "' + device_id +'"', context, True)