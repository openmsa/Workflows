import os
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call(dev_var)

if __name__ == '__main__':

    #Get VNF Descriptor (CSAR file) absolute filename from context.
    vnfd_filename = context.get('vnfd_csar_file')
    
    #Delete VNF Descriptor (CSAR file)
    if os.path.isfile(vnfd_filename):
    	os.remove(vnfd_filename)

    MSA_API.task_success('VNF Descriptor TOSCA is deleted successfully.', context, True)