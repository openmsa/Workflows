import json
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
#dev_var.add('var_name', var_type='String')

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
static_routing = context['StaticRouting']

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

#Static Routing Management WF service name constant variable.
SERVICE_NAME = 'Process/nttcw-gwan-rab-wf/Static_Routing_Management/Static_Routing_Management'
ADD_PROCESS_NAME = 'Delete_Static_Route'

#Loop in StaticRouting dictionary object by calling the Static_Routing_Management process 'Add Static routing'.
for route in static_routing:
    data = dict(source_address=route['source_address'], subnet_mask=route['subnet_mask'], vlan_id=route['vlan_id'], nexthop=route['nexthop'], distance=route['distance'])  
    if isinstance(data, dict):
        service_ext_ref = context.get('static_routing_service_instance').get('external_ref')
        orch.execute_service_by_reference(ubiqube_id, service_ext_ref, SERVICE_NAME, ADD_PROCESS_NAME, data)
        response = json.loads(orch.content)
        status = response.get('status').get('status')
        if status == constants.FAILED:
            ret = MSA_API.process_content(constants.FAILED, 'Execute service by reference operation is failed. More details are available in Static Routing Management with service instance external ref. ' + service_ext_ref, context, True)
            print(ret) 

ret = MSA_API.process_content(constants.ENDED, 'Static Routing deleted successfully to the device ' + device_ref, context, True)
print(ret)
