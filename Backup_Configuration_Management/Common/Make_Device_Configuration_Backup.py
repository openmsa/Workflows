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
 
#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
device_obj = Device(device_id=device_id)


#1) Get list of available backup :
#from /conf-backup/v1/revision-list/{deviceId} List the revisions of the backups
device_obj.action = 'List the revisions of the backups'
device_obj.path = "/conf-backup/v1/revision-list/"+device_id
context.update(list_path=device_obj.path)
device_obj.call_get()
response = json.loads(device_obj.content)
context.update(device_list_revisiont1=response)
# response: { [] },


#2) Run a new backup
device_obj.action = 'Backup Configuration Device'
# API /conf-backup/v1/backup/{deviceId}   : Backup
device_obj.path = "/conf-backup/v1/backup/"+device_id
device_obj.call_post()

response = json.loads(device_obj.content)
context.update(device_obj_respo=response)
# response: { "status": "OK", "result": "", "rawJSONResult": "{\"sms_status\":\"OK\"}",  "rawSmsResult": null, "code": "OK", "ok": true, "message": "Successfully processed" },

if response:
  backup_start=''
  if 'status' in response:
    backup_start=response.get('status')
  if backup_start == "OK":
    time.sleep(4)
    #We check the end of the back
    #Get Back up status from /conf-backup/v1/backup-status/{deviceId}  
    device_obj.action = 'Get Back up status'
    device_obj.path = "/conf-backup/v1/backup-status/"+device_id
    device_obj.call_get()
    response = json.loads(device_obj.content)
    context.update(device_obj_status_respo=response)
    #response = {"date": "01-12-2020 17:05:10",  "message": "BACKUP processed",  "result": null, "revisionId": -1, "status": "ENDED"

    #3) Get the list of available backup to get the latest backup_id
    #from /conf-backup/v1/revision-list/{deviceId} List the revisions of the backups
    device_obj.action = 'List the revisions of the backups'
    device_obj.path = "/conf-backup/v1/revision-list/"+device_id
    device_obj.call_get()
    response = json.loads(device_obj.content)
    context.update(device_list_revisiont2=response)
    # response: { [] },

    backup_status=''
    if 'status' in response:
      backup_status=response.get('status')
      if backup_status == "OK":
        ret = MSA_API.process_content(constants.ENDED, 'Device "' + device_id + '" backup done, status '+backup_status, context, True)
        print(ret)
  backup_response= ''
  if 'message' in response:
    backup_response=response.get('message')
  ret = MSA_API.process_content(constants.FAILED, 'Backup failed on device "' + device_id + '"' + ',  backup_start='+ backup_start+ ', backup_response="'+ str(backup_response) +'"', context, True)
  print(ret)

ret = MSA_API.process_content(constants.FAILED, 'Backup failed on device "' + device_id + '"', context, True)
print(ret)
