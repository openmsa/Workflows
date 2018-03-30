from django.utils.translation import ugettext_lazy as _

NAL_ENDPOINT = 'http://10.169.11.12'

NAL_ID_PASSWORD = 'u_nal:nal@admin'

ENV_NO_TUNNELING = 'normal'
ENV_TUNNRLING_ENCRYPTED = 'tunneling_encrypted'
ENV_TUNNRLING_UNENCRYPTED = 'tunneling_unencrypted'

NAL_CONSTRUCT_SERVICE_TYPE = ENV_NO_TUNNELING

# Mapping of APL_TYPE value and name
APL_TYPE_MAPPING = {
    '1': 'Virtual',
    '2': 'Physical'
}

# Mapping of TYPE value and name
TYPE_MAPPING = {
    '1': 'Firewall',
    '2': 'Load Balancer'
}

# Mapping of APL_TYPE and TYPE and Function_type
NODE_FUNCTION_TYPE_MAPPING = {
    '1': {
        '1': 'vfw',
        '2': 'vlb'
    },
    '2': {
        '1': 'pfw',
        '2': 'plb'
    }
}

# Mapping of DEVICE_TYPE value and name
DEVICE_TYPE_MAPPING = {
    'vfw': {
        '1': 'InterSecVM/SG(Ext)',
        '2': 'FortiGateVM(5.2.4)',
        '3': 'PaloAltoVM',
        '4': 'InterSecVM/SG(Pub)',
        '5': 'FortiGateVM(5.4.1)'
    },
    'vlb': {
        '1': 'InterSecVM/LB',
        '2': 'BIG-IP VE',
        '3': 'vThunder(4.0.1)',
        '4': 'vThunder(4.1.1)'
    },
    'pfw': {
        '1': 'FortiGate',
        '2': 'PaloAlto',
        '3': 'FortiGate Shared',
        '4': 'PaloAlto Shared'
    },
    'plb': {
        '1': 'BIG-IP',
        '2': 'Thunder',
        '3': 'BIG-IP Shared',
        '4': 'Thunder Shared'
    }
}

# Mapping of STATUS value and name
STATUS_MAPPING = {
    '0': _('Build'),
    '1': _('Active'),
    '2': _('No License'),
    '9': _('Error')
}

# Mapping of STATUS value and name
TASK_MAPPING = {
    '0': _('Spawning'),
    '1': _('None'),
    '2': _('None'),
    '9': _('None')
}

# Mapping of NETWORK_TYPE value and name
NETWORK_TYPE_MAPPING = {
    '1': 'Tenant',
    '2': 'External',
    '3': 'Public',
    '4': 'MSA',
    '5': 'WAN'
}

# Mapping of Redundant Config value and name
REDUNDANT_CONFIG_MAPPING = {
    '0': 'Redundancy',
    '1': 'Single'
}

# Mapping of NETWORK_NAME value and name
NETWORK_NAME_MAPPING = {
    '2': 'Ext',
    '3': 'Pub',
    '4': 'MSA'
}

# Shaping of API response
NODE_RETURN_MAPPING = {
    'all_node': {
        'Virtual': {
            'id': 'ID',
            'node_id': 'node_id',
            'name': 'node_name',
            'apl_type': 'apl_type',
            'type': 'type',
            'device_type': 'device_type',
            'task_status': 'task_status',
            'tenant_id': 'IaaS_tenant_id'
        },
        'Physical': {
            'id': 'ID',
            'node_id': 'node_id',
            'name': 'device_user_name',
            'apl_type': 'apl_type',
            'type': 'type',
            'device_type': 'device_type',
            'task_status': 'task_status',
            'tenant_id': 'IaaS_tenant_id'
        }
    },
    'vfw': {
        'vnf_info': {
            'id': 'ID',
            'node_id': 'node_id',
            'name': 'node_name',
            'apl_type': 'apl_type',
            'type': 'type',
            'device_type': 'device_type',
            'device_id': 'MSA_device_id',
            'task_status': 'task_status',
            'default_gateway': 'default_gateway',
            'global_ip': 'global_ip',
            'redundant_configuration_flg': 'redundant_configuration_flg',
            'description': 'description',
            'tenant_id': 'IaaS_tenant_id'
        },
        'port_info': {
            'network_type_detail': 'network_type_detail',
            'IaaS_network_id': 'IaaS_network_id',
            'IaaS_subnet_id': 'IaaS_subnet_id',
            'IaaS_subnet_id_v6': 'IaaS_subnet_id_v6',
            'IaaS_port_id': 'IaaS_port_id',
            'ip_address': 'ip_address',
            'ip_address_v6': 'ip_address_v6',
            'port_id': 'port_id',
            'port_info': 'port_info',
            'nic': 'nic'
        }
    },
    'vlb': {
        'vnf_info': {
            'id': 'ID',
            'node_id': 'node_id',
            'name': 'node_name',
            'apl_type': 'apl_type',
            'type': 'type',
            'device_type': 'device_type',
            'device_id': 'MSA_device_id',
            'task_status': 'task_status',
            'default_gateway': 'default_gateway',
            'global_ip': 'global_ip',
            'redundant_configuration_flg': 'redundant_configuration_flg',
            'description': 'description',
            'tenant_id': 'IaaS_tenant_id'
        },
        'port_info': {
            'network_type_detail': 'network_type_detail',
            'IaaS_network_id': 'IaaS_network_id',
            'IaaS_subnet_id': 'IaaS_subnet_id',
            'IaaS_subnet_id_v6': 'IaaS_subnet_id_v6',
            'IaaS_port_id': 'IaaS_port_id',
            'ip_address': 'ip_address',
            'ip_address_v6': 'ip_address_v6',
            'port_id': 'port_id',
            'port_info': 'port_info',
            'nic': 'nic'
        }
    },
    'pfw': {
        'pnf_info': {
            'id': 'ID',
            'node_id': 'node_id',
            'name': 'device_user_name',
            'apl_type': 'apl_type',
            'type': 'type',
            'device_type': 'device_type',
            'task_status': 'task_status',
            'default_gateway': 'default_gateway',
            'global_ip': 'global_ip',
            'redundant_configuration_flg': 'redundant_configuration_flg',
            'description': 'description',
            'device_name_master': 'device_name_master',
            'actsby_flag_master': 'actsby_flag_master',
            'master_ip_address': 'master_ip_address',
            'master_MSA_device_id': 'master_MSA_device_id',
            'device_name_slave': 'device_name_slave',
            'actsby_flag_slave': 'actsby_flag_slave',
            'slave_ip_address': 'slave_ip_address',
            'slave_MSA_device_id': 'slave_MSA_device_id',
            'tenant_id': 'IaaS_tenant_id'
        },
        'port_info': {
            'network_type_detail': 'network_type_detail',
            'IaaS_network_id': 'IaaS_network_id',
            'IaaS_subnet_id': 'IaaS_subnet_id',
            'IaaS_subnet_id_v6': 'IaaS_subnet_id_v6',
            'IaaS_port_id': 'IaaS_port_id',
            'ip_address': 'ip_address',
            'ip_address_v6': 'ip_address_v6',
            'port_id': 'port_id',
            'port_info': 'port_info',
            'nic': 'nic'
        }
    },
    'plb': {
        'pnf_info': {
            'id': 'ID',
            'node_id': 'node_id',
            'name': 'device_user_name',
            'apl_type': 'apl_type',
            'type': 'type',
            'device_type': 'device_type',
            'task_status': 'task_status',
            'default_gateway': 'default_gateway',
            'global_ip': 'global_ip',
            'redundant_configuration_flg': 'redundant_configuration_flg',
            'description': 'description',
            'device_name_master': 'device_name_master',
            'actsby_flag_master': 'actsby_flag_master',
            'master_ip_address': 'master_ip_address',
            'master_MSA_device_id': 'master_MSA_device_id',
            'device_name_slave': 'device_name_slave',
            'actsby_flag_slave': 'actsby_flag_slave',
            'slave_ip_address': 'slave_ip_address',
            'slave_MSA_device_id': 'slave_MSA_device_id',
            'tenant_id': 'IaaS_tenant_id'
        },
        'port_info': {
            'network_type_detail': 'network_type_detail',
            'IaaS_network_id': 'IaaS_network_id',
            'IaaS_subnet_id': 'IaaS_subnet_id',
            'IaaS_subnet_id_v6': 'IaaS_subnet_id_v6',
            'IaaS_port_id': 'IaaS_port_id',
            'ip_address': 'ip_address',
            'ip_address_v6': 'ip_address_v6',
            'port_id': 'port_id',
            'port_info': 'port_info',
            'nic': 'nic'
        }
    }
}

# Action buttons that can be displayed in a node display
NODE_ALL_BUTTONS = [
    'UpdateAddPortLink',
    'UpdateLicenseLink',
    'DeleteNodeAction',
    'UpdateNetworkV6Link',
    'DeleteNetworkAction'
]

# Conditions to display a button for admin or project
NODE_DISPLAY_BUTTONS_FOR_USER = {
    'admin': ['UpdateLicenseLink'],
    'project': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link', 'DeleteNetworkAction'],
}

# Conditions to display a button for node or network
NODE_DISPLAY_BUTTONS_FOR_CLASS = {
    'node': ['UpdateAddPortLink', 'UpdateLicenseLink', 'DeleteNodeAction'],
    'network': ['UpdateNetworkV6Link', 'DeleteNetworkAction'],
}

# Conditions to display a button for each device
NODE_DISPLAY_BUTTONS_FOR_DEVICE = {
    'InterSecVM/SG(Ext)': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link', 'DeleteNetworkAction'],
    'FortiGateVM(5.2.4)': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link'],
    'PaloAltoVM': ['UpdateAddPortLink', 'UpdateLicenseLink', 'DeleteNodeAction', 'UpdateNetworkV6Link'],
    'InterSecVM/SG(Pub)': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link', 'DeleteNetworkAction'],
    'FortiGateVM(5.4.1)': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link'],
    'InterSecVM/LB': ['DeleteNodeAction', 'UpdateNetworkV6Link'],
    'BIG-IP VE': ['DeleteNodeAction', 'UpdateNetworkV6Link'],
    'vThunder(4.0.1)': ['UpdateLicenseLink', 'DeleteNodeAction', 'UpdateNetworkV6Link'],
    'vThunder(4.1.1)': ['UpdateLicenseLink', 'DeleteNodeAction', 'UpdateNetworkV6Link'],
    'FortiGate': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link', 'DeleteNetworkAction'],
    'PaloAlto': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link', 'DeleteNetworkAction'],
    'FortiGate Shared': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link', 'DeleteNetworkAction'],
    'PaloAlto Shared': ['UpdateAddPortLink', 'DeleteNodeAction', 'UpdateNetworkV6Link', 'DeleteNetworkAction'],
    'BIG-IP': ['DeleteNodeAction', 'UpdateNetworkV6Link'],
    'Thunder': ['DeleteNodeAction', 'UpdateNetworkV6Link'],
    'BIG-IP Shared': ['DeleteNodeAction', 'UpdateNetworkV6Link'],
    'Thunder Shared': ['DeleteNodeAction', 'UpdateNetworkV6Link']
}

# Conditions to display a button for each status
NODE_DISPLAY_BUTTONS_FOR_STATUS = {
    '0': [],
    '1': ['UpdateAddPortLink','DeleteNodeAction', 'UpdateNetworkV6Link', 'DeleteNetworkAction'],
    '2': ['UpdateLicenseLink', 'DeleteNodeAction'],
    '9': ['DeleteNodeAction']
}

# Information to be displayed on the detail screen of the node
PROJECT_NODE_DETAIL_DISPLAY_COLUMNS = {
    'vfw': {
        'title': 'Virtual Firewall:',
        'detail': [
            ['Name', 'name'],
            ['ID', 'node_id'],
            ['Apl Type', 'apl_type'],
            ['Type', 'type'],
            ['Device Type', 'device_type'],
            ['Status', 'task_status'],
            ['Default Gateway', 'default_gateway', '-'],
            ['Global IP', 'global_ip', '-'],
            ['Redundant Config', 'redundant_configuration_flg', '-'],
            ['Description', 'description', '-']
        ],
        'detail_name': 'vnf_info',
        'network_name': 'port_info'
    },
    'vlb': {
        'title': 'Virtual Loadbalancer:',
        'detail': [
            ['Name', 'name'],
            ['ID', 'node_id'],
            ['Apl Type', 'apl_type'],
            ['Type', 'type'],
            ['Device Type', 'device_type'],
            ['Status', 'task_status'],
            ['Default Gateway', 'default_gateway', '-'],
            ['Global IP', 'global_ip', '-'],
            ['Redundant Config', 'redundant_configuration_flg', '-'],
            ['Description', 'description', '-']
        ],
        'detail_name': 'vnf_info',
        'network_name': 'port_info'
    },
    'pfw': {
        'title': 'Physical Firewall:',
        'detail': [
            ['Name', 'name'],
            ['ID', 'node_id'],
            ['Apl Type', 'apl_type'],
            ['Type', 'type'],
            ['Device Type', 'device_type'],
            ['Status', 'task_status'],
            ['Default Gateway', 'default_gateway', '-'],
            ['Global IP', 'global_ip', '-'],
            ['Redundant Config', 'redundant_configuration_flg', '-'],
            ['Description', 'description', '-']
        ],
        'detail_name': 'pnf_info',
        'network_name': 'port_info'
    },
    'plb': {
        'title': 'Physical Loadbalancer:',
        'detail': [
            ['Name', 'name'],
            ['ID', 'node_id'],
            ['Apl Type', 'apl_type'],
            ['Type', 'type'],
            ['Device Type', 'device_type'],
            ['Status', 'task_status'],
            ['Default Gateway', 'default_gateway', '-'],
            ['Global IP', 'global_ip', '-'],
            ['Redundant Config', 'redundant_configuration_flg', '-'],
            ['Description', 'description', '-']
        ],
        'detail_name': 'pnf_info',
        'network_name': 'port_info'
    }
}
# Information to be displayed on the detail screen of the node
ADMIN_NODE_DETAIL_DISPLAY_COLUMNS = {
    'vfw': {
        'title': 'Virtual Firewall:',
        'detail': [
            ['Tenant Name', 'tenant_id'],
            ['Name', 'name'],
            ['ID', 'node_id'],
            ['Apl Type', 'apl_type'],
            ['Type', 'type'],
            ['Device Type', 'device_type'],
            ['Device ID', 'device_id'],
            ['Status', 'task_status'],
            ['Default Gateway', 'default_gateway', '-'],
            ['Global IP', 'global_ip', '-'],
            ['Redundant Config', 'redundant_configuration_flg', '-'],
            ['Description', 'description', '-']
        ],
        'detail_name': 'vnf_info',
        'network_name': 'port_info'
    },
    'vlb': {
        'title': 'Virtual Loadbalancer:',
        'detail': [
            ['Tenant Name', 'tenant_id'],
            ['Name', 'name'],
            ['ID', 'node_id'],
            ['Apl Type', 'apl_type'],
            ['Type', 'type'],
            ['Device Type', 'device_type'],
            ['Device ID', 'device_id'],
            ['Status', 'task_status'],
            ['Default Gateway', 'default_gateway', '-'],
            ['Global IP', 'global_ip', '-'],
            ['Redundant Config', 'redundant_configuration_flg', '-'],
            ['Description', 'description', '-']
        ],
        'detail_name': 'vnf_info',
        'network_name': 'port_info'
    },
    'pfw': {
        'title': 'Physical Firewall:',
        'detail': [
            ['Tenant Name', 'tenant_id'],
            ['Name', 'name'],
            ['ID', 'node_id'],
            ['Apl Type', 'apl_type'],
            ['Type', 'type'],
            ['Device Type', 'device_type'],
            ['Device ID', 'device_id'],
            ['Status', 'task_status'],
            ['Default Gateway', 'default_gateway', '-'],
            ['Global IP', 'global_ip', '-'],
            ['Redundant Config', 'redundant_configuration_flg', '-'],
            ['Description', 'description', '-']
        ],
        'detail_name': 'pnf_info',
        'network_name': 'port_info'
    },
    'plb': {
        'title': 'Physical Loadbalancer:',
        'detail': [
            ['Tenant Name', 'tenant_id'],
            ['Name', 'name'],
            ['ID', 'node_id'],
            ['Apl Type', 'apl_type'],
            ['Type', 'type'],
            ['Device Type', 'device_type'],
            ['Device ID', 'device_id'],
            ['Status', 'task_status'],
            ['Default Gateway', 'default_gateway', '-'],
            ['Global IP', 'global_ip', '-'],
            ['Redundant Config', 'redundant_configuration_flg', '-'],
            ['Description', 'description', '-']
        ],
        'detail_name': 'pnf_info',
        'network_name': 'port_info'
    }
}

# Information to be displayed at the node of the creation screen
NODE_CREATE_COLUMNS = {
    'apl_type': {
        'field': 'ChoiceField',
        'label': _('Apl Type'),
        'required': True,
        'choices': [
            ('1', 'Virtual'),
            ('2', 'Physical')
        ]
    },
    'type': {
        'field': 'ChoiceField',
        'label': _('Type'),
        'required': True,
        'choices': [
            ('1', 'Firewall'),
            ('2', 'Loadbalancer')
        ]
    },
    'device_type': {
        'vfw': {
            'field': 'ChoiceField',
            'label': _('Device Type'),
            'required': True,
            'choices': [
                ('1', 'InterSecVM/SG(Ext)'),
                ('2', 'FortiGateVM(5.2.4)'),
                ('3', 'PaloAltoVM'),
                ('4', 'InterSecVM/SG(Pub)'),
                ('5', 'FortiGateVM(5.4.1)')
            ]
        },
        'vlb': {
            'field': 'ChoiceField',
            'label': _('Device Type'),
            'required': True,
            'choices': [
                ('1', 'InterSecVM/LB'),
                ('2', 'BIG-IP VE'),
                ('3', 'vThunder(4.0.1)'),
                ('4', 'vThunder(4.1.1)')
            ]
        },
        'pfw': {
            'field': 'ChoiceField',
            'label': _('Device Type'),
            'required': True,
            'choices': [
                ('1', 'FortiGate'),
                ('2', 'PaloAlto'),
                ('3', 'FortiGate Shared'),
                ('4', 'PaloAlto Shared')
            ]
        },
        'plb': {
            'field': 'ChoiceField',
            'label': _('Device Type'),
            'required': True,
            'choices': [
                ('1', 'BIG-IP'),
                ('2', 'Thunder'),
                ('3', 'BIG-IP Shared'),
                ('4', 'Thunder Shared')
            ]
        }
    },
    'subnet': {
        'field': 'ChoiceField',
        'label': _('Subnet'),
        'required': True,
        'choices': []
    },
    'separate': [
        (
            'redundant_configuration_flg',
            {
                'field': 'ChoiceField',
                'label': _('Redundant Config'),
                'required': True,
                'choices': [('0', _('Redundancy')),
                            ('1', _('Single'))]
            }
        ),
        (
            'host_name',
            {
                'field': 'CharField',
                'label': _('Host Name'),
                'required': True,
                'choices': []
            }
        ),
        (
            'webclient_ip',
            {
                'field': 'CharField',
                'label': _('InterSec WebClient IP'),
                'required': True,
                'choices': []
            }
        ),
        (
            'dns_server_primary',
            {
                'field': 'CharField',
                'label': _('Dns Server IP(primary)'),
                'required': False,
                'choices': [],
                'help_text': _('If the primary field is empty, '
                               'secondary field are ignored.')
            },
        ),
        (
            'dns_server_secondary',
            {
                'field': 'CharField',
                'label': _('Dns Server IP(secondary)'),
                'required': False,
                'choices': []
            },
        ),
        (
            'ntp_server_primary',
            {
                'field': 'CharField',
                'label': _('Ntp Server IP(primary)'),
                'required': False,
                'choices': [],
                'help_text': _('If the primary field is empty, '
                               'secondary field are ignored.')
            },
        ),
        (
            'ntp_server_secondary',
            {
                'field': 'CharField',
                'label': _('Ntp Server IP(secondary)'),
                'required': False,
                'choices': []
            },
        ),
        (
            'zabbix_vip_ip',
            {
                'field': 'CharField',
                'label': _('Zabbix VIP IP'),
                'required': False,
                'choices': []
            },
        ),
        (
            'zabbix_01_ip',
            {
                'field': 'CharField',
                'label': _('Zabbix 01 IP'),
                'required': False,
                'choices': []
            }
        ),
        (
            'zabbix_02_ip',
            {
                'field': 'CharField',
                'label': _('Zabbix 02 IP'),
                'required': False,
                'choices': []
            }
        ),
        (
            'static_route_ip',
            {
                'field': 'CharField',
                'label': _('Static Route IP'),
                'required': False,
                'choices': []
            }
        ),
        (
            'admin_id',
            {
                'field': 'CharField',
                'label': _('Admin ID'),
                'required': True,
                'choices': []
            }
        ),
        (
            'admin_pw',
            {
                'field': 'CharField',
                'label': _('Admin PW'),
                'required': True,
                'choices': []
            }
        ),
        (
            'pavm_zone_name',
            {
                'field': 'CharField',
                'label': _('Pavm Zone Name'),
                'required': True,
                'choices': []
            }
        ),
        (
            'fw_ip_address',
            {
                'field': 'CharField',
                'label': _('Firewall IP'),
                'required': True,
                'choices': []
            }
        ),
        (
            'domain_name',
            {
                'field': 'CharField',
                'label': _('Domain Name'),
                'required': True,
                'choices': []
            }
        ),
        (
            'self_ip_name',
            {
                'field': 'CharField',
                'label': _('Self IP Name'),
                'required': True,
                'choices': []
            }
        ),
        (
            'timezone',
            {
                'field': 'CharField',
                'label': _('Time Zone'),
                'required': True,
                'choices': []
            }
        ),
        (
            'vdom_name',
            {
                'field': 'CharField',
                'label': _('Host Name(Vdom Name)'),
                'required': True,
                'choices': []
            }
        ),
        (
            'partition_id',
            {
                'field': 'CharField',
                'label': _('Partition ID'),
                'required': True,
                'choices': []
            }
        ),
        (
            'route_domain_id',
            {
                'field': 'CharField',
                'label': _('Route Domain ID'),
                'required': True,
                'choices': []
            }
        ),
        (
            'vsys_name',
            {
                'field': 'CharField',
                'label': _('Vsys Name'),
                'required': True,
                'choices': []
            }
        ),
        (
            'zone_name',
            {
                'field': 'CharField',
                'label': _('Zone Name'),
                'required': True,
                'choices': []
            }
        ),
        (
            'partition_name',
            {
                'field': 'CharField',
                'label': _('Partition Name'),
                'required': True,
                'choices': []
            }
        ),
        (
            'admin_prof_name',
            {
                'field': 'CharField',
                'label': _('Admin Profile Name'),
                'required': True,
                'choices': []
            }
        ),
        (
            'user_account_id',
            {
                'field': 'CharField',
                'label': _('User Account ID'),
                'required': True,
                'choices': []
            }
        ),
        (
            'account_password',
            {
                'field': 'CharField',
                'label': _('Account Password'),
                'required': True,
                'choices': []
            }
        ),
        (
            'mng_user_account_id',
            {
                'field': 'CharField',
                'label': _('Manager Account ID'),
                'required': True,
                'choices': []
            }
        ),
        (
            'mng_account_password',
            {
                'field': 'CharField',
                'label': _('Manager Account Password'),
                'required': True,
                'choices': []
            }
        ),
        (
            'certificate_user_account_id',
            {
                'field': 'CharField',
                'label': _('Prover Account ID'),
                'required': True,
                'choices': []
            }
        ),
        (
            'certificate_account_password',
            {
                'field': 'CharField',
                'label': _('Prover Account Password'),
                'required': True,
                'choices': []
            }
        ),
        (
            'description',
            {
                'field': 'CharField',
                'label': _('Description'),
                'required': False,
                'choices': []
            }
        )
    ]
}

# Columns to display for each device type in the node of the creation screen
NODE_CREATE_DISPLAY_COLUMNS_LIST = {
    'InterSecVM/SG(Ext)': [
        'host_name',
        'webclient_ip',
        'ntp_server_primary',
        'zabbix_vip_ip',
        'zabbix_01_ip',
        'zabbix_02_ip',
        'static_route_ip',
        'description'
    ],
    'FortiGateVM(5.2.4)': [
        'host_name',
        'admin_id',
        'admin_pw',
        'dns_server_primary',
        'dns_server_secondary',
        'ntp_server_primary',
        'ntp_server_secondary',
        'description'
    ],
    'PaloAltoVM': [
        'host_name',
        'admin_id',
        'admin_pw',
        'dns_server_primary',
        'dns_server_secondary',
        'ntp_server_primary',
        'ntp_server_secondary',
        'pavm_zone_name',
        'description'
    ],
    'InterSecVM/SG(Pub)': [
        'host_name',
        'webclient_ip',
        'ntp_server_primary',
        'zabbix_vip_ip',
        'zabbix_01_ip',
        'zabbix_02_ip',
        'description'
    ],
    'FortiGateVM(5.4.1)': [
        'host_name',
        'admin_id',
        'admin_pw',
        'dns_server_primary',
        'dns_server_secondary',
        'ntp_server_primary',
        'ntp_server_secondary',
        'description'
    ],
    'InterSecVM/LB': [
        'host_name',
        'fw_ip_address',
        'ntp_server_primary',
        'zabbix_vip_ip',
        'zabbix_01_ip',
        'zabbix_02_ip',
        'description'
    ],
    'BIG-IP VE': [
        'host_name',
        'fw_ip_address',
        'domain_name',
        'self_ip_name',
        'admin_id',
        'admin_pw',
        'dns_server_primary',
        'dns_server_secondary',
        'ntp_server_primary',
        'ntp_server_secondary',
        'timezone',
        'description'
    ],
    'vThunder(4.0.1)': [
        'host_name',
        'fw_ip_address',
        'admin_id',
        'admin_pw',
        'dns_server_primary',
        'dns_server_secondary',
        'ntp_server_primary',
        'ntp_server_secondary',
        'description'
    ],
    'vThunder(4.1.1)': [
        'host_name',
        'fw_ip_address',
        'admin_id',
        'admin_pw',
        'dns_server_primary',
        'dns_server_secondary',
        'ntp_server_primary',
        'ntp_server_secondary',
        'description'
    ],
    'FortiGate': [
        'redundant_configuration_flg',
        'vdom_name',
        'admin_prof_name',
        'user_account_id',
        'account_password',
        'description'
    ],
    'PaloAlto': [
        'redundant_configuration_flg',
        'vsys_name',
        'admin_id',
        'admin_pw',
        'zone_name',
        'description'
    ],
    'FortiGate Shared': [
        'redundant_configuration_flg',
        'vdom_name',
        'admin_prof_name',
        'user_account_id',
        'account_password',
        'description'
    ],
    'PaloAlto Shared': [
        'redundant_configuration_flg',
        'vsys_name',
        'admin_id',
        'admin_pw',
        'zone_name',
        'description'
    ],
    'BIG-IP': [
        'redundant_configuration_flg',
        'partition_id',
        'fw_ip_address',
        'route_domain_id',
        'mng_user_account_id',
        'mng_account_password',
        'certificate_user_account_id',
        'certificate_account_password',
        'description'
    ],
    'Thunder': [
        'redundant_configuration_flg',
        'partition_name',
        'fw_ip_address',
        'user_account_id',
        'account_password',
        'description'
    ],
    'BIG-IP Shared': [
        'redundant_configuration_flg',
        'partition_id',
        'fw_ip_address',
        'route_domain_id',
        'mng_user_account_id',
        'mng_account_password',
        'certificate_user_account_id',
        'certificate_account_password',
        'description'
    ],
    'Thunder Shared': [
        'redundant_configuration_flg',
        'partition_name',
        'fw_ip_address',
        'user_account_id',
        'account_password',
        'description'
    ]
}

# Information to be displayed at the node of the update screen
NODE_UPDATE_COLUMNS = {
    'interface': {
        'display_type': 'input_column',
        'common': {
            'subnet': {
                'field': 'ChoiceField',
                'label': 'Subnet',
                'required': True,
                'choices': []
            }
        },
        'separate': [
            (
                'pavm_zone_name',
                {
                    'field': 'CharField',
                    'label': 'Pavm Zone Name',
                    'required': True,
                    'choices': []
                }
            ),
            (
                'zone_name',
                {
                    'field': 'CharField',
                    'label': 'Zone Name',
                    'required': True,
                    'choices': []
                }
            )
        ]
    },
    'license': {
        'display_type': 'check',
        'target': 'name',
        'text': '%s check please.'
    },
    'IPv6Add': {
        'display_type': 'input_column',
        'description': _('There is one subnet that can be set by adding an IPv6 address. '
                         'Once set contents can not be updated.'),
        'common': {
            'subnet': {
                'field': 'ChoiceField',
                'label': 'Subnet',
                'required': True,
                'choices': []
            }
        },
        'separate': [
            (
                'ip_v6_ext_auto_set_flg',
                {
                    'field': 'BooleanField',
                    'label': _('Randomly Set External LAN IPv6 Address'),
                    'required': False
                }
            ),
            (
                'fixed_ip_v6_ext',
                {
                    'field': 'CharField',
                    'label': _('Fixedly Set External LAN IPv6 Address'),
                    'required': False,
                    'choices': [],
                    'help_text': _('Apart from the selected subnet, '
                                   'please input the IP address of the External LAN fixedly.')
                }
            ),
            (
                'ip_v6_pub_auto_set_flg',
                {
                    'field': 'BooleanField',
                    'label': _('Randomly Set Public LAN IPv6 Address'),
                    'required': False
                }
            ),
            (
                'fixed_ip_v6_pub',
                {
                    'field': 'CharField',
                    'label': _('Fixedly Set Public LAN IPv6 Address'),
                    'required': False,
                    'choices': [],
                    'help_text': _('Apart from the selected subnet, '
                                   'please input the IP address of the Public LAN fixedly.')
                }
            ),
            (
                'static_route_ip_ipv6',
                {
                    'field': 'CharField',
                    'label': _('Static Route IPv6 Address'),
                    'required': False,
                    'choices': []
                }
            ),
            (
                'fw_ip_v6_address',
                {
                    'field': 'CharField',
                    'label': _('Firewall IPv6 Address'),
                    'required': True,
                    'choices': []
                }
            )
        ]
    }
}

# Columns to display for each device type in the node of the update screen
NODE_UPDATE_DISPLAY_COLUMNS_LIST = {
    'InterSecVM/SG(Ext)': [
        'ip_v6_ext_auto_set_flg',
        'fixed_ip_v6_ext',
        'static_route_ip_ipv6'
    ],
    'FortiGateVM(5.2.4)': [
        'ip_v6_ext_auto_set_flg',
        'fixed_ip_v6_ext',
        'ip_v6_pub_auto_set_flg',
        'fixed_ip_v6_pub'
    ],
    'PaloAltoVM': [
        'pavm_zone_name',
        'ip_v6_ext_auto_set_flg',
        'fixed_ip_v6_ext',
        'ip_v6_pub_auto_set_flg',
        'fixed_ip_v6_pub'
    ],
    'InterSecVM/SG(Pub)': [
        'ip_v6_pub_auto_set_flg',
        'fixed_ip_v6_pub'
    ],
    'FortiGateVM(5.4.1)': [
        'ip_v6_ext_auto_set_flg',
        'fixed_ip_v6_ext',
        'ip_v6_pub_auto_set_flg',
        'fixed_ip_v6_pub'
    ],
    'InterSecVM/LB': [
        'fw_ip_v6_address'
    ],
    'BIG-IP VE': [
        'fw_ip_v6_address'
    ],
    'vThunder(4.0.1)': [
        'fw_ip_v6_address'
    ],
    'vThunder(4.1.1)': [
        'fw_ip_v6_address'
    ],
    'FortiGate': [
        'ip_v6_ext_auto_set_flg',
        'fixed_ip_v6_ext',
        'ip_v6_pub_auto_set_flg',
        'fixed_ip_v6_pub'
    ],
    'PaloAlto': [
        'ip_v6_ext_auto_set_flg',
        'fixed_ip_v6_ext',
        'ip_v6_pub_auto_set_flg',
        'fixed_ip_v6_pub',
        'zone_name'
    ],
    'FortiGate Shared': [
        'ip_v6_ext_auto_set_flg',
        'fixed_ip_v6_ext',
        'ip_v6_pub_auto_set_flg',
        'fixed_ip_v6_pub'
    ],
    'PaloAlto Shared': [
        'ip_v6_ext_auto_set_flg',
        'fixed_ip_v6_ext',
        'ip_v6_pub_auto_set_flg',
        'fixed_ip_v6_pub',
        'zone_name'
    ],
    'BIG-IP': [
        'fw_ip_v6_address'
    ],
    'Thunder': [
        'fw_ip_v6_address'
    ],
    'BIG-IP Shared': [
        'fw_ip_v6_address'
    ],
    'Thunder Shared': [
        'fw_ip_v6_address'
    ]
}


"""Service Config."""

# Shaping of API response
SERVICE_RETURN_MAPPING = {
    'all_dcconnect': {
        'id': 'group_id',
        'service_name': 'group_name',
        'service_type': 'group_type',
        'my_group_flg': 'my_group_flg',
        'task_status': 'task_status',
        'tenant_id': 'IaaS_tenant_id'
    },
    'dcconnect': {
        'dc_info': {
            'id': 'dc_id',
            'name': 'dc_name',
        },
        'dc_group_info': {
            'service_name': 'group_name',
            'service_type': 'group_type',
            'id': 'group_id',
            'my_dc_id': 'my_dc_id',
            'task_status': 'task_status',
            'tenant_id': 'IaaS_tenant_id'
        },
        'dc_member_info': {
            'dc_id': 'dc_id',
            'dc_name': 'dc_name',
            'network_name': 'IaaS_network_name',
            'network_id': 'IaaS_network_id',
            'subnet_id': 'IaaS_subnet_id',
            'subnet_id_v6': 'IaaS_subnet_id_v6',
            'ip_address': 'vrrp_address',
            'ip_address_v6': 'vrrp_address_v6',
            'ce1_address': 'ce1_address',
            'ce2_address': 'ce2_address',
            'bandwidth': 'bandwidth',
            'default_gateway': 'default_gateway'
        },
        'apl_info': {
            'ntp_server_ip_address': 'ntp_server_ip_address',
            'dns_server_ip_address': 'dns_server_ip_address',
            'snmp_server_ip_address': 'snmp_server_ip_address',
            'syslog_server_ip_address': 'syslog_server_ip_address'
        }
    }
}

# Mapping of SERVICE_TYPE and Function_type
SERVICE_FUNCTION_TYPE_MAPPING = {
    '1': 'dcconnect',
    '2': 'dcconnect',
    '3': 'dcconnect',
    '4': 'dcconnect'
}

# Mapping of SERVICE_TYPE value and name
SERVICE_TYPE_MAPPING = {
    '1': 'Firefly',
    '2': 'CSR1000v',
    '3': 'CSR1000v (Encrypted)',
    '4': 'CSR1000v (Unencrypted)'
}

# Mapping of Bandwidth value and name
SERVICE_BANDWIDTH_MAPPING = {
    '1': '10MB',
    '2': '50MB',
    '3': '100MB',
    '4': '250MB',
    '5': '500MB',
    '6': '1000MB',
    '7': '2500MB',
    '8': '5000MB',
    '9': '10000MB',
    '': '-'
}

# Mapping of SERVICE_TYPE value and name
SERVICE_TYPE_DETAIL_MAPPING = {
    'Firefly': {
        'apl_type': '1',
        'type': '3',
        'device_type': '1'
    },
    'CSR1000v': {
        'apl_type': '1',
        'type': '3',
        'device_type': '2'
    },
    'CSR1000v (Encrypted)': {
        'apl_type': '1',
        'type': '3',
        'device_type': '2'
    },
    'CSR1000v (Unencrypted)': {
        'apl_type': '1',
        'type': '3',
        'device_type': '2'
    }
}

# Action buttons that can be displayed in a service list
SERVICE_ALL_BUTTONS = {
    'table': [],
    'row': ['UpdateNetworkLink', 'UpdateBandwidthLink', 'UpdateSettingLink',
            'UpdateMemberLink', 'DeleteServiceAction']
}

# Action buttons that can be displayed in a member list
MEMBER_ALL_BUTTONS = {
    'table': ['UpdateMemberTableAction'],
    'row': ['UpdateBandwidthMemberLink', 'UpdateSettingMemberLink',
            'DeleteMemberAction']
}

# Action buttons that can be displayed in a network list
CONNECT_ALL_BUTTONS = {
    'table': ['UpdateNetworkTableAction'],
    'row': ['UpdateNetworkV6Link']
}

# Conditions to display the action button
SERVICE_DISPLAY_BUTTONS_LIST = {
    'is_member': [
        'UpdateNetworkLink',
        'UpdateNetworkTableAction',
        'UpdateBandwidthLink',
        'UpdateBandwidthMemberLink',
        'UpdateSettingLink',
        'UpdateSettingMemberLink',
        'UpdateNetworkV6Link',
        'DeleteServiceAction',
        'DeleteMemberAction'
    ],
    'is_not_member': [
        'UpdateMemberLink',
        'UpdateMemberTableAction'
    ]
}

# Conditions to display a button for each device
SERVICE_DISPLAY_BUTTONS_FOR_DEVICE = {
    'Firefly': [
        'UpdateNetworkLink', 'UpdateMemberLink', 'UpdateNetworkV6Link',
        'DeleteServiceAction', 'UpdateMemberTableAction',
        'DeleteMemberAction', 'UpdateNetworkTableAction'
    ],
    'CSR1000v': [
        'UpdateNetworkLink', 'UpdateMemberLink', 'UpdateBandwidthLink',
        'UpdateSettingLink', 'DeleteServiceAction', 'UpdateMemberTableAction',
        'DeleteMemberAction', 'UpdateNetworkTableAction',
        'UpdateBandwidthMemberLink', 'UpdateSettingMemberLink',
        'UpdateNetworkV6Link'
    ],
    'CSR1000v (Encrypted)': [
        'UpdateNetworkLink', 'UpdateMemberLink', 'UpdateBandwidthLink',
        'UpdateSettingLink', 'DeleteServiceAction', 'UpdateMemberTableAction',
        'DeleteMemberAction', 'UpdateNetworkTableAction',
        'UpdateBandwidthMemberLink', 'UpdateSettingMemberLink',
        'UpdateNetworkV6Link'
    ],
    'CSR1000v (Unencrypted)': [
        'UpdateNetworkLink', 'UpdateMemberLink', 'UpdateBandwidthLink',
        'UpdateSettingLink', 'DeleteServiceAction', 'UpdateMemberTableAction',
        'DeleteMemberAction', 'UpdateNetworkTableAction',
        'UpdateBandwidthMemberLink', 'UpdateSettingMemberLink',
        'UpdateNetworkV6Link'
    ]
}

# Conditions to display a button for each status
SERVICE_DISPLAY_BUTTONS_FOR_STATUS = {
    '0': [],
    '1': [
        'UpdateNetworkLink', 'UpdateMemberLink', 'UpdateBandwidthLink',
        'UpdateSettingLink', 'DeleteServiceAction', 'UpdateMemberTableAction',
        'DeleteMemberAction', 'UpdateNetworkTableAction',
        'UpdateBandwidthMemberLink', 'UpdateSettingMemberLink',
        'UpdateNetworkV6Link'
    ],
    '9': [
        'DeleteServiceAction', 'DeleteMemberAction'
    ]
}

# Information to be displayed on the detail screen of the service
SERVICE_DETAIL_DISPLAY_COLUMNS = {
    'dcconnect': {
        'title': 'Service Detail:',
        'detail': [
            ['Service Name', 'service_name'],
            ['Service Type', 'service_type'],
            ['ID', 'id'],
            ['Status', 'task_status'],
            ['DNS Server', 'dns_server_ip_address', '-'],
            ['NTP Server', 'ntp_server_ip_address', '-'],
            ['SNMP Server', 'snmp_server_ip_address', '-'],
            ['Syslog Server', 'syslog_server_ip_address', '-'],
            ['DC Name', 'dc_name']
        ],
        'network': 1,
        'member': 1,
        'detail_name': 'dc_group_info',
        'member_name': 'dc_info',
        'network_name': 'dc_member_info',
        'add_detail_name': 'apl_info'
    }
}

# Information to be displayed at the service of the creation screen
SERVICE_CREATE_COLUMNS = {
    'service_name': {
        'field': 'CharField',
        'label': _('Service'),
        'required': True
    },
    'service_type_normal': {
        'field': 'ChoiceField',
        'label': _('Type'),
        'required': True,
        'choices': [
            ('1', 'Firefly'),
            ('2', 'CSR1000v')
        ]
    },
    'service_type_tunneling_encrypted': {
        'field': 'ChoiceField',
        'label': _('Type'),
        'required': True,
        'choices': [
            ('3', 'CSR1000v (Encrypted)')
        ]
    },
    'service_type_tunneling_unencrypted': {
        'field': 'ChoiceField',
        'label': _('Type'),
        'required': True,
        'choices': [
            ('4', 'CSR1000v (Unencrypted)')
        ]
    },
    'separate': [
        (
            'IaaS_subnet_id',
            {
                'field': 'ChoiceField',
                'label': _('Subnet'),
                'required': True,
                'choices': []
            }
        ),
        (
            'fw_ip_address',
            {
                'field': 'CharField',
                'label': _('Gateway IP'),
                'required': True
            }
        ),
        (
            'bandwidth',
            {
                'field': 'ChoiceField',
                'label': _('Bandwidth'),
                'required': True,
                'choices': [
                    ('1', '10MB'),
                    ('2', '50MB'),
                    ('3', '100MB'),
                    ('4', '250MB'),
                    ('5', '500MB'),
                    ('6', '1000MB'),
                    ('7', '2500MB'),
                    ('8', '5000MB'),
                    ('9', '10000MB')
                ]
            }
        ),
        (
            'dns_server_ip_address',
            {
                'field': 'CharField',
                'label': _('DNS Server IP'),
                'required': True
            }
        ),
        (
            'ntp_server_ip_address',
            {
                'field': 'CharField',
                'label': _('NTP Server IP'),
                'required': True
            }
        ),
        (
            'snmp_server_ip_address',
            {
                'field': 'CharField',
                'label': _('SNMP Server IP'),
                'required': False
            }
        ),
        (
            'syslog_server_ip_address',
            {
                'field': 'CharField',
                'label': _('Syslog Server IP'),
                'required': False
            }
        )
    ]
}

# Columns to display for each device type in the service of the creation screen
SERVICE_CREATE_DISPLAY_COLUMNS_LIST = {
    'Firefly': [
        'IaaS_subnet_id',
        'fw_ip_address'
    ],
    'CSR1000v': [
        'IaaS_subnet_id',
        'fw_ip_address',
        'bandwidth',
        'dns_server_ip_address',
        'ntp_server_ip_address',
        'snmp_server_ip_address',
        'syslog_server_ip_address'
    ],
    'CSR1000v (Encrypted)': [
        'IaaS_subnet_id',
        'fw_ip_address',
        'bandwidth',
        'dns_server_ip_address',
        'ntp_server_ip_address',
        'snmp_server_ip_address',
        'syslog_server_ip_address'
    ],
    'CSR1000v (Unencrypted)': [
        'IaaS_subnet_id',
        'fw_ip_address',
        'bandwidth',
        'dns_server_ip_address',
        'ntp_server_ip_address',
        'snmp_server_ip_address',
        'syslog_server_ip_address'
    ]
}

# Information to be displayed at the service of the update screen
SERVICE_UPDATE_COLUMNS = {
    'interface': {
        'display_type': 'input_column',
        'method': 'update',
        'common': [
            (
                'service_name',
                {
                    'field': 'CharField',
                    'label': 'Service Name',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            ),
            (
                'service_type',
                {
                    'field': 'CharField',
                    'label': 'Service Type',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            )
        ],
        'separate': [
            (
                'IaaS_subnet_id',
                {
                    'field': 'ChoiceField',
                    'label': 'Subnet',
                    'required': True,
                    'choices': []
                }
            )
        ]
    },
    'member_create': {
        'display_type': 'input_column',
        'method': 'create',
        'common': [
            (
                'service_name',
                {
                    'field': 'CharField',
                    'label': 'Service Name',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            ),
            (
                'service_type',
                {
                    'field': 'CharField',
                    'label': 'Service Type',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            )
        ],
        'separate': [
            (
                'IaaS_subnet_id',
                {
                    'field': 'ChoiceField',
                    'label': 'Subnet',
                    'required': True,
                    'choices': []
                }
            ),
            (
                'fw_ip_address',
                {
                    'field': 'CharField',
                    'label': _('Gateway IP'),
                    'required': True
                }
            ),
            (
                'bandwidth',
                {
                    'field': 'ChoiceField',
                    'label': _('Bandwidth'),
                    'required': True,
                    'choices': [
                        ('1', '10MB'),
                        ('2', '50MB'),
                        ('3', '100MB'),
                        ('4', '250MB'),
                        ('5', '500MB'),
                        ('6', '1000MB'),
                        ('7', '2500MB'),
                        ('8', '5000MB'),
                        ('9', '10000MB')
                        ]
                }
            ),
            (
                'dns_server_ip_address',
                {
                    'field': 'CharField',
                    'label': _('DNS Server IP'),
                    'required': True
                }
            ),
            (
                'ntp_server_ip_address',
                {
                    'field': 'CharField',
                    'label': _('NTP Server IP'),
                        'required': True
                }
            ),
            (
                'snmp_server_ip_address',
                {
                    'field': 'CharField',
                    'label': _('SNMP Server IP'),
                    'required': False
                }
            ),
            (
                'syslog_server_ip_address',
                {
                    'field': 'CharField',
                    'label': _('Syslog Server IP'),
                    'required': False
                }
            )
        ]
    },
    'bandwidth': {
        'display_type': 'input_column',
        'method': 'update',
        'common': [
            (
                'service_name',
                {
                    'field': 'CharField',
                    'label': 'Service Name',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            ),
            (
                'service_type',
                {
                    'field': 'CharField',
                    'label': 'Service Type',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            )
        ],
        'separate': [
            (
                'bandwidth',
                {
                    'field': 'ChoiceField',
                    'label': _('Bandwidth'),
                    'required': True,
                    'choices': [
                        ('1', '10MB'),
                        ('2', '50MB'),
                        ('3', '100MB'),
                        ('4', '250MB'),
                        ('5', '500MB'),
                        ('6', '1000MB'),
                        ('7', '2500MB'),
                        ('8', '5000MB'),
                        ('9', '10000MB')
                    ]
                }
            )
        ]
    },
    'serviceSetting': {
        'display_type': 'input_column',
        'method': 'update',
        'common': [
            (
                'service_name',
                {
                    'field': 'CharField',
                    'label': 'Service Name',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            ),
            (
                'service_type',
                {
                    'field': 'CharField',
                    'label': 'Service Type',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            )
        ],
        'separate': [
            (
                'dns_server_ip_address',
                {
                    'field': 'CharField',
                    'label': _('DNS Server IP'),
                    'required': False,
                }
            ),
            (
                'ntp_server_ip_address',
                {
                    'field': 'CharField',
                    'label': _('NTP Server IP'),
                    'required': False
                }
            ),
            (
                'ntp_server_interface',
                {
                    'field': 'ChoiceField',
                    'label': _('NTP Server IP'),
                    'required': False,
                    'choices': [],
                    'help_text': _('This item is mandatory when '
                                   'specifying an NTP server.')
                }
            ),
            (
                'snmp_server_ip_address',
                {
                    'field': 'CharField',
                    'label': _('SNMP Server IP'),
                    'required': False
                }
            ),
            (
                'snmp_server_interface',
                {
                    'field': 'ChoiceField',
                    'label': _('SNMP Interface'),
                    'required': False,
                    'choices': [],
                    'help_text': _('This item is mandatory when '
                                   'specifying an SNMP server.')
                }
            ),
            (
                'snmp_server_delete_flg',
                {
                    'field': 'BooleanField',
                    'label': _('SNMP Setting Delete'),
                    'required': False
                }
            ),
            (
                'syslog_server_ip_address',
                {
                    'field': 'CharField',
                    'label': _('Syslog Server IP'),
                    'required': False
                }
            ),
            (
                'syslog_server_interface',
                {
                    'field': 'ChoiceField',
                    'label': _('Syslog Interface'),
                    'required': False,
                    'choices': [],
                    'help_text': _('This item is mandatory when '
                                   'specifying an Syslog server.')
                }
            ),
            (
                'syslog_server_delete_flg',
                {
                    'field': 'BooleanField',
                    'label': _('Syslog Setting Delete'),
                    'required': False
                }
            )
        ]
    },
    'serviceIPv6Add': {
        'display_type': 'input_column',
        'method': 'update',
        'description': _('There is one subnet that can be set by adding an IPv6 address. '
                         'Once set contents can not be updated.'),
        'common': [
            (
                'service_name',
                {
                    'field': 'CharField',
                    'label': 'Service Name',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            ),
            (
                'service_type',
                {
                    'field': 'CharField',
                    'label': 'Service Type',
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            ),
            (
                'IaaS_subnet_id_v6',
                {
                    'field': 'ChoiceField',
                    'label': 'Subnet',
                    'required': True,
                    'choices': [],
                    'widget': {}
                }
            )
        ],
        'separate': [
            (
                'fw_ip_v6_address',
                {
                    'field': 'CharField',
                    'label': _('Gateway IPv6 Address'),
                    'required': True,
                    'choices': []
                }
            )
        ]
    }
}

# Columns to display for each device type in the service of the update screen
SERVICE_UPDATE_DISPLAY_COLUMNS_LIST = {
    'Firefly': [
        'IaaS_subnet_id',
        'fw_ip_address'
    ],
    'CSR1000v': [
        'IaaS_subnet_id',
        'fw_ip_address',
        'bandwidth',
        'dns_server_ip_address',
        'ntp_server_ip_address',
        'ntp_server_interface',
        'snmp_server_ip_address',
        'snmp_server_interface',
        'snmp_server_delete_flg',
        'syslog_server_ip_address',
        'syslog_server_interface',
        'syslog_server_delete_flg',
        'fw_ip_v6_address'
    ],
    'CSR1000v (Encrypted)': [
        'IaaS_subnet_id',
        'fw_ip_address',
        'bandwidth',
        'dns_server_ip_address',
        'ntp_server_ip_address',
        'ntp_server_interface',
        'snmp_server_ip_address',
        'snmp_server_interface',
        'snmp_server_delete_flg',
        'syslog_server_ip_address',
        'syslog_server_interface',
        'syslog_server_delete_flg',
        'fw_ip_v6_address'
    ],
    'CSR1000v (Unencrypted)': [
        'IaaS_subnet_id',
        'fw_ip_address',
        'bandwidth',
        'dns_server_ip_address',
        'ntp_server_ip_address',
        'ntp_server_interface',
        'snmp_server_ip_address',
        'snmp_server_interface',
        'snmp_server_delete_flg',
        'syslog_server_ip_address',
        'syslog_server_interface',
        'syslog_server_delete_flg',
        'fw_ip_v6_address'
    ]
}

# Columns to display for each device type in the service of the update screen
SERVICE_UPDATE_IPV6_DELETE_LIST = [
    'fw_ip_v6_address'
]


"""Resource Config."""

# Mapping of nw_reource_type and Function_type
RESOURCE_FUNCTION_TYPE_MAPPING = {
    'project': {
        '1': 'ext_globalip',
        '2': 'appliances',
        '3': 'service',
    },
    'admin': {
        '1': 'globalip',
        '2': 'license',
        '3': 'pnf',
        '4': 'msa_vlan',
        '5': 'wan_vlan',
        '6': 'cpu_list',
        '7': 'memory_list',
        '8': 'storage_list'
    },
    'admin_detail': {
        'cpu_list': 'cpu_detail',
        'memory_list': 'memory_detail',
        'storage_list': 'storage_detail'
    }
}

# Mapping of nw_reource_type and Function_type
RESOURCE_NAME_MAPPING = {
    'ext_globalip': 'global_ip',
    'appliances': {
        '1': {
            '1': {
                '1': 'intersec_sg_ext',
                '2': 'fortigate_vm_524',
                '3': 'paloalto_vm',
                '4': 'intersec_sg_pub',
                '5': 'fortigate_vm_541'
            },
            '2': {
                '1': 'intersec_lb',
                '2': 'bigip_ve',
                '3': 'vthunder_401',
                '4': 'vthunder_411'
            }
        },
        '2': {
            '1': {
                '1': {
                    '0': 'fortigate_redundancy',
                    '1': 'fortigate_single'
                },
                '2': {
                    '0': 'paloalto_redundancy',
                    '1': 'paloalto_single'
                },
                '3': 'fortigate_share',
                '4': 'paloalto_share'
            },
            '2': {
                '1': {
                    '0': 'bigip_redundancy',
                    '1': 'bigip_single'
                },
                '2': {
                    '0': 'thunder_redundancy',
                    '1': 'thunder_single'
                },
                '3': 'bigip_share',
                '4': 'thunder_share'
            }
        }
    },
    'service': {
        '1': {
            '3': {
                '1': 'firefly',
                '2': 'cisco'
            }
        }
    },
    'globalip': 'global_ip',
    'license': {
        '1': {
            '1': 'intersec_sg_ext',
            '2': 'fortigate_vm_524',
            '3': {
                '1': 'paloalto_vm_base',
                '2': 'paloalto_vm_hip',
                '3': 'paloalto_vm_multi_gateway',
                '4': 'paloalto_vm_threat',
                '5': 'paloalto_vm_btight_cloud',
                '6': 'paloalto_vm_pan_db',
                '7': 'paloalto_vm_wild_fire'
            },
            '4': 'intersec_sg_pub',
            '5': 'fortigate_vm_541'
        },
        '2': {
            '1': 'intersec_lb',
            '2': 'bigip_ve',
            '3': 'vthunder_401',
            '4': 'vthunder_411'
        },
        '3': {
            '2': {
                '1': 'cisco(10)',
                '2': 'cisco(50)',
                '3': 'cisco(100)',
                '4': 'cisco(250)',
                '5': 'cisco(500)',
                '6': 'cisco(1000)',
                '7': 'cisco(2500)',
                '8': 'cisco(5000)',
                '9': 'cisco(10000)'
            }
        }
    },
    'pnf': {
        '1': {
            '1': {
                '0': 'fortigate_redundancy',
                '1': 'fortigate_single'
            },
            '2': {
                '0': 'paloalto_redundancy',
                '1': 'paloalto_single'
            },
            '3': 'fortigate_share',
            '4': 'paloalto_share'
        },
        '2': {
            '1': {
                '0': 'bigip_redundancy',
                '1': 'bigip_single'
            },
            '2': {
                '0': 'thunder_redundancy',
                '1': 'thunder_single'
            },
            '3': 'bigip_share',
            '4': 'thunder_share'
        }
    },
    'cpu_list': {
        '1': 'cpu(vim)',
        '2': 'cpu(wim)',
        '3': 'cpu'
    },
    'memory_list': {
        '1': 'memory(vim)',
        '2': 'memory(wim)',
        '3': 'memory'
    },
    'storage_list': {
        '1': 'storage(vim)',
        '2': 'storage(wim)',
        '3': 'storage'
    },
    'msa_vlan': 'msa_vlan',
    'wan_vlan': 'wan_vlan',
    'cpu_detail': {
        '1': 'cpu(vim)',
        '2': 'cpu(wim)',
        '3': 'cpu'
    },
    'memory_detail': {
        '1': 'memory(vim)',
        '2': 'memory(wim)',
        '3': 'memory'
    },
    'storage_detail': {
        '1': 'storage(vim)',
        '2': 'storage(wim)',
        '3': 'storage'
    }
}

RESOURCE_DISPLAY_NAME_MAPPING = {
    'global_ip': 'Global IP',
    'intersec_sg_ext': 'InterSecVM/SG(Ext)',
    'fortigate_vm_524': 'FortiGateVM(5.2.4)',
    'paloalto_vm': 'PaloAltoVM',
    'intersec_sg_pub': 'InterSecVM/SG(Pub)',
    'fortigate_vm_541': 'FortiGateVM(5.4.1)',
    'intersec_lb': 'InterSecVM/LB',
    'bigip_ve': 'BIG-IP VE',
    'vthunder_401': 'vThunder(4.0.1)',
    'vthunder_411': 'vThunder(4.1.1)',
    'fortigate_redundancy': 'Fortigate Redundancy',
    'fortigate_single': 'Fortigate Single',
    'fortigate_share': 'Fortigate Share',
    'paloalto_redundancy': 'PaloAlto Redundancy',
    'paloalto_single': 'PaloAlto Single',
    'paloalto_share': 'PaloAlto Share',
    'bigip_redundancy': 'BIG-IP Redundancy',
    'bigip_single': 'BIG-IP Single',
    'bigip_share': 'BIG-IP Share',
    'thunder_redundancy': 'Thunder Redundancy',
    'thunder_single': 'Thunder Single',
    'thunder_share': 'Thunder Share',
    'firefly': 'Firefly',
    'cisco': 'Cisco',
    'paloalto_vm_base': 'PaloAltoVM Base License',
    'paloalto_vm_hip': 'PaloAltoVM HIP',
    'paloalto_vm_multi_gateway': 'PaloAltoVM Malti Gateway',
    'paloalto_vm_threat': 'PaloAltoVM Threat',
    'paloalto_vm_btight_cloud': 'PaloAltoVM Btight Cloud',
    'paloalto_vm_pan_db': 'PaloAltoVM Pan DB',
    'paloalto_vm_wild_fire': 'PaloAltoVM Wild Fire',
    'cisco(10)': 'Cisco(10MB)',
    'cisco(50)': 'Cisco(50MB)',
    'cisco(100)': 'Cisco(100MB)',
    'cisco(250)': 'Cisco(250MB)',
    'cisco(500)': 'Cisco(500MB)',
    'cisco(1000)': 'Cisco(1000MB)',
    'cisco(2500)': 'Cisco(2500MB)',
    'cisco(5000)': 'Cisco(5000MB)',
    'cisco(10000)': 'Cisco(10000MB)',
    'cpu(vim)': 'CPU(vim)',
    'memory(vim)': 'Memory(vim)',
    'storage(vim)': 'Storage(vim)',
    'cpu(wim)': 'CPU(wim)',
    'memory(wim)': 'Memory(wim)',
    'storage(wim)': 'Storage(wim)',
    'cpu': 'CPU',
    'memory': 'Memory',
    'storage': 'Storage',
    'msa_vlan': 'MSA Virtual LAN',
    'wan_vlan': 'Wan Virtual LAN'
}

# Mapping of resource status value and name
RESOURCE_STATUS_MAPPING = {
    '0': _('Unused'),
    '1': _('Used'),
    '2': _('Unavailable'),
    '3': _('Unacquired')
}

# Mapping of resource task status value and name
RESOURCE_TASK_STATUS_MAPPING = {
    'appliances': {
        '': '-',
        '0': _('Build'),
        '1': _('Active'),
        '2': _('No License'),
        '9': _('Error')
    },
    'service': {
        '': '-',
        '0': _('Build'),
        '1': _('Active'),
        '2': _('No License'),
        '9': _('Error')
    },
    'globalip': {
        '': '-',
        '0': '-',
        '101': _('Payout'),
        '103': _('Refund'),
        '201': _('Payout'),
        '202': _('Active'),
        '203': _('Refund')
    },
    'pnf': {
        '': '-',
        '0': _('Build'),
        '1': _('Active'),
        '2': _('No License'),
        '9': _('Error')
    },
    'msa_vlan': {
        '': '-',
        '0': '-',
        '1': _('Active')
    },
    'wan_vlan': {
        '': '-',
        '0': '-',
        '1': _('Payout'),
        '2': _('Refund'),
    }
}

RESOURCE_RETURN_MAPPING = {
    'all_resource': {
        'contract_info': {
            'contract_kind': 'contract_kind',
            'nw_resource_kind': 'nw_resource_kind',
            'apl_type': 'apl_type',
            'type': 'type',
            'device_type': 'device_type',
            'type_detail': 'type_detail',
            'redundant': 'redundant_configuration_flg',
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt',
            'unavailable_cnt': 'unavailable_cnt',
            'threshold': 'threshold',
            'warning_flg': 'warning_flg'
        }
    },
    'ext_globalip': {
        'contract_info': {
            'id': 'ID',
            'resource': 'globalip',
            'node_id': 'node_id',
            'status': 'use_status',
            'name': 'node_name'
        }
    },
    'appliances': {
        'contract_info': {
            'id': 'ID',
            'node_id': 'node_id',
            'task_status': 'task_status',
            'name': 'node_name',
            'status': 'use_status'
        }
    },
    'service': {
        'contract_info': {
            'id': 'ID',
            'task_status': 'task_status',
            'name': 'group_name',
            'status': 'use_status'
        }
    },
    'globalip': {
        'total_info': {
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt',
            'unavailable_cnt': 'unavailable_cnt'
        },
        'contract_info': {
            'id': 'ID',
            'node_id': 'node_id',
            'node_name': 'node_name',
            'tenant_id': 'IaaS_tenant_id',
            'resource': 'globalip',
            'task_status': 'task_status',
            'status': 'use_status'
        }
    },
    'license': {
        'total_info': {
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt',
            'unavailable_cnt': 'unavailable_cnt'
        },
        'contract_info': {
            'id': 'ID',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt',
            'tenant_id': 'IaaS_tenant_id'
        }
    },
    'pnf': {
        'total_info': {
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt',
            'unavailable_cnt': 'unavailable_cnt'
        },
        'contract_info': {
            'id': 'ID',
            'node_id': 'node_id',
            'node_name': 'node_name',
            'resource': 'device_name_master',
            'tenant_id': 'IaaS_tenant_id',
            'task_status': 'task_status',
            'status': 'use_status'
        }
    },
    'cpu_list': {
        'total_info': {
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt'
        },
        'contract_info': {
            'pod_name': 'pod_id',
            'quota': 'quota',
            'use_cnt': 'use_cnt'
        }
    },
    'storage_list': {
        'total_info': {
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt'
        },
        'contract_info': {
            'pod_name': 'pod_id',
            'quota': 'quota',
            'use_cnt': 'use_cnt'
        }
    },
    'memory_list': {
        'total_info': {
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt'
        },
        'contract_info': {
            'pod_name': 'pod_id',
            'quota': 'quota',
            'use_cnt': 'use_cnt'
        }
    },
    'cpu_detail': {
        'total_info': {
            'quota': 'quota',
            'use_cnt': 'use_cnt'
        },
        'contract_info': {
            'tenant_id': 'IaaS_tenant_id',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt'
        }
    },
    'storage_detail': {
        'total_info': {
            'quota': 'quota',
            'use_cnt': 'use_cnt'
        },
        'contract_info': {
            'tenant_id': 'IaaS_tenant_id',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt'
        }
    },
    'memory_detail': {
        'total_info': {
            'quota': 'quota',
            'use_cnt': 'use_cnt'
        },
        'contract_info': {
            'tenant_id': 'IaaS_tenant_id',
            'contract_cnt': 'contract_cnt',
            'use_cnt': 'use_cnt'
        }
    },
    'msa_vlan': {
        'total_info': {
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'unavailable_cnt': 'unavailable_cnt',
            'use_cnt': 'use_cnt'
        },
        'contract_info': {
            'id': 'ID',
            'tenant_id': 'IaaS_tenant_id',
            'resource': 'vlan_id',
            'status': 'use_status',
            'task_status': 'task_status'
        }
    },
    'wan_vlan': {
        'total_info': {
            'quota': 'quota',
            'contract_cnt': 'contract_cnt',
            'unavailable_cnt': 'unavailable_cnt',
            'use_cnt': 'use_cnt'
        },
        'contract_info': {
            'id': 'ID',
            'tenant_id': 'IaaS_tenant_id',
            'resource': 'vlan_id',
            'status': 'use_status',
            'task_status': 'task_status'
        }
    }
}

RESOURCE_SCREEN_TRANSITION = {
    'ext_globalip': 'ext_globalip_table',
    'appliances': 'project_base_table',
    'service': 'project_base_table',
    'license': 'license_table',
    'pnf': 'pnf_table',
    'globalip': 'pnf_table',
    'msa_vlan': 'vlan_table',
    'wan_vlan': 'vlan_table',
    'cpu_list': 'pod_list_table',
    'memory_list': 'pod_list_table',
    'storage_list': 'pod_list_table',
    'cpu_detail': 'pod_detail_table',
    'memory_detail': 'pod_detail_table',
    'storage_detail': 'pod_detail_table'
}

RESOURCE_ALL_BUTTONS = [
    'UpdateResourceLink',
    'DeleteResourceAction'
]

# Action buttons that can be displayed in resource
RESOURCE_ALL_BUTTONS = {
    'table': ['CreateResourceAction'],
    'row': ['UpdateResourceLink', 'DeleteResourceAction']
}

# Conditions to display a button for each resource type
RESOURCE_BUTTON_DISPLAY_FOR_TYPE = {
    'appliances': [],
    'service': [],
    'ext_globalip': [
        'CreateResourceAction',
        'UpdateResourceLink',
        'DeleteResourceAction'
    ]
}

# Conditions to display a button for each resource type
RESOURCE_BUTTON_DISPLAY_FOR_STATUS = {
    '0': [
        'UpdateResourceLink',
        'DeleteResourceAction'
    ],
    '1': [
        'UpdateResourceLink'
    ],
    '2': [],
    '3': [],
}

# Information to be displayed on the detail screen of the service
RESOURCE_DETAIL_DISPLAY_COLUMNS = {
    'license': {
        'detail': [
            ['Max', 'quota'],
            ['Contract Count', 'contract_cnt'],
            ['Used Count', 'use_cnt'],
            ['Unavailable Count', 'unavailable_cnt']
        ]
    },
    'pnf_gip': {
        'detail': [
            ['Max', 'quota'],
            ['Contract Count', 'contract_cnt'],
            ['Used Count', 'use_cnt'],
            ['Unavailable Count', 'unavailable_cnt']
        ]
    },
    'vlan_id': {
        'detail': [
            ['Max', 'quota'],
            ['Contract Count', 'contract_cnt'],
            ['Used Count', 'use_cnt'],
            ['Unavailable Count', 'unavailable_cnt']
        ]
    },
    'pod_list': {
        'detail': [
            ['Max', 'quota'],
            ['Used Count', 'use_cnt']
        ]
    },
    'pod_detail': {
        'detail': [
            ['Max', 'quota'],
            ['Used Count', 'use_cnt']
        ]
    }
}

# Information to be displayed at the service of the creation screen
RESOURCE_CREATE_COLUMNS_DEF = {
    'ext_globalip':{
        'create_type': 'globalip_payout',
        'method': 'update',
        'common': [
            (
                'resource_kind',
                {
                    'field': 'CharField',
                    'label': _('Type'),
                    'required': True,
                    'choices': [],
                    'widget': {
                        'readonly': 'readonly'
                    }
                }
            ),
            (
                'count',
                {
                    'field': 'IntegerField',
                    'label': _('Num'),
                    'required': True,
                    'min_value': 1,
                    'initial': 1
                }
            )
        ],
        'separate': [
        ]
    }
}


RESOURCE_UPDATE_COLUMNS_DEF = {
    'change_status': {
        'display_type': 'input_column',
        'method': 'update',
        'common': [
            (
                'status',
                {
                    'field': 'ChoiceField',
                    'label': 'Status',
                    'required': True,
                    'choices': [
                        ('0', 'Unused'),
                        ('2', 'Used')
                    ],
                    'widget': {
                        'class': 'sub_switchable',
                        'id': 'status'
                    }
                }
            )
        ],
        'separate': [
            (
                'node_id',
                {
                    'field': 'ChoiceField',
                    'label': 'Node',
                    'required': True,
                    'choices': [],
                    'input_type': [
                        '1', '2'
                    ]
                }
            )
        ]
    }
}
