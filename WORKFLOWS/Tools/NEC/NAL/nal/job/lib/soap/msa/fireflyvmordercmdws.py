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


class FireflyVmOrderCommandWs(base.MsaClientBase):

    OBJECT_FILE_NAME = {
        'create_firefly_vm_system_common': 'Firefly_VM_System_Common',
        'delete_firefly_vm_system_common': 'Firefly_VM_System_Common',
        'create_firefly_vm_wan_interface': 'Firefly_VM_WAN_Interface',
        'delete_firefly_vm_wan_interface': 'Firefly_VM_WAN_Interface',
        'create_firefly_vm_bgp_basic': 'Firefly_VM_BGP_Basic',
        'delete_firefly_vm_bgp_basic': 'Firefly_VM_BGP_Basic',
        'create_firefly_vm_loopback_interface':
                                        'Firefly_VM_Loopback_Interface',
        'delete_firefly_vm_loopback_interface':
                                        'Firefly_VM_Loopback_Interface',
        'create_firefly_vm_lan_interface': 'Firefly_VM_LAN_Interface',
        'delete_firefly_vm_lan_interface': 'Firefly_VM_LAN_Interface',
        'create_firefly_vm_vrrp': 'Firefly_VM_VRRP',
        'delete_firefly_vm_vrrp': 'Firefly_VM_VRRP',
        'create_firefly_vm_bgp_peer': 'Firefly_VM_BGP_Peer',
        'delete_firefly_vm_bgp_peer': 'Firefly_VM_BGP_Peer',
        'create_firefly_vm_vrrp_tracking': 'Firefly_VM_VRRP_Tracking',
        'delete_firefly_vm_vrrp_tracking': 'Firefly_VM_VRRP_Tracking',
        'create_firefly_vm_static_route': 'Firefly_VM_StaticRoute',
        'delete_firefly_vm_static_route': 'Firefly_VM_StaticRoute',
    }

    def __init__(self, api_config_instance,
                 nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'object_execute_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def create_firefly_vm_system_common(self, device_id, host_name,
                                    firefly_vm_system_common_timezone):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_system_common_timezone':
                    firefly_vm_system_common_timezone
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

    def delete_firefly_vm_system_common(self, device_id, host_name,
                                firefly_vm_system_common_timezone):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_system_common_timezone':
                    firefly_vm_system_common_timezone
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
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

    def create_firefly_vm_wan_interface(self, device_id, interface_name,
                                        firefly_vm_wan_interface_ip_address,
                                        firefly_vm_wan_interface_netmask,
                                        firefly_vm_wan_interface_mtu):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_wan_interface_ip_address':
                    firefly_vm_wan_interface_ip_address,
            'Firefly_vm_wan_interface_netmask':
                    firefly_vm_wan_interface_netmask,
            'Firefly_vm_wan_interface_mtu':
                    firefly_vm_wan_interface_mtu,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        interface_name, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_firefly_vm_wan_interface(self, device_id, interface_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        interface_name, self.OBJECT_FILE_NAME, client_name)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_firefly_vm_bgp_basic(self, device_id, host_name,
                                    firefly_vm_bgp_interface_ip_address,
                                    firefly_vm_bgp_local_preference,
                                    firefly_vm_bgp_authkey):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_bgp_interface_ip_address':
                        firefly_vm_bgp_interface_ip_address,
            'Firefly_vm_bgp_local_preference':
                        firefly_vm_bgp_local_preference,
            'Firefly_vm_bgp_authkey':
                        firefly_vm_bgp_authkey,
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

    def delete_firefly_vm_bgp_basic(self, device_id, node_name,
                                firefly_vm_bgp_interface_ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_bgp_interface_ip_address':
                        firefly_vm_bgp_interface_ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        node_name, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_firefly_vm_loopback_interface(self, device_id, interface_name,
                                    firefly_vm_loopback_interface_ip_address,
                                    firefly_vm_loopback_interface_netmask,
                                    firefly_vm_loopback_interface_segment):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_loopback_interface_ip_address':
                        firefly_vm_loopback_interface_ip_address,
            'Firefly_vm_loopback_interface_netmask':
                        firefly_vm_loopback_interface_netmask,
            'Firefly_vm_loopback_interface_segment':
                        firefly_vm_loopback_interface_segment,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        interface_name, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_firefly_vm_loopback_interface(self, device_id, interface_name,
                                        firefly_vm_loopback_interface_netmask,
                                        firefly_vm_loopback_interface_segment):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_loopback_interface_netmask':
                        firefly_vm_loopback_interface_netmask,
            'Firefly_vm_loopback_interface_segment':
                        firefly_vm_loopback_interface_segment,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        interface_name, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_firefly_vm_lan_interface(self, device_id, interface_name,
                                    firefly_vm_lan_interface_ip_address,
                                    firefly_vm_lan_interface_netmask,
                                    firefly_vm_lan_interface_vrrp_ip_address,
                                    firefly_vm_lan_interface_segment):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_lan_interface_ip_address':
                                firefly_vm_lan_interface_ip_address,
            'Firefly_vm_lan_interface_netmask':
                                firefly_vm_lan_interface_netmask,
            'Firefly_vm_lan_interface_vrrp_ip_address':
                                firefly_vm_lan_interface_vrrp_ip_address,
            'Firefly_vm_lan_interface_segment':
                                firefly_vm_lan_interface_segment,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        interface_name, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_firefly_vm_lan_interface(self, device_id, interface_name,
                                        firefly_vm_lan_interface_netmask,
                                        firefly_vm_lan_interface_segment):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_lan_interface_netmask':
                        firefly_vm_lan_interface_netmask,
            'Firefly_vm_lan_interface_segment':
                        firefly_vm_lan_interface_segment,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        interface_name, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_firefly_vm_vrrp(self, device_id, vrrp_interface_name,
                               firefly_vm_vrrp_vip,
                               firefly_vm_lan_interface_ip_address,
                               firefly_vm_lan_interface_netmask,
                               firefly_vm_vrrp_priority,
                               firefly_vm_vrrp_group_id,
                               firefly_vm_vrrp_authkey):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                'Firefly_vm_vrrp_vip':
                                firefly_vm_vrrp_vip,
                'Firefly_vm_lan_interface_ip_address':
                                firefly_vm_lan_interface_ip_address,
                'Firefly_vm_lan_interface_netmask':
                                firefly_vm_lan_interface_netmask,
                'Firefly_vm_vrrp_priority':
                                firefly_vm_vrrp_priority,
                'Firefly_vm_vrrp_group_id':
                                firefly_vm_vrrp_group_id,
                'Firefly_vm_vrrp_authkey':
                                firefly_vm_vrrp_authkey,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        vrrp_interface_name,
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

    def delete_firefly_vm_vrrp(self, device_id, vrrp_interface_name,
                                firefly_vm_vrrp_vip,
                                firefly_vm_lan_interface_ip_address,
                                firefly_vm_lan_interface_netmask,
                                firefly_vm_vrrp_priority,
                                firefly_vm_vrrp_group_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
                'Firefly_vm_vrrp_vip':
                            firefly_vm_vrrp_vip,
                'Firefly_vm_lan_interface_ip_address':
                            firefly_vm_lan_interface_ip_address,
                'Firefly_vm_lan_interface_netmask':
                            firefly_vm_lan_interface_netmask,
                'Firefly_vm_vrrp_priority':
                            firefly_vm_vrrp_priority,
                'Firefly_vm_vrrp_group_id':
                            firefly_vm_vrrp_group_id,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        vrrp_interface_name,
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

    def create_firefly_vm_bgp_peer(self, device_id, opp_host_name,
                                    firefly_vm_bgp_peer_ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
        'Firefly_vm_bgp_peer_ip_address': firefly_vm_bgp_peer_ip_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        opp_host_name, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_firefly_vm_bgp_peer(self, device_id, peer_name,
                                    firefly_vm_bgp_peer_ip_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
        'Firefly_vm_bgp_peer_ip_address': firefly_vm_bgp_peer_ip_address,
       }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        peer_name, self.OBJECT_FILE_NAME, client_name,
                        object_params_option)

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.executeCommand(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def create_firefly_vm_vrrp_tracking(self, device_id, vrrp_tracking_name,
                                        firefly_vm_interface_name,
                                        firefly_vm_lan_interface_ip_address,
                                        firefly_vm_lan_interface_netmask,
                                        firefly_vm_vrrp_group_id,
                                        firefly_vm_vrrp_track_segment,
                                        firefly_vm_vrrp_track_netmask,
                                        firefly_vm_vrrp_track_prioritycost):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_interface_name':
                                firefly_vm_interface_name,
            'Firefly_vm_lan_interface_ip_address':
                                firefly_vm_lan_interface_ip_address,
            'Firefly_vm_lan_interface_netmask':
                                firefly_vm_lan_interface_netmask,
            'Firefly_vm_vrrp_group_id':
                                firefly_vm_vrrp_group_id,
            'Firefly_vm_vrrp_track_segment':
                                firefly_vm_vrrp_track_segment,
            'Firefly_vm_vrrp_track_netmask':
                                firefly_vm_vrrp_track_netmask,
            'Firefly_vm_vrrp_track_prioritycost':
                                firefly_vm_vrrp_track_prioritycost,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        vrrp_tracking_name,
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

    def delete_firefly_vm_vrrp_tracking(self, device_id, vrrp_tracking_name,
                                        firefly_vm_interface_name,
                                        firefly_vm_lan_interface_ip_address,
                                        firefly_vm_lan_interface_netmask,
                                        firefly_vm_vrrp_group_id,
                                        firefly_vm_vrrp_track_segment,
                                        firefly_vm_vrrp_track_netmask):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_interface_name':
                        firefly_vm_interface_name,
            'Firefly_vm_lan_interface_ip_address':
                        firefly_vm_lan_interface_ip_address,
            'Firefly_vm_lan_interface_netmask':
                        firefly_vm_lan_interface_netmask,
            'Firefly_vm_vrrp_group_id':
                        firefly_vm_vrrp_group_id,
            'Firefly_vm_vrrp_track_segment':
                        firefly_vm_vrrp_track_segment,
            'Firefly_vm_vrrp_track_netmask':
                        firefly_vm_vrrp_track_netmask,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        vrrp_tracking_name,
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

    def create_firefly_vm_static_route(self, device_id, static_route_dst_name,
                                    firefly_vm_static_destination_ip_address,
                                    firefly_vm_static_destination_netmask,
                                    firefly_vm_static_nexthop_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_static_destination_ip_address':
                            firefly_vm_static_destination_ip_address,
            'Firefly_vm_static_destination_netmask':
                            firefly_vm_static_destination_netmask,
            'Firefly_vm_static_nexthop_address':
                            firefly_vm_static_nexthop_address,
        }
        msa_params = self.set_msa_cmd_input_params('CREATE', device_id,
                        static_route_dst_name,
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

    def delete_firefly_vm_static_route(self, device_id, static_route_dst_name,
                                    firefly_vm_static_destination_ip_address,
                                    firefly_vm_static_destination_netmask,
                                    firefly_vm_static_nexthop_address):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        object_params_option = {
            'Firefly_vm_static_destination_ip_address':
                        firefly_vm_static_destination_ip_address,
            'Firefly_vm_static_destination_netmask':
                        firefly_vm_static_destination_netmask,
            'Firefly_vm_static_nexthop_address':
                        firefly_vm_static_nexthop_address,
        }
        msa_params = self.set_msa_cmd_input_params('DELETE', device_id,
                        static_route_dst_name,
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
