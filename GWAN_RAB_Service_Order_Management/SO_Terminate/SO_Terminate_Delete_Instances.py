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

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################


instance_names = ["static_routing_service_instance", "service_policy_service_instance", "policy_map_service_instance", "class_map_service_instance", "backup_configuration_service_instance","acl_service_instance" ]

error=[]

all_removed_instances=''

for instance_name in instance_names:
  instance_id =''
  if instance_name in context:
    values = context.get(instance_name) # {  "external_ref": "RABSID650", "instance_id": 650  }
    if 'instance_id' in values:
      instance_id = values.get('instance_id')

      orch.action = 'Delete one instance'
      # API /orchestration/v1/service/instance/{serviceId} : Delete service instance 
      orch.path = "/orchestration/v1/service/instance/"+str(instance_id)

      orch.call_delete()
      context['delete_instance_'+instance_name] = instance_id
      if orch and orch.content:
        response = json.loads(orch.content)
        #context['delete_resultjson_'+instance_name] = response 
        # response: empty if OK, else  {  "{\"wo_status\": \"FAIL\", \"wo_comment\": \"Delete one instance\", \"wo_newparams\": \
        status = response.get('wo_status')
        if status != constants.FAILED:
          all_removed_instances = all_removed_instances +   ' ,' +instance_name
      else:
        # no return if OK
        all_removed_instances = all_removed_instances +   ' ,' +instance_name
  else:
   error[instance_name] = 'Can not find instance id of ' + instance_name;

ret = MSA_API.process_content(constants.ENDED, 'All instances "' + all_removed_instances + '" removed', context, True)
print(ret)
