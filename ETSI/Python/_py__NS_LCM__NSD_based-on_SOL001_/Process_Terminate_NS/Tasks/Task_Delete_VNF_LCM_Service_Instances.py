import copy
import pandas
import glob
import json
import numpy as np
from re import search
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration


dev_var = Variables()
context = Variables.task_call(dev_var)

#Initiate orchestraction object.
ubiqube_id = context['UBIQUBEID']
orch = Orchestration(ubiqube_id)


error=[]

all_removed_instances=''

#Get from context VNF LCM service instances dict.
vnf_lcm_services_dict = context.get('vnf_lcm_services_dict')

for vnf_lcm_service in vnf_lcm_services_dict:
    instance_id = vnf_lcm_service.get('service_id')
    if instance_id:
        instance_id = values.get('instance_id')

        orch.action = 'Delete one instance'
        # API /orchestration/v1/service/instance/{serviceId} : Delete service instance 
        orch.path = "/orchestration/v1/service/instance/"+str(instance_id)

        orch._call_delete()
        context['delete_instance_'+instance_name] = instance_id
        if orch and orch.content:
            response = json.loads(orch.content)
            
            status = response.get('wo_status')
            if status != constants.FAILED:
                all_removed_instances = all_removed_instances +   ' ,' +instance_name
        else:
            # no return if OK
            all_removed_instances = all_removed_instances +   ' ,' +instance_name

MSA_API.task_success('All instances "' + all_removed_instances + '" removed', context, True)
