from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    vim_short_id = context['vim_device'][3:]

    order1 = Order(str(vim_short_id))
    order1.command_synchronize(timeout=60)
    
    ret = MSA_API.process_content('ENDED',
        f'Devices {context["vim_device"]} synchronized',
        context, True)

    print(ret)