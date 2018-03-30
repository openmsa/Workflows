#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  


"""Service data list
SERVICE_DATA_LIST[0], ID:23, Member in
SERVICE_DATA_LIST[1], ID:24, Member out
SERVICE_DATA_LIST[2], ID:25, Member out and not cisco
"""

SERVICE_DATA_LIST = [
    {
        "create_id": "system",
        "create_date": "20160729000000",
        "update_id": "system",
        "update_date": "20160729000000",
        "delete_flg": "0",
        "ID": "23",
        "group_id": "group_id_00001",
        "group_name": "dc_gru_1",
        "group_type": "1",
        "tenant_name": "admin",
        "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
        "operation_type": "1",
        "task_status": "1",
        "my_group_flg": "1",
        "my_dc_id": "dc_id_00001"
    },
    {
        "create_id": "system",
        "create_date": "20160729000000",
        "update_id": "system",
        "update_date": "20160729000000",
        "delete_flg": "0",
        "ID": "24",
        "group_id": "group_id_00002",
        "group_name": "dc_gru_2",
        "group_type": "2",
        "tenant_name": "admin",
        "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
        "operation_type": "1",
        "task_status": "1",
        "my_dc_id": "dc_id_00001"
    },
    {
        "create_id": "system",
        "create_date": "20160729000000",
        "update_id": "system",
        "update_date": "20160729000000",
        "delete_flg": "0",
        "ID": "25",
        "group_id": "group_id_00002",
        "group_name": "dc_gru_1",
        "group_type": "1",
        "tenant_name": "admin",
        "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
        "operation_type": "1",
        "task_status": "1",
        "my_dc_id": "dc_id_00001"
    }
]

"""service detail data
SERVICE_DATA_DEFAULT
SERVICE_DATA_OUT_OF_MEMBER
SERVICE_DATA_NO_MEMBER_LIST
SERVICE_DATA_NO_NETWORK_LIST
SERVICE_DATA_CISCO
"""

SERVICE_DATA_DEFAULT = {
    "dc_info": [
        {
            "dc_id": "dc_id_00001",
            "dc_name": "dc_1",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03"
        },
        {
            "dc_id": "dc_id_00002",
            "dc_name": "dc_2",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03"
        }
    ],
    "dc_group_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "group_name": "dc_gru_1",
            "group_type": "1",
            "tenant_name": "admin",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "operation_type": "1",
            "task_status": "1",
            "my_dc_id": "dc_id_00001"
        }
    ],
    "dc_member_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "dc_id": "dc_id_00001",
            "tenant_name": "admin",
            "pod_id": "2",
            "tenant_id": "1234",
            "IaaS_region_id": "region1",
            "IaaS_tenant_id": "9876",
            "IaaS_network_type": "vxlan",
            "IaaS_network_id": "network_id_00002",
            "IaaS_subnet_id": "subnet_id_00002",
            "IaaS_subnet_id_v6": "subnet_id_00002_v6",
            "IaaS_network_name": "netA",
            "IaaS_segmentation_id": "21",
            "wan_network_id": "wan_id_00001",
            "vrrp_address": "10.58.79.0/24",
            "ce1_address": "10.10.10.10",
            "ce2_address": "10.11.10.10",
            "vrrp_address_v6": "1234:5678::abc0/124",
            "ce1_address_v6": "1234:5678::abc2",
            "ce2_address_v6": "1234:5678::abc3",
            "dc_name": "dc_1",
            "bandwidth": "2"
        },
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "dc_id": "dc_id_00002",
            "tenant_name": "admin",
            "pod_id": "2",
            "tenant_id": "1234",
            "IaaS_region_id": "region1",
            "IaaS_tenant_id": "9876",
            "IaaS_network_type": "vlan",
            "IaaS_network_id": "network_id_00003",
            "IaaS_subnet_id": "subnet_id_00003",
            "IaaS_subnet_id_v6": "",
            "IaaS_network_name": "netB",
            "IaaS_segmentation_id": "21",
            "wan_network_id": "wan_id_00001",
            "vrrp_address": "10.58.79.0/24",
            "ce1_address": "10.10.10.10",
            "ce2_address": "10.11.10.10",
            "vrrp_address_v6": "",
            "ce1_address_v6": "",
            "ce2_address_v6": "",
            "dc_name": "dc_2",
            "bandwidth": "3"
        }
    ],
    "apl_info": [
        {
            "ID": 117,
            "MSA_device_id": "MSA_device_id_001",
            "apl_type": "1",
            "type": "1",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx1",
            "node_name": "nal_vfw1",
            "pod_id": "podid",
            "task_status": "1",
            "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "ntp_ip_address": "10.58.79.176",
            "dns_ip_address": "10.58.79.177",
            "snmp_ip_address": "10.58.79.178",
            "syslog_ip_address": "10.58.79.179"
        }
    ]
}

SERVICE_DATA_OUT_OF_MEMBER = {
    "dc_info": [
        {
            "dc_id": "dc_id_00002",
            "dc_name": "dc_2",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03"
        }
    ],
    "dc_group_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "24",
            "group_id": "group_id_00001",
            "group_name": "dc_gru_2",
            "group_type": "1",
            "tenant_name": "admin",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "operation_type": "1",
            "task_status": "1",
            "my_dc_id": "dc_id_00001"
        }
    ],
    "dc_member_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00002",
            "dc_id": "dc_id_00001",
            "tenant_name": "admin",
            "pod_id": "2",
            "tenant_id": "1234",
            "IaaS_region_id": "region1",
            "IaaS_tenant_id": "9876",
            "IaaS_network_type": "vxlan",
            "IaaS_network_id": "net_id_00001",
            "IaaS_subnet_id": "subnet_id_00002",
            "IaaS_subnet_id_v6": "subnet_id_00002_v6",
            "IaaS_network_name": "netA",
            "IaaS_segmentation_id": "21",
            "wan_network_id": "wan_id_00001",
            "vrrp_address": "10.58.79.0/24",
            "ce1_address": "10.10.10.10",
            "ce2_address": "10.11.10.10",
            "vrrp_address_v6": "1234:5678::abc0/124",
            "ce1_address_v6": "1234:5678::abc2",
            "ce2_address_v6": "1234:5678::abc3",
            "dc_name": "dc_1",
            "bandwidth": "2"
        },
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "dc_id": "dc_id_00002",
            "tenant_name": "admin",
            "pod_id": "2",
            "tenant_id": "1234",
            "IaaS_region_id": "region1",
            "IaaS_tenant_id": "9876",
            "IaaS_network_type": "vlan",
            "IaaS_network_id": "net_id_00002",
            "IaaS_subnet_id": "subnet_id_00002",
            "IaaS_subnet_id_v6": "",
            "IaaS_network_name": "netB",
            "IaaS_segmentation_id": "21",
            "wan_network_id": "wan_id_00001",
            "vrrp_address": "10.58.79.0/24",
            "ce1_address": "10.10.10.10",
            "ce2_address": "10.11.10.10",
            "vrrp_address_v6": "",
            "ce1_address_v6": "",
            "ce2_address_v6": "",
            "dc_name": "dc_2",
            "bandwidth": "3"
        }
    ],
    "apl_info": [
        {
            "ID": 117,
            "MSA_device_id": "MSA_device_id_001",
            "apl_type": "1",
            "type": "1",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx1",
            "node_name": "nal_vfw1",
            "pod_id": "podid",
            "task_status": "1",
            "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "ntp_ip_address": "10.58.79.176",
            "dns_ip_address": "10.58.79.177",
            "snmp_ip_address": "10.58.79.178",
            "syslog_ip_address": "10.58.79.179"
        }
    ]
}

SERVICE_DATA_NO_MEMBER_LIST = {
    "dc_info": [],
    "dc_group_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "group_name": "dc_gru_1",
            "group_type": "1",
            "tenant_name": "admin",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "operation_type": "1",
            "task_status": "1",
            "my_dc_id": "dc_id_00001"
        }
    ],
    "dc_member_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "dc_id": "dc_id_00001",
            "tenant_name": "admin",
            "pod_id": "2",
            "tenant_id": "1234",
            "IaaS_region_id": "region1",
            "IaaS_tenant_id": "9876",
            "IaaS_network_type": "vxlan",
            "IaaS_network_id": "net_id_00001",
            "IaaS_subnet_id": "subnet_id_00002",
            "IaaS_subnet_id_v6": "subnet_id_00002_v6",
            "IaaS_network_name": "netA",
            "IaaS_segmentation_id": "21",
            "wan_network_id": "wan_id_00001",
            "vrrp_address": "10.58.79.0/24",
            "ce1_address": "10.10.10.10",
            "ce2_address": "10.11.10.10",
            "vrrp_address_v6": "1234:5678::abc0/124",
            "ce1_address_v6": "1234:5678::abc2",
            "ce2_address_v6": "1234:5678::abc3",
            "dc_name": "dc_1",
            "bandwidth": "2"
        },
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "dc_id": "dc_id_00002",
            "tenant_name": "admin",
            "pod_id": "2",
            "tenant_id": "1234",
            "IaaS_region_id": "region1",
            "IaaS_tenant_id": "9876",
            "IaaS_network_type": "vlan",
            "IaaS_network_id": "net_id_00002",
            "IaaS_subnet_id": "subnet_id_00003",
            "IaaS_subnet_id_v6": "",
            "IaaS_network_name": "netB",
            "IaaS_segmentation_id": "21",
            "wan_network_id": "wan_id_00001",
            "vrrp_address": "10.58.79.0/24",
            "ce1_address": "10.10.10.10",
            "ce2_address": "10.11.10.10",
            "vrrp_address_v6": "",
            "ce1_address_v6": "",
            "ce2_address_v6": "",
            "dc_name": "dc_2",
            "bandwidth": "3"
        }
    ],
    "apl_info": [
        {
            "ID": 117,
            "MSA_device_id": "MSA_device_id_001",
            "apl_type": "1",
            "type": "1",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx1",
            "node_name": "nal_vfw1",
            "pod_id": "podid",
            "task_status": "1",
            "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "ntp_ip_address": "10.58.79.176",
            "dns_ip_address": "10.58.79.177",
            "snmp_ip_address": "10.58.79.178",
            "syslog_ip_address": "10.58.79.179"
        }
    ]
}

SERVICE_DATA_NO_NETWORK_LIST = {
    "dc_info": [
        {
            "dc_id": "dc_id_00001",
            "dc_name": "dc_1",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03"
        },
        {
            "dc_id": "dc_id_00002",
            "dc_name": "dc_2",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03"
        }
    ],
    "dc_group_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "group_name": "dc_gru_1",
            "group_type": "1",
            "tenant_name": "admin",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "operation_type": "1",
            "task_status": "1",
            "my_dc_id": "dc_id_00001"
        }
    ],
    "dc_member_info": [],
    "apl_info": [
        {
            "ID": 117,
            "MSA_device_id": "MSA_device_id_001",
            "apl_type": "1",
            "type": "1",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx1",
            "node_name": "nal_vfw1",
            "pod_id": "podid",
            "task_status": "1",
            "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "ntp_ip_address": "10.58.79.176",
            "dns_ip_address": "10.58.79.177",
            "snmp_ip_address": "10.58.79.178",
            "syslog_ip_address": "10.58.79.179"
        }
    ]
}

SERVICE_DATA_CISCO = {
    "dc_info": [
        {
            "dc_id": "dc_id_00001",
            "dc_name": "dc_1",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03"
        }
    ],
    "dc_group_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "group_name": "dc_gru_1",
            "group_type": "2",
            "tenant_name": "admin",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "operation_type": "1",
            "task_status": "1",
            "my_dc_id": "dc_id_00001"
        }
    ],
    "dc_member_info": [
        {
            "create_id": "system",
            "create_date": "20160729000000",
            "update_id": "system",
            "update_date": "20160729000000",
            "delete_flg": "0",
            "ID": "23",
            "group_id": "group_id_00001",
            "dc_id": "dc_id_00001",
            "tenant_name": "admin",
            "pod_id": "2",
            "tenant_id": "1234",
            "IaaS_region_id": "region1",
            "IaaS_tenant_id": "9876",
            "IaaS_network_type": "vxlan",
            "IaaS_network_id": "network_id_00002",
            "IaaS_subnet_id": "subnet_id_00002",
            "IaaS_subnet_id_v6": "",
            "IaaS_network_name": "netA",
            "IaaS_segmentation_id": "21",
            "wan_network_id": "wan_id_00001",
            "vrrp_address": "10.58.79.0/24",
            "ce1_address": "10.10.10.10",
            "ce2_address": "10.11.10.10",
            "vrrp_address_v6": "",
            "ce1_address_v6": "",
            "ce2_address_v6": "",
            "dc_name": "dc_1",
            "bandwidth": "2"
        }
    ],
    "apl_info": [
        {
            "ID": 117,
            "MSA_device_id": "MSA_device_id_001",
            "apl_type": "1",
            "type": "1",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx1",
            "node_name": "nal_vfw1",
            "pod_id": "podid",
            "task_status": "1",
            "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "ntp_ip_address": "10.58.79.176",
            "dns_ip_address": "10.58.79.177",
            "snmp_ip_address": "10.58.79.178",
            "syslog_ip_address": "10.58.79.179"
        }
    ]
}


"""Service id"""
SERVICE_ID = "100"
