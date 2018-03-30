import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import paloaltovmordercmdws


device_id = 'dev001'
object_id = 'obj001'
interface_name = 'if_nm'
name = 'nm'
address = 'addr'
community_name = 'cm_nm'
paloalto_vm_system_timezone = 'Asia/Tokyo'
paloalto_vm_vsys_zone_interface = 'vsys_zn_if'
paloalto_vm_vsys_zone_name = 'vsys_zn_nm'
paloalto_vm_network_interface_ip_address = 'nw_if_ip'
paloalto_vm_network_interface_netmask = 'nw_if_mask'
paloalto_vm_system_dns_primary = 'sys_dns_pr'
paloalto_vm_system_dns_secondary = 'sys_dns_sc'
paloalto_vm_logsetting_snmp_profile = 'log_snm_prof'
paloalto_vm_logsetting_syslog_profile = 'log_sys_prof'
paloalto_vm_system_primary_ntp_server = 'sys_pr_ntp_sv'
paloalto_vm_system_secondary_ntp_server = 'sys_sc_ntp_sv'
paloalto_vm_network_staticroute_destination_address = 'nw_strt_dest_addr'
paloalto_vm_network_staticroute_destination_netmask = 'nw_strt_dest_mask'
paloalto_vm_network_staticroute_nexthop_address = 'nw_strt_nx_addr'
paloalto_vm_network_staticroute_source_interface = 'nw_strt_src_if'
paloalto_vm_system_user_password = 'sys_usr_pass'

try:
    client = paloaltovmordercmdws.PaloaltoVmOrderCommandWs(
                                            config.JobConfig())

    # create_paloalto_vm_system_common
    print('create_paloalto_vm_system_common')
    output = client.create_paloalto_vm_system_common(
                            device_id, object_id,
                            paloalto_vm_system_timezone
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_system_common
    print('delete_paloalto_vm_system_common')
    output = client.delete_paloalto_vm_system_common(
                            device_id, object_id,
                            paloalto_vm_system_timezone
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_vsys_zone
    print('create_paloalto_vm_vsys_zone')
    output = client.create_paloalto_vm_vsys_zone(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_vsys_zone
    print('delete_paloalto_vm_vsys_zone')
    output = client.delete_paloalto_vm_vsys_zone(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_vsys_zone_mapping
    print('create_paloalto_vm_vsys_zone_mapping')
    output = client.create_paloalto_vm_vsys_zone_mapping(
                            device_id, object_id,
                            paloalto_vm_vsys_zone_interface,
                            paloalto_vm_vsys_zone_name
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_vsys_zone_mapping
    print('delete_paloalto_vm_vsys_zone_mapping')
    output = client.delete_paloalto_vm_vsys_zone_mapping(
                            device_id, object_id,
                            paloalto_vm_vsys_zone_name
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_network_vrouter_mapping
    print('create_paloalto_vm_network_vrouter_mapping')
    output = client.create_paloalto_vm_network_vrouter_mapping(
                            device_id, object_id,
                            interface_name
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_network_vrouter_mapping
    print('delete_paloalto_vm_network_vrouter_mapping')
    output = client.delete_paloalto_vm_network_vrouter_mapping(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_network_interface
    print('create_paloalto_vm_network_interface')
    output = client.create_paloalto_vm_network_interface(
                            device_id, object_id,
                            paloalto_vm_network_interface_ip_address,
                            paloalto_vm_network_interface_netmask
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_network_interface
    print('delete_paloalto_vm_network_interface')
    output = client.delete_paloalto_vm_network_interface(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_system_dns
    print('create_paloalto_vm_system_dns')
    output = client.create_paloalto_vm_system_dns(
                            device_id, object_id,
                            paloalto_vm_system_dns_primary,
                            paloalto_vm_system_dns_secondary,
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_system_dns
    print('delete_paloalto_vm_system_dns')
    output = client.delete_paloalto_vm_system_dns(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_logsetting_snmp
    print('create_paloalto_vm_logsetting_snmp')
    output = client.create_paloalto_vm_logsetting_snmp(
                            device_id, object_id,
                            name,
                            address,
                            community_name
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_logsetting_snmp
    print('delete_paloalto_vm_logsetting_snmp')
    output = client.delete_paloalto_vm_logsetting_snmp(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_logsetting_snmp_mapping
    print('create_paloalto_vm_logsetting_snmp_mapping')
    output = client.create_paloalto_vm_logsetting_snmp_mapping(
                            device_id, object_id,
                            paloalto_vm_logsetting_snmp_profile
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_logsetting_snmp_mapping
    print('delete_paloalto_vm_logsetting_snmp_mapping')
    output = client.delete_paloalto_vm_logsetting_snmp_mapping(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_logsetting_syslog
    print('create_paloalto_vm_logsetting_syslog')
    output = client.create_paloalto_vm_logsetting_syslog(
                            device_id, object_id,
                            name,
                            address
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_logsetting_syslog
    print('delete_paloalto_vm_logsetting_syslog')
    output = client.delete_paloalto_vm_logsetting_syslog(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_logsetting_syslog_mapping
    print('create_paloalto_vm_logsetting_syslog_mapping')
    output = client.create_paloalto_vm_logsetting_syslog_mapping(
                            device_id, object_id,
                            paloalto_vm_logsetting_syslog_profile
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_logsetting_syslog_mapping
    print('delete_paloalto_vm_logsetting_syslog_mapping')
    output = client.delete_paloalto_vm_logsetting_syslog_mapping(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_system_ntp
    print('create_paloalto_vm_system_ntp')
    output = client.create_paloalto_vm_system_ntp(
                            device_id, object_id,
                            paloalto_vm_system_primary_ntp_server,
                            paloalto_vm_system_secondary_ntp_server
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_system_ntp
    print('delete_paloalto_vm_system_ntp')
    output = client.delete_paloalto_vm_system_ntp(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_network_static_route
    print('create_paloalto_vm_network_static_route')
    output = client.create_paloalto_vm_network_static_route(
                            device_id, object_id,
                        paloalto_vm_network_staticroute_destination_address,
                        paloalto_vm_network_staticroute_destination_netmask,
                        paloalto_vm_network_staticroute_nexthop_address,
                        paloalto_vm_network_staticroute_source_interface
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_network_static_route
    print('delete_paloalto_vm_network_static_route')
    output = client.delete_paloalto_vm_network_static_route(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

    # create_paloalto_vm_system_users
    print('create_paloalto_vm_system_users')
    output = client.create_paloalto_vm_system_users(
                            device_id, object_id,
                            paloalto_vm_system_user_password
    )
    print(type(output))
    print(output)
    print()

    # delete_paloalto_vm_system_users
    print('delete_paloalto_vm_system_users')
    output = client.delete_paloalto_vm_system_users(
                            device_id, object_id
    )
    print(type(output))
    print(output)
    print()

except:
    print('NG')
    print(traceback.format_exc())
