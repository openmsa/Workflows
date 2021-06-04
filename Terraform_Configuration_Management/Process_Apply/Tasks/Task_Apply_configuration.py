import json
import time
import os
import sys
from msa_sdk import constants
from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################
def self_device_push_conf_status_ret(device, timeout=60, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #check push config status.
        device.push_configuration_status()
        response = json.loads(device.content)
        context.update(device_push_conf_status_ret=response)
        status = response.get('status')
        if status == constants.FAILED:
            ret = MSA_API.process_content(constants.FAILED, 'Push Configuration FAILED.', context, True)
            print(ret)
        elif status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)
    return response

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#get device_id from context.
device_id = context['device_id'][3:]
# instantiate device object.
device = Device(device_id=device_id)

#Work directory where the configuration file is located.
configuration_file = context.get('configuration_file')
work_directory = os.path.dirname(configuration_file)

#workspace directory
terraform_workspace_dir = work_directory
context.update(terraform_workspace_dir=terraform_workspace_dir)

#push configuration to device.
data = dict(configuration='cd ' + terraform_workspace_dir + ' && terraform apply -auto-approve ' + work_directory)

device.push_configuration(json.dumps(data))
response = json.loads(device.content)

#get asynchronous push config status
context.update(device_push_conf_ret=response)
response = self_device_push_conf_status_ret(device, 500, 10)

#the status should be down
status = response.get('status')
context.update(device_push_conf_end_reponse=response)

#parse the terrafom success operation message from response
return_message = response.get('message')
#is_op_completed = return_message.find("Apply complete!")

#if status == constants.FAILED or is_op_completed == -1:
if status == constants.FAILED:
    ret = MSA_API.process_content(constants.FAILED, 'Terraform apply execution is failed: ' + return_message, context, True)
    print(ret)
    sys.exit()

ret = MSA_API.process_content(constants.ENDED, 'Terraform plan is executed successfully: ' + return_message, context, True)
print(ret)
sys.exit()

