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


class IntersecOrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        'create_intersec_sg_startup': 'sg_startup',
        'create_intersec_sg_nw': 'sg_nw',
        'update_intersec_sg_nw': 'sg_nw',
        'delete_intersec_sg_nw': 'sg_nw',
        'create_intersec_sg_reboot': 'sg_reboot',
        'create_intersec_sg_zabbix': 'sg_zabbix',
        'create_intersec_sg_ntp': 'sg_ntp',
        'create_intersec_sg_default_gw': 'sg_default_gw',
        'create_intersec_sg_static_route': 'sg_static_route',
        'check_boot_complete_sg': 'sg_boot_complete_check',
        'create_intersec_lb_startup': 'lb_startup',
        'create_intersec_lb_nw': 'lb_nw',
        'update_intersec_lb_nw': 'lb_nw',
        'delete_intersec_lb_nw': 'lb_nw',
        'create_intersec_lb_reboot': 'lb_reboot',
        'create_intersec_lb_zabbix': 'lb_zabbix',
        'create_intersec_lb_ntp': 'lb_ntp',
        'create_intersec_lb_default_gw': 'lb_default_gw',
        'create_intersec_lb_static_route': 'lb_static_route',
        'check_boot_complete_lb': 'lb_boot_complete_check',
        'create_nec_intersecvmsg_ipv6_interface': \
                                'NecIntersecvmsgIpv6Interface',
        'delete_nec_intersecvmsg_ipv6_interface': \
                                'NecIntersecvmsgIpv6Interface',
        'create_nec_intersecvmsg_ipv6_staticroute': \
                                'NecIntersecvmsgIpv6Staticroute',
        'delete_nec_intersecvmsg_ipv6_staticroute': \
                                'NecIntersecvmsgIpv6Staticroute',
        'create_nec_intersecvmsg_ipv6_defaultgw': \
                                'NecIntersecvmsgIpv6Defaultgw',
        'delete_nec_intersecvmsg_ipv6_defaultgw': \
                                'NecIntersecvmsgIpv6Defaultgw',
        'create_nec_intersecvmsg_ipv6_dns': \
                                'NecIntersecvmsgIpv6Dns',
        'delete_nec_intersecvmsg_ipv6_dns': \
                                'NecIntersecvmsgIpv6Dns',
        'create_nec_intersecvmsg_ipv6_ntp': \
                                'NecIntersecvmsgIpv6Ntp',
        'delete_nec_intersecvmsg_ipv6_ntp': \
                                'NecIntersecvmsgIpv6Ntp',
    }

    OBJECT_ID = '123456'

    def __init__(self, api_config_instance,
                 nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def create_intersec_sg_startup(self, device_id,
                                            instance_name,
                                            license_key):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'instanceName': instance_name,
                    'licenseKey': license_key,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'sg_startup', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_sg_nw(self, device_id,
                                        nic_number,
                                        ip_address,
                                        subnet):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'nicNumber': nic_number,
                    'ipAddress': ip_address,
                    'subnet': subnet,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'sg_nw', self.OBJECT_FILE_NAME, client_name,
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

    def update_intersec_sg_nw(self, device_id,
                                        nic_number,
                                        ip_address,
                                        subnet
                                       ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'nicNumber': nic_number,
                    'ipAddress': ip_address,
                    'subnet': subnet,
        }
        msa_params = self.set_msa_cmd_input_params('UPDATE', device_id,
                        'sg_nw', self.OBJECT_FILE_NAME, client_name,
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

    def delete_intersec_sg_nw(self, device_id,
                                        nic_number
                                       ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'nicNumber': nic_number,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        'sg_nw', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_sg_reboot(self, device_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'sg_reboot', self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_intersec_sg_zabbix(self, device_id,
                                        instance_name,
                                        zabbix_vip_ip_address,
                                        zabbix01_ip_address,
                                        zabbix02_ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'instanceName': instance_name,
                    'zabbixVIPipAddress': zabbix_vip_ip_address,
                    'zabbix01ipAddress': zabbix01_ip_address,
                    'zabbix02ipAddress': zabbix02_ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'sg_zabbix', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_sg_ntp(self, device_id, ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'ipAddress': ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'sg_ntp', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_sg_default_gw(self, device_id, gw_ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'gwIpAddress': gw_ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'sg_default_gw', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_sg_static_route(self, device_id,
                                            dst_ip_address,
                                            dst_subnet,
                                            gw_ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'dstIpAddress': dst_ip_address,
                    'dstSubnet': dst_subnet,
                    'gwIpAddress': gw_ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'sg_static_route', self.OBJECT_FILE_NAME, client_name,
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

    def check_boot_complete_sg(self, device_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {}
        msa_params = self.set_msa_cmd_input_params('CREATE',
                                                   device_id,
                                                   'sg_boot_complete_check',
                                                   self.OBJECT_FILE_NAME,
                                                   client_name,
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

    def create_intersec_lb_startup(self, device_id,
                                            instance_name,
                                            ip_address,
                                            license_key):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'instanceName': instance_name,
                    'ipAddress': ip_address,
                    'licenseKey': license_key,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'lb_startup', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_lb_nw(self, device_id,
                                    nic_number,
                                    ip_address,
                                    subnet,
                                    broadcast_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'nicNumber': nic_number,
                    'ipAddress': ip_address,
                    'subnet': subnet,
                    'broadcastAddress': broadcast_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'lb_nw', self.OBJECT_FILE_NAME, client_name,
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

    def update_intersec_lb_nw(self, device_id,
                                    nic_number,
                                    ip_address,
                                    subnet,
                                    broadcast_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'nicNumber': nic_number,
                    'ipAddress': ip_address,
                    'subnet': subnet,
                    'broadcastAddress': broadcast_address,
        }
        msa_params = self.set_msa_cmd_input_params('UPDATE', device_id,
                        'lb_nw', self.OBJECT_FILE_NAME, client_name,
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

    def delete_intersec_lb_nw(self, device_id, nic_number):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'nicNumber': nic_number,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        'lb_nw', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_lb_reboot(self, device_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'lb_reboot', self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_intersec_lb_zabbix(self, device_id,
                                        instance_name,
                                        zabbix_vip_ip_address,
                                        zabbix01_ip_address,
                                        zabbix02_ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'instanceName': instance_name,
                    'zabbixVIPipAddress': zabbix_vip_ip_address,
                    'zabbix01ipAddress': zabbix01_ip_address,
                    'zabbix02ipAddress': zabbix02_ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'lb_zabbix', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_lb_ntp(self, device_id, ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'ipAddress': ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'lb_ntp', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_lb_default_gw(self, device_id,
                                            gw_ip_address,
                                            nic_number):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'gwIpAddress': gw_ip_address,
                    'nicNumber': nic_number,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'lb_default_gw', self.OBJECT_FILE_NAME, client_name,
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

    def create_intersec_lb_static_route(self, device_id,
                                                dst_ip_address,
                                                dst_subnet,
                                                gw_ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                    'dstIpAddress': dst_ip_address,
                    'dstSubnet': dst_subnet,
                    'gwIpAddress': gw_ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        'lb_static_route', self.OBJECT_FILE_NAME, client_name,
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

    def check_boot_complete_lb(self, device_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {}
        msa_params = self.set_msa_cmd_input_params('CREATE',
                                                   device_id,
                                                   'lb_boot_complete_check',
                                                   self.OBJECT_FILE_NAME,
                                                   client_name,
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

    def create_nec_intersecvmsg_ipv6_interface(self, device_id, object_id,
                                            ipv6_address,
                                            netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': [
                    {
                        'ipv6_address': ipv6_address,
                        'netmask': netmask,
                    },
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

    def delete_nec_intersecvmsg_ipv6_interface(self, device_id, object_id):

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

    def create_nec_intersecvmsg_ipv6_staticroute(self, device_id, object_id,
                                            destination_ipv6_address,
                                            destination_netmask,
                                            ipv6_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'destination_ipv6_address': destination_ipv6_address,
            'destination_netmask': destination_netmask,
            'ipv6_address': ipv6_address,
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

    def delete_nec_intersecvmsg_ipv6_staticroute(self, device_id, object_id,
                                            destination_ipv6_address,
                                            destination_netmask,
                                            ipv6_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'destination_ipv6_address': destination_ipv6_address,
            'destination_netmask': destination_netmask,
            'ipv6_address': ipv6_address,
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

    def create_nec_intersecvmsg_ipv6_defaultgw(self, device_id, object_id,
                                            ipv6_address,
                                            source_interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
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

    def delete_nec_intersecvmsg_ipv6_defaultgw(self, device_id, object_id,
                                            ipv6_address,
                                            source_interface):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': ipv6_address,
            'source_interface': source_interface,
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

    def create_nec_intersecvmsg_ipv6_dns(self, device_id, object_id,
                                            ipv6_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'nameserver': [
                {
                    'ipv6_address': ipv6_address,
                }
            ]
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

    def delete_nec_intersecvmsg_ipv6_dns(self, device_id, object_id,
                                            ipv6_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'nameserver': [
                {
                    'ipv6_address': ipv6_address,
                }
            ]
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

    def create_nec_intersecvmsg_ipv6_ntp(self, device_id, object_id,
                                            ipv6_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ntpserver': [
                {
                    'ipv6_address': ipv6_address,
                }
            ]
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

    def delete_nec_intersecvmsg_ipv6_ntp(self, device_id, object_id,
                                            ipv6_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ntpserver': [
                {
                    'ipv6_address': ipv6_address,
                }
            ]
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
