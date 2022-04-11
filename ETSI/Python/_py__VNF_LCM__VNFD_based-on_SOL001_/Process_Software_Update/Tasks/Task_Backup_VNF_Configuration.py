import json
import time
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.conf_backup import ConfBackup
from builtins import isinstance
from msa_sdk import util
'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()

context = Variables.task_call(dev_var)
process_id = context['SERVICEINSTANCEID']

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


if 'vnf_me_list' in context:
    vnf_me_list = context.get('vnf_me_list')
conf_backup=ConfBackup()
'''for each ME, perform backup'''

for index, vnfc_dict in enumerate(vnf_me_list):
    me_id = vnfc_dict.get('device_ext_ref')[3:]
    # instantiate ConfBackup object
    confbackup_obj = ConfBackup()
    #1) Run a new backup
    confbackup_obj.backup(me_id) 
    response = json.loads(confbackup_obj.content)  #convert string into dict
    # "response": { "status": "OK", "result": "", "rawJSONResult": "{\"sms_status\":\"OK\"}", "rawSmsResult": null, "message": "Successfully processed", "code": "OK", "ok": true },",
    context.update(confbackup_backup_resp=response)
    backup_revisionId='?'

    backup_status=''
    if response:
        if 'status' in response:
          backup_status = response.get('status')
        if backup_status == "OK":
            response = self_wait_end_of_backup(confbackup_obj, me_id, 300)
            # "response": { ""device_backup_status_end": { "date": "20-09-2021 12:18:15", "message": "BACKUP processed", "result": null, "revisionId": 1091, "status": "ENDED" },
            status = response.get('status')
            context.update(device_backup_status_end=response)
            if status == constants.FAILED:
                MSA_API.task_error( 'Device backup failed. ', context, True)
            backup_revisionId = response.get('revisionId')
            #context.update(backup_revisionId=backup_revisionId)
            vnfc_dict.update(backup_revisionId=backup_revisionId)
            util.log_to_process_file(process_id,'Device "' +  me_id + '" backup done, revisionId :'+ str(backup_revisionId))
        util.log_to_process_file(process_id,'Backup failed on device "' + me_id +'"')
MSA_API.task_success('Device Backup completed.', context, True)

