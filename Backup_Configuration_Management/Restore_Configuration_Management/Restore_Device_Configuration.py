import json
import time
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.conf_backup import ConfBackup

from builtins import isinstance

dev_var = Variables()
dev_var.add('revision_id', var_type='int')
context = Variables.task_call(dev_var)


def self_wait_end_of_restore(confbackup_obj, device_id, timeout= 300, interval=5):
    time.sleep(interval)
    #We check the end of the restore
    global_timeout = time.time() + timeout
    while True:
      # We will wait the end of the device backup
      confbackup_obj.restore_status(device_id)
      response = json.loads(confbackup_obj.content)
      # "response": { "message": "Restore processed (restore revision: 1091)\r\n\r\n", "date": "21-09-2021 09:28:16", "step": null, "lastProvDate": null, "status": "ENDED", "finalStep": false
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

# instantiate ConfBackup object
confbackup_obj = ConfBackup()

backup_revisionId = context.get('backup_revisionId')
input_revision_id = context.get('revision_id')

if input_revision_id:
    backup_revisionId = input_revision_id

#1) Restore one backup
confbackup_obj.restore(device_id, str(backup_revisionId)) 

response = json.loads(confbackup_obj.content)
# response:  { "status": "OK", "result": "", "rawJSONResult": "{\"sms_status\":\"OK\"}", "rawSmsResult": null, "message": "Successfully processed", "code": "OK", "ok": true },
context.update(device_restore_obj_response=response)

if response:
  backup_start=''
  if 'status' in response:
    restore_status=response.get('status')
  if restore_status == "OK":
    response = self_wait_end_of_restore(confbackup_obj, device_id, 300)
    # response: { "message": "Restore processed (restore revision: 1091)\r\n\r\n",  "date": "21-09-2021 09:28:16",  "step": null, "lastProvDate": null, "status": "ENDED", "finalStep": false
    context.update(device_restore_status_end=response)
    status = response.get('status')
    if status == constants.FAILED:
      MSA_API.task_error( 'Device restore failed with revisionID='+str(backup_revisionId), context, True)

    MSA_API.task_success('Device "' +  context['device_id'] + '" RESTORE done to revisionID='+str(backup_revisionId), context, True)

MSA_API.task_error('Restore configuration failed on device "' + device_id +'"  with revisionID='+str(backup_revisionId), context, True)

