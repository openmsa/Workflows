import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import fortigateordercmdws


device_id = 'dev001'
object_id = 'obj001'
vdom_name = 'vdom_nm001'
vlan_id = 'vlan001'
ip_address = '10.0.0.1'
netmask = 'mask001'
port_no = 'port010'
management_flg = '1'

try:
    client = fortigateordercmdws.FortigateOrderCommandWs(config.JobConfig())

    # create_fortigate_vdom
    print('create_fortigate_vdom')
    output = client.create_fortigate_vdom(
                            device_id,
                            object_id
    )
    print(type(output))
    print(output)
    print()

    # delete_fortigate_vdom
    print('delete_fortigate_vdom')
    output = client.delete_fortigate_vdom(
                            device_id,
                            object_id
    )
    print(type(output))
    print(output)
    print()

    # create_fortigate_vlan_interface
    print('create_fortigate_vlan_interface')
    output = client.create_fortigate_vlan_interface(
                            device_id,
                            object_id,
                            vdom_name,
                            vlan_id,
                            ip_address,
                            netmask,
                            port_no,
                            management_flg
    )
    print(type(output))
    print(output)
    print()

    # update_fortigate_vlan_interface
    print('update_fortigate_vlan_interface')
    output = client.update_fortigate_vlan_interface(
                            device_id,
                            object_id,
                            vdom_name,
                            vlan_id,
                            ip_address,
                            netmask,
                            port_no,
                            management_flg
    )
    print(type(output))
    print(output)
    print()

    # delete_fortigate_vlan_interface
    print('delete_fortigate_vlan_interface')
    output = client.delete_fortigate_vlan_interface(
                            device_id,
                            object_id,
                            vdom_name,
                            vlan_id,
                            ip_address,
                            netmask,
                            port_no,
                            management_flg
    )
    print(type(output))
    print(output)
    print()

except:
    print('NG')
    print(traceback.format_exc())
