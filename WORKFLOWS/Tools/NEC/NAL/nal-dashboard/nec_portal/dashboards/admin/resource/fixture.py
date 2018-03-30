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


"""Resource data list
RESOURCE_DATA_LIST[0], ID:1, globalip
RESOURCE_DATA_LIST[1], ID:2, license(Node)
RESOURCE_DATA_LIST[2], ID:3, license(Service)
RESOURCE_DATA_LIST[3], ID:4, pnf
RESOURCE_DATA_LIST[4], ID:5, msa-vlan
RESOURCE_DATA_LIST[5], ID:6, wan-vlan
RESOURCE_DATA_LIST[6], ID:7, cpu_list
RESOURCE_DATA_LIST[7], ID:8, memory-list
RESOURCE_DATA_LIST[8], ID:9, storage-list
"""

RESOURCE_DATA_LIST = {
    "contract_info": [
        {
            "nw_resource_kind": "1",
            "type": "",
            "device_type": "",
            "type_detail": "",
            "quota": "30",
            "contract_cnt": "5",
            "use_cnt": "3",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "",
            "ID": "1"
        },
        {
            "nw_resource_kind": "2",
            "type": "1",
            "device_type": "3",
            "type_detail": "1",
            "quota": "30",
            "contract_cnt": "10",
            "use_cnt": "5",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "",
            "ID": "2"
        },
        {
            "nw_resource_kind": "2",
            "type": "3",
            "device_type": "2",
            "type_detail": "2",
            "quota": "30",
            "contract_cnt": "10",
            "use_cnt": "5",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "",
            "ID": "3"
        },
        {
            "nw_resource_kind": "3",
            "type": "1",
            "device_type": "2",
            "type_detail": "",
            "quota": "30",
            "contract_cnt": "10",
            "use_cnt": "5",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "0",
            "ID": "4"
        },
        {
            "nw_resource_kind": "4",
            "type": "",
            "device_type": "",
            "type_detail": "",
            "quota": "30",
            "contract_cnt": "10",
            "use_cnt": "5",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "",
            "ID": "5"
        },
        {
            "nw_resource_kind": "5",
            "type": "",
            "device_type": "",
            "type_detail": "",
            "quota": "30",
            "contract_cnt": "10",
            "use_cnt": "5",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "",
            "ID": "6"
        },
        {
            "nw_resource_kind": "6",
            "type": "",
            "device_type": "",
            "type_detail": "1",
            "quota": "30",
            "contract_cnt": "10",
            "use_cnt": "5",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "",
            "ID": "7"
        },
        {
            "nw_resource_kind": "7",
            "type": "",
            "device_type": "",
            "type_detail": "1",
            "quota": "30",
            "contract_cnt": "10",
            "use_cnt": "5",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "",
            "ID": "8"
        },
        {
            "nw_resource_kind": "8",
            "type": "",
            "device_type": "",
            "type_detail": "1",
            "quota": "30",
            "contract_cnt": "10",
            "use_cnt": "5",
            "threshold": "10",
            "unavailable_cnt": "0",
            "redundant_configuration_flg": "",
            "ID": "9"
        },
    ]
}

"""resource detail data
RESOURCE_DATA_GLOBALIP
RESOURCE_DATA_LICENSE
RESOURCE_DATA_PNF
RESOURCE_DATA_MSA_VLAN
RESOURCE_DATA_WAN_VLAN
RESOURCE_DATA_POD_LIST
RESOURCE_DATA_POD_DETAIL
"""

RESOURCE_DATA_GLOBALIP = {
    "contract_info": [
        {
            "node_id": "553415d8-f2ea-4c23-8cf7-11c41c000001",
            "node_name": "VFW001",
            "task_status": "202",
            "tenant_name": "tenant_name1",
            "IaaS_tenant_id": "aaa8f50f82da4370813e6ea797b1fb87",
            "globalip": "198.169.3.1",
            "ID": "1",
            "use_status": "1"
        },
        {
            "node_id": "553415d8-f2ea-4c66-8cf7-11c41c000101",
            "node_name": "VFW101",
            "task_status": "201",
            "tenant_name": "tenant_name2",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "globalip": "198.169.5.10",
            "ID": "5",
            "use_status": "1",
        },
        {
            "node_id": "",
            "node_name": "",
            "task_status": "",
            "tenant_name": "tenant_name2",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "globalip": "198.169.5.13",
            "ID": "",
            "use_status": "0"
        },
    ],
    "total_info": {
        "quota": "40",
        "contract_cnt": "15",
        "use_cnt": "5",
        "unavailable_cnt": "0"
    }
}

RESOURCE_DATA_LICENSE = {
    "contract_info": [
        {
            "contract_cnt": "5",
            "use_cnt": "2",
            "ID": "1",
            "IaaS_tenant_id": "aaa8f50f82da4370813e6ea797b1fb87",
            "tenant_name": "tenant_name1"
        },
        {
            "contract_cnt": "10",
            "use_cnt": "12",
            "ID": "1",
            "IaaS_tenant_id": "aaa8f50f82da4370813e6ea797b1fb87",
            "tenant_name": "tenant_name2"
        }
    ],
    "total_info": {
        "quota": "40",
        "contract_cnt": "15",
        "use_cnt": "5",
        "unavailable_cnt": "0"
    }
}

RESOURCE_DATA_PNF = {
    "contract_info": [
        {
            "node_id": "553415d8-f2ea-4c23-8cf7-11c41c000001",
            "node_name": "VFW001",
            "tenant_name": "tenant_name1",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "device_user_name": "Palo_phy_share_01_1",
            "ID": "68",
            "task_status": "1",
            "use_status": "1"
        },
        {
            "node_id": "553415d8-f2ea-4c23-8cf7-11c41c000002",
            "node_name": "VFW002",
            "tenant_name": "tenant_name1",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "device_user_name": "Palo_phy_share_01_2",
            "ID": "154",
            "task_status": "1",
            "use_status": "1"
        },
        {
            "node_id": "5346f5d8-f2ea-4c23-8cf7-11c41c5fa201",
            "node_name": "VFW101",
            "tenant_name": "tenant_name2",
            "IaaS_tenant_id": "aaa8f50f82da4370813e6ea797b1fb87",
            "device_user_name": "Palo_phy_share_10_2",
            "ID": "214",
            "task_status": "1",
            "use_status": "1"
        }
    ],
    "total_info": {
        "quota": "40",
        "contract_cnt": "15",
        "use_cnt": "5",
        "unavailable_cnt": "0"
    }
}

RESOURCE_DATA_MSA_VLAN = {
    "contract_info": [
        {
            "vlan_id": "801",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "tenant_name": "tenant_name1",
            "task_status": "1",
            "ID": "1",
            "use_status": "1"
        },
        {
            "vlan_id": "802",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "tenant_name": "tenant_name2",
            "task_status": "1",
            "ID": "6",
            "use_status": "1"
        },
        {
            "vlan_id": "803",
            "IaaS_tenant_id": "",
            "tenant_name": "",
            "task_status": "",
            "ID": "18",
            "use_status": "0"
        }
    ],
    "total_info": {
        "quota": "10",
        "contract_cnt": "2",
        "use_cnt": "1",
        "unavailable_cnt": "0"
    }
}

RESOURCE_DATA_WAN_VLAN = {
    "contract_info": [
        {
            "vlan_id": "801",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "tenant_name": "tenant_name1",
            "task_status": "1",
            "ID": "1",
            "use_status": "1"
        },
        {
            "vlan_id": "802",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "tenant_name": "tenant_name2",
            "task_status": "1",
            "ID": "6",
            "use_status": "1"
        },
        {
            "vlan_id": "803",
            "IaaS_tenant_id": "",
            "tenant_name": "",
            "task_status": "",
            "ID": "18",
            "use_status": "0"
        }
    ],
    "total_info": {
        "quota": "10",
        "contract_cnt": "2",
        "use_cnt": "1",
        "unavailable_cnt": "0"
    }
}

RESOURCE_DATA_POD_LIST = {
    "contract_info": [
        {
            "pod_id": "pod0001",
            "quota": "20",
            "use_cnt": "5"
        },
        {
            "pod_id": "pod0002",
            "quota": "20",
            "use_cnt": "10"
        }
    ],
    "total_info": {
        "quota": "40",
        "contract_cnt": "15",
        "use_cnt": "5",
    }
}

RESOURCE_DATA_POD_DETAIL = {
    "contract_info": [
        {
            "tenant_id": "37db35eebab948e3a5431ffec38b6cd8",
            "use_cnt": "1",
            "contract_cnt": "100",
            "IaaS_tenant_id": "ccc8f50f82da4370813e6ea797b1fb87",
            "tenant_name": "admin1"
        },
        {
            "tenant_id": "37db35eebab948e3a5431ffec38b6cd8",
            "use_cnt": "1",
            "contract_cnt": "100",
            "IaaS_tenant_id": "bbb8f50f82da4370813e6ea797b1fb87",
            "tenant_name": "admin2"
        }
    ],
    "total_info": {
        "quota": "5000",
        "contract_cnt": "5000",
        "use_cnt": "500"
    }
}
