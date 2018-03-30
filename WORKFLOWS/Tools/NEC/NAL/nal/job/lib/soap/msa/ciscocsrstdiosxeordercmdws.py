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


class CsrStdIosXeOrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        # --- Common --------------------------------------------------------
        'create_csr1000v_system_common_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aSystemCommonIpv6',
        'update_csr1000v_system_common_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aSystemCommonIpv6',
        'delete_csr1000v_system_common_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aSystemCommonIpv6',
        'create_csr1000v_bgp_basic_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aBgpBasicIpv4',
        'update_csr1000v_bgp_basic_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aBgpBasicIpv4',
        'delete_csr1000v_bgp_basic_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aBgpBasicIpv4',
        'create_csr1000v_bgp_basic_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aBgpBasicIpv6',
        'update_csr1000v_bgp_basic_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aBgpBasicIpv6',
        'delete_csr1000v_bgp_basic_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aBgpBasicIpv6',
        'create_csr1000v_loopback_interface': \
                            'CiscoCsrStdIosXe16dot03dot01aLoopbackInterface',
        'update_csr1000v_loopback_interface': \
                            'CiscoCsrStdIosXe16dot03dot01aLoopbackInterface',
        'delete_csr1000v_loopback_interface': \
                            'CiscoCsrStdIosXe16dot03dot01aLoopbackInterface',
        'create_csr1000v_lan_interface_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aLanInterfaceIpv4',
        'update_csr1000v_lan_interface_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aLanInterfaceIpv4',
        'delete_csr1000v_lan_interface_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aLanInterfaceIpv4',
        'create_csr1000v_lan_interface_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aLanInterfaceIpv6',
        'update_csr1000v_lan_interface_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aLanInterfaceIpv6',
        'delete_csr1000v_lan_interface_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aLanInterfaceIpv6',
        'create_csr1000v_hsrp_primary_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpPrimaryIpv4',
        'update_csr1000v_hsrp_primary_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpPrimaryIpv4',
        'delete_csr1000v_hsrp_primary_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpPrimaryIpv4',
        'create_csr1000v_hsrp_primary_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpPrimaryIpv6',
        'update_csr1000v_hsrp_primary_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpPrimaryIpv6',
        'delete_csr1000v_hsrp_primary_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpPrimaryIpv6',
        'create_csr1000v_hsrp_secondary_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpSecondaryIpv4',
        'update_csr1000v_hsrp_secondary_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpSecondaryIpv4',
        'delete_csr1000v_hsrp_secondary_ipv4': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpSecondaryIpv4',
        'create_csr1000v_hsrp_secondary_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpSecondaryIpv6',
        'update_csr1000v_hsrp_secondary_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpSecondaryIpv6',
        'delete_csr1000v_hsrp_secondary_ipv6': \
                            'CiscoCsrStdIosXe16dot03dot01aHsrpSecondaryIpv6',
        'create_csr1000v_hsrp_interface_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking',
        'update_csr1000v_hsrp_interface_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking',
        'delete_csr1000v_hsrp_interface_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking',
        'create_csr1000v_default_route_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aDefaultRoute',
        'update_csr1000v_default_route_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aDefaultRoute',
        'delete_csr1000v_default_route_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aDefaultRoute',
        'create_csr1000v_default_route_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aDefaultRouteIpv6',
        'update_csr1000v_default_route_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aDefaultRouteIpv6',
        'delete_csr1000v_default_route_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aDefaultRouteIpv6',
        'create_csr1000v_static_route': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRoute',
        'update_csr1000v_static_route': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRoute',
        'delete_csr1000v_static_route': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRoute',
        'create_csr1000v_static_route_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRouteIpv6',
        'update_csr1000v_static_route_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRouteIpv6',
        'delete_csr1000v_static_route_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRouteIpv6',
        'create_csr1000v_bgp_peer_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aBgpPeerIpv4',
        'update_csr1000v_bgp_peer_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aBgpPeerIpv4',
        'delete_csr1000v_bgp_peer_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aBgpPeerIpv4',
        'create_csr1000v_bgp_peer_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aBgpPeerIpv6',
        'update_csr1000v_bgp_peer_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aBgpPeerIpv6',
        'delete_csr1000v_bgp_peer_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aBgpPeerIpv6',
        'create_csr1000v_hsrp_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpTracking',
        'update_csr1000v_hsrp_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpTracking',
        'delete_csr1000v_hsrp_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpTracking',
        'create_csr1000v_dns_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aDns',
        'update_csr1000v_dns_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aDns',
        'delete_csr1000v_dns_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aDns',
        'create_csr1000v_dns_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aDnsIpv6',
        'update_csr1000v_dns_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aDnsIpv6',
        'delete_csr1000v_dns_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aDnsIpv6',
        'create_csr1000v_snmp_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aSnmpIpv4',
        'update_csr1000v_snmp_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aSnmpIpv4',
        'delete_csr1000v_snmp_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aSnmpIpv4',
        'create_csr1000v_snmp_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aSnmpIpv6',
        'update_csr1000v_snmp_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aSnmpIpv6',
        'delete_csr1000v_snmp_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aSnmpIpv6',
        'create_csr1000v_syslog_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aSyslogIpv4',
        'update_csr1000v_syslog_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aSyslogIpv4',
        'delete_csr1000v_syslog_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aSyslogIpv4',
        'create_csr1000v_syslog_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aSyslogIpv6',
        'update_csr1000v_syslog_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aSyslogIpv6',
        'delete_csr1000v_syslog_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aSyslogIpv6',
        'create_csr1000v_ntp_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aNtp',
        'update_csr1000v_ntp_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aNtp',
        'delete_csr1000v_ntp_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aNtp',
        'create_csr1000v_ntp_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aNtpIpv6',
        'update_csr1000v_ntp_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aNtpIpv6',
        'delete_csr1000v_ntp_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aNtpIpv6',
        'create_csr1000v_license': \
                        'CiscoCsrStdIosXe16dot03dot01aLicense',
        'update_csr1000v_license': \
                        'CiscoCsrStdIosXe16dot03dot01aLicense',
        'delete_csr1000v_license': \
                        'CiscoCsrStdIosXe16dot03dot01aLicense',
        'create_csr1000v_throughput': \
                        'CiscoCsrStdIosXe16dot03dot01aThroughput',
        'update_csr1000v_throughput': \
                        'CiscoCsrStdIosXe16dot03dot01aThroughput',
        'delete_csr1000v_throughput': \
                        'CiscoCsrStdIosXe16dot03dot01aThroughput',

        # --- L2 --------------------------------------------------------
        'create_csr1000v_wan_interface_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceIpv4',
        'update_csr1000v_wan_interface_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceIpv4',
        'delete_csr1000v_wan_interface_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceIpv4',
        'create_csr1000v_wan_interface_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceIpv6',
        'update_csr1000v_wan_interface_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceIpv6',
        'delete_csr1000v_wan_interface_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceIpv6',

        # --- L3 --------------------------------------------------------
        'create_csr1000v_wan_interface_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceGreIpv4',
        'update_csr1000v_wan_interface_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceGreIpv4',
        'delete_csr1000v_wan_interface_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aWanInterfaceGreIpv4',
        'create_csr1000v_tunnel_interface_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aTunnelInterfaceGreIpv4',
        'update_csr1000v_tunnel_interface_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aTunnelInterfaceGreIpv4',
        'delete_csr1000v_tunnel_interface_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aTunnelInterfaceGreIpv4',
        'create_csr1000v_tunnel_interface_gre_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aTunnelInterfaceGreIpv6',
        'update_csr1000v_tunnel_interface_gre_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aTunnelInterfaceGreIpv6',
        'delete_csr1000v_tunnel_interface_gre_ipv6': \
                        'CiscoCsrStdIosXe16dot03dot01aTunnelInterfaceGreIpv6',
        'create_csr1000v_ipsec_basic_esp_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecBasicEspGreIpv4',
        'update_csr1000v_ipsec_basic_esp_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecBasicEspGreIpv4',
        'delete_csr1000v_ipsec_basic_esp_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecBasicEspGreIpv4',
        'create_csr1000v_ipsec_basic_ah_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecBasicAhGreIpv4',
        'update_csr1000v_ipsec_basic_ah_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecBasicAhGreIpv4',
        'delete_csr1000v_ipsec_basic_ah_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecBasicAhGreIpv4',
        'create_csr1000v_ipsec_peer_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecPeerGreIpv4',
        'update_csr1000v_ipsec_peer_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecPeerGreIpv4',
        'delete_csr1000v_ipsec_peer_gre_ipv4': \
                        'CiscoCsrStdIosXe16dot03dot01aIpsecPeerGreIpv4',
        'create_csr1000v_static_route_for_dc': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc',
        'update_csr1000v_static_route_for_dc': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc',
        'delete_csr1000v_static_route_for_dc': \
                        'CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc',
    }

    def __init__(self, api_config_instance,
                 nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    # --- Common --------------------------------------------------------
    def create_csr1000v_system_common_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'timezone': option_params['timezone'],
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

    def update_csr1000v_system_common_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'timezone': option_params['timezone'],
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

    def delete_csr1000v_system_common_ipv6(self, device_id, object_id):

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

    def create_csr1000v_bgp_basic_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'local_preference': option_params['local_preference'],
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

    def update_csr1000v_bgp_basic_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'local_preference': option_params['local_preference'],
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

    def delete_csr1000v_bgp_basic_ipv4(self, device_id, object_id):

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

    def create_csr1000v_bgp_basic_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'local_preference': option_params['local_preference'],
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

    def update_csr1000v_bgp_basic_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'local_preference': option_params['local_preference'],
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

    def delete_csr1000v_bgp_basic_ipv6(self, device_id, object_id):

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

    def create_csr1000v_loopback_interface(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def update_csr1000v_loopback_interface(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def delete_csr1000v_loopback_interface(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def create_csr1000v_lan_interface_ipv4(self, device_id, object_id,
                                           option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'hsrp_ip_address': option_params['hsrp_ip_address'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def update_csr1000v_lan_interface_ipv4(self, device_id, object_id,
                                           option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'hsrp_ip_address': option_params['hsrp_ip_address'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def delete_csr1000v_lan_interface_ipv4(self, device_id, object_id,
                                           option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'hsrp_ip_address': option_params['hsrp_ip_address'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def create_csr1000v_lan_interface_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'hsrp_ipv6_address': option_params['hsrp_ipv6_address'],
            'segment': option_params['segment'],
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

    def update_csr1000v_lan_interface_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'hsrp_ipv6_address': option_params['hsrp_ipv6_address'],
            'segment': option_params['segment'],
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

    def delete_csr1000v_lan_interface_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'hsrp_ipv6_address': option_params['hsrp_ipv6_address'],
            'segment': option_params['segment'],
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

    def create_csr1000v_hsrp_primary_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'priority': option_params['priority'],
            'group_id': option_params['group_id'],
            'authkey': option_params['authkey'],
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

    def update_csr1000v_hsrp_primary_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'priority': option_params['priority'],
            'group_id': option_params['group_id'],
            'authkey': option_params['authkey'],
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

    def delete_csr1000v_hsrp_primary_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'group_id': option_params['group_id'],
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

    def create_csr1000v_hsrp_primary_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'priority': option_params['priority'],
            'group_id': option_params['group_id'],
            'authkey': option_params['authkey'],
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

    def update_csr1000v_hsrp_primary_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'priority': option_params['priority'],
            'group_id': option_params['group_id'],
            'authkey': option_params['authkey'],
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

    def delete_csr1000v_hsrp_primary_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'group_id': option_params['group_id'],
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

    def create_csr1000v_hsrp_secondary_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'priority': option_params['priority'],
            'group_id': option_params['group_id'],
            'authkey': option_params['authkey'],
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

    def update_csr1000v_hsrp_secondary_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'priority': option_params['priority'],
            'group_id': option_params['group_id'],
            'authkey': option_params['authkey'],
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

    def delete_csr1000v_hsrp_secondary_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'group_id': option_params['group_id'],
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

    def create_csr1000v_hsrp_secondary_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'priority': option_params['priority'],
            'group_id': option_params['group_id'],
            'authkey': option_params['authkey'],
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

    def update_csr1000v_hsrp_secondary_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'priority': option_params['priority'],
            'group_id': option_params['group_id'],
            'authkey': option_params['authkey'],
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

    def delete_csr1000v_hsrp_secondary_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'group_id': option_params['group_id'],
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

    def create_csr1000v_hsrp_interface_tracking(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': option_params['interface'],
            'group_id': option_params['group_id'],
            'track_interface': option_params['track_interface'],
            'prioritycost': option_params['prioritycost'],
            'track_id': option_params['track_id'],
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

    def update_csr1000v_hsrp_interface_tracking(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': option_params['interface'],
            'group_id': option_params['group_id'],
            'track_interface': option_params['track_interface'],
            'prioritycost': option_params['prioritycost'],
            'track_id': option_params['track_id'],
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

    def delete_csr1000v_hsrp_interface_tracking(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': option_params['interface'],
            'group_id': option_params['group_id'],
            'track_id': option_params['track_id'],
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

    def create_csr1000v_default_route_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
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

    def update_csr1000v_default_route_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
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

    def delete_csr1000v_default_route_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
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

    def create_csr1000v_default_route_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'nexthop_address': option_params['nexthop_address'],
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

    def update_csr1000v_default_route_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'nexthop_address': option_params['nexthop_address'],
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

    def delete_csr1000v_default_route_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'nexthop_address': option_params['nexthop_address'],
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

    def create_csr1000v_static_route(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def update_csr1000v_static_route(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def delete_csr1000v_static_route(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def create_csr1000v_static_route_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'nexthop_address': option_params['nexthop_address'],
            'prefix': option_params['prefix'],
            'segment': option_params['segment'],
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

    def update_csr1000v_static_route_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'nexthop_address': option_params['nexthop_address'],
            'prefix': option_params['prefix'],
            'segment': option_params['segment'],
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

    def delete_csr1000v_static_route_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'nexthop_address': option_params['nexthop_address'],
            'prefix': option_params['prefix'],
            'segment': option_params['segment'],
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

    def create_csr1000v_bgp_peer_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'authkey': option_params['authkey'],
            'interface': option_params['interface'],
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

    def update_csr1000v_bgp_peer_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'authkey': option_params['authkey'],
            'interface': option_params['interface'],
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

    def delete_csr1000v_bgp_peer_ipv4(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
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

    def create_csr1000v_bgp_peer_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'authkey': option_params['authkey'],
            'interface': option_params['interface'],
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

    def update_csr1000v_bgp_peer_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'authkey': option_params['authkey'],
            'interface': option_params['interface'],
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

    def delete_csr1000v_bgp_peer_ipv6(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
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

    def create_csr1000v_hsrp_tracking(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': option_params['interface'],
            'group_id': option_params['group_id'],
            'segment': option_params['segment'],
            'netmask': option_params['netmask'],
            'prioritycost': option_params['prioritycost'],
            'track_id': option_params['track_id'],
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

    def update_csr1000v_hsrp_tracking(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': option_params['interface'],
            'group_id': option_params['group_id'],
            'segment': option_params['segment'],
            'netmask': option_params['netmask'],
            'prioritycost': option_params['prioritycost'],
            'track_id': option_params['track_id'],
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

    def delete_csr1000v_hsrp_tracking(self, device_id, object_id,
                                        option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': option_params['interface'],
            'group_id': option_params['group_id'],
            'track_id': option_params['track_id'],
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

    def create_csr1000v_dns_ipv4(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
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

    def update_csr1000v_dns_ipv4(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
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

    def delete_csr1000v_dns_ipv4(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
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

    def create_csr1000v_dns_ipv6(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
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

    def update_csr1000v_dns_ipv6(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
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

    def delete_csr1000v_dns_ipv6(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
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

    def create_csr1000v_snmp_ipv4(self, device_id, object_id,
                                option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'community_name': option_params['community_name'],
            'interface': option_params['interface'],
            'ip_address': option_params['ip_address'],
            'version': option_params['version'],
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

    def update_csr1000v_snmp_ipv4(self, device_id, object_id,
                                option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'community_name': option_params['community_name'],
            'interface': option_params['interface'],
            'ip_address': option_params['ip_address'],
            'version': option_params['version'],
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

    def delete_csr1000v_snmp_ipv4(self, device_id, object_id,
                                option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'community_name': option_params['community_name'],
            'ip_address': option_params['ip_address'],
            'version': option_params['version'],
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

    def create_csr1000v_snmp_ipv6(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'community_name': option_params['community_name'],
            'interface': option_params['interface'],
            'ipv6_address': option_params['ipv6_address'],
            'version': option_params['version'],
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

    def update_csr1000v_snmp_ipv6(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'community_name': option_params['community_name'],
            'interface': option_params['interface'],
            'ipv6_address': option_params['ipv6_address'],
            'version': option_params['version'],
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

    def delete_csr1000v_snmp_ipv6(self, device_id, object_id, option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'community_name': option_params['community_name'],
            'ipv6_address': option_params['ipv6_address'],
            'version': option_params['version'],
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

    def create_csr1000v_syslog_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'interface': option_params['interface'],
            'facility': option_params['facility'],
            'severity': option_params['severity'],
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

    def update_csr1000v_syslog_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'interface': option_params['interface'],
            'facility': option_params['facility'],
            'severity': option_params['severity'],
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

    def delete_csr1000v_syslog_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
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

    def create_csr1000v_syslog_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'interface': option_params['interface'],
            'facility': option_params['facility'],
            'severity': option_params['severity'],
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

    def update_csr1000v_syslog_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'interface': option_params['interface'],
            'facility': option_params['facility'],
            'severity': option_params['severity'],
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

    def delete_csr1000v_syslog_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
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

    def create_csr1000v_ntp_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'interface': option_params['interface'],
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

    def update_csr1000v_ntp_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'interface': option_params['interface'],
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

    def delete_csr1000v_ntp_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'interface': option_params['interface'],
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

    def create_csr1000v_ntp_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'interface': option_params['interface'],
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

    def update_csr1000v_ntp_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'interface': option_params['interface'],
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

    def delete_csr1000v_ntp_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'interface': option_params['interface'],
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

    def create_csr1000v_license(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'idtoken': option_params['idtoken'],
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

    def update_csr1000v_license(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'idtoken': option_params['idtoken'],
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

    def delete_csr1000v_license(self, device_id, object_id):

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

    def create_csr1000v_throughput(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'throughput': option_params['throughput'],
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

    def update_csr1000v_throughput(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'throughput': option_params['throughput'],
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

    def delete_csr1000v_throughput(self, device_id, object_id):

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

    # --- L2 --------------------------------------------------------
    def create_csr1000v_wan_interface_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'mtu': option_params['mtu'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
            'tcp_mss': option_params['tcp_mss'],
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

    def update_csr1000v_wan_interface_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'mtu': option_params['mtu'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
            'tcp_mss': option_params['tcp_mss'],
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

    def delete_csr1000v_wan_interface_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
            'mtu': option_params['mtu'],
            'tcp_mss': option_params['tcp_mss'],
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

    def create_csr1000v_wan_interface_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'segment': option_params['segment'],
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

    def update_csr1000v_wan_interface_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'segment': option_params['segment'],
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

    def delete_csr1000v_wan_interface_ipv6(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'segment': option_params['segment'],
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

    # --- L3 --------------------------------------------------------
    def create_csr1000v_wan_interface_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'mtu': option_params['mtu'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
            'tcp_mss': option_params['tcp_mss'],
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

    def update_csr1000v_wan_interface_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'mtu': option_params['mtu'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
            'tcp_mss': option_params['tcp_mss'],
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

    def delete_csr1000v_wan_interface_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'segment': option_params['segment'],
            'netmask_cidr': option_params['netmask_cidr'],
            'mtu': option_params['mtu'],
            'tcp_mss': option_params['tcp_mss'],
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

    def create_csr1000v_tunnel_interface_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'destination_ip_address': option_params['destination_ip_address'],
            'interface': option_params['interface'],
            'segment': option_params['segment'],
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def update_csr1000v_tunnel_interface_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'destination_ip_address': option_params['destination_ip_address'],
            'interface': option_params['interface'],
            'segment': option_params['segment'],
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def delete_csr1000v_tunnel_interface_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'segment': option_params['segment'],
            'ip_address': option_params['ip_address'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def create_csr1000v_tunnel_interface_gre_ipv6(self, device_id, object_id,
                                                  option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'ipv6_segment': option_params['ipv6_segment']
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

    def update_csr1000v_tunnel_interface_gre_ipv6(self, device_id, object_id,
                                                  option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'ipv6_segment': option_params['ipv6_segment'],
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

    def delete_csr1000v_tunnel_interface_gre_ipv6(self, device_id, object_id,
                                                  option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ipv6_address': option_params['ipv6_address'],
            'prefix': option_params['prefix'],
            'ipv6_segment': option_params['ipv6_segment'],
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

    def create_csr1000v_ipsec_basic_esp_gre_ipv4(self, device_id, object_id,
                                option_params
                                ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': option_params['priority'],
            'encryption_algorithm': option_params['encryption_algorithm'],
            'hash_algorithm': option_params['hash_algorithm'],
            'diffie_hellman_group': option_params['diffie_hellman_group'],
            'isakmp_sa_lifetime': option_params['isakmp_sa_lifetime'],
            'transform_set': option_params['transform_set'],
            'encryption_transform': option_params['encryption_transform'],
            'authentication_transform': \
                                option_params['authentication_transform'],
            'ipsec_sa_lifetime': option_params['ipsec_sa_lifetime'],
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

    def update_csr1000v_ipsec_basic_esp_gre_ipv4(self, device_id, object_id,
                                option_params
                                ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': option_params['priority'],
            'encryption_algorithm': option_params['encryption_algorithm'],
            'hash_algorithm': option_params['hash_algorithm'],
            'diffie_hellman_group': option_params['diffie_hellman_group'],
            'isakmp_sa_lifetime': option_params['isakmp_sa_lifetime'],
            'transform_set': option_params['transform_set'],
            'encryption_transform': option_params['encryption_transform'],
            'authentication_transform': \
                                option_params['authentication_transform'],
            'ipsec_sa_lifetime': option_params['ipsec_sa_lifetime'],
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

    def delete_csr1000v_ipsec_basic_esp_gre_ipv4(self, device_id, object_id,
                                option_params
                                ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': option_params['priority'],
            'transform_set': option_params['transform_set'],
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

    def create_csr1000v_ipsec_basic_ah_gre_ipv4(self, device_id, object_id,
                                option_params
                                ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': option_params['priority'],
            'encryption_algorithm': option_params['encryption_algorithm'],
            'hash_algorithm': option_params['hash_algorithm'],
            'diffie_hellman_group': option_params['diffie_hellman_group'],
            'isakmp_sa_lifetime': option_params['isakmp_sa_lifetime'],
            'transform_set': option_params['transform_set'],
            'authentication_transform': \
                                option_params['authentication_transform'],
            'ipsec_sa_lifetime': option_params['ipsec_sa_lifetime'],
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

    def update_csr1000v_ipsec_basic_ah_gre_ipv4(self, device_id, object_id,
                                option_params
                                ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': option_params['priority'],
            'encryption_algorithm': option_params['encryption_algorithm'],
            'hash_algorithm': option_params['hash_algorithm'],
            'diffie_hellman_group': option_params['diffie_hellman_group'],
            'isakmp_sa_lifetime': option_params['isakmp_sa_lifetime'],
            'transform_set': option_params['transform_set'],
            'authentication_transform': \
                                option_params['authentication_transform'],
            'ipsec_sa_lifetime': option_params['ipsec_sa_lifetime'],
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

    def delete_csr1000v_ipsec_basic_ah_gre_ipv4(self, device_id, object_id,
                                option_params
                                ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': option_params['priority'],
            'transform_set': option_params['transform_set'],
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

    def create_csr1000v_ipsec_peer_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'peer_ip_address': option_params['peer_ip_address'],
            'pre_shared_key': option_params['pre_shared_key'],
            'acl_number': option_params['acl_number'],
            'sequence_number': option_params['sequence_number'],
            'transform_set': option_params['transform_set'],
            'interface': option_params['interface'],
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

    def update_csr1000v_ipsec_peer_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'peer_ip_address': option_params['peer_ip_address'],
            'pre_shared_key': option_params['pre_shared_key'],
            'acl_number': option_params['acl_number'],
            'sequence_number': option_params['sequence_number'],
            'transform_set': option_params['transform_set'],
            'interface': option_params['interface'],
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

    def delete_csr1000v_ipsec_peer_gre_ipv4(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'peer_ip_address': option_params['peer_ip_address'],
            'pre_shared_key': option_params['pre_shared_key'],
            'acl_number': option_params['acl_number'],
            'sequence_number': option_params['sequence_number'],
            'interface': option_params['interface'],
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

    def create_csr1000v_static_route_for_dc(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def update_csr1000v_static_route_for_dc(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
            'netmask_cidr': option_params['netmask_cidr'],
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

    def delete_csr1000v_static_route_for_dc(self, device_id, object_id,
                                    option_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': option_params['ip_address'],
            'netmask': option_params['netmask'],
            'nexthop_address': option_params['nexthop_address'],
            'netmask_cidr': option_params['netmask_cidr'],
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
