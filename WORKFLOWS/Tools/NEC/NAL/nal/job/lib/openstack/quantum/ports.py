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


class OscQuantumPorts(base.OscQuantumBase):

    def list_ports(self, endpoint_array):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/ports'

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'ports' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def get_port(self, endpoint_array, port_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(port_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/ports/' + port_id

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'port' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def create_port(self, endpoint_array,
                                network_id,
                                name='',
                                admin_state_up=True,
                                fixed_ips_subnet_id='',
                                fixed_ips_ip_address='',
                                mac_address='',
                                port_security_enabled=None,
                                device_id='',
                                device_owner='',
                                security_groups=[],
                                binding_host_id='',
                                binding_vnic_type=''):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(network_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/ports'

        params = {
            'port': {
                'network_id': network_id,
                'admin_state_up': admin_state_up,
            }
        }

        if len(name) > 0:
            params['port']['name'] = name

        fixed_params = {}
        if len(fixed_ips_subnet_id) > 0:
            fixed_params['subnet_id'] = fixed_ips_subnet_id

        if len(fixed_ips_ip_address) > 0:
            fixed_params['ip_address'] = fixed_ips_ip_address

        if len(fixed_params) > 0:
            params['port']['fixed_ips'] = [fixed_params]

        if len(mac_address) > 0:
            params['port']['mac_address'] = mac_address

        if len(device_id) > 0:
            params['port']['device_id'] = device_id

        if len(device_owner) > 0:
            params['port']['device_owner'] = device_owner

        if len(security_groups) > 0:
            params['port']['security_groups'] = security_groups

        if len(binding_host_id) > 0:
            params['port']['binding:host_id'] = binding_host_id

        if len(binding_vnic_type) > 0:
            params['port']['binding:vnic_type'] = binding_vnic_type

        if port_security_enabled is not None:
            params['port']['port_security_enabled'] = port_security_enabled

        # Execute Rest
        resp = self.rest.rest_post(url, token_id, params)

        # Check Response From OpenStack
        if 'port' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def create_port_dual_stack(self, endpoint_array,
                                network_id,
                                name='',
                                admin_state_up=True,
                                fixed_ips=[],
                                mac_address='',
                                port_security_enabled=None,
                                device_id='',
                                device_owner='',
                                security_groups=[],
                                binding_host_id='',
                                binding_vnic_type=''):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(network_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/ports'

        params = {
            'port': {
                'network_id': network_id,
                'admin_state_up': admin_state_up,
            }
        }

        if len(name) > 0:
            params['port']['name'] = name

        if len(fixed_ips) > 0:
            params['port']['fixed_ips'] = fixed_ips

        if len(mac_address) > 0:
            params['port']['mac_address'] = mac_address

        if len(device_id) > 0:
            params['port']['device_id'] = device_id

        if len(device_owner) > 0:
            params['port']['device_owner'] = device_owner

        if len(security_groups) > 0:
            params['port']['security_groups'] = security_groups

        if len(binding_host_id) > 0:
            params['port']['binding:host_id'] = binding_host_id

        if len(binding_vnic_type) > 0:
            params['port']['binding:vnic_type'] = binding_vnic_type

        if port_security_enabled is not None:
            params['port']['port_security_enabled'] = port_security_enabled

        # Execute Rest
        resp = self.rest.rest_post(url, token_id, params)

        # Check Response From OpenStack
        if 'port' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def update_port(self, endpoint_array, port_id,
                                        name=None,
                                        admin_state_up=None,
                                        fixed_ips=None,
                                        mac_address=None,
                                        device_id=None,
                                        device_owner=None,
                                        security_groups=None,
                                        binding_host_id=None,
                                        binding_vnic_type=None):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(port_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/ports/' + port_id

        params = {'port': {}}

        if name is not None:
            params['port']['name'] = name

        if admin_state_up is not None:
            params['port']['admin_state_up'] = admin_state_up

        if fixed_ips is not None:
            params['port']['fixed_ips'] = fixed_ips

        if mac_address is not None:
            params['port']['mac_address'] = mac_address

        if device_id is not None:
            params['port']['device_id'] = device_id

        if device_owner is not None:
            params['port']['device_owner'] = device_owner

        if security_groups is not None:
            params['port']['security_groups'] = security_groups

        if binding_host_id is not None:
            params['port']['binding:host_id'] = binding_host_id

        if binding_vnic_type is not None:
            params['port']['binding:vnic_type'] = binding_vnic_type

        # Execute Rest
        resp = self.rest.rest_put(url, token_id, params)

        # Check Response From OpenStack
        if 'port' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def detach_port_device(self, endpoint_array, port_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(port_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/ports/' + port_id

        params = {
            'port': {
                'device_owner': '',
                'device_id': '',
            }
        }

        # Execute Rest
        resp = self.rest.rest_put(url, token_id, params)

        # Check Response From OpenStack
        if 'port' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def delete_port(self, endpoint_array, port_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(port_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/ports/' + port_id

        # Execute Rest
        resp = self.rest.rest_delete(url, token_id, None)

        # Check Response From OpenStack
        if resp != None and len(resp) > 0:
            raise SystemError(self.EXCEPT_MSG12)

        return resp
