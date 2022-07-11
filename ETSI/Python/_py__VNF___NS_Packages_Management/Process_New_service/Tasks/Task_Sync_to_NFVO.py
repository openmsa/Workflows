from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add("nfvo_device", var_type='Device')
    context = Variables.task_call(dev_var)
    
    mano_me_id = context["nfvo_device"][3:]
    mano_ip    = Device(device_id=mano_me_id).management_address
    mano_var   = Device(device_id=mano_me_id).get_configuration_variable("HTTP_PORT")
    mano_port  = mano_var.get("value")
    mano_user  = Device(device_id=mano_me_id).login
    mano_pass  = Device(device_id=mano_me_id).password
    
    context["mano_ip"]   = mano_ip
    context["mano_port"] = mano_port
    context["mano_user"] = mano_user
    context["mano_pass"] = mano_pass
    
    #Get SOL005 version.
    sol005_version_var   = Device(device_id=mano_me_id).get_configuration_variable("SOL005_VERSION")
    sol005_version  = sol005_version_var.get("value")
    context.update(sol005_version=sol005_version)
    
    ret = MSA_API.process_content('ENDED', f'Task OK', context, True)
    print(ret)
