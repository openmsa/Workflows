from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('device_id', var_type='Device')
    dev_var.add('mano_user', var_type='String')
    dev_var.add('mano_pass', var_type='Password')
    context = Variables.task_call(dev_var)

    device_short_id = context['device_id'][3:]

    order = Order(str(device_short_id))
    order.command_synchronize(timeout=60)

    ret = MSA_API.process_content('ENDED',
        f'Device {context["device_id"]} synchronized', context, True)

    print(ret)