import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import bigipveordercmdws


device_id = 'dev001'
host_name = 'host001'
bigip_ve_system_common_domain = 'common_domain'
bigip_ve_network_interface_name = 'nw_if001'
vlan_name = 'vlan001'
bigip_ve_network_self_ip_name = 'nw_self_ip_name'
bigip_ve_network_self_ip_address = 'nw_self_ip_addr'
bigip_ve_network_self_ip_netmask = 'nw_self_ip_mask'
bigip_ve_network_vlan_name = 'nw_vlan001'
ip_address1 = '10.0.0.1'
ip_address2 = '10.0.0.2'
server_name = 'sv001'
bigip_ve_system_snmp_trap_community = 'snmp_trap'
bigip_ve_system_snmp_trap_server_address = 'snmp_trap_sv_addr'
community_name = 'comu001'
ip_address = '192.168.0.1'
bigip_ve_snmp_server_end_number = 'snmp_sv_end'
bigip_ve_system_ntp_timezone = 'Asia/Tokyo'
route_name = 'rt001'
bigip_ve_network_routes_default_gateway_action = 'rt_df_gw_act'
bigip_ve_network_routes_gateway_address = 'rt_gw_addr'
bigip_ve_network_routes_network_address = 'rt_nw_addr'
bigip_ve_network_routes_netmask = 'rt_df_nw_mask'
route_no = 'rtnmm001'
user_name = 'usr001'
bigip_ve_system_user_password = 'sys_pass'

try:
    client = bigipveordercmdws.BigIpVeOrderCommandWs(config.JobConfig())

    # create_big_ip_ve_system_common
    print('create_big_ip_ve_system_common')
    output = client.create_big_ip_ve_system_common(
                            device_id,
                            host_name,
                            bigip_ve_system_common_domain
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_ve_system_common
    print('delete_big_ip_ve_system_common')
    output = client.delete_big_ip_ve_system_common(
                            device_id,
                            host_name
    )
    print(type(output))
    print(output)
    print()

    # create_big_ip_ve_network_vlan
    print('create_big_ip_ve_network_vlan')
    output = client.create_big_ip_ve_network_vlan(
                            device_id,
                            host_name,
                            bigip_ve_network_interface_name
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_ve_network_vlan
    print('delete_big_ip_ve_network_vlan')
    output = client.delete_big_ip_ve_network_vlan(
                            device_id,
                            host_name)
    print(type(output))
    print(output)
    print()

    # create_big_ip_network_self_ip
    print('create_big_ip_network_self_ip')
    output = client.create_big_ip_network_self_ip(
                            device_id,
                            bigip_ve_network_self_ip_name,
                            bigip_ve_network_self_ip_address,
                            bigip_ve_network_self_ip_netmask,
                            bigip_ve_network_vlan_name
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_network_self_ip
    print('delete_big_ip_network_self_ip')
    output = client.delete_big_ip_network_self_ip(
                            device_id,
                            bigip_ve_network_self_ip_name
    )
    print(type(output))
    print(output)
    print()

    # create_big_ip_system_dns
    print('create_big_ip_system_dns')
    output = client.create_big_ip_system_dns(
                            device_id,
                            host_name,
                            ip_address1,
                            ip_address2
    )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_system_dns
    print('delete_big_ip_system_dns')
    output = client.delete_big_ip_system_dns(
                            device_id,
                            host_name)
    print(type(output))
    print(output)
    print()

    # create_big_ip_system_snmp_trap
    print('create_big_ip_system_snmp_trap')
    output = client.create_big_ip_system_snmp_trap(
                            device_id,
                            server_name,
                            bigip_ve_system_snmp_trap_community,
                            bigip_ve_system_snmp_trap_server_address
                            )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_system_snmp_trap
    print('delete_big_ip_system_snmp_trap')
    output = client.delete_big_ip_system_snmp_trap(
                            device_id,
                            server_name
                            )
    print(type(output))
    print(output)
    print()

    # create_big_ip_system_snmp
    print('create_big_ip_system_snmp')
    output = client.create_big_ip_system_snmp(
                            device_id,
                            community_name,
                            ip_address
                            )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_system_snmp
    print('delete_big_ip_system_snmp')
    output = client.delete_big_ip_system_snmp(
                            device_id,
                            community_name,
                            bigip_ve_snmp_server_end_number
                            )
    print(type(output))
    print(output)
    print()

    # create_big_ip_system_ntp
    print('create_big_ip_system_ntp')
    output = client.create_big_ip_system_ntp(
                            device_id,
                            host_name,
                            ip_address1,
                            ip_address2,
                            bigip_ve_system_ntp_timezone
                            )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_system_ntp
    print('delete_big_ip_system_ntp')
    output = client.delete_big_ip_system_ntp(
                            device_id,
                            host_name
                            )
    print(type(output))
    print(output)
    print()

    # create_big_ip_network_routes
    print('create_big_ip_network_routes')
    output = client.create_big_ip_network_routes(
                            device_id,
                            route_name,
                            bigip_ve_network_routes_default_gateway_action,
                            bigip_ve_network_routes_gateway_address,
                            bigip_ve_network_routes_network_address,
                            bigip_ve_network_routes_netmask
                            )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_network_routes
    print('delete_big_ip_network_routes')
    output = client.delete_big_ip_network_routes(
                            device_id,
                            route_no
                            )
    print(type(output))
    print(output)
    print()

    # create_big_ip_system_admin_account
    print('create_big_ip_system_admin_account')
    output = client.create_big_ip_system_admin_account(
                            device_id,
                            user_name,
                            bigip_ve_system_user_password
                            )
    print(type(output))
    print(output)
    print()

    # delete_big_ip_system_admin_account
    print('delete_big_ip_system_admin_account')
    output = client.delete_big_ip_system_admin_account(
                            device_id,
                            user_name
                            )
    print(type(output))
    print(output)
    print()
    print()

except:
    print('NG')
    print(traceback.format_exc())
