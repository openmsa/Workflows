import os
import sys
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.repository import Repository
from msa_sdk import constants


dev_var = Variables()
context = Variables.task_call(dev_var)

#Initial Repository object.
repository = Repository()

#Define variables.
ms_path = context['microservice_path']
device_id = context['device_id']

#Get the ME current attached deployment setting profile id.
response = json_decode(_device_asset_by_id(device_id), True)
current_deplyment_settings_id = response['wo_newparams']['configProfileId']

#Prepare array to update deployment settings profile.
matches = array()
result = preg_match('@^\S+?(CommandDefinition.+?)@', ms_path, matches)
uris_array = dict(uri=matches[1])

#Update deployment settings profile.
response = repository.attach_microservices_from_configuration_profile(current_deplyment_settings_id, uris_array)
response = json.loads(device.content)
status = response.get('status')
context.update(device_create_reponse=response)
if status == constants.FAILED:
    ret = MSA_API.process_content(constants.FAILED, 'Failed to create corresponding Ansible host ME with name= "'+me_name+'"', context, True)
    print(ret)

#Clean up context.
context['variables_line'] = ''
context['microservice_create_line'] = ''
context['playbook_variables'] = dict()
context['microservice_name'] = ''

#Finish the task.
ret = MSA_API.process_content(constants.ENDED, 'Success. Deployment settings profile has been updated successfully.', context, True)
print(ret)