import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants
import openstack

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003

# Get VIM connection.

def _get_vim_connection_auth(nfvo_device, vim_id, is_user_domain=False):
    #Openstack Authentification Connection.
    conn = ''
    
    auth_url = context.get('auth_url')
    username = context.get('username')
    password = context.get('password')
    project_id = context.get('project_id')
    user_domain_id = context.get('user_domain_id')
    #
    project_domain_id = context.get('project_domain_id')
    #
    region_name = context.get('region_name')
    compute_api_version = context.get('compute_api_version')
    identity_interface = context.get('identity_interface')
    
    domain_id = user_domain_id
    if is_user_domain == False:
        domain_id = project_domain_id
                    
    #Get Openstack connection
    auth = dict(auth_url=auth_url, username=username, password=password, project_id=project_id, user_domain_id=domain_id)
    conn = openstack.connection.Connection(region_name=region_name, auth=auth, compute_api_version=compute_api_version, identity_interface=identity_interface, verify=False)
                
    return conn

'''
Wait for the server status to become active.
'''
def _wait_for_server_to_be_active(nfvo_device, vim_id, server):
    conn = _get_vim_connection_auth(nfvo_device, vim_id, False)
    server_obj = ''
    try:
        server_obj = conn.compute.get_server(server)
        return conn.compute.wait_for_server(server_obj, status='ACTIVE', failures=None, interval=2, wait=120)
    except Exception as e:
        conn = _get_vim_connection_auth(nfvo_device, vim_id, True)
        server_obj = conn.compute.get_server(server)
        return conn.compute.wait_for_server(server_obj, status='ACTIVE', failures=None, interval=2, wait=120)
    return ''

dev_var = Variables()
context = Variables.task_call(dev_var)

if __name__ == "__main__":
	
	nfvo_device_ref = context.get('nfvo_device')
	
	## Get list of VNFC vdu.
	vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
	vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
	
	r = vnfLcm.vnf_lcm_get_vnf_instance_details(context["vnf_instance_id"])
	
	vnfResourcesList = r.json()["instantiatedVnfInfo"]["vnfcResourceInfo"]
	
	vnfServerStatus = ""
	
	for index, vnfR in enumerate(vnfResourcesList):
		#openstack server instance ID.
		vnfResourceId = vnfR["computeResource"]["resourceId"]
		vim_connection_id = vnfR["computeResource"]['vimConnectionId']
		response = _wait_for_server_to_be_active(nfvo_device_ref, vim_connection_id, vnfResourceId)
		vnfServerStatus = response.get("status")

	MSA_API.task_success('The VNF instance is now ' + vnfServerStatus, context)