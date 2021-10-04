from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order


dev_var = Variables()
context = Variables.task_call()


ms_sdwan_ipsec_start = {context['id']: {"object_id": context['id']}}

try:
  order = Order(context['short_device_id'])
  order.command_execute('UPDATE', {"sdwan_ipsec_start": ms_sdwan_ipsec_start})
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)

ret = MSA_API.process_content('ENDED',
                              f'Take IPsec control.',
                              context, True)

print(ret)
