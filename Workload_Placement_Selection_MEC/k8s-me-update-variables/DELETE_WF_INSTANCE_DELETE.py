from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

if __name__ == "__main__":

    ret = MSA_API.process_content('ENDED', 'WF INSTANCE REMOVED', context, True)
    print(ret)