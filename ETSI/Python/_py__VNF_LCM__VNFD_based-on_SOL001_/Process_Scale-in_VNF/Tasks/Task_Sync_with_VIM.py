import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants
import openstack
from msa_sdk import util

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
Update the VNF totale of CPUs, RAM, DISK.
'''
def _update_vnf_resources_totale_allocated_size(vnfc_flavor,is_addition=True):
    
    cpu_cxt = context.get('vnf_totale_cpu')
    ram_cxt = context.get('vnf_totale_memory')
    disk_cxt = context.get('vnf_totale_disk')
    process_id = context['SERVICEINSTANCEID']
    
    if is_addition == True:
        
        #Loop in the vnfc_flavor list to sum() the VNFC Flavor (cpu, ram, disk)
        cpus = 0
        rams = 0
        disks = 0
        for index, flavor in enumerate(vnfc_flavor):
            cpu_cxt = flavor.get('cpu')
            ram_cxt = flavor.get('memory') 
            disk_cxt = flavor.get('disk')
            
            cpus = cpus + int(cpu_cxt)
            rams = rams + int(ram_cxt)
            disks = disks + int(disk_cxt)
            util.log_to_process_file(process_id, "adding-"+cpu_cxt+"with item"+ram_cxt)
        
        context.update(vnf_totale_cpu=str(cpus))
        context.update(vnf_totale_memory=str(rams))
        context.update(vnf_totale_disk=str(disks))

dev_var = Variables()
'''dev_var.add('vnf_totale_cpu', var_type='String')
dev_var.add('vnf_totale_memory', var_type='String')
dev_var.add('vnf_totale_disk', var_type='String')
dev_var.add('vnfc_flavor.0.vnfc_name', var_type='String')
dev_var.add('vnfc_flavor.0.cpu', var_type='String')
dev_var.add('vnfc_flavor.0.memory', var_type='String')
dev_var.add('vnfc_flavor.0.disk', var_type='String')'''
context = Variables.task_call(dev_var)




if __name__ == "__main__":

    if "is_third_party_vnfm" in context:
        is_third_party_vnfm = context.get('is_third_party_vnfm')
        if is_third_party_vnfm == 'true':
            MSA_API.task_success('Skip for 3rd party VNFM.', context)
    
    #Get NFVO ME Ref.
    nfvo_device = context.get('nfvo_device')
    process_id = context['SERVICEINSTANCEID']
    #Get VNFC list.
    vnf_me_list = context.get('vnf_me_list')
    #util.log_to_process_file(process_id,"vnfmelist::"+vnf_me_list)
    #Get vim_connection_id.
#--------------------------------
    vnfResourcesList = context.get('vnfResourcesList')
    #For each VNFC-VDU create corresponding ME's.
    for index, vnfR in enumerate(vnfResourcesList):
        #openstack server instance ID.
        vnfResourceId = vnfR["computeResource"]["resourceId"]
        vim_connection_id = vnfR["computeResource"]['vimConnectionId']
#--------------------------------
#    vim_connection_id = context.get('vim_connection_id')
    util.log_to_process_file(process_id,"vimconid::"+vim_connection_id)
    vnfc_flavor = list()
    #For each VNFC-VDU create corresponding ME's.
    for index, vnfc_dict in enumerate(vnf_me_list):
        #openstack server instance ID.
        vnf_resource_id = vnfc_dict.get('vnf_resource_id')
        #Get VIM keystone connextion.
        conn = _get_vim_connection_auth(nfvo_device, vim_connection_id, False)
        try:
            util.log_to_process_file(process_id,"going through vnf_list")
            server_obj = conn.compute.get_server(vnf_resource_id)
            context.update(server_obj = str(server_obj))
            util.log_to_process_file(process_id,"got server_obj")
            flavor_dict = server_obj.get('flavor')
            s=json.dumps(flavor_dict)
            util.log_to_process_file(process_id,"got flavour"+s)
            vnfc_name = server_obj.get('name')
            util.log_to_process_file(process_id,"got servername "+vnfc_name)
            vnfc_cpu = flavor_dict['vcpus']
            flavor_name=flavor_dict['original_name']
            util.log_to_process_file(process_id,"got cpu "+str(vnfc_cpu))
            vnfc_ram = flavor_dict['ram']
            vnfc_disk = flavor_dict['disk']
            
            hypervisor_hostname = server_obj.get('OS-EXT-SRV-ATTR:hypervisor_hostname')
            image = server_obj.get('image').get('id')
            #util.log_to_process_file(process_id,"extracted flavour details "+vnfc_name+" - "+vnfc_cpu)
            #Add cpu, ram, disk in the tab and then in the context.
            flavor = dict(vnfc_name=vnfc_name, cpu=str(vnfc_cpu), memory=str(vnfc_ram), disk=str(vnfc_disk), image=image, host=hypervisor_hostname, vnf_resource_id=vnf_resource_id,flavor_name=flavor_name)
            #util.log_to_process_file(process_id, "vnfc_name-"+vnfc_name+"with cpu"+vnfc_cpu)
            vnfc_flavor.append(flavor.copy())      
        except Exception as e:
            util.log_to_process_file(process_id, "Exception occurred")
            continue
    context.update(vnfc_flavor=vnfc_flavor)
    #Calculate the VNF allocated VIM resources.
    _update_vnf_resources_totale_allocated_size(vnfc_flavor,True)
    MSA_API.task_success('The VNF allocated resources are synchronized', context)