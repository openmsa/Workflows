from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('test_var_01', var_type='String')
    
    context = Variables.task_call(dev_var)

    ret = MSA_API.process_content('WARNING', f'{context}', context, True)
    print(ret)

