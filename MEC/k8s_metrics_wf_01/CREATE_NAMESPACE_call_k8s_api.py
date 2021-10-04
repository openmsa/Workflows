import random
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

context = Variables.task_call()

device_id_list = context["device_id_list"]
ms_vars_dict_list = context["ms_vars_dict_list"]

def rand_int():
    return ''.join(random.choice('0123456789') for i in range(8))

for device in device_id_list.values():
    for ms_var_dict in ms_vars_dict_list.values():
        Order(device).command_execute('CREATE', {'k8s_namespaces': {rand_int(): ms_var_dict}})


ret = MSA_API.process_content('ENDED', f'Namespace has been created', context, True)
print(ret)