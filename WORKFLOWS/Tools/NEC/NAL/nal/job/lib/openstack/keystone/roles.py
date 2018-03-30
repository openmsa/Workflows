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


class OscRoles(base.OscKeystoneBase):

    def list_roles(self, endpoint_array, role_name=None, domain_id=None):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Parameters(Rest)
        querys = {}
        if role_name is not None:
            querys['name'] = role_name
        if domain_id is not None:
            querys['domain_id'] = domain_id

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/roles'

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_get(
                        url, token_id, {}, querys)

        # Check Response From OpenStack
        if 'roles' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def list_roles_for_user(self, endpoint_array, user_id, tenant_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 \
                or len(user_id) == 0 or len(tenant_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/projects/' + tenant_id + '/users/' + user_id + '/roles'

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'roles' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def add_role_to_user(self, endpoint_array, user_id, tenant_id, role_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(user_id) == 0 \
                or len(tenant_id) == 0 or len(role_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/projects/' + tenant_id + '/users/' + user_id
        url += '/roles/' + role_id

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_put(url, token_id)

        # Check Response From OpenStack
        if resp != None and len(resp) > 0:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def remove_role_from_user(self,
                            endpoint_array, user_id, tenant_id, role_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(user_id) == 0 \
                        or len(tenant_id) == 0 or len(role_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/projects/' + tenant_id + '/users/' + user_id
        url += '/roles/' + role_id

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_delete(url, token_id)

        # Check Response From OpenStack
        if resp != None and len(resp) > 0:
            raise SystemError(self.EXCEPT_MSG12)

        return resp
