from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order


dev_var = Variables()
dev_var.add('id', var_type='Integer')
dev_var.add('device_id', var_type='Device')
context = Variables.task_call(dev_var)

short_device_id = context['device_id'][-3:]

context['short_device_id'] = short_device_id

ms_sdwan_ipsec_start = {context['id']: {"object_id": context['id']}}

context['ms_sdwan_ipsec_start'] = ms_sdwan_ipsec_start

try:
  order = Order(context['short_device_id'])
  order.command_execute('CREATE', {"sdwan_ipsec_start": ms_sdwan_ipsec_start})
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)

ret = MSA_API.process_content('ENDED',
                              f'Take IPsec control.',
                              context, True)

print(ret)
