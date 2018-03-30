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
from job.lib.common import utils
from job.lib.openstack.common import rest


class OpenstackClientBase:

    # Exception Message
    EXCEPT_MSG01 = 'error args key'
    EXCEPT_MSG02 = 'error GET REST I/F'
    EXCEPT_MSG03 = 'error POST REST I/F'
    EXCEPT_MSG04 = 'error PUT REST I/F'
    EXCEPT_MSG05 = 'error DELETE REST I/F'
    EXCEPT_MSG06 = 'error memcached of token id'
    EXCEPT_MSG07 = 'error memcached of endpoint'
    EXCEPT_MSG08 = 'error ENDPOINT was not found.'
    EXCEPT_MSG08 += ' Probably, you do not have authority.'
    EXCEPT_MSG09 = 'error OpenStack Non Response'
    EXCEPT_MSG10 = 'error memcached set'
    EXCEPT_MSG11 = 'error update quotas'
    EXCEPT_MSG12 = 'error OpenStack Abnormal Response returned'

    # Domain Name(Default)
    DOMAIN_NAME_DEFAULT = 'Default'
    DOMAIN_ID_DEFAULT = 'default'

    # Admin Role Name
    ROLE_NAME_ADMIN = 'admin'

    # Service Catalog Name
    SERVICE_CATALOG_KEYSTONE = 'keystone'
    SERVICE_CATALOG_NOVA = 'nova'
    SERVICE_CATALOG_QUANTUM = 'quantum'
    SERVICE_CATALOG_NEUTRON = 'neutron'

    ERROR_RESP_KEY = 'error'

    def __init__(self, api_config_instance):
        self.utils = utils.Utils()
        self.rest = rest.OscRest(api_config_instance)
        self.char_code = api_config_instance.CHAR_SET

    def get_token_id(self, endpoint_array):

        try:

            token_id = endpoint_array['token']['id']
            return token_id

        except IndexError:
            raise SystemError(self.EXCEPT_MSG06)

        except:
            raise

    def get_endpoint(self, endpoint_array, admin_roles, catalog_names):

        url = ''
        roles = endpoint_array['token']['roles']
        catalogs = endpoint_array['token']['catalog']
        interface_public = 'public'
        interface_admin = 'admin'
        region_id = endpoint_array['region_id']

        # Judge Role
        interface = interface_public
        for role in roles:
            role_name = role.get('name')
            if len(role_name) > 0 and role_name in admin_roles:
                interface = interface_admin
                break

        # Get Endpoint
        for catalog in catalogs:
            if catalog['name'] in catalog_names:
                for endpoint in catalog['endpoints']:
                    if endpoint['region'] == region_id \
                        and endpoint['interface'] == interface:
                        url = endpoint['url']
                        break
                break

        return url
