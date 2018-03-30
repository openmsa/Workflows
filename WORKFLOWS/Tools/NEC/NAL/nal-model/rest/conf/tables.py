# -*- coding: utf-8 -*-

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

# Table Definition

# NAL_POD_MNG define
NAL_POD_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'pod_id': {'type': 'VARCHAR', 'size': '64', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'use_type',
        'ops_version',
        'weight',
        'region_id',
    ]
}
# NAL_VXLANGW_POD_MNG define
NAL_VXLANGW_POD_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'vxlangw_pod_id': {'type': 'VARCHAR', 'size': '64', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'IaaS_region_id',
        'weight'
    ]
}
# NAL_TENANT_MNG define
NAL_TENANT_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'tenant_name': {'type': 'VARCHAR', 'size': '64', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'IaaS_region_id',
        'IaaS_tenant_id',
        'tenant_info'
    ]
}
# NAL_VIRTUAL_LAN_MNG define
NAL_VIRTUAL_LAN_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'network_id': {'type': 'VARCHAR', 'size': '64', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'tenant_name',
        'pod_id',
        'tenant_id',
        'IaaS_region_id',
        'IaaS_tenant_id',
        'IaaS_network_id',
        'IaaS_network_type',
        'IaaS_segmentation_id',
        'vlan_id',
        'vxlangw_pod_id',
        'rule_id',
        'nal_vlan_info'
    ]
}
# NAL_PORT_MNG define
NAL_PORT_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'port_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'tenant_name',
        'pod_id',
        'tenant_id',
        'network_id',
        'network_type',
        'network_type_detail',
        'apl_type',
        'node_id',
        'apl_table_rec_id',
        'IaaS_region_id',
        'IaaS_tenant_id',
        'IaaS_network_id',
        'IaaS_subnet_id',
        'IaaS_subnet_id_v6',
        'IaaS_port_id',
        'nic',
        'ip_address',
        'netmask',
        'ip_address_v6',
        'netmask_v6',
        'port_info',
        'msa_info'
    ]
}
# NAL_APL_MNG define
NAL_APL_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'node_id': {'type': 'VARCHAR', 'size': '64', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'tenant_name',
        'pod_id',
        'tenant_id',
        'apl_type',
        'type',
        'device_type',
        'default_gateway',
        'dns_server_ip_address',
        'ntp_server_ip_address',
        'snmp_server_ip_address',
        'syslog_server_ip_address',
        'global_ip',
        'task_status',
        'err_info',
        'description',
        'node_name',
        'node_detail',
        'MSA_device_id',
        'server_id',
        'server_info',
        'device_user_name',
        'status',
        'redundant_configuration_flg',
        'device_name_master',
        'actsby_flag_master',
        'device_detail_master',
        'master_ip_address',
        'master_MSA_device_id',
        'device_name_slave',
        'actsby_flag_slave',
        'device_detail_slave',
        'slave_ip_address',
        'slave_MSA_device_id',
        'nic_MSA',
        'nic_public',
        'nic_external',
        'nic_tenant',
        'partition_id_seq',
        'vsys_id_seq',
    ]
}
# NAL_THRESHOLD_MNG define
NAL_THRESHOLD_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'nw_resource_kind',
        'type',
        'device_type',
        'redundant_configuration_flg',
        'type_detail',
        'threshold'
    ]
}
# NAL_TENANT_CONTRACT_MNG define
NAL_TENANT_CONTRACT_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'tenant_name',
        'contract_kind',
        'apl_type',
        'type',
        'device_type',
        'redundant_configuration_flg',
        'type_detail_info',
        'contract'
    ]
}
# NAL_MSA_VLAN_MNG define
NAL_MSA_VLAN_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'pod_id',
        'vlan_id',
        'network_address',
        'netmask',
        'msa_ip_address',
        'status',
        'tenant_name',
        'tenant_id',
        'network_id',
        'subnet_id',
        'port_id',
        'network_info',
        'subnet_info',
        'port_info'
    ]
}
# NAL_PNF_VLAN_MNG define
NAL_PNF_VLAN_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'pod_id',
        'vlan_id',
        'status',
        'tenant_name',
        'tenant_id',
        'network_id',
        'subnet_id',
        'port_id',
        'rule_id'
    ]
}
# NAL_GLOBAL_IP_MNG define
NAL_GLOBAL_IP_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'global_ip': {'type': 'VARCHAR', 'size': '15', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'status',
        'node_id',
        'tenant_name'
    ]
}
# NAL_LICENSE_MNG define
NAL_LICENSE_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'license': {'type': 'VARCHAR', 'size': '256', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'type',
        'device_type',
        'type_detail',
        'status',
        'tenant_name',
        'node_id',
        'description'
    ]
}
# NAL_DEVICE_ENDPOINT_MNG define
NAL_DEVICE_ENDPOINT_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'type',
        'dc_id',
        'region_id',
        'pod_id',
        'endpoint_info'
    ]
}
# NAL_CONFIG_MNG define
NAL_CONFIG_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'type',
        'dc_id',
        'region_id',
        'pod_id',
        'config_info'
    ]
}
# WIM_DC_MNG define
WIM_DC_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'dc_id': {'type': 'VARCHAR', 'size': '64', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'dc_name',
        'dc_number'
    ]
}
# WIM_DC_CONNECT_GROUP_MNG define
WIM_DC_CONNECT_GROUP_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'group_id': {'type': 'VARCHAR', 'size': '64', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'group_type',
        'group_name',
        'tenant_name',
        'IaaS_tenant_id',
        'task_status',
        'err_info'
    ]
}
# WIM_DC_VLAN_MNG define
WIM_DC_VLAN_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'dc_id',
        'pod_id',
        'vlan_id',
        'status',
        'group_id'
    ]
}
# WIM_DC_CONNECT_MEMBER_MNG define
WIM_DC_CONNECT_MEMBER_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'group_id',
        'dc_id',
        'tenant_name',
        'pod_id',
        'tenant_id',
        'IaaS_region_id',
        'IaaS_tenant_id',
        'IaaS_network_type',
        'IaaS_network_id',
        'IaaS_network_name',
        'IaaS_subnet_id',
        'IaaS_subnet_id_v6',
        'IaaS_segmentation_id',
        'wan_network_id',
        'bandwidth',
        'default_gateway',
        'vrrp_address',
        'vrrp_address_v6',
        'ce1_address',
        'ce1_address_v6',
        'ce2_address',
        'ce2_address_v6',
        'ce1_info',
        'ce2_info',
        'ce1_node_id',
        'ce2_node_id'
    ]
}
# WIM_DEVICE_ENDPOINT_MNG define
WIM_DEVICE_ENDPOINT_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'type',
        'dc_id',
        'region_id',
        'pod_id',
        'endpoint_info'
    ]
}
# WIM_CONFIG_MNG define
WIM_CONFIG_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'type',
        'dc_id',
        'region_id',
        'pod_id',
        'config_info'
    ]
}
# WIM_DC_SEGMENT_MNG define
WIM_DC_SEGMENT_MNG = {
    'columns': {
        'create_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'create_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'update_id': {'type': 'VARCHAR', 'size': '64', 'notnull': False},
        'update_date': {'type': 'DATETIME', 'size': '', 'notnull': False},
        'delete_flg': {'type': 'DECIMAL', 'size': '1', 'notnull': True},
        'ID': {'type': 'INT', 'size': '', 'notnull': True},
        'extension_info': {'type': 'TEXT', 'size': '', 'notnull': False}
    },
    'primaryKey': [
        'ID'
    ],
    'extension_columns': [
        'dc_id',
        'ce01_ip_address',
        'ce02_ip_address',
        'network_address',
        'netmask',
        'next_hop',
        'status',
        'group_id'
    ]
}
