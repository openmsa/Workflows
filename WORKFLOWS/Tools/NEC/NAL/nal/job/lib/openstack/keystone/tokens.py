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


class OscTokens(base.OscKeystoneBase):

    def create_token(self,
                user_name, password, endpoint_url, domain=''):

        # Check Input Parameters
        if len(user_name) == 0 or len(password) == 0 \
                            or len(endpoint_url) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Set Parameters(Rest)
        url = endpoint_url + '/auth/tokens'
        param = self.__set_token_default_params(user_name, password, domain)

        # Execute Rest
        passwords = self.utils.json_encode_passwords([password])
        resp = self.rest.rest_post_token_v3(url, '', param, {}, passwords)

        # Get Token ID
        token_id = resp['token']

        return  token_id

    def get_endpoints(self, endpoint_url,
                      token_id, user_name, password,
                      tenant_id, domain=''):

        # Check Input Parameters
        if len(endpoint_url) == 0 or len(token_id) == 0 \
            or len(user_name) == 0 or len(password) == 0 \
            or len(tenant_id) == 0:

            raise SystemError(self.EXCEPT_MSG01)

        # Set Parameters(Rest)
        url = endpoint_url + '/auth/tokens'
        param = self.__set_token_default_params(user_name, password, domain)

        if len(tenant_id) > 0:
            param['auth']['scope'] = {'project': {'id': tenant_id}}

        # Execute Rest
        passwords = self.utils.json_encode_passwords([password])
        resp = self.rest.rest_post_token_v3(
                                    url, token_id, param, {}, passwords)

        # Check Response From OpenStack
        if 'token' not in resp['params']:
            raise SystemError(self.EXCEPT_MSG12)

        resp['params']['token']['id'] = resp['token']

        return resp['params']

    def __set_token_default_params(self, user_name, password, domain):

        if len(domain) == 0:
            domain = self.DOMAIN_NAME_DEFAULT

        return {'auth': {
                    'identity': {
                            'methods': ['password'],
                            'password': {
                                'user': {
                                    'name': user_name,
                                    'domain': {'name': domain},
                                    'password': password, }}}}}
