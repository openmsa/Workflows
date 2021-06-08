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
    
        MSA_API.task_success('Configuration file was deleted successfully from: ' + displayed_config_filename + '.', context, True)
        sys.exit()
    
MSA_API.task_success('There is no configuration to be deleted.', context, True)
