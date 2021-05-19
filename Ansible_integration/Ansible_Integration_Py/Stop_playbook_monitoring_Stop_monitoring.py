import os
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants

dev_var = Variables()
context = Variables.task_call(dev_var)

if __name__ == "__main__":
    
    #This is not good way to finish process, but since we are in a loop, lets do it.
    
    service_id = context['service_id']
    
    #Create bash string
    kill_command = '/bin/kill -s TERM (ps aux | grep -v awk | awk \'/^jboss.+?[Aa]nsible.+?'+service_id+'/ {print 2}\')'
    result = os.system(kill_command)
    
    if result != 0:
        ret = MSA_API.process_content(constants.FAILED, 'Failed to create bash string.', context, True)
        print(ret)
        sys.exit()
        
    ret = MSA_API.process_content(constants.ENDED, 'Task success.', context, True)
    print(ret)
