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


"""Node data list
NODE_DATA_LIST[0], ID:117, Virtual FW
NODE_DATA_LIST[1], ID:118, Virtual LB
NODE_DATA_LIST[2], ID:119, Physical FW
NODE_DATA_LIST[3], ID:120, Physical LB
"""

NODE_DATA_LIST = [
    {
        "ID": 117,
        "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
        "apl_type": "1",
        "create_date": "xxxx-xx-xx xx:xx:xx",
        "create_id": "xxxxxxx",
        "delete_flg": "0",
        "device_type": "1",
        "node_detail": "[]",
        "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx1",
        "node_name": "nal_vfw1",
        "pod_id": "podid",
        "task_status": "1",
        "type": "1",
        "update_date": "xxxx-xx-xx xx:xx:xx",
        "update_id": "xxxxxxx"
    },
    {
        "ID": 118,
        "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
        "apl_type": "1",
        "create_date": "xxxx-xx-xx xx:xx:xx",
        "create_id": "xxxxxxx",
        "delete_flg": "0",
        "device_type": "1",
        "node_detail": "[]",
        "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx2",
        "node_name": "nal_vfw2",
        "pod_id": "podid",
        "task_status": "1",
        "type": "2",
        "update_date": "xxxx-xx-xx xx:xx:xx",
        "update_id": "xxxxxxx"
    },
    {
        "ID": 119,
        "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
        "apl_type": "2",
        "create_date": "xxxx-xx-xx xx:xx:xx",
        "create_id": "xxxxxxx",
        "delete_flg": "0",
        "device_type": "1",
        "node_detail": "[]",
        "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx3",
        "node_name": "nal_vfw3",
        "pod_id": "podid",
        "task_status": "1",
        "type": "1",
        "update_date": "xxxx-xx-xx xx:xx:xx",
        "update_id": "xxxxxxx"
    },
    {
        "ID": 120,
        "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
        "apl_type": "2",
        "create_date": "xxxx-xx-xx xx:xx:xx",
        "create_id": "xxxxxxx",
        "delete_flg": "0",
        "device_type": "1",
        "node_detail": "[]",
        "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx9",
        "node_name": "nal_plb1",
        "pod_id": "podid",
        "task_status": "1",
        "type": "2",
        "update_date": "xxxx-xx-xx xx:xx:xx",
        "update_id": "xxxxxxx"
    }
]

"""Node detail data
NODE_DATA_VFW
NODE_DATA_VLB
NODE_DATA_PFW
NODE_DATA_PLB
NODE_DATA_NO_NET
"""

NODE_DATA_VFW = {
    "vnf_info": [
        {
            "ID": 117,
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
            "update_id": "xxxxxxx"
        }
    ],
    "port_info": [
        {
            "create_id": "xxxxxxx",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "delete_flg": "0",
            "ID": 1001,
            "IaaS_network_id": 'network_id_00001',
            "IaaS_subnet_id": 'subnet_id_00001',
            "IaaS_subnet_id_v6": '',
            "IaaS_port_id": 'IaaS_port_id_00001',
            "port_id": "port_id_00001",
            "network_type_detail": "1",
            "ip_address": "10.50.79.190",
            "ip_address_v6": "",
            "nic": "ethernet1/11.2"
        },
        {
            "create_id": "xxxxxxx",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "delete_flg": "0",
            "ID": 1002,
            "IaaS_network_id": 'network_id_00002',
            "IaaS_subnet_id": 'subnet_id_00002',
            "IaaS_subnet_id_v6": '',
            "IaaS_port_id": 'IaaS_port_id_00002',
            "port_id": "port_id_00002",
            "network_type_detail": "1",
            "ip_address": "10.50.79.191",
            "ip_address_v6": "",
            "nic": "ethernet1/11.2"
        }
    ]
}

NODE_DATA_VLB = {
    "vnf_info": [
        {
            "ID": 118,
            "apl_type": "1",
            "type": "2",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx5",
            "node_name": "nal_vlb1",
            "pod_id": "podid",
            "task_status": "1",
            "IaaS_tenant_id": "tenant_name",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx"
        }
    ],
    "port_info": [
        {
            "create_id": "xxxxxxx",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "delete_flg": "0",
            "ID": 1002,
            "IaaS_network_id": 'network_id_00002',
            "IaaS_subnet_id": 'subnet_id_00002',
            "IaaS_subnet_id_v6": '',
            "IaaS_port_id": 'IaaS_port_id_00002',
            "port_id": "port_id_00002",
            "network_type_detail": "1",
            "ip_address": "10.50.79.191",
            "ip_address_v6": "",
            "nic": "ethernet1/11.2"
        }
    ]
}

NODE_DATA_PFW = {
    "pnf_info": [
        {
            "ID": 119,
            "apl_type": "2",
            "type": "1",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx8",
            "node_name": "nal_pfw1",
            "pod_id": "podid",
            "process_state": "active",
            "task_status": "1",
            "IaaS_tenant_id": "tenant_name",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "redundant_configuration_flg": "0",
            "device_name_master": "master_name",
            "actsby_flag_master": "act",
            "device_detail_master": "{}",
            "master_ip_address": "10.58.79.178",
            "master_MSA_device_id": "xxx-xxx-xxxx",
            "device_name_slave": "slave_name",
            "device_detail_slave": "{}",
            "actsby_flag_slave": "sby",
            "slave_ip_address": "127.0.0.1",
            "slave_MSA_device_id": "xxx-xxx-xxxx"
        }
    ],
    "port_info": [
        {
            "create_id": "xxxxxxx",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "delete_flg": "0",
            "ID": 1001,
            "IaaS_network_id": 'network_id_00001',
            "IaaS_port_id": 'IaaS_port_id_00001',
            "IaaS_subnet_id": 'subnet_id_00001',
            "IaaS_subnet_id_v6": '',
            "port_id": "port_id_00001",
            "ip_address": "10.58.79.45",
            "ip_address_v6": "",
            "nic": "ethernet1/11.2"
        },
        {
            "create_id": "xxxxxxx",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "delete_flg": "0",
            "ID": 1002,
            "IaaS_network_id": 'network_id_00002',
            "IaaS_port_id": 'IaaS_port_id_00002',
            "IaaS_subnet_id": 'subnet_id_00002',
            "IaaS_subnet_id_v6": '',
            "port_id": "port_id_00002",
            "ip_address": "10.50.79.190",
            "ip_address_v6": "",
            "nic": "ethernet1/11.2"
        }
    ]
}

NODE_DATA_PLB = {
    "pnf_info": [
        {
            "ID": 125,
            "apl_type": "2",
            "type": "2",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx9",
            "node_name": "nal_plb1",
            "pod_id": "podid",
            "task_status": "1",
            "IaaS_tenant_id": "tenant_name",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "redundant_configuration_flg": "1",
            "device_name_master": "master_name",
            "actsby_flag_master": "act",
            "device_detail_master": "{}",
            "master_ip_address": "10.58.79.178",
            "master_MSA_device_id": "xxx-xxx-xxxx",
            "device_name_slave": "slave_name",
            "device_detail_slave": "{}",
            "actsby_flag_slave": "sby",
            "slave_ip_address": "127.0.0.1",
            "slave_MSA_device_id": "xxx-xxx-xxxx"
        }
    ],
    "port_info": [
        {
            "create_id": "xxxxxxx",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "delete_flg": "0",
            "ID": 1002,
            "IaaS_network_id": 'network_id_00002',
            "IaaS_port_id": 'IaaS_port_id_00002',
            "IaaS_subnet_id": 'subnet_id_00002',
            "IaaS_subnet_id_v6": '',
            "port_id": "port_id_00002",
            "ip_address": "10.50.79.191",
            "ip_address_v6": "",
            "nic": "ethernet1/11.2"
        }
    ]
}

NODE_DATA_NO_NET = {
    "vnf_info": [
        {
            "ID": 126,
            "apl_type": "1",
            "type": "2",
            "device_type": "1",
            "create_date": "xxxx-xx-xx xx:xx:xx",
            "create_id": "xxxxxxx",
            "delete_flg": "0",
            "node_detail": "[]",
            "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx5",
            "node_name": "nal_vlb1",
            "pod_id": "podid",
            "task_status": "1",
            "IaaS_tenant_id": "tenant_name",
            "update_date": "xxxx-xx-xx xx:xx:xx",
            "update_id": "xxxxxxx"
        }
    ],
    "port_info": []
}


"""Catalog id"""
CATALOG_ID = "100"
