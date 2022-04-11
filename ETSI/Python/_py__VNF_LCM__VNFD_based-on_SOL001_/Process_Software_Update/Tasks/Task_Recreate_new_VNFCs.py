'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
import json
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants
import openstack
from msa_sdk import util


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



'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()
dev_var.add('vim_device', var_type='Device')
dev_var.add('vnfc_flavor.0.image', var_type='OBMFRef')
dev_var.add('vnfc_flavor.0.vnfc_name', var_type='String')
context = Variables.task_call(dev_var)

if 'vnf_me_list' in context:
    vnf_me_list = context.get('vnf_me_list')
if 'vnfc_flavor' in context:
    vnfc_flavor = context.get('vnfc_flavor')
#Get VIM connection ID.
vim_connection_id = context.get('vim_connection_id')
#Get VIM connexion.
conn = _get_vim_connection_auth(vim_connection_id, False)
i=0
'''for each ME, boot a new VM with the corresponding port list'''
for index, vnfc_dict in enumerate(vnf_me_list):
    #openstack server instance ID.
    vnf_resource_id = vnfc_dict.get('vnf_resource_id')
    flavor_name=vnfc_flavor[i]['flavor_name']
    server_name=vnfc_flavor[i]['vnfc_name']
    image=vnfc_flavor[i]['image']
    ports=vnfc_dict.get('ports') # ports[]
    networks=[]
    for j, port in enumerate(ports):
        port_dict = {"port":port}
        networks.append(port_dict.copy())
    flavor = conn.compute.find_flavor(flavor_name)
    #MSA_API.task_error('showing networks.'+json.dumps(flavor), context, True) 
    flavor_id=flavor.get('id')
    server=conn.compute.create_server(name=server_name, imageRef=image, flavorRef=flavor_id,networks=networks)
    server = conn.compute.wait_for_server(server, status='ACTIVE', failures=None, interval=2, wait=120)
    vnfc_dict.update(vnf_resource_id=server.id)
    vnfc_flavor[i]['vnf_resource_id']=server.id
    i=i+1
        
time.sleep(60)
'''Update vnf_me_list with new server ids, new root volume ids and also retain old server list'''


ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

