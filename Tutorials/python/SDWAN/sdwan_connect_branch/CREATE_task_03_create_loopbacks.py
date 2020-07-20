from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order


dev_var = Variables()
context = Variables.task_call()

# (1) loopback
try:
    '''check if loopback already exists'''
    # order = Order(left_device_id)
    # order.command_execute('IMPORT', {"sdwan_loopback": context["id"]})
    order = Order(context["left_device_id"])
    order.command_execute("CREATE", context["sdwan_loopback_left"])
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

try:
    order = Order(context["right_device_id"])
    order.command_execute('CREATE', context["sdwan_loopback_right"])
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)

ret = MSA_API.process_content('ENDED',
                              f'Loopbacks Created.',
                              context, True)

print(ret)
