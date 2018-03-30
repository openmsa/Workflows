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


class PaloaltoVmOrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        'create_paloalto_vm_system_common': 'PaloAlto_VM_System_Common',
        'delete_paloalto_vm_system_common': 'PaloAlto_VM_System_Common',
        'create_paloalto_vm_vsys_zone': 'PaloAlto_VM_Vsys_Zone',
        'delete_paloalto_vm_vsys_zone': 'PaloAlto_VM_Vsys_Zone',
        'create_paloalto_vm_vsys_zone_mapping':
                                'PaloAlto_VM_Vsys_Zone_mapping',
        'delete_paloalto_vm_vsys_zone_mapping':
                                'PaloAlto_VM_Vsys_Zone_mapping',
        'create_paloalto_vm_network_vrouter_mapping':
                                'PaloAlto_VM_Network_vRouter_mapping',
        'delete_paloalto_vm_network_vrouter_mapping':
                                'PaloAlto_VM_Network_vRouter_mapping',
        'create_paloalto_vm_network_interface':
                                'PaloAlto_VM_Network_Interface',
        'delete_paloalto_vm_network_interface':
                                'PaloAlto_VM_Network_Interface',
        'create_paloalto_vm_system_dns': 'PaloAlto_VM_System_DNS',
        'delete_paloalto_vm_system_dns': 'PaloAlto_VM_System_DNS',
        'create_paloalto_vm_logsetting_snmp': 'PaloAlto_VM_Logsetting_SNMP',
        'delete_paloalto_vm_logsetting_snmp': 'PaloAlto_VM_Logsetting_SNMP',
        'create_paloalto_vm_logsetting_snmp_mapping':
                                        'PaloAlto_VM_Logsetting_SNMP_mapping',
        'delete_paloalto_vm_logsetting_snmp_mapping':
                                        'PaloAlto_VM_Logsetting_SNMP_mapping',
        'create_paloalto_vm_logsetting_syslog':
                                        'PaloAlto_VM_Logsetting_Syslog',
        'delete_paloalto_vm_logsetting_syslog':
                                        'PaloAlto_VM_Logsetting_Syslog',
        'create_paloalto_vm_logsetting_syslog_mapping':
                                    'PaloAlto_VM_Logsetting_Syslog_mapping',
        'delete_paloalto_vm_logsetting_syslog_mapping':
                                    'PaloAlto_VM_Logsetting_Syslog_mapping',
        'create_paloalto_vm_system_ntp': 'PaloAlto_VM_System_NTP',
        'delete_paloalto_vm_system_ntp': 'PaloAlto_VM_System_NTP',
        'create_paloalto_vm_network_static_route':
                                    'PaloAlto_VM_Network_StaticRoute',
        'create_paloalto_vm_network_static_route':
                                    'PaloAlto_VM_Network_StaticRoute',
        'delete_paloalto_vm_network_static_route':
                                    'PaloAlto_VM_Network_StaticRoute',
        'create_paloalto_vm_system_users': 'PaloAlto_VM_System_Users',
        'delete_paloalto_vm_system_users': 'PaloAlto_VM_System_Users',
        'create_paloalto_vm_network_interface_mng_profile':
                                'PaloAlto_VM_Network_Interface_MngProfile',
        'delete_paloalto_vm_network_interface_mng_profile':
                                'PaloAlto_VM_Network_Interface_MngProfile',
        'create_paloalto_vm_ipv6_enable': 'PaloaltoPaloaltovmIpv6Enable',
        'create_paloalto_vm_ipv6_interface': 'PaloaltoPaloaltovmIpv6Interface',
        'delete_paloalto_vm_ipv6_interface': 'PaloaltoPaloaltovmIpv6Interface',
        'create_paloalto_vm_ipv6_interface_enable':
                                'PaloaltoPaloaltovmIpv6InterfaceEnable',
        'delete_paloalto_vm_ipv6_interface_enable':
                                'PaloaltoPaloaltovmIpv6InterfaceEnable',
        'create_paloalto_vm_ipv6_dns': 'PaloaltoPaloaltovmIpv6Dns',
        'delete_paloalto_vm_ipv6_dns': 'PaloaltoPaloaltovmIpv6Dns',
        'create_paloalto_vm_ipv6_ntp': 'PaloaltoPaloaltovmIpv6Ntp',
        'delete_paloalto_vm_ipv6_ntp': 'PaloaltoPaloaltovmIpv6Ntp',
        'create_paloalto_vm_ipv6_staticroute':
                                        'PaloaltoPaloaltovmIpv6Staticroute',
        'delete_paloalto_vm_ipv6_staticroute':
                                        'PaloaltoPaloaltovmIpv6Staticroute',
        'create_paloalto_vm_permittedip': 'PaloaltoPaloaltovmPermittedip',
        'delete_paloalto_vm_permittedip': 'PaloaltoPaloaltovmPermittedip',
    }

    def __init__(self, api_config_instance,
                 nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def create_paloalto_vm_system_common(self, device_id, object_id,
                                         paloalto_vm_system_timezone):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_system_timezone': paloalto_vm_system_timezone,
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

    def delete_paloalto_vm_system_common(self, device_id, object_id,
                                         paloalto_vm_system_timezone):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_system_timezone': paloalto_vm_system_timezone,
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

    def create_paloalto_vm_vsys_zone(self, device_id, object_id):

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

    def delete_paloalto_vm_vsys_zone(self, device_id, object_id):

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

    def create_paloalto_vm_vsys_zone_mapping(self, device_id, object_id,
                                            paloalto_vm_vsys_zone_interface,
                                            paloalto_vm_vsys_zone_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
        'paloalto_vm_vsys_zone_interface': paloalto_vm_vsys_zone_interface,
        'paloalto_vm_vsys_zone_name': paloalto_vm_vsys_zone_name,
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

    def delete_paloalto_vm_vsys_zone_mapping(self, device_id, object_id,
                                            paloalto_vm_vsys_zone_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_vsys_zone_name': paloalto_vm_vsys_zone_name,
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

    def create_paloalto_vm_network_vrouter_mapping(self, device_id, object_id,
                                            interface_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        vrouter = []
        for val in interface_name:
            vrouter.append({'interface_name': val})

        object_params_option = {
            'paloalto_vm_network_vrouter': vrouter,
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

    def delete_paloalto_vm_network_vrouter_mapping(self, device_id, object_id):

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

    def create_paloalto_vm_network_interface(self, device_id, object_id,
                                paloalto_vm_network_interface_ip_address,
                                paloalto_vm_network_interface_netmask,
                                paloalto_vm_network_profile_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_network_interface_ip_address':
                            paloalto_vm_network_interface_ip_address,
            'paloalto_vm_network_interface_netmask':
                            paloalto_vm_network_interface_netmask,
            'paloalto_vm_network_profile_name':
                            paloalto_vm_network_profile_name,
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

    def delete_paloalto_vm_network_interface(self, device_id, object_id):

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

    def create_paloalto_vm_system_dns(self, device_id, object_id,
                                            paloalto_vm_system_dns_primary,
                                            paloalto_vm_system_dns_secondary):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
        'paloalto_vm_system_dns_primary': paloalto_vm_system_dns_primary,
        'paloalto_vm_system_dns_secondary': paloalto_vm_system_dns_secondary,
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

    def delete_paloalto_vm_system_dns(self, device_id, object_id):

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

    def create_paloalto_vm_logsetting_snmp(self, device_id, object_id,
                                                name,
                                                address,
                                                community_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'name': name,
            'address': address,
            'community_name': community_name,
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

    def delete_paloalto_vm_logsetting_snmp(self, device_id, object_id):

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

    def create_paloalto_vm_logsetting_snmp_mapping(self, device_id, object_id,
                                        paloalto_vm_logsetting_snmp_profile):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_logsetting_snmp_profile':
                                paloalto_vm_logsetting_snmp_profile,
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

    def delete_paloalto_vm_logsetting_snmp_mapping(self, device_id, object_id):

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

    def create_paloalto_vm_logsetting_syslog(self, device_id, object_id,
                                                    name,
                                                    address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_logsetting_syslog_server': {
                'name': name,
                'address': address,
            }
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

    def delete_paloalto_vm_logsetting_syslog(self, device_id, object_id):

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

    def create_paloalto_vm_logsetting_syslog_mapping(self,
                                        device_id, object_id,
                                        paloalto_vm_logsetting_syslog_profile):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_logsetting_syslog_profile':
                        paloalto_vm_logsetting_syslog_profile,
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

    def delete_paloalto_vm_logsetting_syslog_mapping(self,
                                                device_id, object_id):

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

    def create_paloalto_vm_system_ntp(self, device_id, object_id,
                                    paloalto_vm_system_primary_ntp_server,
                                    paloalto_vm_system_secondary_ntp_server):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_system_primary_ntp_server':
                    paloalto_vm_system_primary_ntp_server,
            'paloalto_vm_system_secondary_ntp_server':
                    paloalto_vm_system_secondary_ntp_server,
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

    def delete_paloalto_vm_system_ntp(self, device_id, object_id):

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

    def create_paloalto_vm_network_static_route(self, device_id, object_id,
                    paloalto_vm_network_staticroute_destination_address,
                    paloalto_vm_network_staticroute_destination_netmask,
                    paloalto_vm_network_staticroute_nexthop_address,
                    paloalto_vm_network_staticroute_source_interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_network_staticroute_destination_address':
                        paloalto_vm_network_staticroute_destination_address,
            'paloalto_vm_network_staticroute_destination_netmask':
                        paloalto_vm_network_staticroute_destination_netmask,
            'paloalto_vm_network_staticroute_nexthop_address':
                        paloalto_vm_network_staticroute_nexthop_address,
            'paloalto_vm_network_staticroute_source_interface':
                        paloalto_vm_network_staticroute_source_interface,
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

    def delete_paloalto_vm_network_static_route(self, device_id, object_id):

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

    def create_paloalto_vm_system_users(self, device_id, object_id,
                                            paloalto_vm_system_user_password):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_system_user_password':
                                    paloalto_vm_system_user_password,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        object_id, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        passwords = [paloalto_vm_system_user_password]
        self.output_log_soap_params(
                        'in', __name__, client_name, msa_params, passwords)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params(
                        'out', __name__, client_name, msa_result, passwords)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_paloalto_vm_system_users(self, device_id, object_id):

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

    def create_paloalto_vm_network_interface_mng_profile(self, device_id,
                                object_id,
                                paloalto_vm_network_interface_snmp_action,
                                paloalto_vm_network_interface_ssh_action,
                                paloalto_vm_network_interface_https_action,
                                paloalto_vm_network_interface_ping_action):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'paloalto_vm_network_interface_snmp_action':
                            paloalto_vm_network_interface_snmp_action,
            'paloalto_vm_network_interface_ssh_action':
                            paloalto_vm_network_interface_ssh_action,
            'paloalto_vm_network_interface_https_action':
                            paloalto_vm_network_interface_https_action,
            'paloalto_vm_network_interface_ping_action':
                            paloalto_vm_network_interface_ping_action,
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

    def delete_paloalto_vm_network_interface_mng_profile(self, device_id,
                                                                object_id):

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

    def create_paloalto_vm_ipv6_enable(self, device_id, object_id,
                                                    is_ipv6firewalling):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'is_ipv6firewalling': is_ipv6firewalling,
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

    def create_paloalto_vm_ipv6_interface(self, device_id, object_id,
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

    def delete_paloalto_vm_ipv6_interface(self, device_id, object_id):

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

    def create_paloalto_vm_ipv6_interface_enable(self, device_id, object_id):

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

    def delete_paloalto_vm_ipv6_interface_enable(self, device_id, object_id):

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

    def create_paloalto_vm_ipv6_dns(self, device_id, object_id,
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

    def delete_paloalto_vm_ipv6_dns(self, device_id, object_id):

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

    def create_paloalto_vm_ipv6_ntp(self, device_id, object_id,
                                                    primary_ntp_server,
                                                    secondary_ntp_server):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'primary_ntp_server': primary_ntp_server,
            'secondary_ntp_server': secondary_ntp_server,
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

    def delete_paloalto_vm_ipv6_ntp(self, device_id, object_id):

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

    def create_paloalto_vm_ipv6_staticroute(self, device_id, object_id,
                                                    destination_ipv6_address,
                                                    destination_netmask,
                                                    ipv6_address,
                                                    source_interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'destination_ipv6_address': destination_ipv6_address,
            'destination_netmask': destination_netmask,
            'ipv6_address': ipv6_address,
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

    def delete_paloalto_vm_ipv6_staticroute(self, device_id,
                                                   object_id):

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

    def create_paloalto_vm_permittedip(self, device_id, object_id,
                                                    profile_name,
                                                    ip_address,
                                                    netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'profile_name': profile_name,
            'ip_address': ip_address,
            'netmask': netmask,
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

    def delete_paloalto_vm_permittedip(self, device_id, object_id,
                                                    profile_name,
                                                    ip_address,
                                                    netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'profile_name': profile_name,
            'ip_address': ip_address,
            'netmask': netmask,
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
