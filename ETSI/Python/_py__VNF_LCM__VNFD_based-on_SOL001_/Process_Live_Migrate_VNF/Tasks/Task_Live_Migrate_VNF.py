import json
import typing
import os
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.conf_profile import ConfProfile
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003

'''
Get hypervisor hostname (Host) by ID.
'''
def _get_hypervisor_hostname_by_id(order_object, vim_me_id, host_id):
    object_name = 'hosts'
    command = 'IMPORT'
    params = dict()
    params[object_name] = "0"
    #Import the given device microservice from the device, the MS values in the UI will be not updated.
    obmf.command_call(command, 0, params)
    response = json.loads(obmf.content)
    #context.update(obmf_sync_resp=response)
    if 'entity' in response and 'message' in response.get('entity'):
        message = response.get('entity').get('message')
        message = json.loads(message) 
        context.update(ms_entity_message= message)
        hosts = message.get(object_name)
        if hosts and hosts.values():
            for host in hosts.values():
                if host.get('object_id') == host_id:
                    return host.get('hypervisor_hostname')
    return None


dev_var = Variables()
dev_var.add('vim_device', var_type='Device')
dev_var.add('host', var_type='OBMFRef')
context = Variables.task_call(dev_var)

if __name__ == "__main__":
    #Get host id.
    host_id = context.get('host')
    
    #Get VNF instance (server instance id - openstack)
    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    r = vnfLcm.vnf_lcm_get_vnf_instance_details(context["vnf_instance_id"])
    
    vnfResourcesList = r.json()["instantiatedVnfInfo"]["vnfcResourceInfo"]
    #server_object_id = vnfResourcesList[0]["computeResource"]["resourceId"]
    
    for index, vnfR in enumerate(vnfResourcesList):
        vnfResourceId = vnfR["computeResource"]["resourceId"]
        #get device_id from context
        device_id = context['vim_device'][3:]
        
        #Initiate Order object with the device_id
        obmf = Order(device_id)
        
        #Get hypervisor hostname based-on the host_id.
        hypervisor_hostname = _get_hypervisor_hostname_by_id(obmf, device_id, host_id)
        
        if hypervisor_hostname == None:
            MSA_API.task_error('Failed to get hypervisor hostname by host ID.', context, True)
            
        #Commande method
        command = 'UPDATE'
        
        ##build MS the dictionary input object 
        config = dict()
        action = 'Server Action'
        server_action = "Live Migrate"
        block_migration = "False"
        disk_over_commit = "False"
        config.update(action=action)
        config.update(server_action=server_action)
        config.update(action_arg1=hypervisor_hostname)
        config.update(action_arg2=block_migration)
        config.update(action_arg3=disk_over_commit)
        # mandatory params in MS so passing them empty here
        config.update(image_id='')
        config.update(flavor_id='')
        
        obj = {vnfResourceId:config}
        
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
        
        
    MSA_API.task_success('VNF live migration successful', context, True)
