'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('cisco_nx_device', var_type='Device')
    
    context = Variables.task_call(dev_var)
    
    cisco_me_id = context["cisco_nx_device"][3:]
    cisco_me_ip    = Device(device_id=cisco_me_id).management_address
    cisco_me_user  = Device(device_id=cisco_me_id).login
    cisco_me_pass  = Device(device_id=cisco_me_id).password
    
    context["cisco_me_ip"]  = cisco_me_ip
    context["cisco_me_user"] = cisco_me_user
    context["cisco_me_pass"] = cisco_me_pass

ret = MSA_API.process_content('ENDED', 'Device selected', context, True)
print(ret)

