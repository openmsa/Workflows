import json
import uuid
import os
import errno
import sys
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('nsd_name', var_type='String')
dev_var.add('nsd_contents', var_type='String')
context = Variables.task_call(dev_var)

#get 'vnfd_name' from context.
nsd_name = context.get('nsd_name_uuid')

filename = '/opt/fmc_repository/Datafiles/NFV/NSD/' + nsd_name + '/Definitions/' + nsd_name + '.yaml'

#get VNFD contents from input variable.
nsd_contents = ''
if 'nsd_contents' in context:
    nsd_contents = context.get('nsd_contents')

#create file in http server directory.
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(filename, "w") as file:
    file.write(nsd_contents)
    file.close()

MSA_API.task_success('NS Descriptor definition is created successfully.', context, True)