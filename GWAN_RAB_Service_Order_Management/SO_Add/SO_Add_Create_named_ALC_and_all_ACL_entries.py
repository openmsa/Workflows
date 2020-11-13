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
    if status == 'ENDED':
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #Store service_instance_id of Static_Routing_Management WF in context.
            context['acl_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
        else:
            ret = MSA_API.process_content('FAILED', 'Missing service id return by orchestration operation.', context, True)
            print(ret)
    else:
        ret = MSA_API.process_content('FAILED', 'Execute service operation failed.', context, True)
        print(ret)
#Update service_instance external reference to "ACL_" + device_ext_ref (e.g: ACL_UBI2455).
#service_ext_ref = 'ACL_' + device_ext_ref

#Loop in acl dictionaries and in acl list by calling the Access_List_Management process 'Add_ACL'.
data = dict()
data_acl_list = list()
data_acl_dict = dict()
count = 0
for key, acl_list  in acl_dicts.items():
    acl_name = ''
    #ensure acl_list is not empty otherwise break the loop.
    if len(acl_list):
        #loop in acl list.
        for acl in acl_list:
            if isinstance(acl, dict):
                if count == 0:
                    acl_name = acl.get('acl_name')
                else:
                    data_acl_dict['condition'] = acl.get('conditions')
                    data_acl_dict['protocol'] = acl.get('protocol')
                    data_acl_dict['src_address'] = acl.get('source_address')
                    data_acl_dict['src_wildcard'] = acl.get('source_wildcardmask')
                    data_acl_dict['src_port'] = acl.get('source_port')
                    data_acl_dict['dst_address'] = acl.get('destination_address')
                    data_acl_dict['dst_wildcard'] = acl.get('destination_wildcardmask')
                    data_acl_dict['dst_port'] = acl.get('destination_port')
                    data_acl_list.append(data_acl_dict)
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
        if status == 'FAIL':
            ret = MSA_API.process_content('FAILED', 'Execute service by reference operation is failed. More details are available in Static Routing Management with service instance external ref. ' + service_ext_ref, context, True)
            print(ret)

ret = MSA_API.process_content('ENDED', 'Access-list added successfully to the device ' + device_ref, context, True)
print(ret)