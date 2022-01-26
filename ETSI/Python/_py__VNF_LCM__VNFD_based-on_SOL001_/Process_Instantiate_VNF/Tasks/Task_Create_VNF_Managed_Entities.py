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
Get VIM connection.
'''
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
Get external network from VIM tenant.
'''
def _get_vim_external_network(conn):
    external_network = ''
    for network in conn.network.networks():
        if network.get('is_router_external') == True:
            external_network = network.get('name')
    return external_network

'''
Get VNFC resource (VDU) instance public IP address.
'''
def _get_vnfc_resource_public_ip_address(nfvo_device, vim_id, server_id):
    
    server_ip_addr = ''
    
    #Get openstack authenfication
    conn = _get_vim_connection_auth(nfvo_device, vim_id)
    
    #Get openstack tenant external networks.
    external_network = _get_vim_external_network(conn)
    
    #Get VDU (server instance) details.
    servers = conn.compute.servers()
    for server in servers:
        if server.id == server_id:
            addresses = server.addresses
            
            time.sleep(10)
            for index, address in enumerate(addresses.get(external_network)):
                if address.get('addr'):
                    server_ip_addr = address.get('addr')
                    break
                                        
    return server_ip_addr


dev_var = Variables()
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']
vnf_service_instance_ref = context.get('SERVICEINSTANCEREFERENCE')

if __name__ == "__main__":
    
    ## Get list of VNFC vdu.
    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    r = vnfLcm.vnf_lcm_get_vnf_instance_details(context["vnf_instance_id"])
    
    #MSA_API.task_error('DEBUG = ' + json.dumps(r.json()), context)
    
    context.update(vnf_instance_details=r.json())
        
    vnfResourcesList = r.json()["instantiatedVnfInfo"]["vnfcResourceInfo"]
    
    context.update(vnfResourcesList=vnfResourcesList)
    
    #VNF Managed Entities.
    vnf_me_list = list()
    
    #For each VNFC-VDU create corresponding ME's.
    for index, vnfR in enumerate(vnfResourcesList):
        #openstack server instance ID.
        vnfResourceId = vnfR["computeResource"]["resourceId"]
        vim_connection_id = vnfR["computeResource"]['vimConnectionId']
    
        ## get VDU details (@IP, Hostname).
        #TODO: create VIM SDK to call Openstack API servers resources.
        
        #Customer ID
        customer_id = subtenant_ext_ref[4:]
        #Kubernetes_generic manufacturer_id
        manufacturer_id='14020601'
        #Kubernetes_generic model_id
        model_id='14020601'
        #default IP address
        nfvo_device_ref = context.get('nfvo_device')
        management_address = _get_vnfc_resource_public_ip_address(nfvo_device_ref, vim_connection_id, vnfResourceId)
        if not management_address:
            management_address = '1.1.1.1'
        
        #Kubernetes adaptor does not use the password and login of ME.
        password = 'fake38passwOrd'
        management_port='22'
        name = vnf_service_instance_ref + '_VNFC_' + vnfResourceId
        #Create Device
        device = Device(customer_id=customer_id, name=name, manufacturer_id=manufacturer_id, model_id=model_id, login='admin', password=password, password_admin=password, management_address=management_address, management_port=management_port, device_external="", log_enabled=True, log_more_enabled=True, mail_alerting=False, reporting=True, snmp_community='ubiqube', device_id="")
        response = device.create()
        context.update(device=response)
        #get device external reference
        device_ext_ref = response.get('externalReference')
        
        #Add device_ext_ref to the VNF ME list.
        vnf_me_list.append(device_ext_ref)
        
        #get device external reference
        device_id = response.get('id')
        context.update(vnf_me_id=device_id)
    
        #add ns_service_instance_ref as VNF ME variable configuration.
        if 'ns_service_instance_ref' in context:
            ns_service_instance_ref = context.get('ns_service_instance_ref')
            if ns_service_instance_ref:
                device.create_configuration_variable('nslcm_wf_service_instance_ref', ns_service_instance_ref)
                
        #add VNF LCM service instance REF:
        device.create_configuration_variable('vnflcm_wf_service_instance_ref', vnf_service_instance_ref)
        
    #Store vnf_me_list in the context.
    context.update(vnf_me_list=vnf_me_list)

    MSA_API.task_success('The VNF managed entities are created.', context)

