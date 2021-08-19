import json
import copy
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
Get parameters values from class_map dictionary.

@param context:
    Service instance context.
@param policy_map:
    policy_map dictionary.
@param param: 
    Parameter key name.
@param is_madatory:
    True or False is parameter is mandatory or not.
@return: 
    Parameter value.
'''
def get_config_param_val(context, policy_map, param, is_madatory=True):
    value = ''
    if param in policy_map:
        value = policy_map.get(param)
        if is_madatory == True:
            if not value:
                MSA_API.task_error('The required input "' + param + '" value is empty.', context, True)
    elif is_madatory == True:
        MSA_API.task_error('The required input parameter "' + param + '" key in the policy_map object is missing.', context, True)

    return value

'''
Retrieve process instance by service instance ID.

@param orch:
    Ochestration class object reference.
@param service_id:
    Baseline workflow service instance ID.
@param timeout:
    loop duration before to break.
@param interval:
    loop time interval.
@return:
    Response of the get process instance execution.
'''
def get_process_instance(orch, process_id, timeout = 600, interval=5):
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

if 'policyMaps' in context and context['policyMaps']:

    #Get device id (router) from context (e.g: UBI2455).
    device_ref = context['device_external_ref']
    device_id = device_ref[3:]

    #Get StaticRouting dictionary object from context.
    policy_map_dicts = context['policyMaps']

    #Initiate orchestraction object.
    ubiqube_id = context['UBIQUBEID']
    orch = Orchestration(ubiqube_id)

    #Static Routing Management WF service name constant variable.
    SERVICE_NAME = 'Process/nttcw-gwan-rab-wf/Policy_Map_Management/Policy_Map_Management'
    CREATE_PROCESS_NAME = 'New_Service'
    ADD_PROCESS_NAME = 'Add_Policy_Map'
    service_id = ''
    service_ext_ref = ''
    #Instantiate new Policy_Map_Management WF dedicated for the device_id.
    if not 'policy_map_service_instance' in context:
        data = dict(device_id=device_ref, SO_service_instance_id=context['SERVICEINSTANCEID'], SO_service_external_ref=context['SERVICEINSTANCEREFERENCE'])
        orch.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
        response = json.loads(orch.content)
        context['response'] = response
        status = response.get('status').get('status')
        if status == constants.ENDED:
            if 'serviceId' in response:
                service_id = response.get('serviceId').get('id')
                service_ext_ref = response.get('serviceId').get('serviceExternalReference')
                #Store service_instance_id of Policy_Map_Management WF in context.
                context['policy_map_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
            else:
                MSA_API.task_error('Missing service id return by orchestration operation.', context, True)
        else:
            MSA_API.task_error( 'Execute service operation failed.', context, True)
    #Update service_instance external reference to "ACL_" + device_ext_ref (e.g: ACL_UBI2455).
    #service_ext_ref = 'ACL_' + device_ext_ref

    #Loop in policy_map dictionaries and in policy_map list by calling the Policy_Map_Management process 'Add_ACL'.
    #loop which handling list of sheets
    data = dict(policy_map_list=[], SO_service_instance_id=context['SERVICEINSTANCEID'], SO_service_external_ref=context['SERVICEINSTANCEREFERENCE'])
    for key, policy_map_list  in policy_map_dicts.items():
        policy_map_name = ''
        #ensure policy_map_list is not empty otherwise break the loop.
        if len(policy_map_list):
            count = 0
            data_policy_map_list = list()
            policy_map_dict = dict()
            #loop in policy_map list (specific sheet config).
            for policy_map in policy_map_list:
                data_policy_map_dict = dict()
                if isinstance(policy_map, dict):
                    if count == 0:
                        policy_map_name = get_config_param_val(context, policy_map, 'policy_map_name')
                    else:
                        data_policy_map_dict['class_map'] = get_config_param_val(context, policy_map, 'class_name')
                        data_policy_map_dict['cir_before'] = get_config_param_val(context, policy_map, 'cir_before', False)
                        data_policy_map_dict['cir_after'] = get_config_param_val(context, policy_map, 'cir_after', False)
                        data_policy_map_dict['bc_before'] = get_config_param_val(context, policy_map, 'bc_before', False)
                        data_policy_map_dict['bc_after'] = get_config_param_val(context, policy_map, 'bc_after', False)
                        data_policy_map_dict['be_before'] = get_config_param_val(context, policy_map, 'be_before', False)
                        data_policy_map_dict['be_after'] = get_config_param_val(context, policy_map, 'be_after', False)
                        data_policy_map_dict['conform_action'] = get_config_param_val(context, policy_map, 'conform_action')
                        data_policy_map_dict['exceed_action'] = get_config_param_val(context, policy_map, 'exceed_action')
                        data_policy_map_dict['violate_action'] = get_config_param_val(context, policy_map, 'violate_action')

                    if data_policy_map_dict:
                        data_policy_map_list.append(data_policy_map_dict.copy())
                    count +=1
            #prepare data dict
            policy_map_dict['policy_map_name'] = policy_map_name
            policy_map_dict['policy'] = data_policy_map_list
            data['policy_map_list'].append(policy_map_dict.copy())


    #execute 'Policy_Map_Management' process 'Add_Policy_Map' 1 times
    if data['policy_map_list'] and isinstance(data, dict):
        service_ext_ref = context.get('policy_map_service_instance').get('external_ref')
        #execute service by ref.
        orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, ADD_PROCESS_NAME, data)
        response = json.loads(orch.content)
        service_id = response.get('serviceId').get('id')
        process_id = response.get('processId').get('id')
        #get service process details.
        response = get_process_instance(orch, process_id)
        status = response.get('status').get('status')
        details = response.get('status').get('details')
        if status == constants.FAILED:
            MSA_API.task_error( 'Execute service operation is failed: ' + details + ' (#' + str(service_id) + ')', context, True)


    MSA_API.task_success('Policy-map configuration added successfully to the device ' + device_ref + ' (#' + str(service_id) + ')', context, True)
MSA_API.task_success('No Policy-map configuration to be added to the device.', context, True)