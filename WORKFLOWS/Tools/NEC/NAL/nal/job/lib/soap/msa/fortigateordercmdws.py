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


class FortigateOrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        'create_fortigate_vdom': 'FortiVdomProvPNF',
        'delete_fortigate_vdom': 'FortiVdomProvPNF',
        'create_fortigate_vlan_interface': 'FortiVlanProvPNF',
        'update_fortigate_vlan_interface': 'FortiVlanProvPNF',
        'delete_fortigate_vlan_interface': 'FortiVlanProvPNF',
        'create_fortigate_physical_interface': 'FortiPhysicalIPProvPNF',
        'update_fortigate_physical_interface': 'FortiPhysicalIPProvPNF',
        'delete_fortigate_physical_interface': 'FortiPhysicalIPProvPNF',
        'create_fortigate_admin_profile': 'FortiAdminProfileProvPNF',
        'delete_fortigate_admin_profile': 'FortiAdminProfileProvPNF',
        'create_fortigate_admin_user': 'FortiAdminUserProvPNF',
        'delete_fortigate_admin_user': 'FortiAdminUserProvPNF',
        'create_fortigate_vlan_ipv6_interface': \
                              'FortinetFortigateVlanIpv6Interface',
        'delete_fortigate_vlan_ipv6_interface': \
                              'FortinetFortigateVlanIpv6Interface',
        'create_fortigate_physical_ipv6_interface': \
                              'FortinetFortigatePhysicalIpv6Interface',
        'delete_fortigate_physical_ipv6_interface': \
                              'FortinetFortigatePhysicalIpv6Interface',
    }

    def __init__(self, api_config_instance,
                 nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def create_fortigate_vdom(self, device_id, object_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id,
                        self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_fortigate_vdom(self, device_id, object_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
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

    def create_fortigate_vlan_interface(self, device_id, object_id,
                                            vdom_name,
                                            vlan_id,
                                            ip_address,
                                            netmask,
                                            port_no,
                                            management_flg):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'vdom_name': vdom_name,
                    'vlan_id': vlan_id,
                    'ip_address': ip_address,
                    'netmask': netmask,
                    'port_no': port_no,
                    'management_flg': management_flg,
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

    def update_fortigate_vlan_interface(self, device_id, object_id,
                                            vdom_name,
                                            vlan_id,
                                            ip_address,
                                            netmask,
                                            port_no,
                                            management_flg):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'vdom_name': vdom_name,
                    'vlan_id': vlan_id,
                    'ip_address': ip_address,
                    'netmask': netmask,
                    'port_no': port_no,
                    'management_flg': management_flg,
        }
        msa_params = self.set_msa_cmd_input_params('UPDATE', device_id,
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

    def delete_fortigate_vlan_interface(self, device_id, object_id):

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

    def create_fortigate_physical_interface(self, device_id, object_id,
                                            vdom_name,
                                            ip_address,
                                            netmask,
                                            management_flg):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'vdom_name': vdom_name,
                    'ip_address': ip_address,
                    'netmask': netmask,
                    'management_flg': management_flg,
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

    def update_fortigate_physical_interface(self, device_id, object_id,
                                            vdom_name,
                                            ip_address,
                                            netmask,
                                            management_flg):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'vdom_name': vdom_name,
                    'ip_address': ip_address,
                    'netmask': netmask,
                    'management_flg': management_flg,
        }
        msa_params = self.set_msa_cmd_input_params('UPDATE', device_id,
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

    def delete_fortigate_physical_interface(self, device_id, object_id):

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

    def create_fortigate_admin_profile(self, device_id, object_id,
                                                            profile_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'profile_name': profile_name,
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

    def delete_fortigate_admin_profile(self, device_id, object_id,
                                                            profile_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'profile_name': profile_name,
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

    def create_fortigate_admin_user(self, device_id, object_id,
                                                        vdom_name,
                                                        user_name,
                                                        password,
                                                        admin_prof):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'vdom_name': vdom_name,
                    'user_name': user_name,
                    'password': password,
                    'admin_prof': admin_prof,
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

    def delete_fortigate_admin_user(self, device_id, object_id, user_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'user_name': user_name,
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

    def create_fortigate_vlan_ipv6_interface(self, device_id, object_id,
                                            vdom_name,
                                            vlan_id,
                                            port_no,
                                            management_flg,
                                            ipv6_address,
                                            netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'vdom_name': vdom_name,
            'vlan_id': vlan_id,
            'port_no': port_no,
            'management_flg': management_flg,
            'interface': [
                {
                    'ipv6_address': ipv6_address,
                    'netmask': netmask,
                }
            ],
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

    def delete_fortigate_vlan_ipv6_interface(self, device_id, object_id):

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

    def create_fortigate_physical_ipv6_interface(self, device_id, object_id,
                                            vdom_name,
                                            management_flg,
                                            ipv6_address,
                                            netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'vdom_name': vdom_name,
            'management_flg': management_flg,
            'interface': [
                {
                    'ipv6_address': ipv6_address,
                    'netmask': netmask,
                }
            ],
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

    def delete_fortigate_physical_ipv6_interface(self, device_id, object_id,
                                            ipv6_address,
                                            netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': [
                {
                    'ipv6_address': ipv6_address,
                    'netmask': netmask,
                }
            ],
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
