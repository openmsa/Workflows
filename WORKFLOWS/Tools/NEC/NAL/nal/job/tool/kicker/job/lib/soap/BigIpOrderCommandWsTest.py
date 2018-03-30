import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import bigipordercmdws


device_id = 'dev001'
partition_id = 'p001'
rtdomain_id = 'rtd001'
vlan_name = 'vlan_nm001'
params_interface_name = 'pif_nm001'
vlan_id = 'vlan001'
physical_ip_name = 'pf_ip_nm'
ip_address = '192.168.0.1'
vip_name = 'vip_nm001'
netmask = 'mask001'
traffic_name = 'tf_nm001'

try:
    client = bigipordercmdws.BigIpOrderCommandWs(config.JobConfig())

    # create_big_ip_partition
    print('create_big_ip_partition')
    output = client.create_big_ip_partition(
                            device_id,
                            partition_id
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_partition
    print('delete_big_ip_partition')
    output = client.delete_big_ip_partition(
                            device_id,
                            partition_id
    )
    print(type(output))
    print(output)
    print()

    # create_big_ip_route_domain
    print('create_big_ip_route_domain')
    output = client.create_big_ip_route_domain(
                            device_id,
                            partition_id,
                            rtdomain_id
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_route_domain
    print('delete_big_ip_route_domain')
    output = client.delete_big_ip_route_domain(
                            device_id,
                            partition_id)
    print(type(output))
    print(output)
    print()

    # create_big_ip_default_route_domain
    print('create_big_ip_default_route_domain')
    output = client.create_big_ip_default_route_domain(
                            device_id,
                            partition_id,
                            rtdomain_id
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_default_route_domain
    print('delete_big_ip_default_route_domain')
    output = client.delete_big_ip_default_route_domain(
                            device_id,
                            partition_id)
    print(type(output))
    print(output)
    print()

    # create_big_ip_vlan
    print('create_big_ip_vlan')
    output = client.create_big_ip_vlan(
                            device_id,
                            partition_id,
                            vlan_name,
                            params_interface_name,
                            vlan_id
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_vlan
    print('delete_big_ip_vlan')
    output = client.delete_big_ip_vlan(
                            device_id,
                            partition_id,
                            vlan_name
    )
    print(type(output))
    print(output)
    print()

    # create_big_ip_physical_ip
    print('create_big_ip_physical_ip')
    output = client.create_big_ip_physical_ip(
                            device_id,
                            partition_id,
                            physical_ip_name,
                            ip_address,
                            netmask,
                            vlan_name
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_physical_ip
    print('delete_big_ip_physical_ip')
    output = client.delete_big_ip_physical_ip(
                            device_id,
                            partition_id,
                            physical_ip_name
    )
    print(type(output))
    print(output)
    print()

    # create_big_ip_vip
    print('create_big_ip_vip')
    output = client.create_big_ip_vip(
                            device_id,
                            partition_id,
                            vip_name,
                            ip_address,
                            netmask,
                            vlan_name,
                            traffic_name
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_vip
    print('delete_big_ip_vip')
    output = client.delete_big_ip_vip(
                            device_id,
                            partition_id,
                            vip_name
    )
    print(type(output))
    print(output)
    print()

except:
    print('NG')
    print(traceback.format_exc())
