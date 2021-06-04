import json
import time
import os
import sys
from msa_sdk import constants
from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('playbook_hosts_filename', var_type='String')
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
device_ref = context['ansible_me']
device_id = device_ref[3:]

# instantiate device object.
device = Device(device_id=device_id)

#get hosts filename
hosts_filename = context.get('playbook_hosts_filename')

#push configuration to device. WARNING: MUST BE ENHANCED AND MORE GENERIC for multicloud
context.get('ansible_hosts_inventory')
if 'ansible_hosts_inventory' in context:
    ansible_hosts_inventory = context.get('ansible_hosts_inventory')
    for host_dict in ansible_hosts_inventory:
        
        host_ip_address = host_dict.get("host_ip_address")
        user_login = host_dict.get("user_login")
        user_password = host_dict.get("user_password")
        
        ansible_server_public_ssh_rsa_id_path = '/root/.ssh/id_rsa.pub'
        configuration = "sshpass -p '"+ user_password +"' ssh-copy-id -o StrictHostKeyChecking=no -i " + ansible_server_public_ssh_rsa_id_path + " " + user_login + "@" + host_ip_address
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
        	ret = MSA_API.process_content(constants.FAILED, 'Failed, copying Ansible server SSH key id to the hosts:' + return_message , context, True)
        	print(ret)
    
ret = MSA_API.process_content(constants.ENDED, 'Ansible server SSH key id is copied successfully to the hosts:' + return_message, context, True)
print(ret)
sys.exit()