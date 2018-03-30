import datetime
import json
import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib import logger
from lib.openstack.keystone import tokens
from lib.openstack.quantum import networks, ports, subnets


# endpoint = 'http://localhost:8080/api_nal/Stubs/OpenStackClient/index.php?/v2.0'
endpoint = 'http://10.58.70.69:5000/v2.0'
admin_user_name = 'admin'
admin_password = 'i-portal'
tenant_id = '9ba7d56906cc4d0cbe055e06971b12a7'
nw_name = 'nw_ksp'
subnet_name = 'subnet_ksp'
port_name = 'port_ksp'
cidr = '0.0.0.0/29'

config = config.JobConfig()
log = logger.LibLogger(config)

try:
    OscTokens = tokens.OscTokens(config)
    Networks = networks.OscQuantumNetworks(config)
    Ports = ports.OscQuantumPorts(config)
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

#     print('list_networks')
#     result = Networks.list_networks(endpoint_array)
#     print(type(result))
#     print(result)
#     print()
#
#     print('create_network')
#     nw_name_new = nw_name + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
#     result = Networks.create_network(endpoint_array, nw_name_new)
#     nw_id_new = result['network']['id']
#     print(type(result))
#     print(result)
#     print(type(nw_id_new))
#     print(nw_id_new)
#     print()
#
#     print('get_network')
#     result = Networks.get_network(endpoint_array, nw_id_new)
#     print(type(result))
#     print(result)
#     print()
#
    print('list_subnets')
    result = json.dumps(Subnets.list_subnets(endpoint_array))
    print(type(result))
    print(result)
    print()
#
#     print('create_subnet')
#     subnet_name_new = subnet_name + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
#     result = Subnets.create_subnet(endpoint_array, nw_id_new, cidr, subnet_name_new)
#     print(type(result))
#     print(result)
#     subnet_id_new = result['subnet']['id']
#     print(type(nw_id_new))
#     print(subnet_id_new)
#     print()

    print('get_subnet')
    result = Subnets.get_subnet(endpoint_array, 'ef2c37fb-015b-4a7a-a7dc-e3a86d1e3e3f')
    print(type(result))
    print(result)
    print()

#     print('list_ports')
#     result = Ports.list_ports(endpoint_array)
#     print(type(result))
#     print(result)
#     print()
#
#     print('create_port')
#     port_name_new = port_name + datetime.datetime.today().strftime('%Y%m%d%H%M%S')
#     result = Ports.create_port(endpoint_array, nw_id_new, port_name_new)
#     print(type(result))
#     print(result)
#     port_id_new = result['port']['id']
#     print(type(port_id_new))
#     print(port_id_new)
#     print()
#
#     print('get_subnet')
#     result = Ports.get_port(endpoint_array, port_id_new)
#     print(type(result))
#     print(result)
#     print()
#
#     print('update_port')
#     result = Ports.update_port(endpoint_array, port_id_new, port_name_new + 'upd')
#     print(type(result))
#     print(result)
#     print()
#
#     print('detach_port_device')
#     result = Ports.detach_port_device(endpoint_array, port_id_new)
#     print(type(result))
#     print(result)
#     print()
#
#     print('delete_port')
#     result = Ports.delete_port(endpoint_array, port_id_new)
#     print(type(result))
#     print(result)
#     print()
#
#     print('list_ports')
#     result = Ports.list_ports(endpoint_array)
#     print(type(result))
#     print(result)
#     print()
#
#     print('delete_subnet')
#     result = Subnets.delete_subnet(endpoint_array, subnet_id_new)
#     print(type(result))
#     print(result)
#     print()
#
#     print('list_subnets')
#     result = Subnets.list_subnets(endpoint_array)
#     print(type(result))
#     print(result)
#     print()
#
#     print('delete_network')
#     result = Networks.delete_network(endpoint_array, nw_id_new)
#     print(type(result))
#     print(result)
#     print()
#
#     print('list_networks')
#     result = Networks.list_networks(endpoint_array)
#     print(type(result))
#     print(result)
#     print()

except:
    print('NG')
    msg = traceback.format_exc()
    print(msg)
    log.log_error(__name__, msg)
