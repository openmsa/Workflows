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
from job.lib.openstack.keystone import base


class OscTenants(base.OscKeystoneBase):

    def list_tenants(self, endpoint_array):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/projects'

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'projects' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def get_tenant(self, endpoint_array, tenant_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(tenant_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/projects/' + tenant_id

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'project' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def create_tenant(self, endpoint_array, tenant_name,
            description='', enabled=True, domain_id='', is_domain=None):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(tenant_name) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Parameters(Rest)
        params = {
            'project': {
                'name': tenant_name,
                'description': description,
                'enabled': enabled,
                'domain_id': domain_id,
            }
        }

        if len(params['project']['domain_id']) == 0:
            params['project']['domain_id'] = self.DOMAIN_ID_DEFAULT

        if is_domain is not None:
            params['project']['is_domain'] = is_domain

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/projects'

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_post(url, token_id, params)

        # Check Response From OpenStack
        if 'project' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def update_tenant(self, endpoint_array, tenant_id,
                      tenant_name=None, description=None, enabled=None,
                      domain_id=None, is_domain=None):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(tenant_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Parameters(Rest)
        params = {'project': {}}

        if tenant_name is not None:
            params['project']['name'] = tenant_name

        if description is not None:
            params['project']['description'] = description

        if enabled is not None:
            params['project']['enabled'] = enabled

        if domain_id is not None:
            params['project']['domain_id'] = domain_id

        if is_domain is not None:
            params['project']['is_domain'] = is_domain

        if len(params['project']) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/projects/' + tenant_id

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_patch(url, token_id, params)

        # Check Response From OpenStack
        if 'project' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def delete_tenant(self, endpoint_array, tenant_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(tenant_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/projects/' + tenant_id

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_delete(url, token_id)

        # Check Response From OpenStack
        if resp != None and len(resp) > 0:
            raise SystemError(self.EXCEPT_MSG12)

        return resp
