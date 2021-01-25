import json
import os
import errno
import time
import re
import sys
from json2html import *
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('check_config_first', var_type='Boolean')
dev_var.add('parsed_config', var_type='Link')

context = Variables.task_call(dev_var)


####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################
'''
Write in http server repository file the configurations from the context.

'''
def write_configs_to_http_repo():
    #retrieve configuration from the context.
    acl_config = json.dumps(context['ACL'])
    acl_config = json2html.convert(json = acl_config)
    service_policy_config = json.dumps(context['ServicePolicy'])
    service_policy_config = json2html.convert(json = service_policy_config)
    class_map_config = json.dumps(context['ClassMap'])
    class_map_config = json2html.convert(json = class_map_config)
    policy_map_config = json.dumps(context['policyMaps'])
    policy_map_config = json2html.convert(json = policy_map_config)
    static_routing_config = json.dumps(context['StaticRouting'])
    static_routing_config = json2html.convert(json = static_routing_config)
    
    #filename is created based-on the device external reference
    path_separator = '/'
    repo_base = '/opt/fmc_repository'
    repo_path = '/Datafiles/GWAN_RAB/Configurations'
    device_external_ref = context['device_external_ref']
    service_instance_id = context['SERVICEINSTANCEID']
    file_extension = '.html'
    file_name = repo_path + path_separator + device_external_ref + '_configuration_' + service_instance_id + file_extension
    filename_full_path = repo_base + file_name
    #create file in http server directory.
    if not os.path.exists(os.path.dirname(filename_full_path)):
        try:
            os.makedirs(os.path.dirname(filename_full_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename_full_path, "w") as file:
        file.write("<h1>Static Routing</h1>")
        file.write("<p>")
        file.write(static_routing_config)
        file.write("</p>")
        file.write("<h1>Service Policy</h1>")
        file.write("<p>")
        file.write(service_policy_config)
        file.write("<h1>Class Map</h1>")
        file.write("<p>")
        file.write(class_map_config)
        file.write("</p>")
        file.write("<h1>Policy Map</h1>")
        file.write("<p>")
        file.write(policy_map_config)
        file.write("</p>")
        file.write("<h1>Access list (ACL)</h1>")
        file.write("<p>")
        file.write(acl_config)
        file.write("</p>")
        file.close()

    return file_name

'''
Instantiate Configuration Backup Management WF.

'''
def create_new_service(context, orch, service_name, process_name, service_instance_name):

    #Instantiate new Backup_Configuration_Service_Mangement WF dedicated for the device_id.
    if not service_instance_name in context:
        data = dict(device_id=device_ref)
        orch.execute_service(service_name, process_name, data)
        response = json.loads(orch.content)
        context['response'] = response
        status = response.get('status').get('status')
        if status == constants.ENDED:
            if 'serviceId' in response:
                service_id = response.get('serviceId').get('id')
                service_ext_ref = response.get('serviceId').get('serviceExternalReference')
                #Store service_instance_id of Backup_Configuration_Service_Mangement WF in context.
                context[service_instance_name] = dict(external_ref=service_ext_ref, instance_id=service_id)
            else:
                ret = MSA_API.process_content(constants.FAILED, 'Missing service id return by orchestration operation.', context, True)
                print(ret)
        else:
            ret = MSA_API.process_content(constants.FAILED, 'Execute service operation failed.', context, True)
            print(ret)
 
'''
Retrieve process instance by service instance ID.

@param orch:
    Ochestration class object reference.
@param process_id:
    Baseline workflow process ID.
@param timeout:
    loop duration before to break.
@param interval:
    loop time interval.
@return:
    Response of the get process instance execution.
'''
def get_process_instance(orch, process_id, timeout=60, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #get service instance execution status.
        orch.get_process_instance(process_id)
        response = json.loads(orch.content)
        status = response.get('status').get('status')
        #context.update(get_process_instance=status)
        if status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)

    return response

'''
Do backup of the device running-configuration.
'''
def execute_do_backup_config_process(context, orch, service_name, process_name, service_instance_name, data={}):
    service_ext_ref = context.get(service_instance_name).get('external_ref')
    #execute Backup_Configuration_Management WF 
    orch.execute_service_by_reference(ubiqube_id, service_ext_ref, service_name, process_name, data)
    response = json.loads(orch.content)
    process_id = response.get('processId').get('id')
    #get service process details.
    response = get_process_instance(orch, process_id)
    status = response.get('status').get('status')
    details = response.get('status').get('details')
    if status == constants.FAILED:
        ret = MSA_API.process_content(constants.FAILED, 'Execute service operation is failed: ' + details, context, True)
        print(ret)
    return details
####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Get device id (router) from context (e.g: UBI2455).
device_ref = context['device_external_ref']
#device_ref = context['device_id']
device_id = device_ref[3:]

########## Display parsed Configuration from spreadsheet.

skip_config_review = 'False'
if 'check_config_first' in context:
    skip_config_review = str(context['check_config_first'])
  
#wirte parsed configurations in repository Datafile.
file_name = write_configs_to_http_repo()

#set link value in the context varible 'parsed_config'.
context['parsed_config'] = file_name
    
if skip_config_review == 'False' or skip_config_review == 'false' or skip_config_review == False:
    #display to the GUI the configuration file URL.
    ret = MSA_API.process_content(constants.PAUSED, 'To review the configuration, click on the "Parsed Configuration" link.' , context, True)
    print(ret)
    sys.exit()

########## Do backup of the device running-config. 

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

SERVICE_NAME = 'Process/nttcw-gwan-rab-wf/Backup_Configuration_Management/Backup_Configuration_Management'
CREATE_PROCESS_NAME = 'New_Service'
ADD_PROCESS_NAME = 'Backup_Configuration_Management'
service_instance_name = 'backup_configuration_service_instance'

#instantiate Configuration Backup Management WF.
if not 'backup_configuration_service_instance' in context: 
    create_new_service(context, orch, SERVICE_NAME, CREATE_PROCESS_NAME, service_instance_name)

#execute do backup of the device running-configuration service process.
details = execute_do_backup_config_process(context, orch, SERVICE_NAME, ADD_PROCESS_NAME, service_instance_name)

#extract backup revisionId from 'execute_do_backup_config_process()' response details.
ret = re.search(':(\d+)', details, re.IGNORECASE)

if ret:
    revision_id = ret.group(1)
    context.update(pre_op_backup_revision_id=revision_id)

#    
ret = MSA_API.process_content(constants.ENDED, 'Device running-configuration backup is created successfully with revision_id: ' + details, context, True)
print(ret)