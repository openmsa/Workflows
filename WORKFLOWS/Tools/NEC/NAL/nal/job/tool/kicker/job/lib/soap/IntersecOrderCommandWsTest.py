import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import intersecordercmdws


device_id = 'dev001'
instance_name = 'nal'
license_key = 'key001'
nic_number = '10'
ip_address = '192.168.0.1'
subnet = '255.255.255.0'
zabbix_vip_ip_address = '10.0.0.1'
zabbix01_ip_address = '10.0.0.2'
zabbix02_ip_address = '10.0.0.3'
gw_ip_address = '192.168.0.2'
dst_ip_address = '10.1.0.1'
dst_subnet = '255.255.255.1'
broadcast_address = '128.0.0.1'

try:
    client = intersecordercmdws.IntersecOrderCommandWs(
                                            config.JobConfig())

    # create_intersec_sg_startup
    print('create_intersec_sg_startup')
    output = client.create_intersec_sg_startup(
                            device_id,
                            instance_name,
                            license_key
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_sg_nw
    print('create_intersec_sg_nw')
    output = client.create_intersec_sg_nw(
                            device_id,
                            nic_number,
                            ip_address,
                            subnet
    )
    print(type(output))
    print(output)
    print()

    # update_intersec_sg_nw
    print('update_intersec_sg_nw')
    output = client.update_intersec_sg_nw(
                            device_id,
                            nic_number,
                            ip_address,
                            subnet
    )
    print(type(output))
    print(output)
    print()

    # delete_intersec_sg_nw
    print('delete_intersec_sg_nw')
    output = client.delete_intersec_sg_nw(
                            device_id,
                            nic_number
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_sg_reboot
    print('create_intersec_sg_reboot')
    output = client.create_intersec_sg_reboot(
                            device_id
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_sg_zabbix
    print('create_intersec_sg_zabbix')
    output = client.create_intersec_sg_zabbix(
                            device_id,
                            instance_name,
                            zabbix_vip_ip_address,
                            zabbix01_ip_address,
                            zabbix02_ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_sg_ntp
    print('create_intersec_sg_ntp')
    output = client.create_intersec_sg_ntp(
                            device_id,
                            ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_sg_default_gw
    print('create_intersec_sg_default_gw')
    output = client.create_intersec_sg_default_gw(
                            device_id,
                            gw_ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_sg_static_route
    print('create_intersec_sg_static_route')
    output = client.create_intersec_sg_static_route(
                            device_id,
                            dst_ip_address,
                            dst_subnet,
                            gw_ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_lb_startup
    print('create_intersec_lb_startup')
    output = client.create_intersec_lb_startup(
                            device_id,
                            instance_name,
                            ip_address,
                            license_key
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_lb_nw
    print('create_intersec_lb_nw')
    output = client.create_intersec_lb_nw(
                            device_id,
                            nic_number,
                            ip_address,
                            subnet,
                            broadcast_address
    )
    print(type(output))
    print(output)
    print()

    # update_intersec_lb_nw
    print('update_intersec_lb_nw')
    output = client.update_intersec_lb_nw(
                            device_id,
                            nic_number,
                            ip_address,
                            subnet,
                            broadcast_address
    )
    print(type(output))
    print(output)
    print()

    # delete_intersec_lb_nw
    print('delete_intersec_lb_nw')
    output = client.delete_intersec_lb_nw(
                            device_id,
                            nic_number
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_lb_reboot
    print('create_intersec_lb_reboot')
    output = client.create_intersec_lb_reboot(
                            device_id
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_lb_zabbix
    print('create_intersec_lb_zabbix')
    output = client.create_intersec_lb_zabbix(
                            device_id,
                            instance_name,
                            zabbix_vip_ip_address,
                            zabbix01_ip_address,
                            zabbix02_ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_lb_ntp
    print('create_intersec_lb_ntp')
    output = client.create_intersec_lb_ntp(
                            device_id,
                            ip_address
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_lb_default_gw
    print('create_intersec_lb_default_gw')
    output = client.create_intersec_lb_default_gw(
                            device_id,
                            gw_ip_address,
                            nic_number
    )
    print(type(output))
    print(output)
    print()

    # create_intersec_lb_static_route
    print('create_intersec_lb_static_route')
    output = client.create_intersec_lb_static_route(
                            device_id,
                            dst_ip_address,
                            dst_subnet,
                            gw_ip_address
    )
    print(type(output))
    print(output)

except:
    print('NG')
    print(traceback.format_exc())
