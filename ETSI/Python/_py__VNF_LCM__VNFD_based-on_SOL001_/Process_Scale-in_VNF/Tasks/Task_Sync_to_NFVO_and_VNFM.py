from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    nfvo_short_id = context["nfvo_device"][3:]
    vnfm_short_id = context["vnfm_device"][3:]

    order1 = Order(str(nfvo_short_id))
    order1.command_synchronize(timeout=60)
    
    order2 = Order(str(vnfm_short_id))
    order2.command_synchronize(timeout=60)

    ret = MSA_API.process_content('ENDED',
        f'Devices {context["nfvo_device"]} {context["vnfm_device"]} synchronized',
        context, True)

    print(ret)
