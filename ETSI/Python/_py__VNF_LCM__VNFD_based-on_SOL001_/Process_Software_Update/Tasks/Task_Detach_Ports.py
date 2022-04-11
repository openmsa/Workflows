import json
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants
import openstack
from msa_sdk import util

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003

# Get VIM connection.

def _get_vim_connection_auth(vim_id, is_user_domain=False):
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

def _save_server_ports(conn, vnf_resource_id):
    ports=[]
    server_interfaces = conn.compute.server_interfaces(vnf_resource_id)
    #util.log_to_process_file(process_id, "DEBUB_SLE" + str(server_interfaces))
    for port in server_interfaces:
        prt=port['port_id']
        ports.append(prt)
    return ports


dev_var = Variables()
context = Variables.task_call(dev_var)

if __name__ == "__main__":
    
    #Get VIM connection ID.
    vim_connection_id = context.get('vim_connection_id')
    #Get VIM connexion.
    conn = _get_vim_connection_auth(vim_connection_id, False)
    
    #VNF Managed Entities.
    
    vnf_me_list = context.get('vnf_me_list')
    
    vnfServerStatus = ''
    #For each VNFC-VDU create corresponding ME's.
    for index, vnfc_dict in enumerate(vnf_me_list):
        #openstack server instance ID.
        vnf_resource_id = vnfc_dict.get('vnf_resource_id')
        
        #Seve the ports:
        ports =_save_server_ports(conn, vnf_resource_id)
        vnfc_dict['ports']=ports
        #my_obj=conn.compute.find_server(vnf_resource_id)
        obj=conn.compute.delete_server(vnf_resource_id)
        time.sleep(5)
        #obj=conn.compute.wait_for_delete(my_obj)

    MSA_API.task_success('The ports are now detached and VMs removed', context)