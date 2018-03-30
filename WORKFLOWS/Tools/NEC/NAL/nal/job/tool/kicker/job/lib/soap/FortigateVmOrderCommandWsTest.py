import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import fortigatevmordercmdws


device_id = 'dev001'
host_name = 'host001'
port = '80'
num = '100'
dummy = 'dm'
fortigate_vm_system_common_language = 'sys_cm_lang'
fortigate_vm_system_common_timezone = 'sys_cm_tz'
fortigate_vm_interface_ip_address = '192.168.0.1'
fortigate_vm_interface_netmask = 'mask'
fortigate_vm_interface_service_ping_action = 'ping'
fortigate_vm_interface_service_https_action = 'https'
fortigate_vm_interface_service_ssh_action = 'ssh'
fortigate_vm_account_name = 'ac_nm'
fortigate_vm_account_password = 'ac_pass'
fortigate_vm_account_profile = 'ac_pf'
fortigate_vm_dns_primary = 'dns_pr'
fortigate_vm_dns_secondary = 'dns_sc'
fortigate_vm_ntp_sync_action = 'ntp_sync_act'
fortigate_vm_ntp_sync_interval = 'ntp_sync_int'
fortigate_vm_ntp_server_ip_address = 'ntp_sv_ip'
fortigate_vm_firewall_router_default_gateway_action = 'fw_rt_df_gw_act'
fortigate_vm_firewall_router_default_gateway_address = 'fw_rt_df_gw_addr'
fortigate_vm_firewall_router_static_network_address = 'fw_rt_st_nw_addr'
fortigate_vm_firewall_router_static_network_mask = 'fw_rt_st_nw_mask'
fortigate_vm_firewall_router_static_device = 'fw_rt_st_dev'

try:
    client = fortigatevmordercmdws.FortigateVmOrderCommandWs(
                                            config.JobConfig())

    # create_fortigate_vm_system_common
    print('create_fortigate_vm_system_common')
    output = client.create_fortigate_vm_system_common(
                            device_id,
                            host_name,
                            fortigate_vm_system_common_language,
                            fortigate_vm_system_common_timezone
    )
    print(type(output))
    print(output)
    print()

    # create_fortigate_vm_interface
    print('create_fortigate_vm_interface')
    output = client.create_fortigate_vm_interface(
                            device_id,
                            port,
                            fortigate_vm_interface_ip_address,
                            fortigate_vm_interface_netmask,
                            fortigate_vm_interface_service_ping_action,
                            fortigate_vm_interface_service_https_action,
                            fortigate_vm_interface_service_ssh_action
    )
    print(type(output))
    print(output)
    print()

    # delete_fortigate_vm_interface
    print('delete_fortigate_vm_interface')
    output = client.delete_fortigate_vm_interface(
                            device_id,
                            port
    )
    print(type(output))
    print(output)
    print()

    # create_fortigate_vm_admin_account
    print('create_fortigate_vm_admin_account')
    output = client.create_fortigate_vm_admin_account(
                            device_id,
                            fortigate_vm_account_name,
                            fortigate_vm_account_password,
                            fortigate_vm_account_profile
    )
    print(type(output))
    print(output)
    print()

    # create_fortigate_vm_dns
    print('create_fortigate_vm_dns')
    output = client.create_fortigate_vm_dns(
                            device_id,
                            host_name,
                            fortigate_vm_dns_primary,
                            fortigate_vm_dns_secondary
    )
    print(type(output))
    print(output)
    print()

    # create_fortigate_vm_ntp
    print('create_fortigate_vm_ntp')
    output = client.create_fortigate_vm_ntp(
                            device_id,
                            host_name,
                            fortigate_vm_ntp_sync_action,
                            fortigate_vm_ntp_sync_interval,
                            fortigate_vm_ntp_server_ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_fortigate_vm_router_static
    print('create_fortigate_vm_router_static')
    output = client.create_fortigate_vm_router_static(
                    device_id,
                    num,
                    dummy,
                    fortigate_vm_firewall_router_default_gateway_action,
                    fortigate_vm_firewall_router_default_gateway_address,
                    fortigate_vm_firewall_router_static_network_address,
                    fortigate_vm_firewall_router_static_network_mask,
                    fortigate_vm_firewall_router_static_device
    )
    print(type(output))
    print(output)
    print()

except:
    print('NG')
    print(traceback.format_exc())
