insert into WIM_CONFIG_MNG
(create_id, create_date, update_id, update_date, extension_info)
values
('system', now(), 'system', now(),
'{
	"type":"3",
	"dc_id":"dc02",
	"region_id":"",
	"pod_id":"pod0001",
	"config_info":"
	{
		"msa_config_for_common":
		{
			"msa_ip_address":"10.169.245.64",
			"tftp_server_ip_address":"10.169.245.64",
			"pub_vlan_gateway":"100.96.1.254",
			"ext_vlan_gateway":"172.17.3.158",
			"svc_vlan_network_address":"100.96.0.0",
			"svc_vlan_network_mask":"24",
			"svc_vlan_dns_primary_ip_address":"100.96.0.12",
			"svc_vlan_dns_secondary_ip_address":"100.96.0.13",
			"svc_vlan_ntp_primary_ip_address":"100.96.0.12",
			"svc_vlan_ntp_secondary_ip_address":"100.96.0.13",
			"svc_vlan_proxy_ip_address":"100.96.0.14",
			"svc_vlan_proxy_port":"8080",
			"msa_customer_name_prefix":"c_tenant",
			"msa_server_device_id":"100"
		},
		"msa_config_for_device":
		{
			"filefly":
			{
				"manufacturer_id":18,
				"model_id":121,
				"object_attach_file":[
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_System_Common.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_LAN_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_WAN_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_Loopback_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Basic.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Peer.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP_Tracking.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_StaticRoute.xml"
				 ],
				 "user_id":"admin",
				 "user_default_password":"",
				 "user_new_password":"Passw0rd",
				 "admin_password":"Passw0rd",
				 "nic_prefix":"ge-0/0/",
				 "default_timezone":"GMT-9",
				 "default_wan_interface_mtu":"1400",
				 "device_name":"Firefly",
				 "nic_for_msa":"0",
				 "nic_for_wan":"1",
				 "nic_for_first_lan":"2"
			},
			"csr1000v":
			{
				"manufacturer_id":1,
				"model_id":113,
				"object_attach_file":[
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSystemCommon.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aWanInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLanInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLoopbackInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aDefaultRoute.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aStaticRoute.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aBgpBasic.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aBgpPeer.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpPrimary.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpSecondary.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpTracking.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aDns.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSnmp.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSyslog.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aNtp.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLicense.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aThroughput.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecBasicAh.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecPeer.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aTunnelInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecBasicEsp.xml"
				],
				"user_id":"admin",
				"user_default_password":"",
				"user_new_password":"Passw0rd",
				"admin_password":"Passw0rd",
				"nic_prefix":"GigabitEthernet",
				"device_name":"CSR1000v",
				"default_timezone":"JST 9 0",
				"nic_for_msa":"1",
				"nic_for_wan":"2",
				"nic_for_first_lan":"3",
				"snmp_community_name":"Public",
				"snmp_trap_version":"2c",
				"syslog_facility":"local0",
				"syslog_severity":"warnings",
				"default_wan_interface_mtu":1400,
				"loopback_interface_name":"Loopback0",
				"static_route_for_dc":"static001",
				"static_route_dst_name":"_static001",
				"license_key":"ZWQ5MjQyZjEtYWJjZS00MGQ4LWE1ODgtNDMyYmQxZmY3ZWMyLTE1MDY2Njg5%0ANTQ4NjZ8L1hhMkpzY0NQRy93QXp2NnpMSXV0eHJtT2QyU1U0bFA5QWZnemJi%0AOEhLUT0%3D%0A",
				"ce01":
				{
					"bgp_local_preference":200,
					"hsrp_priority":120,
					"hsrp_track_prioritycost":10
				},
				"ce02":
				{
					"bgp_local_preference":110,
					"hsrp_priority":115,
					"hsrp_track_prioritycost":10
				},
				"throughput":
				{
					"1":10,
					"2":50,
					"3":100,
					"4":250,
					"5":500,
					"6":1000,
					"7":2500,
					"8":5000,
					"9":10000
				},
				"msa_client_params":
				{
					"3":
					{
						"create_csr1000v_vm_ipsec_basic_esp":
						{
							"ce01":
							{
								"authentication_transform":"esp-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"encryption_transform":"esp-3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							},
							"ce02":
							{
								"authentication_transform":"esp-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"encryption_transform":"esp-3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							}
						}
					},
					"4":
					{
						"create_csr1000v_vm_ipsec_basic_ah":
						{
							"ce01":
							{
								"authentication_transform":"ah-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							},
							"ce02":
							{
								"authentication_transform":"ah-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							}
						}
					}
				},
				"nic_prefix_tunnel": "Tunnel",
				"nic_profile_tunnel": "VTI"
			}
		}
	}"
}'),
('system', now(), 'system', now(),
'{
	"type":"3",
	"dc_id":"dc01",
	"region_id":"",
	"pod_id":"pod0001",
	"config_info":"
	{
		"msa_config_for_common":
		{
			"msa_ip_address":"100.94.246.64",
			"tftp_server_ip_address":"100.94.246.64",
			"pub_vlan_gateway":"100.65.255.254",
			"ext_vlan_gateway":"171.17.1.158",
			"svc_vlan_network_address":"100.64.0.0",
			"svc_vlan_network_mask":"16",
			"svc_vlan_dns_primary_ip_address":"100.64.10.16",
			"svc_vlan_dns_secondary_ip_address":"100.64.10.17",
			"svc_vlan_ntp_primary_ip_address":"100.64.10.16",
			"svc_vlan_ntp_secondary_ip_address":"100.64.10.17",
			"svc_vlan_proxy_ip_address":"100.64.10.9",
			"svc_vlan_proxy_port":"8080",
			"msa_customer_name_prefix":"c_tenant",
			"msa_server_device_id":"100"
		},
		"msa_config_for_device":
		{
			"filefly":
			{
				"manufacturer_id":18,
				"model_id":121,
				"object_attach_file":[
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_System_Common.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_LAN_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_WAN_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_Loopback_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Basic.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Peer.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP_Tracking.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_StaticRoute.xml"
				],
				"user_id":"admin",
				"user_default_password":"",
				"user_new_password":"Passw0rd",
				"admin_password":"Passw0rd",
				"nic_prefix":"ge-0/0/",
				"default_timezone":"GMT-9",
				"default_wan_interface_mtu":"1400",
				"device_name":"Firefly",
				"nic_for_msa":"0",
				"nic_for_wan":"1",
				"nic_for_first_lan":"2"
			},
			"csr1000v":
			{
				"manufacturer_id":1,
				"model_id":113,
				"object_attach_file":[
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSystemCommon.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aWanInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLanInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLoopbackInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aDefaultRoute.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aStaticRoute.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aBgpBasic.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aBgpPeer.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpPrimary.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpSecondary.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpTracking.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aDns.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSnmp.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSyslog.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aNtp.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLicense.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aThroughput.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecBasicAh.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecPeer.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aTunnelInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecBasicEsp.xml"
				],
				"user_id":"admin",
				"user_default_password":"",
				"user_new_password":"Passw0rd",
				"admin_password":"Passw0rd",
				"nic_prefix":"GigabitEthernet",
				"device_name":"CSR1000v",
				"default_timezone":"JST 9 0",
				"nic_for_msa":"1",
				"nic_for_wan":"2",
				"nic_for_first_lan":"3",
				"snmp_community_name":"Public",
				"snmp_trap_version":"2c",
				"syslog_facility":"local0",
				"syslog_severity":"warnings",
				"default_wan_interface_mtu":1400,
				"loopback_interface_name":"Loopback0",
				"static_route_for_dc":"static001",
				"static_route_dst_name":"_static001",
				"license_key":"ZWQ5MjQyZjEtYWJjZS00MGQ4LWE1ODgtNDMyYmQxZmY3ZWMyLTE1MDY2Njg5%0ANTQ4NjZ8L1hhMkpzY0NQRy93QXp2NnpMSXV0eHJtT2QyU1U0bFA5QWZnemJi%0AOEhLUT0%3D%0A",
				"ce01":
				{
					"bgp_local_preference":200,
					"hsrp_priority":120,
					"hsrp_track_prioritycost":10
				},
				"ce02":
				{
					"bgp_local_preference":110,
					"hsrp_priority":115,
					"hsrp_track_prioritycost":10
				},
				"throughput":
				{
					"1":10,
					"2":50,
					"3":100,
					"4":250,
					"5":500,
					"6":1000,
					"7":2500,
					"8":5000,
					"9":10000
				},
				"msa_client_params":
				{
					"3":
					{
						"create_csr1000v_vm_ipsec_basic_esp":
						{
							"ce01":
							{
								"authentication_transform":"esp-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"encryption_transform":"esp-3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							},
							"ce02":
							{
								"authentication_transform":"esp-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"encryption_transform":"esp-3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							}
						}
					},
					"4":
					{
						"create_csr1000v_vm_ipsec_basic_ah":
						{
							"ce01":
							{
								"authentication_transform":"ah-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							},
							"ce02":
							{
								"authentication_transform":"ah-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							}
						}
					}
				},
				"nic_prefix_tunnel": "Tunnel",
				"nic_profile_tunnel": "VTI"
			}
		}
	}"
}'),
('system', now(), 'system', now(),
'{
	"type":"3",
	"dc_id":"dc03",
	"region_id":"",
	"pod_id":"pod0001",
	"config_info":"
	{
		"msa_config_for_common":
		{
			"msa_ip_address":"10.3.245.63",
			"tftp_server_ip_address":"10.3.245.63",
			"pub_vlan_gateway":"100.104.1.254",
			"ext_vlan_gateway":"172.17.5.158",
			"svc_vlan_network_address":"100.104.0.0",
			"svc_vlan_network_mask":"24",
			"svc_vlan_dns_primary_ip_address":"100.104.0.10",
			"svc_vlan_dns_secondary_ip_address":"100.104.0.11",
			"svc_vlan_ntp_primary_ip_address":"100.104.0.10",
			"svc_vlan_ntp_secondary_ip_address":"100.104.0.11",
			"svc_vlan_proxy_ip_address":"100.104.0.12",
			"svc_vlan_proxy_port":"8080",
			"msa_customer_name_prefix":"c_tenant",
			"msa_server_device_id":"100"
		},
		"msa_config_for_device":
		{
			"filefly":
			{
				"manufacturer_id":18,
				"model_id":121,
				"object_attach_file":[
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_System_Common.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_LAN_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_WAN_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_Loopback_Interface.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Basic.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Peer.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP_Tracking.xml",
					"/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_StaticRoute.xml"
				],
				"user_id":"admin",
				"user_default_password":"",
				"user_new_password":"Passw0rd",
				"admin_password":"Passw0rd",
				"nic_prefix":"ge-0/0/",
				"default_timezone":"GMT-9",
				"default_wan_interface_mtu":"1400",
				"device_name":"Firefly",
				"nic_for_msa":"0",
				"nic_for_wan":"1",
				"nic_for_first_lan":"2"
			},
			"csr1000v":
			{
				"manufacturer_id":1,
				"model_id":113,
				"object_attach_file":[
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSystemCommon.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aWanInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLanInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLoopbackInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aDefaultRoute.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aStaticRoute.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aBgpBasic.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aBgpPeer.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpPrimary.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpSecondary.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpTracking.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aDns.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSnmp.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aSyslog.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aNtp.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aLicense.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aThroughput.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecBasicAh.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecPeer.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aTunnelInterface.xml",
					"/CommandDefinition/CISCO/ISR/CiscoCsrStdIosXe16dot03dot01aIpsecBasicEsp.xml"
				],
				"user_id":"admin",
				"user_default_password":"",
				"user_new_password":"Passw0rd",
				"admin_password":"Passw0rd",
				"nic_prefix":"GigabitEthernet",
				"device_name":"CSR1000v",
				"default_timezone":"JST 9 0",
				"nic_for_msa":"1",
				"nic_for_wan":"2",
				"nic_for_first_lan":"3",
				"snmp_community_name":"Public",
				"snmp_trap_version":"2c",
				"syslog_facility":"local0",
				"syslog_severity":"warnings",
				"default_wan_interface_mtu":1400,
				"loopback_interface_name":"Loopback0",
				"static_route_for_dc":"static001",
				"static_route_dst_name":"_static001",
				"license_key":"ZWQ5MjQyZjEtYWJjZS00MGQ4LWE1ODgtNDMyYmQxZmY3ZWMyLTE1MDY2Njg5%0ANTQ4NjZ8L1hhMkpzY0NQRy93QXp2NnpMSXV0eHJtT2QyU1U0bFA5QWZnemJi%0AOEhLUT0%3D%0A",
				"ce01":
				{
					"bgp_local_preference":200,
					"hsrp_priority":120,
					"hsrp_track_prioritycost":10
				},
				"ce02":
				{
					"bgp_local_preference":110,
					"hsrp_priority":115,
					"hsrp_track_prioritycost":10
				},
				"throughput":
				{
					"1":10,
					"2":50,
					"3":100,
					"4":250,
					"5":500,
					"6":1000,
					"7":2500,
					"8":5000,
					"9":10000
				},
				"msa_client_params":
				{
					"3":
					{
						"create_csr1000v_vm_ipsec_basic_esp":
						{
							"ce01":
							{
								"authentication_transform":"esp-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"encryption_transform":"esp-3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							},
							"ce02":
							{
								"authentication_transform":"esp-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"encryption_transform":"esp-3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							}
						}
					},
					"4":
					{
						"create_csr1000v_vm_ipsec_basic_ah":
						{
							"ce01":
							{
								"authentication_transform":"ah-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							},
							"ce02":
							{
								"authentication_transform":"ah-md5-hmac",
								"diffie_hellman_group":2,
								"encryption_algorithm":"3des",
								"hash_algorithm":"md5",
								"priority":1,
								"profile_name":"VTI",
								"transform_set":"IPSEC",
								"isakmp_sa_lifetime":86400,
								"ipsec_sa_lifetime":3600
							}
						}
					}
				},
				"nic_prefix_tunnel": "Tunnel",
				"nic_profile_tunnel": "VTI"
			}
		}
	}"
}'),
('system', now(), 'system', now(),
'{
	"type":"5",
	"dc_id":"dc02",
	"region_id":"",
	"pod_id":"",
	"config_info":"
	{
		"device_name_list":
		{
			"1":
			{
				"3":
				{
					"1":
					{
						"name":"filefly"
					},
					"2":
					{
						"name":"csr1000v"
					}
				}
			}
		},
		"os_image_and_flavor_name_list":
		{
			"3":
			{
				"1":
				{
					"flavor_name":"vsrx-12.1x47_d20.7-M2D2E0S0C2F1.0P1",
					"image_name":"vsrx-12.1x47_d20.7"
				},
				"2":
				{
					"flavor_name":"csr1000v-16.03.01a-M4D8E0S0C4F1.0P1",
					"image_name":"csr1000v-16.03.01a"
				}
			}
		},
		"os_vlan_name_list":
		{
			"msa_lan":
			{
				"name":"MSA"
			},
			"pub_lan":
			{
				"name":"Pub"
			},
			"ext_lan":
			{
				"name":"Ext"
			},
			"idc_lan":
			{
				"name":"IDC"
			}
		},
		"inter_dc_netowrk_info":
		{
			"dc01":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.1",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.129",
					"loopback_seg":"100.80.251.128",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.2",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.130",
					"loopback_seg":"100.80.251.128",
					"loopback_netmask":"30"
				}
			},
			"dc02":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.3",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.133",
					"loopback_seg":"100.80.251.132",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.4",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.134",
					"loopback_seg":"100.80.251.132",
					"loopback_netmask":"30"
				}
			},
			"dc03":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.5",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.137",
					"loopback_seg":"100.80.251.136",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.6",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.138",
					"loopback_seg":"100.80.251.136",
					"loopback_netmask":"30"
				}
			}
		},
		"inter_dc_netowrk_info_for_tunnel":
		{
			"dc01":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc02":
						{
							"ce01": "100.80.251.1",
							"ce01_network": "100.80.251.0",
							"ce01_netmask": "30",
							"ce02": "100.80.251.5",
							"ce02_network": "100.80.251.4",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.17",
							"ce01_network": "100.80.251.16",
							"ce01_netmask": "30",
							"ce02": "100.80.251.21",
							"ce02_network": "100.80.251.20",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.129",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.128"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc02":
						{
							"ce01": "100.80.251.9",
							"ce01_network": "100.80.251.8",
							"ce01_netmask": "30",
							"ce02": "100.80.251.13",
							"ce02_network": "100.80.251.12",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.25",
							"ce01_network": "100.80.251.24",
							"ce01_netmask": "30",
							"ce02": "100.80.251.29",
							"ce02_network": "100.80.251.28",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.130",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.128"
				}
			},
			"dc02":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.2",
							"ce01_network": "100.80.251.0",
							"ce01_netmask": "30",
							"ce02": "100.80.251.10",
							"ce02_network": "100.80.251.8",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.33",
							"ce01_network": "100.80.251.32",
							"ce01_netmask": "30",
							"ce02": "100.80.251.37",
							"ce02_network": "100.80.251.36",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.133",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.132"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.6",
							"ce01_network": "100.80.251.4",
							"ce01_netmask": "30",
							"ce02": "100.80.251.14",
							"ce02_network": "100.80.251.12",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.41",
							"ce01_network": "100.80.251.40",
							"ce01_netmask": "30",
							"ce02": "100.80.251.45",
							"ce02_network": "100.80.251.44",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.134",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.132"
				}
			},
			"dc03":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.18",
							"ce01_network": "100.80.251.16",
							"ce01_netmask": "30",
							"ce02": "100.80.251.26",
							"ce02_network": "100.80.251.24",
							"ce02_netmask": "30"
						},
						"dc02":
						{
							"ce01": "100.80.251.34",
							"ce01_network": "100.80.251.32",
							"ce01_netmask": "30",
							"ce02": "100.80.251.42",
							"ce02_network": "100.80.251.40",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.137",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.136"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.22",
							"ce01_network": "100.80.251.20",
							"ce01_netmask": "30",
							"ce02": "100.80.251.30",
							"ce02_network": "100.80.251.28",
							"ce02_netmask": "30"
						},
						"dc02":
						{
							"ce01": "100.80.251.38",
							"ce01_network": "100.80.251.36",
							"ce01_netmask": "30",
							"ce02": "100.80.251.46",
							"ce02_network": "100.80.251.44",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.138",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.136"
				}
			}
		}
	}"
}'),
('system', now(), 'system', now(),
'{
	"type":"5",
	"dc_id":"dc01",
	"region_id":"",
	"pod_id":"",
	"config_info":"
	{
		"device_name_list":
		{
			"1":
			{
				"3":
				{
					"1":
					{
						"name":"filefly"
					},
					"2":
					{
						"name":"csr1000v"
					}
				}
			}
		},
		"os_image_and_flavor_name_list":
		{
			"3":
			{
				"1":
				{
					"flavor_name":"vsrx-12.1x47_d20.7-M2D2E0S0C2F1.0P1",
					"image_name":"vsrx-12.1x47_d20.7"
				},
				"2":
				{
					"flavor_name":"csr1000v-16.03.01a-M4D8E0S0C4F1.0P1",
					"image_name":"csr1000v-16.03.01a"
				}
			}
		},
		"os_vlan_name_list":
		{
			"msa_lan":
			{
				"name":"MSA"
			},
			"pub_lan":
			{
				"name":"Pub"
			},
			"ext_lan":
			{
				"name":"Ext"
			},
			"idc_lan":
			{
				"name":"IDC"
			}
		},
		"inter_dc_netowrk_info":
		{
			"dc01":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.1",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.129",
					"loopback_seg":"100.80.251.128",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.2",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.130",
					"loopback_seg":"100.80.251.128",
					"loopback_netmask":"30"
				}
			},
			"dc02":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.3",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.133",
					"loopback_seg":"100.80.251.132",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.4",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.134",
					"loopback_seg":"100.80.251.132",
					"loopback_netmask":"30"
				}
			},
			"dc03":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.5",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.137",
					"loopback_seg":"100.80.251.136",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.6",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.138",
					"loopback_seg":"100.80.251.136",
					"loopback_netmask":"30"
				}
			}
		},
		"inter_dc_netowrk_info_for_tunnel":
		{
			"dc01":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc02":
						{
							"ce01": "100.80.251.1",
							"ce01_network": "100.80.251.0",
							"ce01_netmask": "30",
							"ce02": "100.80.251.5",
							"ce02_network": "100.80.251.4",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.17",
							"ce01_network": "100.80.251.16",
							"ce01_netmask": "30",
							"ce02": "100.80.251.21",
							"ce02_network": "100.80.251.20",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.129",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.128"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc02":
						{
							"ce01": "100.80.251.9",
							"ce01_network": "100.80.251.8",
							"ce01_netmask": "30",
							"ce02": "100.80.251.13",
							"ce02_network": "100.80.251.12",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.25",
							"ce01_network": "100.80.251.24",
							"ce01_netmask": "30",
							"ce02": "100.80.251.29",
							"ce02_network": "100.80.251.28",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.130",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.128"
				}
			},
			"dc02":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.2",
							"ce01_network": "100.80.251.0",
							"ce01_netmask": "30",
							"ce02": "100.80.251.10",
							"ce02_network": "100.80.251.8",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.33",
							"ce01_network": "100.80.251.32",
							"ce01_netmask": "30",
							"ce02": "100.80.251.37",
							"ce02_network": "100.80.251.36",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.133",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.132"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.6",
							"ce01_network": "100.80.251.4",
							"ce01_netmask": "30",
							"ce02": "100.80.251.14",
							"ce02_network": "100.80.251.12",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.41",
							"ce01_network": "100.80.251.40",
							"ce01_netmask": "30",
							"ce02": "100.80.251.45",
							"ce02_network": "100.80.251.44",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.134",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.132"
				}
			},
			"dc03":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.18",
							"ce01_network": "100.80.251.16",
							"ce01_netmask": "30",
							"ce02": "100.80.251.26",
							"ce02_network": "100.80.251.24",
							"ce02_netmask": "30"
						},
						"dc02":
						{
							"ce01": "100.80.251.34",
							"ce01_network": "100.80.251.32",
							"ce01_netmask": "30",
							"ce02": "100.80.251.42",
							"ce02_network": "100.80.251.40",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.137",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.136"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.22",
							"ce01_network": "100.80.251.20",
							"ce01_netmask": "30",
							"ce02": "100.80.251.30",
							"ce02_network": "100.80.251.28",
							"ce02_netmask": "30"
						},
						"dc02":
						{
							"ce01": "100.80.251.38",
							"ce01_network": "100.80.251.36",
							"ce01_netmask": "30",
							"ce02": "100.80.251.46",
							"ce02_network": "100.80.251.44",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.138",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.136"
				}
			}
		}
	}"
}'),
('system', now(), 'system', now(),
'{
	"type":"5",
	"dc_id":"dc03",
	"region_id":"",
	"pod_id":"",
	"config_info":"
	{
		"device_name_list":
		{
			"1":
			{
				"3":
				{
					"1":
					{
						"name":"filefly"
					},
					"2":
					{
						"name":"csr1000v"
					}
				}
			}
		},
		"os_image_and_flavor_name_list":
		{
			"3":
			{
				"1":
				{
					"flavor_name":"vsrx-12.1x47_d20.7-M2D2E0S0C2F1.0P1",
					"image_name":"vsrx-12.1x47_d20.7"
				},
				"2":
				{
					"flavor_name":"csr1000v-16.03.01a-M4D8E0S0C4F1.0P1",
					"image_name":"csr1000v-16.03.01a"
				}
			}
		},
		"os_vlan_name_list":
		{
			"msa_lan":
			{
				"name":"MSA"
			},
			"pub_lan":
			{
				"name":"Pub"
			},
			"ext_lan":
			{
				"name":"Ext"
			},
			"idc_lan":
			{
				"name":"IDC"
			}
		},
		"inter_dc_netowrk_info":
		{
			"dc01":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.1",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.129",
					"loopback_seg":"100.80.251.128",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.2",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.130",
					"loopback_seg":"100.80.251.128",
					"loopback_netmask":"30"
				}
			},
			"dc02":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.3",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.133",
					"loopback_seg":"100.80.251.132",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.4",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.134",
					"loopback_seg":"100.80.251.132",
					"loopback_netmask":"30"
				}
			},
			"dc03":
			{
				"ce01":
				{
					"wan_ip":"100.80.251.5",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.137",
					"loopback_seg":"100.80.251.136",
					"loopback_netmask":"30"
				},
				"ce02":
				{
					"wan_ip":"100.80.251.6",
					"wan_subnet_ip":"100.80.251.0",
					"wan_netmask":"25",
					"loopback_ip":"100.80.251.138",
					"loopback_seg":"100.80.251.136",
					"loopback_netmask":"30"
				}
			}
		},
		"inter_dc_netowrk_info_for_tunnel":
		{
			"dc01":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc02":
						{
							"ce01": "100.80.251.1",
							"ce01_network": "100.80.251.0",
							"ce01_netmask": "30",
							"ce02": "100.80.251.5",
							"ce02_network": "100.80.251.4",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.17",
							"ce01_network": "100.80.251.16",
							"ce01_netmask": "30",
							"ce02": "100.80.251.21",
							"ce02_network": "100.80.251.20",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.129",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.128"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc02":
						{
							"ce01": "100.80.251.9",
							"ce01_network": "100.80.251.8",
							"ce01_netmask": "30",
							"ce02": "100.80.251.13",
							"ce02_network": "100.80.251.12",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.25",
							"ce01_network": "100.80.251.24",
							"ce01_netmask": "30",
							"ce02": "100.80.251.29",
							"ce02_network": "100.80.251.28",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.130",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.128"
				}
			},
			"dc02":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.2",
							"ce01_network": "100.80.251.0",
							"ce01_netmask": "30",
							"ce02": "100.80.251.10",
							"ce02_network": "100.80.251.8",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.33",
							"ce01_network": "100.80.251.32",
							"ce01_netmask": "30",
							"ce02": "100.80.251.37",
							"ce02_network": "100.80.251.36",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.133",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.132"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.6",
							"ce01_network": "100.80.251.4",
							"ce01_netmask": "30",
							"ce02": "100.80.251.14",
							"ce02_network": "100.80.251.12",
							"ce02_netmask": "30"
						},
						"dc03":
						{
							"ce01": "100.80.251.41",
							"ce01_network": "100.80.251.40",
							"ce01_netmask": "30",
							"ce02": "100.80.251.45",
							"ce02_network": "100.80.251.44",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.134",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.132"
				}
			},
			"dc03":
			{
				"ce01":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.18",
							"ce01_network": "100.80.251.16",
							"ce01_netmask": "30",
							"ce02": "100.80.251.26",
							"ce02_network": "100.80.251.24",
							"ce02_netmask": "30"
						},
						"dc02":
						{
							"ce01": "100.80.251.34",
							"ce01_network": "100.80.251.32",
							"ce01_netmask": "30",
							"ce02": "100.80.251.42",
							"ce02_network": "100.80.251.40",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.137",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.136"
				},
				"ce02":
				{
					"innter_dc_seg_for_tenant":
					{
						"dc01":
						{
							"ce01": "100.80.251.22",
							"ce01_network": "100.80.251.20",
							"ce01_netmask": "30",
							"ce02": "100.80.251.30",
							"ce02_network": "100.80.251.28",
							"ce02_netmask": "30"
						},
						"dc02":
						{
							"ce01": "100.80.251.38",
							"ce01_network": "100.80.251.36",
							"ce01_netmask": "30",
							"ce02": "100.80.251.46",
							"ce02_network": "100.80.251.44",
							"ce02_netmask": "30"
						}
					},
					"loopback_ip": "100.80.251.138",
					"loopback_netmask": "30",
					"loopback_seg": "100.80.251.136"
				}
			}
		}
	}"
}');
