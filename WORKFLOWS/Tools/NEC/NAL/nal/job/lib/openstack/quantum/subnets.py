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
from job.lib.openstack.quantum import base


class OscQuantumSubnets(base.OscQuantumBase):

    def list_subnets(self, endpoint_array):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/subnets'

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'subnets' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def get_subnet(self, endpoint_array, subnet_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(subnet_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/subnets/' + subnet_id

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'subnet' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def create_subnet(self, endpoint_array,
                                network_id,
                                cidr,
                                name='',
                                tenant_id='',
                                ip_version='4',
                                gateway_ip=None,
                                enable_dhcp=False,
                                allocation_pools=[],
                                host_routes=[],
                                dns_nameservers=[]):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(network_id) == 0 or len(cidr) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/subnets'

        params = {
            'subnet': {
                'network_id': network_id,
                'cidr': cidr,
                'ip_version': ip_version,
                'gateway_ip': gateway_ip,
                'enable_dhcp': enable_dhcp,
            }
        }

        if len(name) > 0:
            params['subnet']['name'] = name

        if len(tenant_id) > 0:
            params['subnet']['project_id'] = tenant_id

        if len(allocation_pools) > 0:
            params['subnet']['allocation_pools'] = allocation_pools

        if len(host_routes) > 0:
            params['subnet']['host_routes'] = host_routes

        if len(dns_nameservers) > 0:
            params['subnet']['dns_nameservers'] = dns_nameservers

        # Execute Rest
        resp = self.rest.rest_post(url, token_id, params)

        # Check Response From OpenStack
        if 'subnet' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def delete_subnet(self, endpoint_array, subnet_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(subnet_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/subnets/' + subnet_id

        # Execute Rest
        resp = self.rest.rest_delete(url, token_id, None)

        # Check Response From OpenStack
        if resp != None and len(resp) > 0:
            raise SystemError(self.EXCEPT_MSG12)

        return resp
