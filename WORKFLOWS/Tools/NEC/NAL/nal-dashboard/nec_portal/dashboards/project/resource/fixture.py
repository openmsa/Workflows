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


RESOURCE_DATA_LIST = {
    "contract_info": [
        {
            "contract_kind": "1",
            "apl_type": "",
            "type": "",
            "device_type": "",
            "contract_cnt": "5",
            "use_cnt": "3",
            "redundant_configuration_flg": "",
            "ID": "1"
        },
        {
            "contract_kind": "2",
            "apl_type": "1",
            "type": "1",
            "device_type": "3",
            "contract_cnt": "10",
            "use_cnt": "5",
            "redundant_configuration_flg": "",
            "ID": "2"
        },
        {
            "contract_kind": "2",
            "apl_type": "2",
            "type": "1",
            "device_type": "1",
            "contract_cnt": "10",
            "use_cnt": "5",
            "redundant_configuration_flg": "0",
            "ID": "3"
        },
        {
            "contract_kind": "3",
            "apl_type": "1",
            "type": "3",
            "device_type": "2",
            "contract_cnt": "10",
            "use_cnt": "5",
            "redundant_configuration_flg": "",
            "ID": "4"
        }
    ]
}

"""resource detail data
RESOURCE_DATA_GLOBALIP
RESOURCE_DATA_VNF
RESOURCE_DATA_PNF
RESOURCE_DATA_ROUTER
"""

RESOURCE_DATA_GLOBALIP = {
    "contract_info": [
        {
            "ID": "133",
            "use_status": "1",
            "node_id": "118",
            "node_name": "VFW001",
            "tenant_name": "tenant_name1",
            "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
            "globalip": "198.169.3.1"
        },
        {
            "ID": "134",
            "use_status": "1",
            "node_id": "119",
            "node_name": "VFW002",
            "tenant_name": "tenant_name1",
            "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
            "globalip": "198.169.3.2"
        },
        {
            "ID": "135",
            "use_status": "0",
            "node_id": "",
            "node_name": "",
            "tenant_name": "",
            "IaaS_tenant_id": "",
            "globalip": "198.169.3.3"
        }
    ]
}

RESOURCE_DATA_VNF = {
    "contract_info": [
        {
            "node_id": "553415d8-f2ea-4c23-8cf7-11c41c000001",
            "node_name": "VFW001",
            "task_status": "1",
            "tenant_name": "tenant_name1",
            "ID": "67",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "use_status": "1"
        },
        {
            "node_id": "553415d8-f2ea-4c23-8cf7-11c41c000002",
            "node_name": "VFW002",
            "task_status": "1",
            "tenant_name": "tenant_name1",
            "ID": "69",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "use_status": "1"
        },
        {
            "node_id": "",
            "node_name": "",
            "task_status": "",
            "tenant_name": "tenant_name1",
            "ID": "",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "use_status": "0"
        }
    ]
}

RESOURCE_DATA_PNF = {
    "contract_info": [
        {
            "node_id": "553415d8-f2ea-4c23-8cf7-11c41c000001",
            "node_name": "PFW001",
            "task_status": "1",
            "tenant_name": "tenant_name1",
            "ID": "67",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "use_status": "1"
        },
        {
            "node_id": "553415d8-f2ea-4c23-8cf7-11c41c000002",
            "node_name": "PFW002",
            "task_status": "1",
            "tenant_name": "tenant_name1",
            "ID": "69",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "use_status": "1"
        },
        {
            "node_id": "",
            "node_name": "",
            "task_status": "",
            "tenant_name": "tenant_name1",
            "ID": "",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "use_status": "0"
        }
    ]
}

RESOURCE_DATA_ROUTER = {
    "contract_info": [
        {
            "group_id": "81eb81d5-72b5-420a-86ff-d3e6a05d7667",
            "group_type": "1",
            "group_name": "dcconnect1",
            "tenant_name": "tenant_name1",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "ID": "56",
            "task_status": 1,
            "use_status": 1
        },
        {
            "group_id": "",
            "group_type": "",
            "group_name": "",
            "tenant_name": "tenant_name1",
            "IaaS_tenant_id": "a0d58ee41a364026a1031aca2548fd03",
            "ID": "",
            "task_status": "",
            "use_status": 0
        }
    ]
}

NODE_DATA_LIST = [
    {
        "ID": "117",
        "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
        "apl_type": "1",
        "create_date": "xxxx-xx-xx xx:xx:xx",
        "create_id": "xxxxxxx",
        "delete_flg": "0",
        "device_type": "1",
        "node_detail": "[]",
        "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx1",
        "node_name": "nal_vlb1",
        "pod_id": "podid",
        "task_status": "1",
        "type": "2",
        "update_date": "xxxx-xx-xx xx:xx:xx",
        "update_id": "xxxxxxx"
    },
    {
        "ID": "118",
        "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
        "apl_type": "1",
        "create_date": "xxxx-xx-xx xx:xx:xx",
        "create_id": "xxxxxxx",
        "delete_flg": "0",
        "device_type": "1",
        "node_detail": "[]",
        "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx2",
        "node_name": "nal_vlb2",
        "pod_id": "podid",
        "task_status": "1",
        "type": "2",
        "update_date": "xxxx-xx-xx xx:xx:xx",
        "update_id": "xxxxxxx"
    },
    {
        "ID": "119",
        "IaaS_tenant_id": "bdb8f50f82da4370813e6ea797b1fb87",
        "apl_type": "2",
        "create_date": "xxxx-xx-xx xx:xx:xx",
        "create_id": "xxxxxxx",
        "delete_flg": "0",
        "device_type": "1",
        "node_detail": "[]",
        "node_id": "xxxxx-xxxxx-xxxxx-xxxxx-xxxx3",
        "node_name": "nal_vfw1",
        "pod_id": "podid",
        "task_status": "1",
        "type": "1",
        "update_date": "xxxx-xx-xx xx:xx:xx",
        "update_id": "xxxxxxx"
    },
    {
        "ID": "120",
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
