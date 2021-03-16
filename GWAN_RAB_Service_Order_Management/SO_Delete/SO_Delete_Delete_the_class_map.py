import json
import time
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################
'''
Get parameters values from dictionary.

@param context:
    Service instance context.
@param dict:
    data dictionary.
@param param: 
    Parameter key name.
@param is_madatory:
    True or False is parameter is mandatory or not.
@return: 
    Parameter value.
'''
def get_config_param_val(context, dict, param, is_madatory=True):
    value = ''
    if param in dict:
        value = dict.get(param)
        if is_madatory == True:
            if not value:
                ret = MSA_API.process_content(constants.FAILED, 'The required input "' + param + '" value is empty.', context, True)
                print(ret)
    elif is_madatory == True:
        ret = MSA_API.process_content(constants.FAILED, 'The required input parameter "' + param + '" key in the policy_map object is missing.', context, True)
        print(ret)
        
    return value

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
####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Get device id (router) from context (e.g: UBI2455).
device_ref = context['device_external_ref']
#device_ref = context['device_id']
device_id = device_ref[3:]

#Get StaticRouting dictionary object from context.
class_map_list = context['ClassMap']

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

#Static Routing Management WF service name constant variable.
SERVICE_NAME = 'Process/nttcw-gwan-rab-wf/Class_Map_Management/Class_Map_Management'
CREATE_PROCESS_NAME = 'New_Service'
ADD_PROCESS_NAME = 'Delete_Class_Map'
service_id = ''
service_ext_ref = ''
#Instantiate new Class_Map_Service_Mangement WF dedicated for the device_id.
if not 'class_map_service_instance' in context:
    data = dict(device_id=device_ref, SO_service_instance_id=context['SERVICEINSTANCEID'], SO_service_external_ref=context['SERVICEINSTANCEREFERENCE'])
    orch.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
    response = json.loads(orch.content)
    context['response'] = response
    status = response.get('status').get('status')
    if status == constants.ENDED:
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #Store service_instance_id of Class_Map_Service_Mangement WF in context.
            context['class_map_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
        else:
            ret = MSA_API.process_content(constants.FAILED, 'Missing service id return by orchestration operation.', context, True)
            print(ret) 
    else:
        ret = MSA_API.process_content(constants.FAILED, 'Execute service operation failed.', context, True)
        print(ret) 
#Update service_instance external reference to "CLASS_MAP_" + device_ext_ref (e.g: CLASS_MAP_UBI2455).
#service_ext_ref = 'CLASS_MAP_' + device_ext_ref

#Loop in StaticRouting dictionary object by calling the Class_Map_Management process 'Delete Class Map'.
for class_map in class_map_list:
    # get parameters values from class_map dict
    class_map_name = get_config_param_val(context, class_map, 'class_map_name')
    method = get_config_param_val(context, class_map, 'method', False)
    acl = get_config_param_val(context, class_map, 'acl_name', False)
    
    #build data input parameter for Class_Map_Management baseline WF
    data = dict(method=method, object_id=class_map_name, acl=acl, SO_service_instance_id=context['SERVICEINSTANCEID'], SO_service_external_ref=context['SERVICEINSTANCEREFERENCE']) 
    if isinstance(data, dict):
        service_ext_ref = context.get('class_map_service_instance').get('external_ref')
        #execute Class_Map_Management WF 
        orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, ADD_PROCESS_NAME, data)
        response = json.loads(orch.content)
        service_id = response.get('serviceId').get('id')
        process_id = response.get('processId').get('id')
        #get service process details.
        response = get_process_instance(orch, process_id)
        status = response.get('status').get('status')
        details = response.get('status').get('details')
        if status == constants.FAILED:
            ret = MSA_API.process_content(constants.FAILED, 'Execute service operation is failed: ' + details + ' (#' + str(service_id) + ')', context, True)
            print(ret) 

ret = MSA_API.process_content(constants.ENDED, 'Class Map deleted successfully to the device ' + device_ref + ' (#' + str(service_id) + ')', context, True)
print(ret)
