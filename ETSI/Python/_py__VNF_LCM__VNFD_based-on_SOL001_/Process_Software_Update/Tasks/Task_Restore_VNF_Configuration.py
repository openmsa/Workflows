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

def self_wait_end_of_restore(confbackup_obj, device_id, timeout = 300, interval=5):
    time.sleep(interval)
    #We check the end of the back 

    global_timeout = time.time() + timeout
    while True:
      # We will wait the end of the device backup
      confbackup_obj.restore_status(device_id)
      response = json.loads(confbackup_obj.content)
      # response: "device_backup_status": {  "date": "21-09-2021 08:43:55", "message": "BACKUP processed", "result": "", "revisionId": 1100, "status": "ENDED" },
      context.update(device_restore_status=response)
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
    #1) Run restore
    rev_id=str(vnfc_dict.get('backup_revisionId'))
    confbackup_obj.restore(me_id,rev_id) 
    response = json.loads(confbackup_obj.content)
    context.update(confbackup_restore_resp=response)

    restore_status=''
    if response:
        if 'status' in response:
          restore_status = response.get('status')
        if restore_status == "OK":
            response = self_wait_end_of_restore(confbackup_obj, me_id, 300)
            status = response.get('status')
            if status == constants.FAILED:
                util.log_to_process_file(process_id,'Device "' +  me_id + '"restore revision failed, revisionId :'+ rev_id)
 
            util.log_to_process_file(process_id,'Device "' +  me_id + '" revision done, revisionId :'+ rev_id)
        util.log_to_process_file(process_id,'Restore failed on device "' + me_id +'"')
MSA_API.task_success('Device Restore completed.', context, True)

