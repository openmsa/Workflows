import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import fireflyvmordercmdws


device_id = 'dev001'
host_name = 'host001'
interface_name = 'if001'
opp_host_name = 'opp_host001'
vrrp_interface_name = 'vrrp_if001'
vrrp_tracking_name = 'vrrp_tr001'
static_route_dst_name = 'st_rt_dst_nm'
firefly_vm_system_common_timezone = 'Asia/Tokyo'
firefly_vm_wan_interface_ip_address = 'wan_if_ip'
firefly_vm_wan_interface_netmask = 'wan_if_mask'
firefly_vm_wan_interface_mtu = 'wan_if_mtu'
firefly_vm_bgp_interface_ip_address = 'bgp_if_ip'
firefly_vm_bgp_local_preference = 'bgp_lc_pref'
firefly_vm_bgp_authkey = 'bgp_auth'
firefly_vm_loopback_interface_ip_address = 'lpb_if_ip'
firefly_vm_loopback_interface_netmask = 'lpb_if_mask'
firefly_vm_loopback_interface_segment = 'lpb_if_seg'
firefly_vm_lan_interface_ip_address = 'lan_if_ip'
firefly_vm_lan_interface_netmask = 'lan_if_mask'
firefly_vm_lan_interface_vrrp_ip_address = 'lan_if_vrrp_ip'
firefly_vm_lan_interface_segment = 'lan_if_seg'
firefly_vm_vrrp_vip = 'vrrp_vip'
firefly_vm_vrrp_priority = 'vrrp_pr'
firefly_vm_vrrp_group_id = 'vrrp_g001'
firefly_vm_vrrp_authkey = 'vrrp_auth'
firefly_vm_bgp_peer_ip_address = 'bgp_p_ip'
firefly_vm_interface_name = 'if_nm'
firefly_vm_vrrp_track_segment = 'vrrp_tr_seg'
firefly_vm_vrrp_track_netmask = 'vrrp_tr_mask'
firefly_vm_vrrp_track_prioritycost = 'vrrp_tr_pr_cost'
firefly_vm_static_destination_ip_address = 'st_dst_ip'
firefly_vm_static_destination_netmask = 'st_dst_mask'
firefly_vm_static_nexthop_address = 'st_dst_nxhp'

try:
    client = fireflyvmordercmdws.FireflyVmOrderCommandWs(
                                            config.JobConfig())

    # create_firefly_vm_system_common
    print('create_firefly_vm_system_common')
    output = client.create_firefly_vm_system_common(
                    device_id,
                    host_name,
                    firefly_vm_system_common_timezone
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_system_common
    print('delete_firefly_vm_system_common')
    output = client.delete_firefly_vm_system_common(
                    device_id,
                    host_name,
                    firefly_vm_system_common_timezone
    )
    print(type(output))
    print(output)
    print()

    # create_firefly_vm_wan_interface
    print('create_firefly_vm_wan_interface')
    output = client.create_firefly_vm_wan_interface(
                    device_id,
                    interface_name,
                    firefly_vm_wan_interface_ip_address,
                    firefly_vm_wan_interface_netmask,
                    firefly_vm_wan_interface_mtu
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_wan_interface
    print('delete_firefly_vm_wan_interface')
    output = client.delete_firefly_vm_wan_interface(
                    device_id,
                    interface_name
    )
    print(type(output))
    print(output)
    print()

    # create_firefly_vm_bgp_basic
    print('create_firefly_vm_bgp_basic')
    output = client.create_firefly_vm_bgp_basic(
                    device_id,
                    host_name,
                    firefly_vm_bgp_interface_ip_address,
                    firefly_vm_bgp_local_preference,
                    firefly_vm_bgp_authkey
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_bgp_basic
    print('delete_firefly_vm_bgp_basic')
    output = client.delete_firefly_vm_bgp_basic(
                    device_id,
                    host_name,
                    firefly_vm_bgp_interface_ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_firefly_vm_loopback_interface
    print('create_firefly_vm_loopback_interface')
    output = client.create_firefly_vm_loopback_interface(
                    device_id,
                    interface_name,
                    firefly_vm_loopback_interface_ip_address,
                    firefly_vm_loopback_interface_netmask,
                    firefly_vm_loopback_interface_segment
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_loopback_interface
    print('delete_firefly_vm_loopback_interface')
    output = client.delete_firefly_vm_loopback_interface(
                    device_id,
                    interface_name,
                    firefly_vm_loopback_interface_netmask,
                    firefly_vm_loopback_interface_segment
    )
    print(type(output))
    print(output)
    print()

    # create_firefly_vm_lan_interface
    print('create_firefly_vm_lan_interface')
    output = client.create_firefly_vm_lan_interface(
                    device_id,
                    interface_name,
                    firefly_vm_lan_interface_ip_address,
                    firefly_vm_lan_interface_netmask,
                    firefly_vm_lan_interface_vrrp_ip_address,
                    firefly_vm_lan_interface_segment
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_lan_interface
    print('delete_firefly_vm_lan_interface')
    output = client.delete_firefly_vm_lan_interface(
                    device_id,
                    interface_name,
                    firefly_vm_lan_interface_netmask,
                    firefly_vm_lan_interface_segment
    )
    print(type(output))
    print(output)
    print()

    # create_firefly_vm_vrrp
    print('create_firefly_vm_vrrp')
    output = client.create_firefly_vm_vrrp(
                    device_id,
                    vrrp_interface_name,
                    firefly_vm_vrrp_vip,
                    firefly_vm_lan_interface_ip_address,
                    firefly_vm_lan_interface_netmask,
                    firefly_vm_vrrp_priority,
                    firefly_vm_vrrp_group_id,
                    firefly_vm_vrrp_authkey
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_vrrp
    print('delete_firefly_vm_vrrp')
    output = client.delete_firefly_vm_vrrp(
                    device_id,
                    vrrp_interface_name,
                    firefly_vm_vrrp_vip,
                    firefly_vm_lan_interface_ip_address,
                    firefly_vm_lan_interface_netmask,
                    firefly_vm_vrrp_priority,
                    firefly_vm_vrrp_group_id
    )
    print(type(output))
    print(output)
    print()

    # create_firefly_vm_bgp_peer
    print('create_firefly_vm_bgp_peer')
    output = client.create_firefly_vm_bgp_peer(
                    device_id,
                    opp_host_name,
                    firefly_vm_bgp_peer_ip_address
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_bgp_peer
    print('delete_firefly_vm_bgp_peer')
    output = client.delete_firefly_vm_bgp_peer(
                    device_id,
                    opp_host_name,
                    firefly_vm_bgp_peer_ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_firefly_vm_vrrp_tracking
    print('create_firefly_vm_vrrp_tracking')
    output = client.create_firefly_vm_vrrp_tracking(
                    device_id,
                    vrrp_tracking_name,
                    firefly_vm_interface_name,
                    firefly_vm_lan_interface_ip_address,
                    firefly_vm_lan_interface_netmask,
                    firefly_vm_vrrp_group_id,
                    firefly_vm_vrrp_track_segment,
                    firefly_vm_vrrp_track_netmask,
                    firefly_vm_vrrp_track_prioritycost
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_vrrp_tracking
    print('delete_firefly_vm_vrrp_tracking')
    output = client.delete_firefly_vm_vrrp_tracking(
                    device_id,
                    vrrp_tracking_name,
                    firefly_vm_interface_name,
                    firefly_vm_lan_interface_ip_address,
                    firefly_vm_lan_interface_netmask,
                    firefly_vm_vrrp_group_id,
                    firefly_vm_vrrp_track_segment,
                    firefly_vm_vrrp_track_netmask
    )
    print(type(output))
    print(output)
    print()

    # create_firefly_vm_static_route
    print('create_firefly_vm_static_route')
    output = client.create_firefly_vm_static_route(
                    device_id,
                    static_route_dst_name,
                    firefly_vm_static_destination_ip_address,
                    firefly_vm_static_destination_netmask,
                    firefly_vm_static_nexthop_address
    )
    print(type(output))
    print(output)
    print()

    # delete_firefly_vm_static_route
    print('delete_firefly_vm_static_route')
    output = client.delete_firefly_vm_static_route(
                    device_id,
                    static_route_dst_name,
                    firefly_vm_static_destination_ip_address,
                    firefly_vm_static_destination_netmask,
                    firefly_vm_static_nexthop_address
    )
    print(type(output))
    print(output)
    print()

except:
    print('NG')
    print(traceback.format_exc())
