import json
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants
import openstack

from custom.ETSI.NfviVim import NfviVim
from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005


'''
WIP - Use Openstacksdk to wait until server status is active

Get VIM connection.

def _get_vim_connection_auth(nfvo_device, vim_id):
    #Openstack Authification Connection.
    conn = ''
    
    #NFVO Info.
    nfvo_mano_me_id = context["nfvo_device"][3:]
    nfvo_mano_ip    = Device(device_id=nfvo_mano_me_id).management_address
    nfvo_mano_var   = Device(device_id=nfvo_mano_me_id).get_configuration_variable("HTTP_PORT")
    nfvo_mano_port  = nfvo_mano_var.get("value")
    nfvo_mano_user  = Device(device_id=nfvo_mano_me_id).login
    nfvo_mano_pass  = Device(device_id=nfvo_mano_me_id).password
    
    nfviVim = NfviVim(nfvo_mano_ip, nfvo_mano_port)
    nfviVim.set_parameters(nfvo_mano_user, nfvo_mano_pass)
    
    #Get VIM connection info by id.
    vim_list = nfviVim.nfvi_vim_get()

    if vim_list:
        for index, vimInfo in enumerate(vim_list.json()):
            if vimInfo.get('vimId') == vim_id:
                
                context.update(vimInfo=vimInfo)
                
                auth_url = vimInfo['interfaceInfo']['endpoint']
                auth_url = auth_url[:-2]
                username = vimInfo['accessInfo']['username']
                password = vimInfo['accessInfo']['password']
                project_id = vimInfo['accessInfo']['projectId']
                user_domain_id = vimInfo['accessInfo']['userDomain']
                
                context.update(auth_url=auth_url)
                context.update(password=password)
                context.update(project_id=project_id)
                context.update(user_domain_id=user_domain_id)
                
                #Get Openstack connection
                auth = dict(auth_url=auth_url, username=username, password=password, project_id=project_id, user_domain_id=user_domain_id)
                conn = openstack.connection.Connection(region_name='RegionOne', auth=auth, compute_api_version='2',identity_interface ='public')
    return conn
'''

dev_var = Variables()
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']
vnf_service_instance_ref = context.get('SERVICEINSTANCEREFERENCE')

if __name__ == "__main__":
    
    ## Get list of VNFC vdu.
    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    r = vnfLcm.vnf_lcm_get_vnf_instance_details(context["vnf_instance_id"])
    
    # MSA_API.task_error('DEBUG = ' + json.dumps(r.json()), context)

    MSA_API.task_success('The VNF managed entities are created.', context)