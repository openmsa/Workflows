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
#device_ref = context['device_id']
device_id = device_ref[3:]

#Get StaticRouting dictionary object from context.
service_policy_list = context['ServicePolicy']

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

#Static Routing Management WF service name constant variable.
SERVICE_NAME = 'Process/nttcw-gwan-rab-wf/Service_Policy_Management/Service_Policy_Management'
CREATE_PROCESS_NAME = 'New_Service'
ADD_PROCESS_NAME = 'Delete_Service_Policy'
service_id = ''
service_ext_ref = ''
#Instantiate new Static_Routing_Management WF dedicated for the device_id.
if not 'service_policy_service_instance' in context:
    data = dict(device_id=device_ref)
    response = orch.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
    context['response'] = response
    status = response.get('status').get('status')
    if status == 'ENDED':
        if 'serviceId' in response:
            service_id = response.get('serviceId').get('id')
            service_ext_ref = response.get('serviceId').get('serviceExternalReference')
            #Store service_instance_id of Static_Routing_Management WF in context.
            context['service_policy_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
        else:
            ret = MSA_API.process_content('FAILED', 'Missing service id return by orchestration operation.', context, True)
            print(ret) 
    else:
        ret = MSA_API.process_content('FAILED', 'Execute service operation failed.', context, True)
        print(ret) 
#Update service_instance external reference to "SERVICE_POLICY_" + device_ext_ref (e.g: SERVICE_POLICY_UBI2455).
#service_ext_ref = 'SERVICE_POLICY_' + device_ext_ref

#Loop in StaticRouting dictionary object by calling the Static_Routing_Management process 'Add Static routing'.
for sp in service_policy_list:
    data = dict(interface_name=sp['interface_name'], direction=sp['direction'], policy_name=sp['policy_name'])  
    if isinstance(data, dict):
        service_ext_ref = context.get('service_policy_service_instance').get('external_ref')
        response = orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, ADD_PROCESS_NAME, data)
        status = response.get('status').get('status')
        if status != 'ENDED':
            ret = MSA_API.process_content('FAILED', 'Execute service by reference operation is failed. More details are available in Static Routing Management with service instance external ref. ' + service_ext_ref, context, True)
            print(ret) 

ret = MSA_API.process_content('ENDED', 'Service Policy deleted successfully to the device ' + device_ref, context, True)
print(ret)
