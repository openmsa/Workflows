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


class OscUsers(base.OscKeystoneBase):

    def list_users(self, endpoint_array, domain_id=None):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Parameters(Rest)
        querys = {}

        if domain_id is not None:
            querys = {'domain_id': domain_id}

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/users'

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_get(url, token_id, {}, querys)

        # Check Response From OpenStack
        if 'users' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def get_user(self, endpoint_array, user_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(user_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/users/' + user_id

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'user' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def create_user(self, endpoint_array, user_name, password, tenant_id,
                            email=None, enabled=True, domain_id=''):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(user_name) == 0 \
                        or len(password) == 0 or len(tenant_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Parameters(Rest)
        params = {
            'user': {
                'name': user_name,
                'password': password,
                'default_project_id': tenant_id,
                'enabled': enabled,
                'domain_id': domain_id,
            }
        }

        if len(params['user']['domain_id']) == 0:
            params['user']['domain_id'] = self.DOMAIN_ID_DEFAULT

        if email is not None:
            params['user']['email'] = email

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/users'

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        passwords = self.utils.json_encode_passwords([password])
        resp = self.rest.rest_post(url, token_id, params, {}, passwords)

        # Check Response From OpenStack
        if 'user' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def update_user(self, endpoint_array, user_id,
                    tenant_id=None, user_name=None,
                    email=None, password=None, enabled=None, domain_id=None):

        passwords = []

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(user_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Parameters(Rest)
        params = {'user': {}}

        if tenant_id is not None:
            params['user']['default_project_id'] = tenant_id

        if user_name is not None:
            params['user']['name'] = user_name

        if email is not None:
            params['user']['email'] = email

        if password is not None:
            params['user']['password'] = password
            passwords = self.utils.json_encode_passwords([password])

        if enabled is not None:
            params['user']['enabled'] = enabled

        if domain_id is not None:
            params['user']['domain_id'] = domain_id

        if len(params['user']) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/users/' + user_id

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_patch(url, token_id, params, {}, passwords)

        # Check Response From OpenStack
        if 'user' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def delete_user(self, endpoint_array, user_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(user_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Endpoint URL
        url = self.get_endpoint(endpoint_array)
        url += '/users/' + user_id

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Execute Rest
        resp = self.rest.rest_delete(url, token_id)

        # Check Response From OpenStack
        if resp != None and len(resp) > 0:
            raise SystemError(self.EXCEPT_MSG12)

        return resp
