import json
import uuid
import os
import errno
import sys
import base64
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('vnfd_name', var_type='String')
dev_var.add('vnfd_contents', var_type='String')
context = Variables.task_call(dev_var)

#get 'vnfd_name' from context.
vnfd_name = context.get('vnfd_name_uuid')

filename = '/opt/fmc_repository/Datafiles/NFV/VNFD/' + vnfd_name + '/Definitions/' + vnfd_name + '.yaml'

#get VNFD contents from input variable.
vnfd_contents = ''
if 'vnfd_contents' in context:
    vnfd_contents = context.get('vnfd_contents')

#create file in http server directory.
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(filename, "w") as file:
    file.write(vnfd_contents)
    file.close()

MSA_API.task_success('VNFD TOSCA Sol001 meta was created successfully.', context, True)