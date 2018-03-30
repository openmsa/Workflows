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


class Csr1000vOrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        'create_csr1000v_vm_system_common': \
                                'CiscoCsrStdIosXe16dot03dot01aSystemCommon',
        'update_csr1000v_vm_system_common': \
                                'CiscoCsrStdIosXe16dot03dot01aSystemCommon',
        'delete_csr1000v_vm_system_common': \
                                'CiscoCsrStdIosXe16dot03dot01aSystemCommon',
        'create_csr1000v_vm_wan_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aWanInterface',
        'update_csr1000v_vm_wan_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aWanInterface',
        'delete_csr1000v_vm_wan_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aWanInterface',
        'create_csr1000v_vm_lan_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aLanInterface',
        'update_csr1000v_vm_lan_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aLanInterface',
        'delete_csr1000v_vm_lan_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aLanInterface',
        'create_csr1000v_vm_loopback_interface': \
                            'CiscoCsrStdIosXe16dot03dot01aLoopbackInterface',
        'update_csr1000v_vm_loopback_interface': \
                            'CiscoCsrStdIosXe16dot03dot01aLoopbackInterface',
        'delete_csr1000v_vm_loopback_interface': \
                            'CiscoCsrStdIosXe16dot03dot01aLoopbackInterface',
        'create_csr1000v_vm_defaultroute': \
                                'CiscoCsrStdIosXe16dot03dot01aDefaultRoute',
        'update_csr1000v_vm_defaultroute': \
                                'CiscoCsrStdIosXe16dot03dot01aDefaultRoute',
        'delete_csr1000v_vm_defaultroute': \
                                'CiscoCsrStdIosXe16dot03dot01aDefaultRoute',
        'create_csr1000v_vm_staticroute': \
                                'CiscoCsrStdIosXe16dot03dot01aStaticRoute',
        'update_csr1000v_vm_staticroute': \
                                'CiscoCsrStdIosXe16dot03dot01aStaticRoute',
        'delete_csr1000v_vm_staticroute': \
                                'CiscoCsrStdIosXe16dot03dot01aStaticRoute',
        'create_csr1000v_vm_bgp_basic': \
                                'CiscoCsrStdIosXe16dot03dot01aBgpBasic',
        'update_csr1000v_vm_bgp_basic': \
                                'CiscoCsrStdIosXe16dot03dot01aBgpBasic',
        'delete_csr1000v_vm_bgp_basic': \
                                'CiscoCsrStdIosXe16dot03dot01aBgpBasic',
        'create_csr1000v_vm_bgp_peer': \
                                'CiscoCsrStdIosXe16dot03dot01aBgpPeer',
        'update_csr1000v_vm_bgp_peer': \
                                'CiscoCsrStdIosXe16dot03dot01aBgpPeer',
        'delete_csr1000v_vm_bgp_peer': \
                                'CiscoCsrStdIosXe16dot03dot01aBgpPeer',
        'create_csr1000v_vm_hsrp_primary': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpPrimary',
        'update_csr1000v_vm_hsrp_primary': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpPrimary',
        'delete_csr1000v_vm_hsrp_primary': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpPrimary',
        'create_csr1000v_vm_hsrp_secondary': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpSecondary',
        'update_csr1000v_vm_hsrp_secondary': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpSecondary',
        'delete_csr1000v_vm_hsrp_secondary': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpSecondary',
        'create_csr1000v_vm_hsrp_tracking': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpTracking',
        'update_csr1000v_vm_hsrp_tracking': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpTracking',
        'delete_csr1000v_vm_hsrp_tracking': \
                                'CiscoCsrStdIosXe16dot03dot01aHsrpTracking',
        'create_csr1000v_vm_hsrp_interface_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking',
        'update_csr1000v_vm_hsrp_interface_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking',
        'delete_csr1000v_vm_hsrp_interface_tracking': \
                        'CiscoCsrStdIosXe16dot03dot01aHsrpInterfaceTracking',
        'create_csr1000v_vm_snmp': 'CiscoCsrStdIosXe16dot03dot01aSnmp',
        'update_csr1000v_vm_snmp': 'CiscoCsrStdIosXe16dot03dot01aSnmp',
        'delete_csr1000v_vm_snmp': 'CiscoCsrStdIosXe16dot03dot01aSnmp',
        'create_csr1000v_vm_syslog': 'CiscoCsrStdIosXe16dot03dot01aSyslog',
        'update_csr1000v_vm_syslog': 'CiscoCsrStdIosXe16dot03dot01aSyslog',
        'delete_csr1000v_vm_syslog': 'CiscoCsrStdIosXe16dot03dot01aSyslog',
        'create_csr1000v_vm_ntp': 'CiscoCsrStdIosXe16dot03dot01aNtp',
        'update_csr1000v_vm_ntp': 'CiscoCsrStdIosXe16dot03dot01aNtp',
        'delete_csr1000v_vm_ntp': 'CiscoCsrStdIosXe16dot03dot01aNtp',
        'create_csr1000v_vm_dns': 'CiscoCsrStdIosXe16dot03dot01aDns',
        'update_csr1000v_vm_dns': 'CiscoCsrStdIosXe16dot03dot01aDns',
        'delete_csr1000v_vm_dns': 'CiscoCsrStdIosXe16dot03dot01aDns',
        'create_csr1000v_vm_license': 'CiscoCsrStdIosXe16dot03dot01aLicense',
        'update_csr1000v_vm_license': 'CiscoCsrStdIosXe16dot03dot01aLicense',
        'delete_csr1000v_vm_license': 'CiscoCsrStdIosXe16dot03dot01aLicense',
        'create_csr1000v_vm_throughput': \
                                    'CiscoCsrStdIosXe16dot03dot01aThroughput',
        'update_csr1000v_vm_throughput': \
                                    'CiscoCsrStdIosXe16dot03dot01aThroughput',
        'delete_csr1000v_vm_throughput': \
                                    'CiscoCsrStdIosXe16dot03dot01aThroughput',
        'create_csr1000v_vm_tunnel_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aTunnelInterface',
        'update_csr1000v_vm_tunnel_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aTunnelInterface',
        'delete_csr1000v_vm_tunnel_interface': \
                                'CiscoCsrStdIosXe16dot03dot01aTunnelInterface',
        'create_csr1000v_vm_ipsec_basic_esp': \
                                'CiscoCsrStdIosXe16dot03dot01aIpsecBasicEsp',
        'update_csr1000v_vm_ipsec_basic_esp': \
                                'CiscoCsrStdIosXe16dot03dot01aIpsecBasicEsp',
        'delete_csr1000v_vm_ipsec_basic_esp': \
                                'CiscoCsrStdIosXe16dot03dot01aIpsecBasicEsp',
        'create_csr1000v_vm_ipsec_basic_ah': \
                                'CiscoCsrStdIosXe16dot03dot01aIpsecBasicAh',
        'update_csr1000v_vm_ipsec_basic_ah': \
                                'CiscoCsrStdIosXe16dot03dot01aIpsecBasicAh',
        'delete_csr1000v_vm_ipsec_basic_ah': \
                                'CiscoCsrStdIosXe16dot03dot01aIpsecBasicAh',
        'create_csr1000v_vm_ipsec_peer': \
                                    'CiscoCsrStdIosXe16dot03dot01aIpsecPeer',
        'update_csr1000v_vm_ipsec_peer': \
                                    'CiscoCsrStdIosXe16dot03dot01aIpsecPeer',
        'delete_csr1000v_vm_ipsec_peer': \
                                    'CiscoCsrStdIosXe16dot03dot01aIpsecPeer',
        'create_csr1000v_vm_staticroute_for_dc': \
                            'CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc',
        'update_csr1000v_vm_staticroute_for_dc': \
                            'CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc',
        'delete_csr1000v_vm_staticroute_for_dc': \
                            'CiscoCsrStdIosXe16dot03dot01aStaticRouteForDc',
    }

    def __init__(self, api_config_instance,
                 nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def create_csr1000v_vm_system_common(self,
                                         device_id,
                                         object_id,
                                         timezone):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'timezone': timezone,
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

    def update_csr1000v_vm_system_common(self,
                                         device_id,
                                         object_id,
                                         timezone):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'timezone': timezone,
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

    def delete_csr1000v_vm_system_common(self,
                                         device_id,
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

    def create_csr1000v_vm_wan_interface(self,
                                         device_id,
                                         object_id,
                                         ip_address,
                                         netmask,
                                         mtu,
                                         segment,
                                         netmask_cidr
                                         ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'mtu': mtu,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def update_csr1000v_vm_wan_interface(self,
                                         device_id,
                                         object_id,
                                        ip_address,
                                        netmask,
                                        mtu,
                                        segment,
                                        netmask_cidr
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'mtu': mtu,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def delete_csr1000v_vm_wan_interface(self,
                                         device_id,
                                         object_id,
                                         ip_address,
                                         mtu,
                                         segment,
                                         netmask_cidr
                                         ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'mtu': mtu,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def create_csr1000v_vm_lan_interface(self,
                                         device_id,
                                         object_id,
                                         ip_address,
                                         netmask,
                                         hsrp_ip_address,
                                         segment,
                                         netmask_cidr
                                         ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'hsrp_ip_address': hsrp_ip_address,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def update_csr1000v_vm_lan_interface(self,
                                         device_id,
                                         object_id,
                                         ip_address,
                                         netmask,
                                         hsrp_ip_address,
                                         segment,
                                         netmask_cidr
                                         ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'hsrp_ip_address': hsrp_ip_address,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def delete_csr1000v_vm_lan_interface(self,
                                         device_id,
                                         object_id,
                                         ip_address,
                                         hsrp_ip_address,
                                         segment,
                                         netmask_cidr
                                         ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'hsrp_ip_address': hsrp_ip_address,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def create_csr1000v_vm_loopback_interface(self,
                                              device_id,
                                              object_id,
                                              ip_address,
                                              netmask,
                                              segment,
                                              netmask_cidr
                                              ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def update_csr1000v_vm_loopback_interface(self,
                                              device_id,
                                              object_id,
                                              ip_address,
                                              netmask,
                                              segment,
                                              netmask_cidr
                                              ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def delete_csr1000v_vm_loopback_interface(self,
                                              device_id,
                                              object_id,
                                              ip_address,
                                              segment,
                                              netmask_cidr
                                              ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
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

    def create_csr1000v_vm_defaultroute(self,
                                        device_id,
                                        object_id,
                                        ip_address,
                                        netmask,
                                        nexthop_address,
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask':  netmask,
            'nexthop_address': nexthop_address,
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

    def update_csr1000v_vm_defaultroute(self,
                                        device_id,
                                        object_id,
                                        ip_address,
                                        netmask,
                                        nexthop_address,
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'nexthop_address': nexthop_address,
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

    def delete_csr1000v_vm_defaultroute(self,
                                        device_id,
                                        object_id,
                                        ip_address,
                                        netmask,
                                        nexthop_address,
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'nexthop_address': nexthop_address,
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

    def create_csr1000v_vm_staticroute(self,
                                       device_id,
                                       object_id,
                                       ip_address,
                                       netmask,
                                       nexthop_address,
                                       netmask_cidr
                                       ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask':  netmask,
            'nexthop_address': nexthop_address,
            'netmask_cidr': netmask_cidr,
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

    def update_csr1000v_vm_staticroute(self,
                                       device_id,
                                       object_id,
                                       ip_address,
                                       netmask,
                                       nexthop_address,
                                       netmask_cidr
                                       ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'nexthop_address': nexthop_address,
            'netmask_cidr': netmask_cidr,
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

    def delete_csr1000v_vm_staticroute(self,
                                       device_id,
                                       object_id,
                                       ip_address,
                                       netmask,
                                       nexthop_address,
                                       netmask_cidr
                                       ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'nexthop_address': nexthop_address,
            'netmask_cidr': netmask_cidr,
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

    def create_csr1000v_vm_bgp_basic(self,
                                     device_id,
                                     object_id,
                                     ip_address,
                                     local_preference
                                     ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'local_preference': local_preference,
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

    def update_csr1000v_vm_bgp_basic(self,
                                     device_id,
                                     object_id,
                                     ip_address,
                                     local_preference
                                     ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'local_preference': local_preference,
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

    def delete_csr1000v_vm_bgp_basic(self,
                                     device_id,
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

    def create_csr1000v_vm_bgp_peer(self,
                                    device_id,
                                    object_id,
                                    ip_address,
                                    authkey,
                                    interface
                                    ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'authkey': authkey,
            'interface': interface,
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

    def update_csr1000v_vm_bgp_peer(self,
                                    device_id,
                                    object_id,
                                    ip_address,
                                    authkey,
                                    interface
                                    ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'authkey': authkey,
            'interface': interface,
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

    def delete_csr1000v_vm_bgp_peer(self,
                                    device_id,
                                    object_id,
                                    ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
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

    def create_csr1000v_vm_hsrp_primary(self,
                                        device_id,
                                        object_id,
                                        ip_address,
                                        priority,
                                        group_id,
                                        authkey
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'priority': priority,
            'group_id': group_id,
            'authkey': authkey,
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

    def update_csr1000v_vm_hsrp_primary(self,
                                        device_id,
                                        object_id,
                                        ip_address,
                                        priority,
                                        group_id,
                                        authkey
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'priority': priority,
            'group_id': group_id,
            'authkey': authkey,
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

    def delete_csr1000v_vm_hsrp_primary(self,
                                        device_id,
                                        object_id,
                                        hsrp_group_id
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'hsrp_group_id': hsrp_group_id,
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

    def create_csr1000v_vm_hsrp_secondary(self,
                                          device_id,
                                          object_id,
                                          ip_address,
                                          priority,
                                          group_id,
                                          authkey
                                          ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'priority': priority,
            'group_id': group_id,
            'authkey': authkey,
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

    def update_csr1000v_vm_hsrp_secondary(self,
                                          device_id,
                                          object_id,
                                          ip_address,
                                          priority,
                                          group_id,
                                          authkey
                                          ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'priority': priority,
            'group_id': group_id,
            'authkey': authkey,
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

    def delete_csr1000v_vm_hsrp_secondary(self,
                                          device_id,
                                          object_id,
                                          group_id
                                          ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'group_id': group_id,
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

    def create_csr1000v_vm_hsrp_tracking(self,
                                         device_id,
                                         object_id,
                                         interface,
                                         group_id,
                                         segment,
                                         netmask,
                                         prioritycost,
                                         track_id
                                         ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
            'group_id': group_id,
            'segment': segment,
            'netmask': netmask,
            'prioritycost': prioritycost,
            'track_id': track_id,
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

    def update_csr1000v_vm_hsrp_tracking(self,
                                         device_id,
                                         object_id,
                                         interface,
                                         group_id,
                                         segment,
                                         netmask,
                                         prioritycost,
                                         track_id
                                         ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
            'group_id': group_id,
            'segment': segment,
            'netmask': netmask,
            'prioritycost': prioritycost,
            'track_id': track_id,
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

    def delete_csr1000v_vm_hsrp_tracking(self,
                                         device_id,
                                         object_id,
                                         interface,
                                         group_id,
                                         track_id
                                         ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
            'group_id': group_id,
            'track_id': track_id,
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

    def create_csr1000v_vm_hsrp_interface_tracking(self,
                                                   device_id,
                                                   object_id,
                                                   interface,
                                                   group_id,
                                                   track_interface,
                                                   prioritycost,
                                                   track_id
                                                   ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
            'group_id': group_id,
            'track_interface': track_interface,
            'prioritycost': prioritycost,
            'track_id': track_id,
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

    def update_csr1000v_vm_hsrp_interface_tracking(self,
                                                   device_id,
                                                   object_id,
                                                   interface,
                                                   group_id,
                                                   track_interface,
                                                   prioritycost,
                                                   track_id
                                                   ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
            'group_id': group_id,
            'track_interface': track_interface,
            'prioritycost': prioritycost,
            'track_id': track_id,
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

    def delete_csr1000v_vm_hsrp_interface_tracking(self,
                                                   device_id,
                                                   object_id,
                                                   interface,
                                                   group_id,
                                                   track_id
                                                   ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'interface': interface,
            'group_id': group_id,
            'track_id': track_id,
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

    def create_csr1000v_vm_snmp(self,
                                device_id,
                                object_id,
                                community_name,
                                interface,
                                ip_address,
                                version
                                ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'community_name': community_name,
            'interface': interface,
            'ip_address': ip_address,
            'version': version,
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

    def update_csr1000v_vm_snmp(self,
                                device_id,
                                object_id,
                                community_name,
                                interface,
                                ip_address,
                                version
                                ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'community_name': community_name,
            'interface': interface,
            'ip_address': ip_address,
            'version': version,
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

    def delete_csr1000v_vm_snmp(self,
                                device_id,
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

    def create_csr1000v_vm_syslog(self,
                                  device_id,
                                  object_id,
                                  ip_address,
                                  interface,
                                  facility,
                                  severity
                                  ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'interface': interface,
            'facility': facility,
            'severity': severity,
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

    def update_csr1000v_vm_syslog(self,
                                  device_id,
                                  object_id,
                                  ip_address,
                                  interface,
                                  facility,
                                  severity
                                  ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'interface': interface,
            'facility': facility,
            'severity': severity,
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

    def delete_csr1000v_vm_syslog(self,
                                  device_id,
                                  object_id,
                                  ip_address,
                                  interface
                                  ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'interface': interface,
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

    def create_csr1000v_vm_ntp(self,
                               device_id,
                               object_id,
                               ip_address,
                               interface
                               ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'interface': interface,
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

    def update_csr1000v_vm_ntp(self,
                               device_id,
                               object_id,
                               ip_address,
                               interface
                               ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'interface': interface,
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

    def delete_csr1000v_vm_ntp(self,
                               device_id,
                               object_id,
                               ip_address,
                               interface
                               ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'interface': interface,
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

    def create_csr1000v_vm_dns(self, device_id, object_id, ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
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

    def update_csr1000v_vm_dns(self, device_id, object_id, ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
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

    def delete_csr1000v_vm_dns(self, device_id, object_id, ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
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

    def create_csr1000v_vm_license(self, device_id, object_id, idtoken):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'idtoken': idtoken,
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

    def update_csr1000v_vm_license(self, device_id, object_id, idtoken):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'idtoken': idtoken,
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

    def delete_csr1000v_vm_license(self, device_id, object_id):

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

    def create_csr1000v_vm_throughput(self, device_id, object_id, throughput):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'throughput': throughput,
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

    def update_csr1000v_vm_throughput(self, device_id, object_id, throughput):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'throughput': throughput,
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

    def delete_csr1000v_vm_throughput(self, device_id, object_id):

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

    def create_csr1000v_vm_tunnel_interface(self, device_id, object_id,
                                            ip_address,
                                            netmask,
                                            segment,
                                            netmask_cidr,
                                            destination_ip_address,
                                            interface,
                                            profile_name
                                            ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
            'destination_ip_address': destination_ip_address,
            'interface': interface,
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

    def update_csr1000v_vm_tunnel_interface(self, device_id, object_id,
                                            ip_address,
                                            netmask,
                                            segment,
                                            netmask_cidr,
                                            destination_ip_address,
                                            interface,
                                            profile_name
                                            ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
            'destination_ip_address': destination_ip_address,
            'interface': interface,
            'profile_name': profile_name,
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

    def delete_csr1000v_vm_tunnel_interface(self, device_id, object_id,
                                            ip_address,
                                            netmask,
                                            segment,
                                            netmask_cidr,
                                            destination_ip_address,
                                            interface,
                                            profile_name
                                            ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'segment': segment,
            'netmask_cidr': netmask_cidr,
            'destination_ip_address': destination_ip_address,
            'interface': interface,
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

    def create_csr1000v_vm_ipsec_basic_esp(self, device_id, object_id,
                                           other_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': other_params['priority'],
            'encryption_algorithm': other_params['encryption_algorithm'],
            'hash_algorithm': other_params['hash_algorithm'],
            'diffie_hellman_group': other_params['diffie_hellman_group'],
            'isakmp_sa_lifetime': other_params['isakmp_sa_lifetime'],
            'transform_set': other_params['transform_set'],
            'encryption_transform': other_params['encryption_transform'],
            'authentication_transform': \
                                 other_params['authentication_transform'],
            'ipsec_sa_lifetime': other_params['ipsec_sa_lifetime'],
            'profile_name': other_params['profile_name'],
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

    def update_csr1000v_vm_ipsec_basic_esp(self, device_id, object_id,
                                           other_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': other_params['priority'],
            'encryption_algorithm': other_params['encryption_algorithm'],
            'hash_algorithm': other_params['hash_algorithm'],
            'diffie_hellman_group': other_params['diffie_hellman_group'],
            'isakmp_sa_lifetime': other_params['isakmp_sa_lifetime'],
            'transform_set': other_params['transform_set'],
            'encryption_transform': other_params['encryption_transform'],
            'authentication_transform': \
                                other_params['authentication_transform'],
            'ipsec_sa_lifetime': other_params['ipsec_sa_lifetime'],
            'profile_name': other_params['profile_name'],
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

    def delete_csr1000v_vm_ipsec_basic_esp(self, device_id, object_id,
                                           other_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': other_params['priority'],
            'transform_set': other_params['transform_set'],
            'profile_name': other_params['profile_name'],
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

    def create_csr1000v_vm_ipsec_basic_ah(self, device_id, object_id,
                                          other_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': other_params['priority'],
            'encryption_algorithm': other_params['encryption_algorithm'],
            'hash_algorithm': other_params['hash_algorithm'],
            'diffie_hellman_group': other_params['diffie_hellman_group'],
            'isakmp_sa_lifetime': other_params['isakmp_sa_lifetime'],
            'transform_set': other_params['transform_set'],
            'authentication_transform': \
                                other_params['authentication_transform'],
            'ipsec_sa_lifetime': other_params['ipsec_sa_lifetime'],
            'profile_name': other_params['profile_name'],
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

    def update_csr1000v_vm_ipsec_basic_ah(self, device_id, object_id,
                                          other_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': other_params['priority'],
            'encryption_algorithm': other_params['encryption_algorithm'],
            'hash_algorithm': other_params['hash_algorithm'],
            'diffie_hellman_group': other_params['diffie_hellman_group'],
            'isakmp_sa_lifetime': other_params['isakmp_sa_lifetime'],
            'transform_set': other_params['transform_set'],
            'authentication_transform': \
                                other_params['authentication_transform'],
            'ipsec_sa_lifetime': other_params['ipsec_sa_lifetime'],
            'profile_name': other_params['profile_name'],
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

    def delete_csr1000v_vm_ipsec_basic_ah(self, device_id, object_id,
                                          other_params):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'priority': other_params['priority'],
            'transform_set': other_params['transform_set'],
            'profile_name': other_params['profile_name'],
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

    def create_csr1000v_vm_ipsec_peer(self, device_id, object_id,
                                        ip_address,
                                        pre_shared_key
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'pre_shared_key': pre_shared_key,
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

    def update_csr1000v_vm_ipsec_peer(self, device_id, object_id,
                                        ip_address,
                                        pre_shared_key
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'pre_shared_key': pre_shared_key,
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

    def delete_csr1000v_vm_ipsec_peer(self, device_id, object_id,
                                        ip_address,
                                        pre_shared_key
                                        ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'pre_shared_key': pre_shared_key,
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

    def create_csr1000v_vm_staticroute_for_dc(self, device_id, object_id,
                                            ip_address,
                                            netmask,
                                            nexthop_address,
                                            interface,
                                            netmask_cidr
                                            ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'nexthop_address': nexthop_address,
            'interface': interface,
            'netmask_cidr': netmask_cidr,
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

    def update_csr1000v_vm_staticroute_for_dc(self, device_id, object_id,
                                            ip_address,
                                            netmask,
                                            nexthop_address,
                                            interface,
                                            netmask_cidr
                                            ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'nexthop_address': nexthop_address,
            'interface': interface,
            'netmask_cidr': netmask_cidr,
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

    def delete_csr1000v_vm_staticroute_for_dc(self, device_id, object_id,
                                            ip_address,
                                            netmask,
                                            nexthop_address,
                                            interface,
                                            netmask_cidr
                                            ):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'ip_address': ip_address,
            'netmask': netmask,
            'nexthop_address': nexthop_address,
            'interface': interface,
            'netmask_cidr': netmask_cidr,
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
