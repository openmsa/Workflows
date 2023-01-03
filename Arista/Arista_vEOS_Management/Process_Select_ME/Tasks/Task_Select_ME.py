'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('arista_eos_device', var_type='Device')
    
    context = Variables.task_call(dev_var)
    
    eos_me_id = context["arista_eos_device"][3:]
    eos_me_ip    = Device(device_id=eos_me_id).management_address
    eos_me_user  = Device(device_id=eos_me_id).login
    eos_me_pass  = Device(device_id=eos_me_id).password
    
    context["eos_me_ip"]  = eos_me_ip
    context["eos_me_user"] = eos_me_user
    context["eos_me_pass"] = eos_me_pass

ret = MSA_API.process_content('ENDED', 'Device selected', context, True)
print(ret)
