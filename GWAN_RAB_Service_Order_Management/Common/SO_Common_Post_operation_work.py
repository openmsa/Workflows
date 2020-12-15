import json
import os
import errno
import time
import re
from json2html import *
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from SO_Common_Pre_operation_work import *

dev_var = Variables()
dev_var.add('check_config_first', var_type='Boolean')
dev_var.add('parsed_config', var_type='Link')

context = Variables.task_call(dev_var)


####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Get device id (router) from context (e.g: UBI2455).
device_ref = context['device_external_ref']
#device_ref = context['device_id']
device_id = device_ref[3:]

########## Do backup of the device running-config. 

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

SERVICE_NAME = 'Process/nttcw-gwan-rab-wf/Backup_Configuration_Management/Backup_Configuration_Management'
CREATE_PROCESS_NAME = 'New_Service'
ADD_PROCESS_NAME = 'Backup_Configuration_Management'
service_instance_name = 'backup_configuration_service_instance'

#instantiate Configuration Backup Management WF.
create_new_service(context, orch, SERVICE_NAME, CREATE_PROCESS_NAME, service_instance_name)

#execute do backup of the device running-configuration service process.
details = execute_do_backup_config_process(context, orch, SERVICE_NAME, ADD_PROCESS_NAME, service_instance_name)

#extract backup revisionId from 'execute_do_backup_config_process()' response details.
ret = re.search(':(\d+)', details, re.IGNORECASE)

if ret:
    revision_id = ret.group(1)
    context.update(post_op_backup_revision_id=revision_id)
    
#
ret = MSA_API.process_content(constants.ENDED, 'Device running-configuration backup is created successfully with revision_id: ' + details, context, True)
print(ret)