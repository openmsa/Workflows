from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call()
    
    context["test_var_01"] = context["UBIQUBEID"]

    ret = MSA_API.process_content('ENDED', f'{context["UBIQUBEID"]}', context, True)
    print(ret)

