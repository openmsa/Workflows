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


class PaloaltoOrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        'create_paloalto_vsys': 'PaloAlto_Vsys',
        'delete_paloalto_vsys': 'PaloAlto_Vsys',
        'create_paloalto_system_vsys_users': 'PaloAlto_System_Vsys_Users',
        'delete_paloalto_system_vsys_users': 'PaloAlto_System_Vsys_Users',
        'create_paloalto_network_interface_mngprofile': \
                                'PaloAlto_Network_Interface_MngProfile',
        'delete_paloalto_network_interface_mngprofile': \
                                'PaloAlto_Network_Interface_MngProfile',
        'create_paloalto_network_subinterface': \
                                'PaloAlto_Network_SubInterface',
        'delete_paloalto_network_subinterface': \
                                'PaloAlto_Network_SubInterface',
        'create_paloalto_vsys_zone': 'PaloAlto_Vsys_Zone',
        'delete_paloalto_vsys_zone': 'PaloAlto_Vsys_Zone',
        'create_paloalto_network_virtualrouter': \
                                'PaloAlto_Network_VirtualRouter',
        'delete_paloalto_network_virtualrouter': \
                                'PaloAlto_Network_VirtualRouter',
        'create_paloalto_network_vrouter_mapping': \
                                'PaloAlto_Network_vRouter_mapping',
        'delete_paloalto_network_vrouter_mapping': \
                                'PaloAlto_Network_vRouter_mapping',
        'create_paloalto_network_staticroute': \
                                'PaloAlto_Network_StaticRoute',
        'delete_paloalto_network_staticroute': \
                                'PaloAlto_Network_StaticRoute',
        'create_paloalto_vsys_interface_importing': \
                                'PaloAlto_Vsys_Interface_importing',
        'delete_paloalto_vsys_interface_importing': \
                                'PaloAlto_Vsys_Interface_importing',
        'create_paloalto_vsys_vrouter_importing': \
                                'PaloAlto_Vsys_vRouter_importing',
        'delete_paloalto_vsys_vrouter_importing': \
                                'PaloAlto_Vsys_vRouter_importing',
        'create_paloalto_vsys_zone_mapping': \
                                'PaloAlto_Vsys_Zone_mapping',
        'delete_paloalto_vsys_zone_mapping': \
                                'PaloAlto_Vsys_Zone_mapping',
        'create_paloalto_paloalto_ipv6_interface': \
                                'PaloaltoPaloaltoIpv6Interface',
        'delete_paloalto_paloalto_ipv6_interface': \
                                'PaloaltoPaloaltoIpv6Interface',
        'create_paloalto_paloalto_ipv6_interface_enable': \
                                'PaloaltoPaloaltoIpv6InterfaceEnable',
        'delete_paloalto_paloalto_ipv6_interface_enable': \
                                'PaloaltoPaloaltoIpv6InterfaceEnable',
        'create_paloalto_paloalto_ipv6_static_route': \
                                'PaloaltoPaloaltoIpv6Staticroute',
        'delete_paloalto_paloalto_ipv6_static_route': \
                                'PaloaltoPaloaltoIpv6Staticroute',
        'create_paloalto_paloalto_permitted_ip': \
                                'PaloaltoPaloaltoPermittedip',
        'delete_paloalto_paloalto_permitted_ip': \
                                'PaloaltoPaloaltoPermittedip',

    }

    def __init__(self, api_config_instance,
                 nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def create_paloalto_vsys(
                self, device_id, vsys_id, paloalto_vsys_display_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vsys_display_name': paloalto_vsys_display_name,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        vsys_id, self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_vsys(self, device_id, vsys_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        vsys_id, self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_paloalto_system_vsys_users(self, device_id,
                                          virtual_system_user_name,
                                          paloalto_system_user_password,
                                          paloalto_system_vsys_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_system_user_password': paloalto_system_user_password,
            'paloalto_system_vsys_name': paloalto_system_vsys_name,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                virtual_system_user_name, self.OBJECT_FILE_NAME, client_name,
                object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params,
                                            [paloalto_system_user_password])

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_paloalto_system_vsys_users(self, device_id,
                                          virtual_system_user_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                virtual_system_user_name, self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_paloalto_network_interface_mngprofile(self, device_id,
                                    interface_management_profile_name,
                                    paloalto_network_interface_snmp_action,
                                    paloalto_network_interface_ssh_action,
                                    paloalto_network_interface_https_action,
                                    paloalto_network_interface_ping_action):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_network_interface_snmp_action': \
                                    paloalto_network_interface_snmp_action,
            'paloalto_network_interface_ssh_action': \
                                    paloalto_network_interface_ssh_action,
            'paloalto_network_interface_https_action': \
                                    paloalto_network_interface_https_action,
            'paloalto_network_interface_ping_action': \
                                    paloalto_network_interface_ping_action,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        interface_management_profile_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_network_interface_mngprofile(self, device_id,
                                          interface_management_profile_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        interface_management_profile_name,
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

    def create_paloalto_network_subinterface(self, device_id,
                                    sub_interface_name,
                                    paloalto_network_interface_name,
                                    paloalto_network_subinterface_ip_address,
                                    paloalto_network_subinterface_netmask,
                                    paloalto_network_subinterface_vlan,
                                    paloalto_network_profile_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_network_interface_name': \
                                    paloalto_network_interface_name,
            'paloalto_network_subinterface_ip_address': \
                                    paloalto_network_subinterface_ip_address,
            'paloalto_network_subinterface_netmask': \
                                    paloalto_network_subinterface_netmask,
            'paloalto_network_subinterface_vlan': \
                                    paloalto_network_subinterface_vlan,
            'paloalto_network_profile_name': \
                                    paloalto_network_profile_name,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        sub_interface_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_network_subinterface(self, device_id,
                                        sub_interface_name,
                                        paloalto_network_interface_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_network_interface_name': paloalto_network_interface_name
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        sub_interface_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def create_paloalto_vsys_zone(self, device_id,
                                  zone_name, paloalto_vsys_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vsys_name': paloalto_vsys_name,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        zone_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_vsys_zone(self, device_id,
                                  zone_name, paloalto_vsys_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vsys_name': paloalto_vsys_name
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        zone_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def create_paloalto_network_virtualrouter(self, device_id,
                                              virtual_router_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        virtual_router_name,
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

    def delete_paloalto_network_virtualrouter(self, device_id,
                                              virtual_router_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        virtual_router_name,
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

    def create_paloalto_network_vrouter_mapping(self, device_id,
                                              vrouter_name, interface_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_network_vrouter': [],
        }
        for val in interface_name:
            str_wk = {}
            str_wk['interface_name'] = val
            object_params_option['paloalto_network_vrouter'].append(str_wk)

        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        vrouter_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_network_vrouter_mapping(self, device_id,
                                                            vrouter_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        vrouter_name,
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

    def create_paloalto_network_staticroute(self, device_id,
                            static_route_name,
                            paloalto_network_staticroute_vrouter,
                            paloalto_network_staticroute_destination_address,
                            paloalto_network_staticroute_destination_netmask,
                            paloalto_network_staticroute_nexthop_address,
                            paloalto_network_staticroute_source_interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_network_staticroute_vrouter': \
                            paloalto_network_staticroute_vrouter,
            'paloalto_network_staticroute_destination_address': \
                            paloalto_network_staticroute_destination_address,
            'paloalto_network_staticroute_destination_netmask': \
                            paloalto_network_staticroute_destination_netmask,
            'paloalto_network_staticroute_nexthop_address': \
                            paloalto_network_staticroute_nexthop_address,
            'paloalto_network_staticroute_source_interface': \
                            paloalto_network_staticroute_source_interface,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        static_route_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_network_staticroute(self, device_id,
                                        static_route_name,
                                        paloalto_network_staticroute_vrouter):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_network_staticroute_vrouter': \
                                        paloalto_network_staticroute_vrouter,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        static_route_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def create_paloalto_vsys_interface_importing(self, device_id,
                                              vsys_name, interface_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vsys': [],
        }
        for val in interface_name:
            str_wk = {}
            str_wk['interface_name'] = val
            object_params_option['paloalto_vsys'].append(str_wk)

        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        vsys_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_vsys_interface_importing(self, device_id,
                                                            vsys_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        vsys_name,
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

    def create_paloalto_vsys_vrouter_importing(self, device_id,
                                              vsys_name, vrouter_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vsys': [],
        }
        for val in vrouter_name:
            str_wk = {}
            str_wk['vrouter_name'] = val
            object_params_option['paloalto_vsys'].append(str_wk)
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        vsys_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_vsys_vrouter_importing(self, device_id,
                                                            vsys_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        vsys_name,
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

    def create_paloalto_vsys_zone_mapping(self, device_id,
                                          zone_name,
                                          paloalto_vsys_name,
                                          interface_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vsys_name': paloalto_vsys_name,
            'paloalto_vsys_zone': [],
        }
        for val in interface_name:
            str_wk = {}
            str_wk['interface_name'] = val
            object_params_option['paloalto_vsys_zone'].append(str_wk)
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        zone_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_vsys_zone_mapping(self, device_id,
                                          zone_name,
                                          paloalto_vsys_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vsys_name': paloalto_vsys_name,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        zone_name,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def create_paloalto_paloalto_ipv6_interface(self, device_id,
                                          object_id,
                                          interface,
                                          ipv6_address,
                                          netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
            'sub_interface': [
                {
                    'ipv6_address': ipv6_address,
                    'netmask': netmask,
                }
            ],
        }

        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        object_id,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_paloalto_ipv6_interface(self, device_id,
                                          object_id,
                                          interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
        }

        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        object_id,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def create_paloalto_paloalto_ipv6_interface_enable(self, device_id,
                                          object_id,
                                          interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
        }

        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        object_id,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_paloalto_ipv6_interface_enable(self, device_id,
                                          object_id,
                                          interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
        }

        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        object_id,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def create_paloalto_paloalto_ipv6_static_route(self, device_id,
                                          object_id,
                                          virtual_router,
                                          destination_ipv6_address,
                                          destination_netmask,
                                          ipv6_address,
                                          source_interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'virtual_router': virtual_router,
            'destination_ipv6_address': destination_ipv6_address,
            'destination_netmask': destination_netmask,
            'ipv6_address': ipv6_address,
            'source_interface': source_interface
        }

        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        object_id,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_paloalto_ipv6_static_route(self, device_id, object_id,
                                                   virtual_router):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'virtual_router': virtual_router
        }

        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        object_id,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def create_paloalto_paloalto_permitted_ip(self, device_id,
                                          object_id,
                                          profile_name,
                                          ip_address,
                                          netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'profile_name': profile_name,
            'ip_address': ip_address,
            'netmask': netmask
        }

        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                                        object_id,
                                        self.OBJECT_FILE_NAME, client_name,
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

    def delete_paloalto_paloalto_permitted_ip(self, device_id,
                                          object_id,
                                          profile_name,
                                          ip_address,
                                          netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'profile_name': profile_name,
            'ip_address': ip_address,
            'netmask': netmask
        }

        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                                        object_id,
                                        self.OBJECT_FILE_NAME, client_name,
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
