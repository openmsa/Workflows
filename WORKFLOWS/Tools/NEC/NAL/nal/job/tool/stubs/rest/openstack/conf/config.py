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
CHAR_SET = 'utf-8'
SCRIPT_STDOUT_SEPARATER = '\r\n'

OS_USER_ID_ADMIN = '4034dbce1e3946dbba822288baa330d3'
OS_USER_NAME_ADMIN = 'admin'
OS_NETWORK_SEGMENT_ID_INI = 1000
OS_NETWORK_MTU = 0
OS_SERVER_PROGRESS = 0
OS_EXT_STS_POWER_STATE = 1
OS_EXT_STS_VM_STATE = 'active'
OS_EXT_IPS_TYPE = 'fixed'
OS_SERVER_STATUS = 'ACTIVE'
OS_NETWORK_STATUS = 'ACTIVE'
OS_VIF_TYPE = 'unbound'
OS_PORT_STATUS = 'DOWN'
OS_HOST_ID = 'a709afe49269d847a21da12cd0b03830485519d28969864c69912355'
OS_VNIC_TYPE = 'normal'
OS_AVAILABILITY_ZONE = 'nova'
OS_DCF_DISK_CONFIG = 'MANUAL'
OS_HOST_NAME = 'rhel7-kilo-dev7069'
OS_VNC_CONSOLE_GET_URI = '/vnc_auto.html?token='
OS_VNC_CONSOLE_KEYNAME = 'os-getVNCConsole'

# HTTP Status Definition
HTTP_STATUS_DEF = {
    'OK': '200 OK',
    'NOTFOUND': '404 Not Found',
    'ERROR': '500 Internal Server Error',
}

# OpenStack Response Definition
OS_RESPONSE_DEF = {
        # token
        'create_token': {
            'file': 'POST@v3@auth@tokens',
        },

        # tenant(project)
        'list_tenants': {
            'file': 'GET@v3@projects',
            'resp': '{"links": {}, "projects": []}',
        },
        'get_tenant': {
            'file': 'GET@v3@projects@%project_id%',
        },
        'create_tenant': {
            'file': 'POST@v3@projects',
        },
        'update_tenant': {
            'file': 'PATCH@v3@projects@%project_id%',
            'rexp': '^PATCH@v3@projects@([^@]+)$',
        },
        'delete_tenant': {
            'file': 'DELETE@v3@projects@%project_id%',
            'rexp': '^DELETE@v3@projects@([^@]+)$',
        },

        # user
        'list_users': {
            'file': 'GET@v3@users',
            'resp': '{"links": {}, "users": []}',
        },
        'get_user': {
            'file': 'GET@v3@users@%user_id%',
        },
        'create_user': {
            'file': 'POST@v3@users',
            'resp': '{"user": {"default_project_id": "", "domain_id": "default", "email": "", "enabled": true, "id": "", "links": {"self": ""}, "name": "", "password_expires_at": null}}',
        },
        'update_user': {
            'file': 'PATCH@v3@users@%user_id%',
            'rexp': '^PATCH@v3@users@([^@]+)$',
        },
        'delete_user': {
            'file': 'DELETE@v3@users@%user_id%',
            'rexp': '^DELETE@v3@users@([^@]+)$',
        },

        # role
        'list_roles': {
            'file': 'GET@v3@roles',
        },
        'list_roles_for_user': {
            'file': 'GET@v3@projects@%project_id%@users@%user_id%@roles',
            'rexp': '^GET@v3@projects@([^@]+)@users@([^@]+)@roles$',
            'resp': '{"links": {}, "roles": []}',
        },
        'add_role_to_user': {
            'file': 'PUT@v3@projects@%project_id%@users@%user_id%@roles@%role_id%',
            'rexp': '^PUT@v3@projects@([^@]+)@users@([^@]+)@roles@([^@]+)$',
        },
        'remove_role_from_user': {
            'file': 'DELETE@v3@projects@%project_id%@users@%user_id%@roles@%role_id%',
            'rexp': '^DELETE@v3@projects@([^@]+)@users@([^@]+)@roles@([^@]+)$',
        },

        # network
        'list_networks': {
            'file': 'GET@v2.0@networks',
            'resp': '{"networks": []}',
        },
        'create_network': {
            'file': 'POST@v2.0@networks',
        },
        'get_network': {
            'file': 'GET@v2.0@networks@%network_id%',
        },
        'delete_network': {
            'file': 'DELETE@v2.0@networks@%network_id%',
            'rexp': '^DELETE@v2\.0@networks@([^@]+)$',
        },

        # subnet
        'list_subnets': {
            'file': 'GET@v2.0@subnets',
            'resp': '{"subnets": []}',
        },
        'create_subnet': {
            'file': 'POST@v2.0@subnets',
        },
        'get_subnet': {
            'file': 'GET@v2.0@subnets@%subnet_id%',
        },
        'delete_subnet': {
            'file': 'DELETE@v2.0@subnets@%subnet_id%',
            'rexp': '^DELETE@v2\.0@subnets@([^@]+)$',
        },

        # port
        'list_ports': {
            'file': 'GET@v2.0@ports',
            'resp': '{"ports": []}',
        },
        'create_port': {
            'file': 'POST@v2.0@ports',
        },
        'get_port': {
            'file': 'GET@v2.0@ports@%port_id%',
        },
        'update_port': {
            'file': 'PUT@v2.0@ports@%port_id%',
            'rexp': '^PUT@v2\.0@ports@([^@]+)$',
        },
        'delete_port': {
            'file': 'DELETE@v2.0@ports@%port_id%',
            'rexp': '^DELETE@v2\.0@ports@([^@]+)$',
        },

        # server(instance)
        'list_servers': {
            'file': 'GET@v2.1@%project_id%@servers@detail',
            'resp': '{"servers":[]}',
            'rexp': '^GET@v2\.1@([^@]+)@servers@detail$',
        },
        'get_server': {
            'file': 'GET@v2.1@%project_id%@servers@%server_id%',
        },
        'create_server': {
            'file': 'POST@v2.1@%project_id%@servers',
            'rexp': '^POST@v2\.1@([^@]+)@servers$',
        },
        'action_server': {
            'file': 'POST@v2.1@%project_id%@servers@%server_id%@action',
            'rexp': '^POST@v2\.1@([^@]+)@servers@([^@]+)@action$',
        },
        'delete_server': {
            'file': 'DELETE@v2.1@%project_id%@servers@%server_id%',
            'rexp': '^DELETE@v2\.1@([^@]+)@servers@([^@]+)$',
        },
        'list_interfaces': {
            'file': 'GET@v2.1@%project_id%@servers@%server_id%@os-interface',
            'resp': '{"interfaceAttachments":[]}',
        },
        'attach_interface': {
            'file': 'POST@v2.1@%project_id%@servers@%server_id%@os-interface',
            'rexp': '^POST@v2\.1@([^@]+)@servers@([^@]+)@os-interface$',
        },
        'detach_interface': {
            'file': 'DELETE@v2.1@%project_id%@servers@%server_id%@os-interface@%port_id%',
            'rexp': '^DELETE@v2\.1@([^@]+)@servers@([^@]+)@os-interface@([^@]+)$',
        },

        # flavor
        'list_flavors': {
            'file': 'GET@v2.1@%project_id%@flavors',
            'rexp': '^GET@v2\.1@([^@]+)@flavors$',
        },
}
