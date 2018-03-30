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


class FortigateVm541OrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        'create_fortigate_vm_system_common': \
                        'FortinetFortigatevmFortios5dot4dot1SystemCommon',
        'delete_fortigate_vm_system_common': \
                        'FortinetFortigatevmFortios5dot4dot1SystemCommon',
        'create_fortigate_vm_interface': 'Fortigate_VM_Interface',
        'delete_fortigate_vm_interface': 'Fortigate_VM_Interface',
        'create_fortigate_vm_admin_account': 'Fortigate_VM_Admin_Account',
        'create_fortigate_vm_dns': 'Fortigate_VM_DNS',
        'create_fortigate_vm_ntp': 'Fortigate_VM_NTP',
        'create_fortigate_vm_router_static': 'Fortigate_VM_Router_Static',
        'create_fortigate_vm_ipv6_gui_enable': \
                        'FortinetFortigatevmFortios5dot4dot1Ipv6GuiEnable',
        'delete_fortigate_vm_ipv6_gui_enable': \
                        'FortinetFortigatevmFortios5dot4dot1Ipv6GuiEnable',
        'create_fortigate_vm_ipv6_interface': \
                                    'FortinetFortigatevmIpv6Interface',
        'delete_fortigate_vm_ipv6_interface': \
                                    'FortinetFortigatevmIpv6Interface',
        'create_fortigate_vm_ipv6_dns': \
                                    'FortinetFortigatevmIpv6Dns',
        'delete_fortigate_vm_ipv6_dns': \
                                    'FortinetFortigatevmIpv6Dns',
        'create_fortigate_vm_ipv6_ntp': \
                                    'FortinetFortigatevmIpv6Ntp',
        'delete_fortigate_vm_ipv6_ntp': \
                                    'FortinetFortigatevmIpv6Ntp',
        'create_fortigate_vm_ipv6_staticroute': \
                                    'FortinetFortigatevmIpv6Staticroute',
        'delete_fortigate_vm_ipv6_staticroute': \
                                    'FortinetFortigatevmIpv6Staticroute',
    }

    def __init__(self, api_config_instance, nal_endpoint_config, pod_id):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id)

    def create_fortigate_vm_system_common(self, device_id, host_name,
                                       language,
                                       timezone):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'language': language,
            'timezone': timezone,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        host_name, self.OBJECT_FILE_NAME, client_name,
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

    def delete_fortigate_vm_system_common(self, device_id, host_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        host_name, self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_fortigate_vm_interface(self, device_id, port,
                                fortigate_vm_interface_ip_address,
                                fortigate_vm_interface_netmask,
                                fortigate_vm_interface_service_ping_action,
                                fortigate_vm_interface_service_https_action,
                                fortigate_vm_interface_service_ssh_action):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'fortigate_vm_interface_ip_address':
                        fortigate_vm_interface_ip_address,
            'fortigate_vm_interface_netmask':
                        fortigate_vm_interface_netmask,
            'fortigate_vm_interface_service_ping_action':
                        fortigate_vm_interface_service_ping_action,
            'fortigate_vm_interface_service_https_action':
                        fortigate_vm_interface_service_https_action,
            'fortigate_vm_interface_service_ssh_action':
                        fortigate_vm_interface_service_ssh_action,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        port, self.OBJECT_FILE_NAME, client_name,
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

    def delete_fortigate_vm_interface(self, device_id, port):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        port, self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_fortigate_vm_admin_account(self, device_id,
                                fortigate_vm_account_name,
                                fortigate_vm_account_password,
                                fortigate_vm_account_profile='super_admin'):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'fortigate_vm_account_password': fortigate_vm_account_password,
            'fortigate_vm_account_profile': fortigate_vm_account_profile,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        fortigate_vm_account_name,
                        self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        passwords = [fortigate_vm_account_password]
        self.output_log_soap_params(
                        'in', __name__, client_name, msa_params, passwords)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params(
                        'out', __name__, client_name, msa_result, passwords)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_fortigate_vm_dns(self, device_id, host_name,
                                fortigate_vm_dns_primary,
                                fortigate_vm_dns_secondary=None):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'fortigate_vm_dns_primary': fortigate_vm_dns_primary,
            'fortigate_vm_dns_secondary': fortigate_vm_dns_secondary,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        host_name, self.OBJECT_FILE_NAME, client_name,
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

    def create_fortigate_vm_ntp(self, device_id, host_name,
                                fortigate_vm_ntp_sync_action,
                                fortigate_vm_ntp_sync_interval,
                                fortigate_vm_ntp_primary,
                                fortigate_vm_ntp_secondary):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        fortigate_vm_ntp_server = []
        for ntp_ip in [fortigate_vm_ntp_primary, fortigate_vm_ntp_secondary]:
            if len(ntp_ip) != 0:
                fortigate_vm_ntp_server.append({'ip_address': ntp_ip})
        object_params_option = {
            'fortigate_vm_ntp_sync_action': fortigate_vm_ntp_sync_action,
            'fortigate_vm_ntp_sync_interval': fortigate_vm_ntp_sync_interval,
            'fortigate_vm_ntp_server': fortigate_vm_ntp_server,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        host_name, self.OBJECT_FILE_NAME, client_name,
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

    def create_fortigate_vm_router_static(self,
                    device_id, num, dummy,
                    fortigate_vm_firewall_router_default_gateway_action,
                    fortigate_vm_firewall_router_default_gateway_address,
                    fortigate_vm_firewall_router_static_network_address=None,
                    fortigate_vm_firewall_router_static_network_mask=None,
                    fortigate_vm_firewall_router_static_device=None):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'fortigate_vm_firewall_router_default_gateway_action':
                    fortigate_vm_firewall_router_default_gateway_action,
            'fortigate_vm_firewall_router_default_gateway_address':
                    fortigate_vm_firewall_router_default_gateway_address,
            'fortigate_vm_firewall_router_static_network_address':
                    fortigate_vm_firewall_router_static_network_address,
            'fortigate_vm_firewall_router_static_network_mask':
                    fortigate_vm_firewall_router_static_network_mask,
            'fortigate_vm_firewall_router_static_device':
                    fortigate_vm_firewall_router_static_device,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        num, self.OBJECT_FILE_NAME, client_name,
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

    def create_fortigate_vm_ipv6_gui_enable(self, device_id, object_id):

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

    def delete_fortigate_vm_ipv6_gui_enable(self, device_id, object_id):

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

    def create_fortigate_vm_ipv6_interface(self, device_id, object_id,
                                            ipv6_address,
                                            netmask,
                                            is_ping,
                                            is_https,
                                            is_ssh):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': [
                {
                    'ipv6_address': ipv6_address,
                    'netmask': netmask,
                }
            ],
            'is_ping': is_ping,
            'is_https': is_https,
            'is_ssh': is_ssh,
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

    def delete_fortigate_vm_ipv6_interface(self, device_id, object_id,
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

    def create_fortigate_vm_ipv6_dns(self, device_id, object_id,
                                        dns_primary,
                                        dns_secondary):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'dns_primary': dns_primary,
            'dns_secondary': dns_secondary,
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

    def delete_fortigate_vm_ipv6_dns(self, device_id, object_id):

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

    def create_fortigate_vm_ipv6_ntp(self, device_id, object_id,
                                            ipv6_address,
                                            sync_interval):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ntpserver': [
                {
                    'ipv6_address': ipv6_address,
                }
            ],
            'sync_interval': sync_interval,
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

    def delete_fortigate_vm_ipv6_ntp(self, device_id, object_id,
                                            ipv6_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ntpserver': [
                {
                    'ipv6_address': ipv6_address,
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

    def create_fortigate_vm_ipv6_staticroute(self, device_id, object_id,
                                            is_default_gateway,
                                            gateway_ipv6_address,
                                            destination_ipv6_address,
                                            destination_netmask,
                                            source_interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'is_default_gateway': is_default_gateway,
            'gateway_ipv6_address': gateway_ipv6_address,
            'destination_ipv6_address': destination_ipv6_address,
            'destination_netmask': destination_netmask,
            'source_interface': source_interface,
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

    def delete_fortigate_vm_ipv6_staticroute(self, device_id, object_id):

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
