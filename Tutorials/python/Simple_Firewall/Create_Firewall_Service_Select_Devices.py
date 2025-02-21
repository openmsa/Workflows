from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('devices.0.id', var_type='Device')
dev_var.add('devices.0.A.0.elt1')
dev_var.add('devices.0.A.0.elt2')

context = Variables.task_call(dev_var)
ret = MSA_API.process_content('ENDED',
                              f'Firewall service created. {len(context["devices"])} Managed Entity selected',
                              context, True)
print(ret)
