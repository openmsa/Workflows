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


class OscQuantumNetworks(base.OscQuantumBase):

    PROVIDER_NETWORK_TYPE_VXLAN = 'vxlan'
    PROVIDER_NETWORK_TYPE_VLAN = 'vlan'
    PROVIDER_PHYSICAL_NETWORK = 'physnet'

    def list_networks(self, endpoint_array):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/networks'

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'networks' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def get_network(self, endpoint_array, network_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(network_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/networks/' + network_id

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'network' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def create_network(self, endpoint_array, name,
                    admin_state_up=True, shared=False, segmentation_id=None,
                    physical_network_name=None, port_security_enabled=None):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(name) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/networks'

        params = {
            'network': {
                'name': name,
                'admin_state_up': admin_state_up,
                'shared': shared,
            }
        }

        if segmentation_id is not None:
            if physical_network_name == None:
                physical_network_name = self.PROVIDER_PHYSICAL_NETWORK
            params['network'][
                'provider:network_type'] = self.PROVIDER_NETWORK_TYPE_VLAN
            params['network'][
                'provider:segmentation_id'] = segmentation_id
            params['network'][
                'provider:physical_network'] = physical_network_name

        if port_security_enabled is not None:
            params['network'][
                'port_security_enabled'] = port_security_enabled

        # Execute Rest
        resp = self.rest.rest_post(url, token_id, params)

        # Check Response From OpenStack
        if 'network' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def delete_network(self, endpoint_array, network_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(network_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/networks/' + network_id

        # Execute Rest
        resp = self.rest.rest_delete(url, token_id, None)

        # Check Response From OpenStack
        if resp != None and len(resp) > 0:
            raise SystemError(self.EXCEPT_MSG12)

        return resp
