import os
import sys
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call(dev_var)

displayed_config_filename = ''
if 'displayed_config_filename' in context:
    displayed_config_filename = context.get('displayed_config_filename')
    if displayed_config_filename:
        try:
            os.remove(displayed_config_filename)
        except OSError:
            pass
    
        ret = MSA_API.process_content(constants.ENDED, 'Configuration file was deleted successfully from: ' + displayed_config_filename + '.', context, True)
        print(ret)
        sys.exit()
    
ret = MSA_API.process_content(constants.ENDED, 'There is no configuration to be deleted.', context, True)
print(ret)