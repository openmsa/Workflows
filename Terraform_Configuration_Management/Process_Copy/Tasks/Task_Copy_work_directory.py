import json
import time
import os
from unicodedata import normalize
from msa_sdk import constants
from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('configuration_file', var_type='String')

context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################


####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
device = Device(device_id=device_id)

configuration_file = context.get('configuration_file')
work_directory = os.path.dirname(configuration_file)
context.update(work_directory=work_directory)

#workspace directory
terraform_workspace_dir = work_directory
context.update(terraform_workspace_dir=terraform_workspace_dir)

if context.get('src_configuration_file'):
  src_terraform_workspace_dir = context.get('src_configuration_file')
else:
  src_terraform_workspace_dir = terraform_workspace_dir 


params_json_string= '{"src_dir":"' + src_terraform_workspace_dir + '","file_pattern":"*","dst_dir":"' + terraform_workspace_dir + '"}'

params = json.loads(params_json_string)      
#params = dict(src_dir= '/tmp/',file_pattern='testfile.txt', dest_dir='/tmp')

context['param_string']=  json.dumps(params)

# Push files to the terrafomr serveur
device.run_jsa_command_device('send_files', params)
response = json.loads(device.content)
context['response_send_files']= str(response)

return_message = response.get('message')

ret = MSA_API.process_content(constants.ENDED, 'Files from MSA:"'+src_terraform_workspace_dir + '" copied succesfully to terraform server to' + terraform_workspace_dir + ' return=' + return_message, context, True)
print(ret)

