import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    device_short_id = context["nfvo_device"][3:]
    
    time.sleep(6)
    order = Order(str(device_short_id))
    order.command_synchronize(timeout=60)

    ret = MSA_API.process_content('ENDED',
        f'Device {context["nfvo_device"]} synchronized', context, True)

    print(ret)
