import datetime
import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib import logger
from lib.openstack.keystone import tokens
from lib.openstack.nova import servers
from lib.openstack.quantum import networks, ports, subnets


endpoint = 'http://localhost:8080/api_nal/Stubs/OpenStackClient/index.php?/v2.0'
# endpoint = 'http://10.58.70.69:5000/v2.0'
admin_user_name = 'admin'
admin_password = 'i-portal'
tenant_id = '9ba7d56906cc4d0cbe055e06971b12a7'
sv_name = 'sv_ksp'
nw_name = 'nw_ksp'
subnet_name = 'subnet_ksp'
port_name = 'port_ksp'
cidr = '0.0.0.0/27'

imageRef = '55f7012b-4c5b-4fb8-90c7-2e1e1205e128'
flavorRef = '2'

network_list = [
    {
        'uuid': '6141844163e191152455519bc83d2bda',
        'port': 'b411cd48241a5d2bc11b02cac16e2f91',
    }
]

config = config.JobConfig()
log = logger.LibLogger(config)

try:
    OscTokens = tokens.OscTokens(config)
    Networks = networks.OscQuantumNetworks(config)
    Ports = ports.OscQuantumPorts(config)
    Servers = servers.OscServers(config)
    Subnets = subnets.OscQuantumSubnets(config)

    # create_token
    print('create_token')
    token = OscTokens.create_token(admin_user_name, admin_password, endpoint)
    print(type(token))
    print(token)
    print()

    print('get_endpoints(tenant_id)')
    endpoint_array = OscTokens.get_endpoints(
        endpoint, token, admin_user_name, admin_password, '', tenant_id)
    print(type(endpoint_array))
    print(endpoint_array)
    print()

    print('create_network')
    nw_name_new = nw_name + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    result = Networks.create_network(endpoint_array, nw_name_new)
    nw_id_new = result['network']['id']
    print(type(result))
    print(result)
    print(type(nw_id_new))
    print(nw_id_new)
    print()

    print('create_subnet')
    subnet_name_new = subnet_name + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    result = Subnets.create_subnet(endpoint_array, nw_id_new, cidr, subnet_name_new)
    print(type(result))
    print(result)
    subnet_id_new = result['subnet']['id']
    print(type(nw_id_new))
    print(subnet_id_new)
    print()

    print('create_port')
    port_name_new = port_name + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    result = Ports.create_port(endpoint_array, nw_id_new, port_name_new)
    print(type(result))
    print(result)
    port_id_new = result['port']['id']
    print(type(port_id_new))
    print(port_id_new)
    print()

    print('list_servers')
    result = Servers.list_servers(endpoint_array)
    print(type(result))
    print(result)
    print()

    print('create_server')
    sv_name_new = sv_name + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    network_list[0]['uuid'] = nw_id_new
    network_list[0]['port'] = port_id_new
    result = Servers.create_server(
            endpoint_array, sv_name_new, imageRef, flavorRef, network_list)
    server_id_new = result['server']['id']
    print(type(result))
    print(result)
    print(type(server_id_new))
    print(server_id_new)
    print()

    print('get_server')
    result = Servers.get_server(endpoint_array, server_id_new)
    print(type(result))
    print(result)
    print()

#     server_id_new = 'a7eb9e1b-10c3-4655-a717-d8b6743978a7'

    print('action_server')
    actionkey = Servers.SERVER_ACTION_RESUME
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey)
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_ACTION_RESETNETWORK
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey)
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_ACTION_SUSPEND
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey)
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_ACTION_REBOOT
    boottype = Servers.SERVER_REBOOT_TYPE_SOFT
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey, boottype)
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_ACTION_RESIZE
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, None, '2')
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_ACTION_CONFIRMRESIZE
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey)
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_ACTION_OS_START
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey)
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_ACTION_OS_STOP
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey)
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_ACTION_GETCONSOLE
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey, None, None, 'xvpvnc')
    print(type(result))
    print(result)
    print()

    print('action_server')
    actionkey = Servers.SERVER_STATUS_PAUSE
    print(actionkey)
    result = Servers.action_server(endpoint_array, server_id_new, actionkey)
    print(type(result))
    print(result)
    print()

#     port_id_new = '98377b7e-78b2-434d-9b97-5c5701ac5bd1'

    print('attach_interface')
    result = Servers.attach_interface(endpoint_array, server_id_new, port_id_new)
    print(type(result))
    print(result)
    print()

    print('list_interfaces')
    result = Servers.list_interfaces(endpoint_array, server_id_new)
    print(type(result))
    print(result)
    print()

    print('detach_interface')
    result = Servers.detach_interface(endpoint_array, server_id_new, port_id_new)
    print(type(result))
    print(result)
    print()

    print('delete_port')
    result = Ports.delete_port(endpoint_array, port_id_new)
    print(type(result))
    print(result)
    print()

    print('delete_subnet')
    result = Subnets.delete_subnet(endpoint_array, subnet_id_new)
    print(type(result))
    print(result)
    print()

    print('delete_network')
    result = Networks.delete_network(endpoint_array, nw_id_new)
    print(type(result))
    print(result)
    print()

    print('delete_server')
    result = Servers.delete_server(endpoint_array, server_id_new)
    print(type(result))
    print(result)
    print()

except:
    print('NG')
    msg = traceback.format_exc()
    print(msg)
    log.log_error(__name__, msg)
