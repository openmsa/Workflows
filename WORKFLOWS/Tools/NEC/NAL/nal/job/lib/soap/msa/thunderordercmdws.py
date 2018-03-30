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
import inspect

from job.lib.soap.msa import base


class ThunderOrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        'create_thunder_login': 'A10ThunderApiLogin',
        'delete_thunder_login': 'A10ThunderApiLogin',
        'create_thunder_partition': 'A10ThunderApiPartition',
        'delete_thunder_partition': 'A10ThunderApiPartition',
        'create_thunder_move_partition': 'A10ThunderApiMovePartition',
        'delete_thunder_move_partition': 'A10ThunderApiMovePartition',
        'create_thunder_vlan': 'A10ThunderApiVlan',
        'delete_thunder_vlan': 'A10ThunderApiVlan',
        'create_thunder_set_ip': 'A10ThunderApiSetIp',
        'delete_thunder_set_ip': 'A10ThunderApiSetIp',
        'create_thunder_save': 'A10ThunderApiSave',
        'delete_thunder_save': 'A10ThunderApiSave',
        'create_thunder_vrrp': 'A10ThunderApiVrrp',
        'delete_thunder_vrrp': 'A10ThunderApiVrrp',
        'create_thunder_manage': 'A10ThunderApiManagement',
        'create_thunder_static_route': 'A10ThunderApiStaticRoute',
        'delete_thunder_static_route': 'A10ThunderApiStaticRoute',
        'create_thunder_user': 'A10ThunderApiUser',
        'delete_thunder_user': 'A10ThunderApiUser',
        'create_thunder_api_set_ipv6': 'A10ThunderApiSetIpv6',
        'delete_thunder_api_set_ipv6': 'A10ThunderApiSetIpv6',
        'create_thunder_api_vrrpv6': 'A10ThunderApiVrrpv6',
        'delete_thunder_api_vrrpv6': 'A10ThunderApiVrrpv6',
        'create_thunder_api_static_routev6': 'A10ThunderApiStaticRoutev6',
        'delete_thunder_api_static_routev6': 'A10ThunderApiStaticRoutev6',
    }

    def __init__(self, api_config_instance,
                 nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def create_thunder_login(self, device_id, object_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_login(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id
        }

        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_partition(self, device_id, object_id, session_id,
                                 partition_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
            'partition_id': partition_id,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_partition(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_move_partition(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_move_partition(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_vlan(self, device_id, object_id, session_id,
                                                port_number):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
            'port_number': port_number,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_vlan(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_set_ip(self, device_id, object_id, session_id,
                                                        subnet_mask,
                                                        vlan_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
            'subnet_mask': subnet_mask,
            'vlan_id': vlan_id,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_set_ip(self, device_id, object_id, session_id,
                                                            vlan_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
            'vlan_id': vlan_id,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_save(self, device_id, object_id):

        client_name = inspect.currentframe().f_code.co_name

        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_save(self, device_id, object_id):

        client_name = inspect.currentframe().f_code.co_name

        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_vrrp(self, device_id, object_id, session_id,
                                                        enable_password,
                                                        preempt_mode,
                                                        vrid,
                                                        vrrp_priority):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
            'enable_password': enable_password,
            'preempt_mode': preempt_mode,
            'vrid': vrid,
            'vrrp_priority': vrrp_priority
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        passwords = [enable_password]
        self.output_log_soap_params(
                    'in', __name__, client_name, msa_params, passwords)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params(
                    'out', __name__, client_name, msa_result, passwords)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_vrrp(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_manage(self, device_id, object_id, enable_password,
                              session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'enable_password': enable_password,
            'session_id': session_id
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        passwords = [enable_password]
        self.output_log_soap_params(
                    'in', __name__, client_name, msa_params, passwords)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params(
                    'out', __name__, client_name, msa_result, passwords)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_static_route(self, device_id, object_id,
                                                     gateway,
                                                     session_id,
                                                     subnet_mask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'gateway': gateway,
            'session_id': session_id,
            'subnet_mask': subnet_mask
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_static_route(self, device_id, object_id,
                                                     gateway,
                                                     session_id,
                                                     subnet_mask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'gateway': gateway,
            'session_id': session_id,
            'subnet_mask': subnet_mask
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_user(self, device_id, object_id, session_id,
                                            partition_name,
                                            password,
                                            role_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
            'partition_name': partition_name,
            'password': password,
            'role_name': role_name,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        passwords = [password]
        self.output_log_soap_params(
                        'in', __name__, client_name, msa_params, passwords)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params(
                        'out', __name__, client_name, msa_result, passwords)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_user(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_api_set_ipv6(self, device_id, object_id,
                                                     ipv6_address,
                                                     ipv6_prefix_length,
                                                     session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': [
                {
                    'ipv6_address': ipv6_address,
                    'ipv6_prefix_length': ipv6_prefix_length,
                }
             ],
            'session_id': session_id
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_api_set_ipv6(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_api_vrrpv6(self, device_id, object_id,
                                                   enable_password,
                                                   session_id,
                                                   preempt_mode,
                                                   vrid,
                                                   vrrp_priority):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'enable_password': enable_password,
            'session_id': session_id,
            'preempt_mode': preempt_mode,
            'vrid': vrid,
            'vrrp_priority': vrrp_priority
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_api_vrrpv6(self, device_id, object_id, session_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'session_id': session_id,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_thunder_api_static_routev6(self, device_id, object_id,
                                                           gateway,
                                                           session_id,
                                                           vlan_id,
                                                           prefix):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'gateway': gateway,
            'session_id': session_id,
            'vlan_id': vlan_id,
            'prefix': prefix
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_thunder_api_static_routev6(self, device_id, object_id,
                                                           gateway,
                                                           session_id,
                                                           prefix):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'gateway': gateway,
            'session_id': session_id,
            'prefix': prefix
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}
