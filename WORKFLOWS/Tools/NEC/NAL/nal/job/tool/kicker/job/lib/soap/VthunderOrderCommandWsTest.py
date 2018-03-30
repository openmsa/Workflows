import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import vthunderordercmdws


device_id = 'dev001'
object_id = 'obj001'
address = '192.168.0.1'
netmask = '255.255.255.0'
version = '1'
community_name = 'commu_nm'
address_delete = '192.168.0.0'
version_delete = '0'
community_name_delete = 'commu_nm_del'
action = 'action'
member = 'member'
member_delete = 'member_del'
vthunder_system_common_timezone = 'Asia/Tokyo'
vthunder_network_vlan_untagged_interface_number = 'nw_vlan_untag_if_num'
vthunder_network_virtual_interface_ip_address = 'nw_vr_if_ip'
vthunder_network_virtual_interface_netmask = 'nw_vr_if_mask'
vthunder_network_vlan_description = 'nw_vlan_descript'
vthunder_system_dns_primary_ip_address = 'sys_dns_pr_ip'
vthunder_system_dns_secondary_ip_address = 'sys_dns_sc_ip'
vthunder_system_syslog_ip_address = 'sys_syslog_ip'
vthunder_network_routes_network_address = 'nw_rt_nw_addr'
vthunder_network_routes_netmask = 'nw_rt_mask'
vthunder_network_routes_gateway_address = 'nw_rt_gw_addr'
vthunder_system_user_password = 'sys_usr_pass'

try:
    client = vthunderordercmdws.VthunderOrderCommandWs(
                                            config.JobConfig())

    # create_vthunder_system_common
    print('create_vthunder_system_common')
    output = client.create_vthunder_system_common(
                            device_id, object_id,
                            vthunder_system_common_timezone
    )
    print(type(output))
    print(output)
    print()

    # update_vthunder_system_common
    print('update_vthunder_system_common')
    output = client.update_vthunder_system_common(
                            device_id, object_id,
                            vthunder_system_common_timezone
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_system_common
    print('delete_vthunder_system_common')
    output = client.delete_vthunder_system_common(
                            device_id, object_id,
                            vthunder_system_common_timezone
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_network_vlan_interface
    print('create_vthunder_network_vlan_interface')
    output = client.create_vthunder_network_vlan_interface(
                            device_id, object_id,
                            vthunder_network_vlan_untagged_interface_number,
                            vthunder_network_virtual_interface_ip_address,
                            vthunder_network_virtual_interface_netmask,
                            vthunder_network_vlan_description
    )
    print(type(output))
    print(output)
    print()

    # update_vthunder_network_vlan_interface
    print('update_vthunder_network_vlan_interface')
    output = client.update_vthunder_network_vlan_interface(
                            device_id, object_id,
                            vthunder_network_vlan_untagged_interface_number,
                            vthunder_network_virtual_interface_ip_address,
                            vthunder_network_virtual_interface_netmask,
                            vthunder_network_vlan_description
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_network_vlan_interface
    print('delete_vthunder_network_vlan_interface')
    output = client.delete_vthunder_network_vlan_interface(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_system_dns
    print('create_vthunder_system_dns')
    output = client.create_vthunder_system_dns(
                            device_id, object_id,
                            vthunder_system_dns_primary_ip_address,
                            vthunder_system_dns_secondary_ip_address,
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_system_dns
    print('delete_vthunder_system_dns')
    output = client.delete_vthunder_system_dns(
                            device_id, object_id,
                            vthunder_system_dns_primary_ip_address,
                            vthunder_system_dns_secondary_ip_address,
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_system_snmp_trap
    print('create_vthunder_system_snmp_trap')
    output = client.create_vthunder_system_snmp_trap(
                            device_id, object_id,
                            address,
                            version,
                            community_name,
    )
    print(type(output))
    print(output)
    print()

    # update_vthunder_system_snmp_trap
    print('update_vthunder_system_snmp_trap')
    output = client.update_vthunder_system_snmp_trap(
                            device_id, object_id,
                            address,
                            version,
                            community_name,
                            address_delete,
                            version_delete,
                            community_name_delete,
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_system_snmp_trap
    print('delete_vthunder_system_snmp_trap')
    output = client.delete_vthunder_system_snmp_trap(
                            device_id, object_id,
                            address,
                            version,
                            community_name,
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_system_snmp_enable
    print('create_vthunder_system_snmp_enable')
    output = client.create_vthunder_system_snmp_enable(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_system_snmp_enable
    print('delete_vthunder_system_snmp_enable')
    output = client.delete_vthunder_system_snmp_enable(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_system_snmp
    print('create_vthunder_system_snmp')
    output = client.create_vthunder_system_snmp(
                            device_id, object_id,
                            address,
                            netmask
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_system_snmp
    print('delete_vthunder_system_snmp')
    output = client.delete_vthunder_system_snmp(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_system_syslog
    print('create_vthunder_system_syslog')
    output = client.create_vthunder_system_syslog(
                            device_id, object_id,
                            vthunder_system_syslog_ip_address
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_system_syslog
    print('delete_vthunder_system_syslog')
    output = client.delete_vthunder_system_syslog(
                            device_id, object_id,
                            vthunder_system_syslog_ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_system_ntp
    print('create_vthunder_system_ntp')
    output = client.create_vthunder_system_ntp(
                            device_id, object_id,
                            action, member
    )
    print(type(output))
    print(output)
    print()

    # update_vthunder_system_ntp
    print('update_vthunder_system_ntp')
    output = client.update_vthunder_system_ntp(
                            device_id, object_id,
                            action, member, member_delete
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_system_ntp
    print('delete_vthunder_system_ntp')
    output = client.delete_vthunder_system_ntp(
                            device_id, object_id,
                            member
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_network_routes
    print('create_vthunder_network_routes')
    output = client.create_vthunder_network_routes(
                            device_id, object_id,
                            vthunder_network_routes_network_address,
                            vthunder_network_routes_netmask,
                            vthunder_network_routes_gateway_address,
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_network_routes
    print('delete_vthunder_network_routes')
    output = client.delete_vthunder_network_routes(
                            device_id, object_id,
                            vthunder_network_routes_network_address,
                            vthunder_network_routes_netmask,
                            vthunder_network_routes_gateway_address,
    )
    print(type(output))
    print(output)
    print()

    # create_vthunder_system_admin_account
    print('create_vthunder_system_admin_account')
    output = client.create_vthunder_system_admin_account(
                            device_id, object_id,
                            vthunder_system_user_password
    )
    print(type(output))
    print(output)
    print()

    # update_vthunder_system_admin_account
    print('update_vthunder_system_admin_account')
    output = client.update_vthunder_system_admin_account(
                            device_id, object_id,
                            vthunder_system_user_password
    )
    print(type(output))
    print(output)
    print()

    # delete_vthunder_system_admin_account
    print('delete_vthunder_system_admin_account')
    output = client.delete_vthunder_system_admin_account(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

except:
    print('NG')
    print(traceback.format_exc())
