import json
import copy
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
####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Get device id (router) from context (e.g: UBI2455).
device_ref = context['device_external_ref']
device_id = device_ref[3:]

#Get StaticRouting dictionary object from context.
acl_dicts = context['ACL']

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

#Static Routing Management WF service name constant variable.
SERVICE_NAME = 'Process/nttcw-gwan-rab-wf/Access_List_Management/Access_List_Management'
CREATE_PROCESS_NAME = 'New_Service'
ADD_PROCESS_NAME = 'Add_ACL'
service_id = ''
service_ext_ref = ''
#Instantiate new Static_Routing_Management WF dedicated for the device_id.
if not 'acl_service_instance' in context:
    data = dict(device_id=device_ref)
    response = orch.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
    #context['response'] = response
    status = response.get('status').get('status')
    if status == constants.ENDED:
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #Store service_instance_id of Static_Routing_Management WF in context.
            context['acl_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
        else:
            ret = MSA_API.process_content(constants.FAILED, 'Missing service id return by orchestration operation.', context, True)
            print(ret)
    else:
        ret = MSA_API.process_content(constants.FAILED, 'Execute service operation failed.', context, True)
        print(ret)
#Update service_instance external reference to "ACL_" + device_ext_ref (e.g: ACL_UBI2455).
#service_ext_ref = 'ACL_' + device_ext_ref

#Loop in acl dictionaries and in acl list by calling the Access_List_Management process 'Add_ACL'.
data = dict()
for key, acl_list  in acl_dicts.items():
    acl_name = ''
    #ensure acl_list is not empty otherwise break the loop.
    if len(acl_list):
        count = 0
        data_acl_list = list()
        #loop in acl list.
        for acl in acl_list:
            data_acl_dict = dict()
            if isinstance(acl, dict):
                if count == 0:
                    acl_name = acl.get('acl_name')
                else:
                    data_acl_dict['condition'] = get_config_param_val(context, acl, 'conditions')
                    data_acl_dict['protocol'] = get_config_param_val(context, acl, 'protocol')
                    data_acl_dict['src_address'] = get_config_param_val(context, acl, 'source_address')
                    data_acl_dict['src_wildcard'] = get_config_param_val(context, acl, 'source_wildcardmask')
                    data_acl_dict['src_port'] = get_config_param_val(context, acl, 'source_port', False)
                    data_acl_dict['dst_address'] = get_config_param_val(context, acl, 'destination_address')
                    data_acl_dict['dst_wildcard'] = get_config_param_val(context, acl, 'destination_wildcardmask')
                    data_acl_dict['dst_port'] = get_config_param_val(context, acl, 'destination_port', False)

                if data_acl_dict:
                    data_acl_list.append(data_acl_dict.copy())
                count +=1
        #prepare data dict
        data['acl_name'] = acl_name
        data['acl'] = data_acl_list
        #execute 'Access_List_Management' process 'Add_ACL'
        if isinstance(data, dict) and acl_name:
            service_ext_ref = context.get('acl_service_instance').get('external_ref')
            orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, ADD_PROCESS_NAME, data)
            response = json.loads(orch.content)
            status = response.get('status').get('status')
            if status == constants.FAILED:
                ret = MSA_API.process_content(constants.FAILED, 'Execute service by reference operation is failed. More details are available in Static Routing Management with service instance external ref. ' + service_ext_ref, context, True)
                print(ret)

ret = MSA_API.process_content(constants.ENDED, 'Access-list added successfully to the device ' + device_ref, context, True)
print(ret)