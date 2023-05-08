from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('devices.0.device', var_type='Device')
    
    context = Variables.task_call(dev_var)

    ret = MSA_API.process_content('ENDED', 'Device(s) selected', context, True)
    print(ret)
