import json
import typing
import os
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.conf_profile import ConfProfile
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('vim_device', var_type='Device')
dev_var.add('servers', var_type='OBMFRef')
dev_var.add('images', var_type='OBMFRef')
context = Variables.task_call(dev_var)

if __name__ == "__main__":
    #Get image will be used for the rebuild server instance.
    image_id = context.get('images')
    
    #Get VNF instance (server instance id - openstack)
    server_object_id = context.get('servers')

    #get device_id from context
    device_id = context['vim_device'][3:]

    #Initiate Order object with the device_id
    obmf = Order(device_id)

    command = 'UPDATE'
    
    ##build MS the dictionary input object 
    config = dict()
    action = 'Server Action'
    server_action = "Rebuild"
    config.update(action=action)
    config.update(server_action=server_action)
    config.update(action_arg1=image_id)
    # # mandatory params in MS so passing them empty here
    config.update(image_id='')
    config.update(flavor_id='')
    
    obj = {server_object_id:config}
    
    ms_name = 'servers'
    params = {ms_name : obj}

    obmf.command_execute(command, params, timeout = 300) #execute the MS UPDATE servers
    response = json.loads(obmf.content)
    
    if response.get('wo_status') == constants.FAILED:
        details = ''
        if 'wo_newparams' in response:
            details = response.get('wo_newparams')
        MSA_API.task_error('Failure details: ' + details, context, True)
    
    # store OBMF command execution response in context
    context['response'] = response.get('wo_newparams')


    MSA_API.task_success('VNF rebuild successful', context, True)
