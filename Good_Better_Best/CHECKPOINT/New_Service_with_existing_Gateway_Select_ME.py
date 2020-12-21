import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('device', var_type='Device')
dev_var.add('gateway', var_type='String')
context = Variables.task_call(dev_var)

context['service_id_display']=f'{context["SERVICEINSTANCEID"]} - Firewall {context["device"]}';

ret = MSA_API.process_content('ENDED',
                              f'Service created. Managed Entity: {context["device"]}',
                              context, True)
print(ret)
