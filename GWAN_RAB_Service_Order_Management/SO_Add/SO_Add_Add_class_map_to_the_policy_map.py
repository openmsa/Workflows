import json
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
    value = class_map.get(param)
    if not value and is_madatory == True:
        ret = MSA_API.process_content('FAILED', 'Missing required input "' + param + '" value.', context, True)
        print(ret)
        
    return value

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

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
    data = dict(device_id=device_ref)
    response = orch.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
    #context['response'] = response
    status = response.get('status').get('status')
    if status == 'ENDED':
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #Store service_instance_id of Policy_Map_Management WF in context.
            context['policy_map_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
        else:
            ret = MSA_API.process_content('FAILED', 'Missing service id return by orchestration operation.', context, True)
            print(ret)
    else:
        ret = MSA_API.process_content('FAILED', 'Execute service operation failed.', context, True)
        print(ret)
#Update service_instance external reference to "ACL_" + device_ext_ref (e.g: ACL_UBI2455).
#service_ext_ref = 'ACL_' + device_ext_ref

#Loop in policy_map dictionaries and in policy_map list by calling the Policy_Map_Management process 'Add_ACL'.
data = dict()
data_policy_map_list = list()
data_policy_map_dict = dict()
count = 0
for key, policy_map_list  in policy_map_dicts.items():
    policy_map_name = ''
    #ensure policy_map_list is not empty otherwise break the loop.
    if len(policy_map_list):
        #loop in policy_map list.
        for policy_map in policy_map_list:
            if isinstance(policy_map, dict):
                if count == 0:
                    policy_map_name = get_config_param_val(context, policy_map, 'policy_map_name')
                else:
                    data_policy_map_dict['class_name'] = get_config_param_val(context, policy_map, 'class_name')
                    data_policy_map_dict['cir_before'] = get_config_param_val(context, policy_map, 'cir_before', False)
                    data_policy_map_dict['cir_after'] = get_config_param_val(context, policy_map, 'cir_after', False)
                    data_policy_map_dict['bc_before'] = get_config_param_val(context, policy_map, 'bc_before', False)
                    data_policy_map_dict['bc_after'] = get_config_param_val(context, policy_map, 'bc_after', False)
                    data_policy_map_dict['be_before'] = get_config_param_val(context, policy_map, 'be_before', False)
                    data_policy_map_dict['be_after'] = get_config_param_val(context, policy_map, 'be_after', False)
                    data_policy_map_dict['conform_action'] = get_config_param_val(context, policy_map, 'conform_action')
                    data_policy_map_dict['exceed_action'] = get_config_param_val(context, policy_map, 'exceed_action')
                    data_policy_map_dict['violate_action'] = get_config_param_val(context, policy_map, 'violate_action')
                    
                    data_policy_map_list.append(data_policy_map_dict)
            count +=1    
        #prepare data dict
        data['policy_map_name'] = policy_map_name
        data['policy'] = data_policy_map_list

    #execute 'Policy_Map_Management' process 'Add_Policy_Map'
    if isinstance(data, dict):
        service_ext_ref = context.get('policy_map_service_instance').get('external_ref')
        orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, ADD_PROCESS_NAME, data)
        response = json.loads(orch.content)
        status = response.get('status').get('status')
        if status == 'FAIL':
            ret = MSA_API.process_content('FAILED', 'Execute service by reference operation is failed. More details are available in Static Routing Management with service instance external ref. ' + service_ext_ref, context, True)
            print(ret)

ret = MSA_API.process_content('ENDED', 'Policy-map configuration added successfully to the device ' + device_ref, context, True)
print(ret)