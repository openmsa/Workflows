import os
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call(dev_var)

if __name__ == '__main__':

    #Get NSD Descriptor (CSAR file) absolute filename from context.
    nsd_filename = context.get('nsd_csar_file')
    
    #Delete NSD Descriptor (CSAR file)
    if os.path.isfile(nsd_filename):
    	os.remove(nsd_filename)

    MSA_API.task_success('NS Descriptor is deleted successfully.', context, True)