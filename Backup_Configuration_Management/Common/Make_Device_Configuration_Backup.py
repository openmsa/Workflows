import json
import time
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from builtins import isinstance

dev_var = Variables()
dev_var.add('policy_map_name', var_type='String')
context = Variables.task_call(dev_var)

def self_end_of_backup(device_obj, timeout=60, interval=5):
    time.sleep(interval)
    #We check the end of the back
    #Get Back up status from /conf-backup/v1/backup-status/{deviceId}  
    device_obj.action = 'Get Back up status'
    device_obj.path = "/conf-backup/v1/backup-status/"+device_id
    global_timeout = time.time() + timeout
    while True:
      # We will wait the end of the device backup
      device_obj.call_get()
      response = json.loads(device_obj.content)
      # response: {"date" : "11-12-2020 16:19:37",  "message" : "BACKUP processed", "result" : null, "revisionId" : 12, "status" : "ENDED"
      context.update(device_backup_status=response)
      status = response.get('status')
      if status == constants.FAILED:
          ret = MSA_API.process_content(constants.FAILED, 'Device Backup FAILED.', context, True)
          print(ret)
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
# API /conf-backup/v1/backup/{deviceId}   : Backup
device_obj.path = "/conf-backup/v1/backup/"+device_id
device_obj.call_post()

response = json.loads(device_obj.content)
context.update(device_obj_respo=response)
# response: { "  "status" : "OK", "result" : "", "rawJSONResult" : "{\"sms_status\":\"OK\"}",  "rawSmsResult" : null, "code" : "OK",   "ok" : true,  "message" : "Successfully processed" },

backup_revisionId='?'

if response:
  backup_start=''
  if 'status' in response:
    backup_start=response.get('status')
  if backup_start == "OK":
    response = self_end_of_backup(device_obj, 300)
    # response: {"date" : "11-12-2020 16:19:37",  "message" : "BACKUP processed", "result" : null, "revisionId" : 12, "status" : "ENDED"
    status = response.get('status')
    context.update(device_backup_status_end=response)
    if status == constants.FAILED:
      ret = MSA_API.process_content(constants.FAILED, 'Device backup failed.', context, True)
      print(ret)
    backup_revisionId = response.get('revisionId')
    context.update(backup_revisionId=backup_revisionId)
    ret = MSA_API.process_content(constants.ENDED, 'Device "' +  context['device_id'] + '" backup done, revisionId :'+ str(backup_revisionId), context, True)
    print(ret)


ret = MSA_API.process_content(constants.FAILED, 'Backup failed on device "' + device_id , context, True)
print(ret)

