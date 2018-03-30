import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import thunderordercmdws


device_id = 'dev001'
object_id = 'obj001'
partition_id = 'part001'
partition_name = 'part_nm'
vlan_id = 'vlan001'
ip_address = '192.168.0.1'
netmask = '255.255.255.0'
port_no = '100'
vrid = 'vr001'
vrrp_preempt = 'vr_pre'
vrrp_priority = 'vr_pri'
floating_ip = '10.0.0.1'
dst_ip = '10.0.0.2'
dst_mask = '255.255.255.1'
gateway_ip = '10.1.0.1'

try:
    client = thunderordercmdws.ThunderOrderCommandWs(
                                            config.JobConfig())

    # create_thunder_partition
    print('create_thunder_partition')
    output = client.create_thunder_partition(
                            device_id, object_id,
                            partition_id
    )
    print(type(output))
    print(output)
    print()

    # delete_thunder_partition
    print('delete_thunder_partition')
    output = client.delete_thunder_partition(
                            device_id, object_id,
                            partition_id
    )
    print(type(output))
    print(output)
    print()

    # create_thunder_vlan
    print('create_thunder_vlan')
    output = client.create_thunder_vlan(
                            device_id, object_id,
                             partition_name,
                             vlan_id,
                             ip_address,
                             netmask,
                             port_no
    )
    print(type(output))
    print(output)
    print()

    # delete_thunder_vlan
    print('delete_thunder_vlan')
    output = client.delete_thunder_vlan(
                            device_id, object_id,
                             partition_name,
                             vlan_id
    )
    print(type(output))
    print(output)
    print()

    # create_thunder_vrrp
    print('create_thunder_vrrp')
    output = client.create_thunder_vrrp(
                            device_id, object_id,
                             partition_name,
                             vrid,
                             vrrp_preempt,
                             vrrp_priority,
                             floating_ip
    )
    print(type(output))
    print(output)
    print()

    # delete_thunder_vrrp
    print('delete_thunder_vrrp')
    output = client.delete_thunder_vrrp(
                            device_id, object_id,
                             partition_name,
                             vrid
    )
    print(type(output))
    print(output)
    print()

    # create_thunder_static_route
    print('create_thunder_static_route')
    output = client.create_thunder_static_route(
                            device_id, object_id,
                             partition_name,
                             dst_ip,
                             dst_mask,
                             gateway_ip
    )
    print(type(output))
    print(output)
    print()

    # delete_thunder_static_route
    print('delete_thunder_static_route')
    output = client.delete_thunder_static_route(
                            device_id, object_id,
                             partition_name,
                             dst_ip,
                             dst_mask,
                             gateway_ip
    )
    print(type(output))
    print(output)
    print()

except:
    print('NG')
    print(traceback.format_exc())
