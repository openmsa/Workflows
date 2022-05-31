from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
context = Variables.task_call()

sdwan_loopback_ms_data = {context['id']: {"object_id": context['id']}}
sdwan_ipsec_secret_ms_data = {context['id']: {"object_id": context['id']}}
sdwan_ipsec_conf_ms_data = {context['id']: {"object_id": context['id']}}
sdwan_ipsec_conf_cryptomap_ms_data = {context['id']: {"object_id": context['id']}}

# left device cleanup
try:
    order = Order(context["left_device_id"])
    order.command_execute("DELETE", {"sdwan_loopback": sdwan_loopback_ms_data})
    order.command_execute("DELETE", {"sdwan_ipsec_secret": sdwan_ipsec_secret_ms_data})
    order.command_execute("DELETE", {"sdwan_ipsec_conf": sdwan_ipsec_conf_ms_data})
    order.command_execute("DELETE", {"sdwan_ipsec_conf_cryptomap": sdwan_ipsec_conf_cryptomap_ms_data})
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

# right device cleanup
try:
    order = Order(context["right_device_id"])
    order.command_execute("DELETE", {"sdwan_loopback": context['id']})
    order.command_execute("DELETE", {"sdwan_ipsec_secret": context['id']})
    order.command_execute("DELETE", {"sdwan_ipsec_conf": context['id']})
    order.command_execute("DELETE", {"sdwan_ipsec_conf_cryptomap": context['id']})
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

ret = MSA_API.process_content('ENDED', f'IPsec instance deleted.', context, True)

print(ret)
