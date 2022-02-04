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
context = Variables.task_call(dev_var)

#get uuid from context.
uuid_gen = context.get('uuid_gen')

nsd_name = uuid_gen
if 'nsd_name' in context:
    name = context.get('nsd_name')
    if name:
        nsd_name = name + '_' + uuid_gen

TOSCA_meta = 'TOSCA.meta'
filename = '/opt/fmc_repository/Datafiles/NFV/NSD/' + nsd_name + '/TOSCA-Metadata/' + TOSCA_meta

#nsd_sol0001_schema content

TOSCA_meta_contents = """
TOSCA-Meta-File-Version: 1.0
CSAR-Version: 1.1
Created-By: OASIS TOSCA TC
Entry-Definitions: Definitions/""" + nsd_name + '.yaml'

#create file in http server directory.
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    with open(filename, "w") as file:
        file.write(TOSCA_meta_contents)
        file.close()

MSA_API.task_success('NSD TOSCA Sol001 meta was created successfully.', context, True)