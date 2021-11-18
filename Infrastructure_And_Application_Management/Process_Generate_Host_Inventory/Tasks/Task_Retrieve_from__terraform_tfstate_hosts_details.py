import json
import time
import os
import sys
import re
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
#Get device id from context (e.g: UBI2455).
device_ref = context['terraform_managed_entity']
device_id = device_ref[3:]
# instantiate device object.
device = Device(device_id=device_id)

#terraform tfstate filename
if 'terraform_configuration' not in context:
    ret = MSA_API.process_content(constants.FAILED, 'Failed, Terraform configuration filename is empty.' , context, True)
    print(ret)
    sys.exit()
configuration_file = context.get('terraform_configuration')
work_directory = os.path.dirname(configuration_file)
terraform_tfstate_filename = work_directory + '/terraform.tfstate'

#push configuration to device. WARNING: MUST BE ENHANCED AND MORE GENERIC for multicloud
configuration ='grep -oP \'"computer_name": ".*"\' ' + terraform_tfstate_filename
configuration += ' && grep -oP \'"public_ip_address": "[0-9.]+"\' ' + terraform_tfstate_filename
configuration += ' && grep -oP \'"admin_password": ".*"\' ' + terraform_tfstate_filename
configuration +=' && grep -oP \'"admin_username": ".*"\' ' + terraform_tfstate_filename
data = dict(configuration=configuration)

device.push_configuration(json.dumps(data))
response = json.loads(device.content)

#get asynchronous push config status
context.update(device_push_conf_ret=response)
response = self_device_push_conf_status_ret(device, 60)

#the status should be down
status = response.get('status')
context.update(device_push_conf_end_reponse=response)

#parse the terrafom success operation message from response
return_message = response.get('message')

if status == constants.FAILED:
	ret = MSA_API.process_content(constants.FAILED, 'Failed to generate Ansible playbook hosts: ' + return_message, context, True)
	print(ret)

#parse value from response

##host_group
m = re.search( r'(.*)"computer_name": "(.*?)"', return_message, re.M|re.I)
computer_name = m.group(2)

##public_ip_address
m = re.search( r'(.*)"public_ip_address": "(.*?)"', return_message, re.M|re.I)
public_ip_address = m.group(2)

##admin_username
m = re.search( r'(.*)"admin_username": "(.*?)"', return_message, re.M|re.I)
admin_username = m.group(2)

##admin_password
m = re.search( r'(.*)"admin_password": "(.*?)"', return_message, re.M|re.I)
admin_password = m.group(2)

#add hosts inventory details into the context
ansible_hosts_inventory = list()
host_dict = dict(group_name=computer_name, host_ip_address=public_ip_address, user_login=admin_username, user_password=admin_password)
ansible_hosts_inventory.append(host_dict.copy())
context.update(ansible_hosts_inventory=ansible_hosts_inventory)

ret = MSA_API.process_content(constants.ENDED, 'Ansible playbook hosts is generated successfully: ' + return_message, context, True)
print(ret)