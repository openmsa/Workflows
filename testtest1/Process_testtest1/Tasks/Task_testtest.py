from msa_sdk.variables import Variables             
from msa_sdk.msa_api import MSA_API
#aaaa
dev_var = Variables()
dev_var.add('devices.0.id', var_type='Device')      

context = Variables.task_call(dev_var)              

ret = MSA_API.process_content('ENDED',              
                              f'Firewall service created. {len(context["devices"])} Managed Entity selected',
                              context, True)
print(ret)