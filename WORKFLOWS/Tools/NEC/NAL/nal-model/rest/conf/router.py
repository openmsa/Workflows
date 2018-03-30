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

# Router Definition(Classname & Methodname & Tablename)
CLASS_METHOD_TABLE = {

    # NAL_POD_MNG
    'pods': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_POD_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_POD_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_POD_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_POD_MNG'
        }
    },
    # NAL_POD_MNG
    'vxlangw-pods': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_VXLANGW_POD_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_VXLANGW_POD_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_VXLANGW_POD_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_VXLANGW_POD_MNG'
        }
    },
    # NAL_TENANT_MNG
    'tenants': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_TENANT_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_TENANT_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_TENANT_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_TENANT_MNG'
        }
    },
    # NAL_VIRTUAL_LAN_MNG
    'vlans': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_VIRTUAL_LAN_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_VIRTUAL_LAN_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_VIRTUAL_LAN_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_VIRTUAL_LAN_MNG'
        }
    },
    # NAL_PORT_MNG
    'ports': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_PORT_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_PORT_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_PORT_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_PORT_MNG'
        }
    },
    # NAL_APL_MNG
    'appliances': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_APL_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_APL_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_APL_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_APL_MNG'
        }
    },
    # NAL_THRESHOLD_MNG
    'thresholds': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_THRESHOLD_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_THRESHOLD_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_THRESHOLD_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_THRESHOLD_MNG'
        }
    },
    # NAL_TENANT_CONTRACT_MNG
    'contracts': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_TENANT_CONTRACT_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_TENANT_CONTRACT_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_TENANT_CONTRACT_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_TENANT_CONTRACT_MNG'
        }
    },
    # NAL_MSA_VLAN_MNG
    'msa-vlan': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_MSA_VLAN_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_MSA_VLAN_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_MSA_VLAN_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_MSA_VLAN_MNG'
        }
    },
    # NAL_PNF_VLAN_MNG
    'pnf-vlan': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_PNF_VLAN_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_PNF_VLAN_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_PNF_VLAN_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_PNF_VLAN_MNG'
        }
    },
    # NAL_GLOBAL_IP_MNG
    'global-ip-addresses': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_GLOBAL_IP_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_GLOBAL_IP_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_GLOBAL_IP_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_GLOBAL_IP_MNG'
        }
    },
    # NAL_LICENSE_MNG
    'licenses': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_LICENSE_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_LICENSE_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_LICENSE_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_LICENSE_MNG'
        }
    },
    # NAL_DEVICE_ENDPOINT_MNG
    'nal-endpoints': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_DEVICE_ENDPOINT_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_DEVICE_ENDPOINT_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_DEVICE_ENDPOINT_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_DEVICE_ENDPOINT_MNG'
        }
    },
    # NAL_CONFIG_MNG
    'nal-configs': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'NAL_CONFIG_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'NAL_CONFIG_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'NAL_CONFIG_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'NAL_CONFIG_MNG'
        }
    },
    # NAL_DC_MNG
    'dcs': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'WIM_DC_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'WIM_DC_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'WIM_DC_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'WIM_DC_MNG'
        }
    },
    # WIM_DC_CONNECT_GROUP_MNG
    'dc-con-groups': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'WIM_DC_CONNECT_GROUP_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'WIM_DC_CONNECT_GROUP_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'WIM_DC_CONNECT_GROUP_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'WIM_DC_CONNECT_GROUP_MNG'
        }
    },
    # WIM_DC_VLAN_MNG
    'dc-vlans': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'WIM_DC_VLAN_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'WIM_DC_VLAN_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'WIM_DC_VLAN_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'WIM_DC_VLAN_MNG'
        }
    },
    # WIM_DC_CONNECT_MEMBER_MNG
    'dc-con-members': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'WIM_DC_CONNECT_MEMBER_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'WIM_DC_CONNECT_MEMBER_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'WIM_DC_CONNECT_MEMBER_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'WIM_DC_CONNECT_MEMBER_MNG'
        }
    },
    # WIM_DEVICE_ENDPOINT_MNG
    'wim-endpoints': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'WIM_DEVICE_ENDPOINT_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'WIM_DEVICE_ENDPOINT_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'WIM_DEVICE_ENDPOINT_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'WIM_DEVICE_ENDPOINT_MNG'
        }
    },
    # WIM_CONFIG_MNG
    'wim-configs': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'WIM_CONFIG_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'WIM_CONFIG_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'WIM_CONFIG_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'WIM_CONFIG_MNG'
        }
    },
    # WIM_DC_SEGMENT_MNG
    'dc-segment': {
        'GET': {
            'moduleName': 'select',
            'className': 'Select',
            'methodName': 'execute',
            'tableName': 'WIM_DC_SEGMENT_MNG'
        },
        'POST': {
            'moduleName': 'insert',
            'className': 'Insert',
            'methodName': 'execute',
            'tableName': 'WIM_DC_SEGMENT_MNG'
        },
        'PUT': {
            'moduleName': 'update',
            'className': 'Update',
            'methodName': 'execute',
            'tableName': 'WIM_DC_SEGMENT_MNG'
        },
        'DELETE': {
            'moduleName': 'delete',
            'className': 'Delete',
            'methodName': 'execute',
            'tableName': 'WIM_DC_SEGMENT_MNG'
        }
    }
}
