import json
import time
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.conf_backup import ConfBackup
from builtins import isinstance

dev_var = Variables()
context = Variables.task_call(dev_var)

def self_wait_end_of_backup(confbackup_obj, device_id, timeout = 300, interval=5):
    time.sleep(interval)
    #We check the end of the back 

    global_timeout = time.time() + timeout
    while True:
      # We will wait the end of the device backup
      confbackup_obj.backup_status(device_id)
      response = json.loads(confbackup_obj.content)
      # response: "device_backup_status": {  "date": "21-09-2021 08:43:55", "message": "BACKUP processed", "result": "", "revisionId": 1100, "status": "ENDED" },
      context.update(device_backup_status=response)
      status = response.get('status')
      if status == constants.FAILED:
         MSA_API.task_error('Device Backup FAILED.', context, True)
      elif status != constants.RUNNING or time.time() > global_timeout:
         break
      time.sleep(interval)
    return response 


#get device_id from context
device_id = context['device_id'][3:]

# instantiate ConfBackup object
confbackup_obj = ConfBackup()

#1) Run a new backup
confbackup_obj.backup(device_id) 

response = json.loads(confbackup_obj.content)  #convert string into dict
# "response": { "status": "OK", "result": "", "rawJSONResult": "{\"sms_status\":\"OK\"}", "rawSmsResult": null, "message": "Successfully processed", "code": "OK", "ok": true },",

context.update(confbackup_backup_resp=response)

backup_revisionId='?'

backup_start=''
if response:
  if 'status' in response:
    backup_start = response.get('status')
  if backup_start == "OK":
    response = self_wait_end_of_backup(confbackup_obj, device_id, 300)
    # "response": { ""device_backup_status_end": { "date": "20-09-2021 12:18:15", "message": "BACKUP processed", "result": null, "revisionId": 1091, "status": "ENDED" },
    status = response.get('status')
    context.update(device_backup_status_end=response)
    if status == constants.FAILED:
      MSA_API.task_error( 'Device backup failed. ', context, True)
    backup_revisionId = response.get('revisionId')
    context.update(backup_revisionId=backup_revisionId)
    MSA_API.task_success( 'Device "' +  context['device_id'] + '" backup done, revisionId :'+ str(backup_revisionId), context, True)

MSA_API.task_error('Backup failed on device "' + device_id +'"', context, True)
