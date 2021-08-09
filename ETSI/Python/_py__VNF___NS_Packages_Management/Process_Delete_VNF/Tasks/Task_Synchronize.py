from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    context = Variables.task_call()
    
    ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
    print(ret)
