'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.conf_backup import ConfBackup
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

if 'vnf_me_list' in context:
    vnf_me_list = context.get('vnf_me_list')
conf_backup=ConfBackup();
'''for each ME, perform backup'''
for index, vnfc_dict in enumerate(vnf_me_list):
    me_id = vnfc_dict.get('device_ext_ref')[3:]
    conf_backup.backup(device_id=me_id)
    i=0
    while(i<10):
        status=conf_backup.backup_status(device_id=me_id)
        util.log_to_process_file(process_id,"backup status=".status)
        sleep(1);
        i=i+1

ret = MSA_API.process_content('ENDED', 'Back up completed', context, True)
print(ret)