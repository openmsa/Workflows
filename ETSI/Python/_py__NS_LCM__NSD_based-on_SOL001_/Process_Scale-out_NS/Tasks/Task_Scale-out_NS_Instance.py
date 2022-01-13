from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)

    ret = MSA_API.process_content('ENDED',
        f'NS Scale-out OK!',
        context, True)

    print(ret)