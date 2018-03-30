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
import json
import traceback

from job.auto import base
from job.lib.db import create
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import ciscocsrstdiosxeordercmdws
from job.lib.soap.msa import fireflyvmordercmdws


class ConnectWim(base.JobAutoBase):

    CSR1000V_VARIABLE_CONFIG = {
        'hsrp_group_id': {
            '4': 1,
            '6': 1000,
        },
        'hsrp_track_id_prefix': {
            '4': '0',
            '6': '1',
        },
    }

    def dc_connect_firefly_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        dc_member_list = job_input['dc_member_list']

        # Create Router Connection Setting(Firefly VM)
        if len(dc_member_list) > 0:
            self.__dc_connect_firefly_vm(job_input, 'create')

        # Create WIM_DC_CONNECT_MEMBER_MNG(DB)
        self.__create_db_dc_member(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def dc_connect_csr1000v_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        dc_member_list = job_input['dc_member_list']

        # Create Router Connection Setting
        if len(dc_member_list) > 0:
            self.__dc_connect_csr1000v_vm(job_input, 'create')

        # Create WIM_DC_CONNECT_MEMBER_MNG(DB)
        self.__create_db_dc_member(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_dc_connect_csr1000v_for_tunnel(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        dc_member_list = job_input['dc_member_list']

        # Create Router Connection Setting
        if len(dc_member_list) > 0:
            self.__dc_connect_csr1000v_vm_for_tunnel(job_input, 'create')

        # Create WIM_DC_CONNECT_MEMBER_MNG(DB)
        self.__create_db_dc_member(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def dc_connect_update_firefly_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create Router Connection Setting(Firefly VM)
        self.__dc_connect_firefly_vm(job_input)

        # Create WIM_DC_CONNECT_MEMBER_MNG(DB)
        self.__create_db_dc_member(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def dc_connect_update_csr1000v_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create Router Connection Setting(Firefly VM)
        self.__dc_connect_csr1000v_vm(job_input)

        # Create WIM_DC_CONNECT_MEMBER_MNG(DB)
        self.__create_db_dc_member(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_dc_connect_update_csr1000v_for_tunnel(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create Router Connection Setting(CSR1000v)
        self.__dc_connect_csr1000v_vm_for_tunnel(job_input)

        # Create WIM_DC_CONNECT_MEMBER_MNG(DB)
        self.__create_db_dc_member(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def dc_disconnect_firefly_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Delete Router Connection Setting(Firefly VM)
        self.__dc_disconnect_firefly_vm(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def dc_disconnect_csr1000v_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Delete Router Connection Setting(CISCO CSR1000V)
        self.__dc_disconnect_csr1000v_vm(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_dc_disconnect_csr1000v_for_tunnel(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Delete Router Connection Setting(CISCO CSR1000V)
        self.__dc_disconnect_csr1000v_vm_for_tunnel(job_input)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __dc_connect_firefly_vm(self, job_input, mode=''):

        # Get JOB Input Parameters
        ce_info = job_input['ce_info']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        dc_member_list = job_input['dc_member_list']

        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        dc_self_id = dc_id

        dc_self_ce1_msa_device_id = ce_info[0]['MSA_device_id']
        dc_self_ce1_host_name = ce_info[0]['host_name']
        dc_self_ce1_wan_ip_address = ce_info[0]['wan_ip_address']
        dc_self_ce1_lan_ip_address = ce_info[0]['lan_ip_address']
        dc_self_ce1_lan_netmask = ce_info[0]['lan_netmask']
        dc_self_ce1_loopback_seg = ce_info[0]['loopback_seg']
        dc_self_ce1_loopback_netmask = ce_info[0]['loopback_netmask']

        dc_self_ce2_msa_device_id = ce_info[1]['MSA_device_id']
        dc_self_ce2_host_name = ce_info[1]['host_name']
        dc_self_ce2_wan_ip_address = ce_info[1]['wan_ip_address']
        dc_self_ce2_lan_ip_address = ce_info[1]['lan_ip_address']
        dc_self_ce2_lan_netmask = ce_info[1]['lan_netmask']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_self_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_self_id)
        nic_name = msa_config_for_device['nic_prefix']

        # Create Instance(MSA Soap Client)(DC_SELF)
        msa_self = fireflyvmordercmdws.FireflyVmOrderCommandWs(
                                self.job_config,
                                self.nal_endpoint_config, pod_id, dc_self_id)

        if mode == 'create':

            # Create BGP Peer(DC_SELF-CE#1)
            msa_self.create_firefly_vm_bgp_peer(dc_self_ce1_msa_device_id,
                                               dc_self_ce1_host_name,
                                               dc_self_ce1_wan_ip_address)

            # Create BGP Peer(DC_SELF-CE#2)
            msa_self.create_firefly_vm_bgp_peer(dc_self_ce2_msa_device_id,
                                               dc_self_ce2_host_name,
                                               dc_self_ce2_wan_ip_address)

        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_self_id:
                continue

            dc_other_id = dc_member['dc_id']

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_ce1_msa_device_id = ce1_info['MSA_device_id']
            dc_other_ce1_host_name = ce1_info['host_name']
            dc_other_ce1_wan_ip_address = ce1_info['wan_ip_address']
            dc_other_ce1_lan_ip_address = ce1_info['lan_ip_address']
            dc_other_ce1_lan_netmask = ce1_info['lan_netmask']
            dc_other_ce1_loopback_seg = ce1_info['loopback_seg']
            dc_other_ce1_loopback_netmask = ce1_info['loopback_netmask']

            dc_other_ce2_msa_device_id = ce2_info['MSA_device_id']
            dc_other_ce2_host_name = ce2_info['host_name']
            dc_other_ce2_wan_ip_address = ce2_info['wan_ip_address']
            dc_other_ce2_lan_ip_address = ce2_info['lan_ip_address']
            dc_other_ce2_lan_netmask = ce2_info['lan_netmask']

            tracking_name_self = nic_name + '-' + dc_self_id
            tracking_name_other = nic_name + '-' + dc_other_id

            if mode == 'create':

                # Create BGP Peer(DC_SELF-CE#1)
                msa_self.create_firefly_vm_bgp_peer(dc_self_ce1_msa_device_id,
                                               dc_other_ce1_host_name,
                                               dc_other_ce1_wan_ip_address)

                msa_self.create_firefly_vm_bgp_peer(dc_self_ce2_msa_device_id,
                                               dc_other_ce2_host_name,
                                               dc_other_ce2_wan_ip_address)

            # Create VRRP Tracking(DC_SELF-CE#1)
            msa_self.create_firefly_vm_vrrp_tracking(dc_self_ce1_msa_device_id,
                                                tracking_name_other,
                                                nic_name,
                                                dc_self_ce1_lan_ip_address,
                                                dc_self_ce1_lan_netmask,
                                                1,
                                                dc_other_ce1_loopback_seg,
                                                dc_other_ce1_loopback_netmask,
                                                10)

            if mode == 'create':
                # Create BGP Peer(DC_SELF-CE#2)
                msa_self.create_firefly_vm_bgp_peer(dc_self_ce2_msa_device_id,
                                               dc_other_ce1_host_name,
                                               dc_other_ce1_wan_ip_address)

                msa_self.create_firefly_vm_bgp_peer(dc_self_ce2_msa_device_id,
                                               dc_other_ce2_host_name,
                                               dc_other_ce2_wan_ip_address)

            # Create VRRP Tracking(DC_SELF-CE#2)
            msa_self.create_firefly_vm_vrrp_tracking(dc_self_ce2_msa_device_id,
                                                tracking_name_other,
                                                nic_name,
                                                dc_self_ce2_lan_ip_address,
                                                dc_self_ce2_lan_netmask,
                                                1,
                                                dc_other_ce1_loopback_seg,
                                                dc_other_ce1_loopback_netmask,
                                                10)

            # Create Instance(MSA Soap Client)(DC_OTHER)
            msa_other = fireflyvmordercmdws.FireflyVmOrderCommandWs(
                                self.job_config,
                                self.nal_endpoint_config, pod_id, dc_other_id)

            if mode == 'create':
                # Create BGP Peer(DC_OTHER-CE#1)
                msa_other.create_firefly_vm_bgp_peer(
                                            dc_other_ce1_msa_device_id,
                                               dc_self_ce1_host_name,
                                               dc_self_ce1_wan_ip_address)

                msa_other.create_firefly_vm_bgp_peer(
                                            dc_other_ce1_msa_device_id,
                                               dc_self_ce2_host_name,
                                               dc_self_ce2_wan_ip_address)

            # Create VRRP Tracking(DC_OTHER-CE#1)
            msa_other.create_firefly_vm_vrrp_tracking(
                                            dc_other_ce1_msa_device_id,
                                                tracking_name_self,
                                                nic_name,
                                                dc_other_ce1_lan_ip_address,
                                                dc_other_ce1_lan_netmask,
                                                1,
                                                dc_self_ce1_loopback_seg,
                                                dc_self_ce1_loopback_netmask,
                                                10)

            if mode == 'create':
                # Create BGP Peer(DC_OTHER-CE#2)
                msa_other.create_firefly_vm_bgp_peer(
                                            dc_other_ce2_msa_device_id,
                                               dc_self_ce1_host_name,
                                               dc_self_ce1_wan_ip_address)

                msa_other.create_firefly_vm_bgp_peer(
                                            dc_other_ce2_msa_device_id,
                                               dc_self_ce2_host_name,
                                               dc_self_ce2_wan_ip_address)

            # Create VRRP Tracking(DC_OTHER-CE#2)
            msa_other.create_firefly_vm_vrrp_tracking(
                                            dc_other_ce2_msa_device_id,
                                                tracking_name_self,
                                                nic_name,
                                                dc_other_ce2_lan_ip_address,
                                                dc_other_ce2_lan_netmask,
                                                1,
                                                dc_self_ce1_loopback_seg,
                                                dc_self_ce1_loopback_netmask,
                                                10)

    def __dc_connect_csr1000v_vm(self, job_input, mode=''):

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        group_rec_id = job_input['group_rec_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        dc_member_list = job_input['dc_member_list']

        # Get JOB Input Router Info
        ce_info = job_input['ce_info']

        dc_self_loopback_seg = ce_info[0]['loopback_seg']
        dc_self_loopback_netmask = ce_info[0]['loopback_netmask']
        dc_self_hsrp_track_prioritycost \
            = ce_info[0]['csr1000v']['hsrp_track_prioritycost']

        dc_self_ce1_msa_device_id = ce_info[0]['MSA_device_id']
        dc_self_ce1_host_name = ce_info[0]['host_name']
        dc_self_ce1_wan_ip_address = ce_info[0]['wan_ip_address']
        dc_self_ce1_nic = ce_info[0]['nic']
        dc_self_lan_ip_ver = self.utils.get_ipaddress_version(
                                    ce_info[0]['lan_ip_address'])

        dc_self_ce2_msa_device_id = ce_info[1]['MSA_device_id']
        dc_self_ce2_host_name = ce_info[1]['host_name']
        dc_self_ce2_wan_ip_address = ce_info[1]['wan_ip_address']
        dc_self_ce2_nic = ce_info[1]['nic']

        dc_self_id = dc_id
        dc_self_list = self.__get_dc_info(dc_self_id)

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_self_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_self_id)
        prefix = msa_config_for_device['nic_prefix']

        # -----------------------------------------------------------------
        # Self DC Setting
        # -----------------------------------------------------------------
        # Create Instance(MSA Soap Client)(DC_SELF)
        msa_self = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                                     self.job_config,
                                                     self.nal_endpoint_config,
                                                     pod_id,
                                                     dc_self_id)

        dc_uniq_list = []
        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_self_id:
                continue

            dc_other_id = dc_member['dc_id']
            dc_other_list = self.__get_dc_info(dc_other_id)

            bgp_wan_interface = \
                            msa_config_for_device['nic_prefix'] \
                                + msa_config_for_device['nic_for_wan']

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_loopback_seg = ce1_info['loopback_seg']
            dc_other_loopback_netmask = ce1_info['loopback_netmask']
            dc_other_hsrp_track_prioritycost \
                        = ce1_info['csr1000v']['hsrp_track_prioritycost']

            dc_other_ce1_host_name = ce1_info['host_name']
            dc_other_ce1_wan_ip_address = ce1_info['wan_ip_address']

            dc_other_ce2_host_name = ce2_info['host_name']
            dc_other_ce2_wan_ip_address = ce2_info['wan_ip_address']

            if dc_member['dc_id'] not in dc_uniq_list:
                if mode == 'create':

                    dc_uniq_list.append(dc_member['dc_id'])

                    # Create BGP Peer IPv4(MSA)
                    msa_client_name = 'create_csr1000v_bgp_peer_ipv4'
                    msa_option_params = {
                        'authkey': authkey,
                        'interface': bgp_wan_interface,
                    }

                    # selfDC CE#1 - otherDC CE#1
                    msa_option_params['ip_address'] \
                        = dc_other_ce1_wan_ip_address[self.utils.IP_VER_V4]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_other_ce1_host_name,
                        msa_option_params
                    )
                    # selfDC CE#1 - otherDC CE#2
                    msa_option_params['ip_address'] \
                        = dc_other_ce2_wan_ip_address[self.utils.IP_VER_V4]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )
                    # selfDC CE#2 - otherDC CE#1
                    msa_option_params['ip_address'] \
                        = dc_other_ce1_wan_ip_address[self.utils.IP_VER_V4]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce1_host_name,
                        msa_option_params
                    )
                    # selfDC CE#2 - otherDC CE#2
                    msa_option_params['ip_address'] \
                        = dc_other_ce2_wan_ip_address[self.utils.IP_VER_V4]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )

                # Create HSRP Tracking(MSA)
                msa_client_name = 'create_csr1000v_hsrp_tracking'

                dc_other_hsrp_netmask = \
                    self.utils.get_subnet_mask_from_cidr_ipv6(
                                        dc_other_loopback_seg + '/' \
                                        + str(dc_other_loopback_netmask))

                dc_other_hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][dc_self_lan_ip_ver]

                dc_other_ce1_hsrp_track_id = self.__get_hsrp_tracking_track_id(
                                        dc_self_ce1_nic.replace(prefix, ''),
                                        dc_other_list['dc_number'],
                                        dc_self_lan_ip_ver)

                dc_other_ce2_hsrp_track_id = self.__get_hsrp_tracking_track_id(
                                        dc_self_ce2_nic.replace(prefix, ''),
                                        dc_other_list['dc_number'],
                                        dc_self_lan_ip_ver)

                # selfDC CE#1
                self.execute_msa_command(
                    msa_config_for_device,
                    msa_self,
                    msa_client_name,
                    dc_self_ce1_msa_device_id,
                    dc_self_ce1_nic + '-' + dc_other_list['dc_name'],
                    {
                        'interface': dc_self_ce1_nic,
                        'group_id': dc_other_hsrp_group_id,
                        'segment': dc_other_loopback_seg,
                        'netmask': dc_other_hsrp_netmask,
                        'prioritycost': dc_other_hsrp_track_prioritycost,
                        'track_id': dc_other_ce1_hsrp_track_id,
                    }
                )
                # selfDC CE#2
                self.execute_msa_command(
                    msa_config_for_device,
                    msa_self,
                    msa_client_name,
                    dc_self_ce2_msa_device_id,
                    dc_self_ce2_nic + '-' + dc_other_list['dc_name'],
                    {
                        'interface': dc_self_ce2_nic,
                        'group_id': dc_other_hsrp_group_id,
                        'segment': dc_other_loopback_seg,
                        'netmask': dc_other_hsrp_netmask,
                        'prioritycost': dc_other_hsrp_track_prioritycost,
                        'track_id': dc_other_ce2_hsrp_track_id,
                    }
                )

        # -----------------------------------------------------------------
        # Other DC Setting
        # -----------------------------------------------------------------
        dc_uniq_list = []
        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_self_id:
                continue

            dc_other_id = dc_member['dc_id']
            dc_other_list = self.__get_dc_info(dc_other_id)

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_loopback_seg = ce1_info['loopback_seg']
            dc_other_loopback_netmask = ce1_info['loopback_netmask']
            dc_other_hsrp_track_prioritycost \
                = ce1_info['csr1000v']['hsrp_track_prioritycost']

            dc_other_ce1_msa_device_id = ce1_info['MSA_device_id']
            dc_other_ce1_nic = ce1_info['nic']

            dc_other_ce2_msa_device_id = ce2_info['MSA_device_id']
            dc_other_ce2_nic = ce2_info['nic']

            # Create Instance(MSA Soap Client)(DC_OTHER)
            msa_other = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                self.job_config,
                                self.nal_endpoint_config, pod_id, dc_other_id)

            if mode == 'create':
                if dc_member['dc_id'] not in dc_uniq_list:

                    dc_uniq_list.append(dc_member['dc_id'])

                    # Create BGP Peer IPv4(MSA)
                    msa_client_name = 'create_csr1000v_bgp_peer_ipv4'
                    msa_option_params = {
                        'authkey': authkey,
                        'interface': bgp_wan_interface,
                    }

                    # otherDC CE#1 - selfDC CE#1
                    msa_option_params['ip_address'] \
                        = dc_self_ce1_wan_ip_address[self.utils.IP_VER_V4]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_self_ce1_host_name,
                        msa_option_params
                    )
                    # otherDC CE#1 - selfDC CE#2
                    msa_option_params['ip_address'] \
                        = dc_self_ce2_wan_ip_address[self.utils.IP_VER_V4]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )
                    # otherDC CE#2 - selfDC CE#1
                    msa_option_params['ip_address'] \
                        = dc_self_ce1_wan_ip_address[self.utils.IP_VER_V4]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce1_host_name,
                        msa_option_params
                    )
                    # otherDC CE#2 - selfDC CE#2
                    msa_option_params['ip_address'] \
                        = dc_self_ce2_wan_ip_address[self.utils.IP_VER_V4]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )

                if len(dc_member['IaaS_subnet_id_v6']) > 0:
                    ip_ver_list = ['4', '6']
                else:
                    ip_ver_list = [dc_self_lan_ip_ver]

                for ip_ver in ip_ver_list:
                    # Create HSRP Tracking
                    msa_client_name = 'create_csr1000v_hsrp_tracking'
                    dc_self_hsrp_netmask = \
                        self.utils.get_subnet_mask_from_cidr_ipv6(
                                        dc_self_loopback_seg + '/' \
                                        + str(dc_self_loopback_netmask))

                    dc_self_hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][ip_ver]

                    dc_self_ce1_hsrp_track_id = \
                        self.__get_hsrp_tracking_track_id(
                                        dc_other_ce1_nic.replace(prefix, ''),
                                        dc_self_list['dc_number'],
                                        ip_ver)

                    dc_self_ce2_hsrp_track_id = \
                        self.__get_hsrp_tracking_track_id(
                                        dc_other_ce2_nic.replace(prefix, ''),
                                        dc_self_list['dc_number'],
                                        ip_ver)

                    # oherDC CE#1
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_other_ce1_nic + '-' + dc_self_list['dc_name'],
                        {
                            'interface': dc_other_ce1_nic,
                            'group_id': dc_self_hsrp_group_id,
                            'segment': dc_self_loopback_seg,
                            'netmask': dc_self_hsrp_netmask,
                            'prioritycost': dc_self_hsrp_track_prioritycost,
                            'track_id': dc_self_ce1_hsrp_track_id,
                        }
                    )
                    # oherDC CE#2
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_other_ce2_nic + '-' + dc_self_list['dc_name'],
                        {
                            'interface': dc_other_ce2_nic,
                            'group_id': dc_self_hsrp_group_id,
                            'segment': dc_self_loopback_seg,
                            'netmask': dc_self_hsrp_netmask,
                            'prioritycost': dc_self_hsrp_track_prioritycost,
                            'track_id': dc_self_ce2_hsrp_track_id,
                        }
                    )

    def __dc_connect_csr1000v_vm_for_tunnel(self, job_input, mode=''):

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        group_id = job_input['group_id']
        pod_id = job_input['pod_id']
        group_rec_id = job_input['group_rec_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        dc_member_list = job_input['dc_member_list']
        wan_allocation_info_self = job_input['wan_allocation_info']

        # Get JOB Input Router Info
        ce_info = job_input['ce_info']

        dc_self_loopback_seg = ce_info[0]['loopback_seg']
        dc_self_loopback_netmask = ce_info[0]['loopback_netmask']
        dc_self_hsrp_track_prioritycost \
            = ce_info[0]['csr1000v']['hsrp_track_prioritycost']

        dc_self_ce1_msa_device_id = ce_info[0]['MSA_device_id']
        dc_self_ce1_host_name = ce_info[0]['host_name']
        dc_self_ce1_wan_ip_address = ce_info[0]['wan_ip_address']
        dc_self_ce1_nic = ce_info[0]['nic']

        dc_self_lan_ip_ver = self.utils.get_ipaddress_version(
                                            ce_info[0]['lan_ip_address'])

        dc_self_hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                    'hsrp_group_id'][dc_self_lan_ip_ver]

        dc_self_ce2_msa_device_id = ce_info[1]['MSA_device_id']
        dc_self_ce2_host_name = ce_info[1]['host_name']
        dc_self_ce2_wan_ip_address = ce_info[1]['wan_ip_address']
        dc_self_ce2_nic = ce_info[1]['nic']

        dc_self_id = dc_id
        dc_self_list = self.__get_dc_info(dc_self_id)

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_self_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_self_id)
        prefix = msa_config_for_device['nic_prefix']

        bgp_wan_interface = msa_config_for_device['nic_prefix'] \
                                + msa_config_for_device['nic_for_wan']

        prefix_tunnel = msa_config_for_device['nic_prefix_tunnel']

        ipsec_transform_set = msa_config_for_device['ipsec_transform_set']

        rtname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rtname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # -----------------------------------------------------------------
        # Self DC Setting
        # -----------------------------------------------------------------
        # Create Instance(MSA Soap Client)(DC_SELF)
        msa_self = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                                     self.job_config,
                                                     self.nal_endpoint_config,
                                                     pod_id,
                                                     dc_self_id)

        # Get DC Segment(SelfDC)
        dc_self_segment = self._get_dc_segment(dc_self_id, group_id)

        dc_uniq_list = []
        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_self_id:
                continue

            dc_other_id = dc_member['dc_id']
            dc_other_list = self.__get_dc_info(dc_other_id)

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_loopback_seg = ce1_info['loopback_seg']
            dc_other_loopback_netmask = ce1_info['loopback_netmask']
            dc_other_hsrp_track_prioritycost \
                        = ce1_info['csr1000v']['hsrp_track_prioritycost']

            dc_other_ce1_host_name = ce1_info['host_name']
            dc_other_ce1_wan_ip_address = ce1_info['wan_ip_address']

            dc_other_ce2_host_name = ce2_info['host_name']
            dc_other_ce2_wan_ip_address = ce2_info['wan_ip_address']

            # SelfDC-OtherDC Tenant Setting(IPv4)
            dc_self1_other1_tenant_v4 = \
                wan_allocation_info_self[rtname1]['tenant'][
                        dc_other_id][rtname1][self.utils.IP_VER_V4]

            dc_self1_other2_tenant_v4 = \
                wan_allocation_info_self[rtname1]['tenant'][
                        dc_other_id][rtname2][self.utils.IP_VER_V4]

            dc_self2_other1_tenant_v4 = \
                wan_allocation_info_self[rtname2]['tenant'][
                        dc_other_id][rtname1][self.utils.IP_VER_V4]

            dc_self2_other2_tenant_v4 = \
                wan_allocation_info_self[rtname2]['tenant'][
                        dc_other_id][rtname2][self.utils.IP_VER_V4]

            wan_allocation_info_other \
                = self.get_wan_allocation_info_for_tunnel(dc_other_id)

            # SelfDC-OtherDC Tenant Peer Setting(IPv4)
            dc_peer_self1_other1_tenant_v4 = \
                wan_allocation_info_other[rtname1]['tenant'][
                        dc_self_id][rtname1][self.utils.IP_VER_V4]

            dc_peer_self1_other2_tenant_v4 = \
                wan_allocation_info_other[rtname2]['tenant'][
                        dc_self_id][rtname1][self.utils.IP_VER_V4]

            dc_peer_self2_other1_tenant_v4 = \
                wan_allocation_info_other[rtname1]['tenant'][
                        dc_self_id][rtname2][self.utils.IP_VER_V4]

            dc_peer_self2_other2_tenant_v4 = \
                wan_allocation_info_other[rtname2]['tenant'][
                        dc_self_id][rtname2][self.utils.IP_VER_V4]

            if dc_other_id not in dc_uniq_list:
                if mode == 'create':

                    dc_uniq_list.append(dc_other_id)

                    # Get DC Segment(OtherDC)
                    dc_other_segment = self._get_dc_segment(dc_other_id,
                                                                  group_id)

                    # Create Static Route For DC(MSA)
                    msa_client_name = 'create_csr1000v_static_route_for_dc'

                    static_route_dst_name_other \
                        = msa_config_for_device[
                                        'static_route_for_dc'] + dc_other_id

                    msa_option_params = {
                        'ip_address': dc_other_segment['network_address'],
                        'netmask': self.utils.get_subnet_mask_from_cidr_ipv6(
                                    dc_other_segment['network_address'] \
                                    + '/' \
                                    + str(dc_other_segment['netmask'])),
                        'nexthop_address': dc_self_segment['next_hop'],
                        'netmask_cidr': dc_other_segment['netmask'],
                    }

                    # selfDC CE#1 - otherDC
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        static_route_dst_name_other,
                        msa_option_params
                    )

                    # selfDC CE#2 - otherDC
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        static_route_dst_name_other,
                        msa_option_params
                    )

                    # Create Tunnel Interface Gre IPv4(MSA)
                    msa_client_name \
                        = 'create_csr1000v_tunnel_interface_gre_ipv4'

                    dc_self_ce1_tunnel_interface_name \
                        = prefix_tunnel \
                                + str(dc_self_list['dc_number']) \
                                + '1' \
                                + str(dc_other_list['dc_number'])

                    dc_self_ce2_tunnel_interface_name \
                        = prefix_tunnel \
                                + str(dc_self_list['dc_number']) \
                                + '2' \
                                + str(dc_other_list['dc_number'])

                    # selfDC CE#1 - otherDC CE#1
                    tunnel_netmask = \
                        self.utils.get_subnet_mask_from_cidr_ipv6(
                                dc_self1_other1_tenant_v4['network'] \
                                + '/' + \
                                str(dc_self1_other1_tenant_v4['netmask']))
                    msa_option_params = {
                        'destination_ip_address': dc_other_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'interface': bgp_wan_interface,
                        'segment': dc_self1_other1_tenant_v4['network'],
                        'ip_address': dc_self1_other1_tenant_v4['ip'],
                        'netmask': tunnel_netmask,
                        'netmask_cidr': dc_self1_other1_tenant_v4['netmask'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_self_ce1_tunnel_interface_name + '1',
                        msa_option_params
                    )

                    # selfDC CE#1 - otherDC CE#2
                    tunnel_netmask = \
                        self.utils.get_subnet_mask_from_cidr_ipv6(
                                dc_self1_other2_tenant_v4['network'] \
                                + '/' + \
                                str(dc_self1_other2_tenant_v4['netmask']))
                    msa_option_params = {
                        'destination_ip_address': dc_other_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'interface': bgp_wan_interface,
                        'segment': dc_self1_other2_tenant_v4['network'],
                        'ip_address': dc_self1_other2_tenant_v4['ip'],
                        'netmask': tunnel_netmask,
                        'netmask_cidr': dc_self1_other2_tenant_v4['netmask'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_self_ce1_tunnel_interface_name + '2',
                        msa_option_params
                    )

                    # selfDC CE#2 - otherDC CE#1
                    tunnel_netmask = \
                        self.utils.get_subnet_mask_from_cidr_ipv6(
                                dc_self2_other1_tenant_v4['network'] \
                                + '/' + \
                                str(dc_self2_other1_tenant_v4['netmask']))
                    msa_option_params = {
                        'destination_ip_address': dc_other_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'interface': bgp_wan_interface,
                        'segment': dc_self2_other1_tenant_v4['network'],
                        'ip_address': dc_self2_other1_tenant_v4['ip'],
                        'netmask': tunnel_netmask,
                        'netmask_cidr': dc_self2_other1_tenant_v4['netmask'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_self_ce2_tunnel_interface_name + '1',
                        msa_option_params
                    )

                    # selfDC CE#2 - otherDC CE#2
                    tunnel_netmask = \
                        self.utils.get_subnet_mask_from_cidr_ipv6(
                                dc_self2_other2_tenant_v4['network'] \
                                + '/' + \
                                str(dc_self2_other2_tenant_v4['netmask']))
                    msa_option_params = {
                        'destination_ip_address': dc_other_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'interface': bgp_wan_interface,
                        'segment': dc_self2_other2_tenant_v4['network'],
                        'ip_address': dc_self2_other2_tenant_v4['ip'],
                        'netmask': tunnel_netmask,
                        'netmask_cidr': dc_self2_other2_tenant_v4['netmask'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_self_ce2_tunnel_interface_name + '2',
                        msa_option_params
                    )

                    # Create IPsec Peer(MSA)
                    msa_client_name = 'create_csr1000v_ipsec_peer_gre_ipv4'

                    dc_self_ce1_seqnumber = str(dc_self_list['dc_number']) \
                                        + '1' \
                                        + str(dc_other_list['dc_number'])

                    dc_self_ce2_seqnumber = str(dc_self_list['dc_number']) \
                                        + '2' \
                                        + str(dc_other_list['dc_number'])

                    # selfDC CE#1 - otherDC CE#1
                    msa_option_params = {
                        'ip_address': dc_self_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'peer_ip_address': dc_other_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'pre_shared_key': authkey,
                        'acl_number': dc_other_ce1_host_name,
                        'sequence_number': dc_self_ce1_seqnumber + '1',
                        'transform_set': ipsec_transform_set,
                        'interface': bgp_wan_interface,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_other_ce1_host_name,
                        msa_option_params
                    )

                    # selfDC CE#1 - otherDC CE#2
                    msa_option_params = {
                        'ip_address': dc_self_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'peer_ip_address': dc_other_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'pre_shared_key': authkey,
                        'acl_number': dc_other_ce2_host_name,
                        'sequence_number': dc_self_ce1_seqnumber + '2',
                        'transform_set': ipsec_transform_set,
                        'interface': bgp_wan_interface,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )

                    # selfDC CE#2 - otherDC CE#1
                    msa_option_params = {
                        'ip_address': dc_self_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'peer_ip_address': dc_other_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'pre_shared_key': authkey,
                        'acl_number': dc_other_ce1_host_name,
                        'sequence_number': dc_self_ce2_seqnumber + '1',
                        'transform_set': ipsec_transform_set,
                        'interface': bgp_wan_interface,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce1_host_name,
                        msa_option_params
                    )

                    # selfDC CE#2 - otherDC CE#2
                    msa_option_params = {
                        'ip_address': dc_self_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'peer_ip_address': dc_other_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'pre_shared_key': authkey,
                        'acl_number': dc_other_ce2_host_name,
                        'sequence_number': dc_self_ce2_seqnumber + '2',
                        'transform_set': ipsec_transform_set,
                        'interface': bgp_wan_interface,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )

                    # Create BGP Peer(MSA)
                    dc_self_ce1_prefix_tunnel = \
                                        prefix_tunnel \
                                        + str(dc_self_list['dc_number']) \
                                        + '1' \
                                        + str(dc_other_list['dc_number'])

                    dc_self_ce2_prefix_tunnel = \
                                        prefix_tunnel \
                                        + str(dc_self_list['dc_number']) \
                                        + '2' \
                                        + str(dc_other_list['dc_number'])

                    # Create BGP Peer IPv4(MSA)
                    msa_client_name = 'create_csr1000v_bgp_peer_ipv4'

                    # selfDC CE#1 - otherDC CE#1
                    msa_option_params = {
                        'ip_address': dc_peer_self1_other1_tenant_v4['ip'],
                        'authkey': authkey,
                        'interface': dc_self_ce1_prefix_tunnel + '1',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_other_ce1_host_name,
                        msa_option_params
                    )

                    # selfDC CE#1 - otherDC CE#2
                    msa_option_params = {
                        'ip_address': dc_peer_self1_other2_tenant_v4['ip'],
                        'authkey': authkey,
                        'interface': dc_self_ce1_prefix_tunnel + '2',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )

                    # selfDC CE#2 - otherDC CE#1
                    msa_option_params = {
                        'ip_address': dc_peer_self2_other1_tenant_v4['ip'],
                        'authkey': authkey,
                        'interface': dc_self_ce2_prefix_tunnel + '1',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce1_host_name,
                        msa_option_params
                    )

                    # selfDC CE#2 - otherDC CE#2
                    msa_option_params = {
                        'ip_address': dc_peer_self2_other2_tenant_v4['ip'],
                        'authkey': authkey,
                        'interface': dc_self_ce2_prefix_tunnel + '2',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )

                # Create HSRP Tracking(MSA)
                msa_client_name = 'create_csr1000v_hsrp_tracking'

                dc_other_hsrp_netmask = \
                    self.utils.get_subnet_mask_from_cidr_ipv6(
                                        dc_other_loopback_seg + '/' \
                                        + str(dc_other_loopback_netmask))

                dc_other_hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][dc_self_lan_ip_ver]

                dc_other_ce1_hsrp_track_id = self.__get_hsrp_tracking_track_id(
                                        dc_self_ce1_nic.replace(prefix, ''),
                                        dc_other_list['dc_number'],
                                        dc_self_lan_ip_ver)

                dc_other_ce2_hsrp_track_id = self.__get_hsrp_tracking_track_id(
                                        dc_self_ce2_nic.replace(prefix, ''),
                                        dc_other_list['dc_number'],
                                        dc_self_lan_ip_ver)

                # selfDC CE#1
                msa_option_params = {
                    'interface': dc_self_ce1_nic,
                    'group_id': dc_other_hsrp_group_id,
                    'segment': dc_other_loopback_seg,
                    'netmask': dc_other_hsrp_netmask,
                    'prioritycost': dc_other_hsrp_track_prioritycost,
                    'track_id': dc_other_ce1_hsrp_track_id,
                }
                self.execute_msa_command(
                    msa_config_for_device,
                    msa_self,
                    msa_client_name,
                    dc_self_ce1_msa_device_id,
                    dc_self_ce1_nic + '-' + dc_other_list['dc_name'],
                    msa_option_params
                )

                # selfDC CE#2
                msa_option_params = {
                    'interface': dc_self_ce2_nic,
                    'group_id': dc_other_hsrp_group_id,
                    'segment': dc_other_loopback_seg,
                    'netmask': dc_other_hsrp_netmask,
                    'prioritycost': dc_other_hsrp_track_prioritycost,
                    'track_id': dc_other_ce2_hsrp_track_id,
                }
                self.execute_msa_command(
                    msa_config_for_device,
                    msa_self,
                    msa_client_name,
                    dc_self_ce2_msa_device_id,
                    dc_self_ce2_nic + '-' + dc_other_list['dc_name'],
                    msa_option_params
                )

        # -----------------------------------------------------------------
        # Other DC Setting
        # -----------------------------------------------------------------
        static_route_dst_name_self = msa_config_for_device[
                                        'static_route_for_dc'] + dc_self_id

        dc_uniq_list = []
        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_self_id:
                continue

            dc_other_id = dc_member['dc_id']
            dc_other_list = self.__get_dc_info(dc_other_id)

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_loopback_seg = ce1_info['loopback_seg']
            dc_other_loopback_netmask = ce1_info['loopback_netmask']
            dc_other_hsrp_track_prioritycost \
                = ce1_info['csr1000v']['hsrp_track_prioritycost']

            dc_other_ce1_msa_device_id = ce1_info['MSA_device_id']
            dc_other_ce1_nic = ce1_info['nic']

            dc_other_ce1_wan_ip_address = ce1_info['wan_ip_address']

            dc_other_ce2_msa_device_id = ce2_info['MSA_device_id']
            dc_other_ce2_nic = ce2_info['nic']

            dc_other_ce2_wan_ip_address = ce2_info['wan_ip_address']

            wan_allocation_info_other \
                = self.get_wan_allocation_info_for_tunnel(dc_other_id)

            # OtherDC-SelfDC Tenant Setting(IPv4)
            dc_other1_self1_tenant_v4 \
                = wan_allocation_info_other[rtname1]['tenant'][
                        dc_self_id][rtname1][self.utils.IP_VER_V4]

            dc_other1_self2_tenant_v4 \
                = wan_allocation_info_other[rtname1]['tenant'][
                        dc_self_id][rtname2][self.utils.IP_VER_V4]

            dc_other2_self1_tenant_v4 \
                = wan_allocation_info_other[rtname2]['tenant'][
                        dc_self_id][rtname1][self.utils.IP_VER_V4]

            dc_other2_self2_tenant_v4 \
                = wan_allocation_info_other[rtname2]['tenant'][
                        dc_self_id][rtname2][self.utils.IP_VER_V4]

            # OtherDC-SelfDC Peer Tenant Setting(IPv4)
            dc_peer_other1_self1_tenant_v4 \
                = wan_allocation_info_self[rtname1]['tenant'][
                        dc_other_id][rtname1][self.utils.IP_VER_V4]

            dc_peer_other1_self2_tenant_v4 \
                = wan_allocation_info_self[rtname2]['tenant'][
                        dc_other_id][rtname1][self.utils.IP_VER_V4]

            dc_peer_other2_self1_tenant_v4 \
                = wan_allocation_info_self[rtname1]['tenant'][
                        dc_other_id][rtname2][self.utils.IP_VER_V4]

            dc_peer_other2_self2_tenant_v4 \
                = wan_allocation_info_self[rtname2]['tenant'][
                        dc_other_id][rtname2][self.utils.IP_VER_V4]

            # Create Instance(MSA Soap Client)(DC_OTHER)
            msa_other = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                self.job_config,
                                self.nal_endpoint_config, pod_id, dc_other_id)

            if mode == 'create':
                if dc_other_id not in dc_uniq_list:

                    dc_uniq_list.append(dc_other_id)

                    # Get DC Segment(OtherDC)
                    dc_other_segment = self._get_dc_segment(dc_other_id,
                                                                  group_id)

                    # Create Static Route For DC(MSA)
                    msa_client_name = 'create_csr1000v_static_route_for_dc'

                    msa_option_params = {
                        'ip_address': dc_self_segment['network_address'],
                        'netmask': self.utils.get_subnet_mask_from_cidr_ipv6(
                                    dc_self_segment['network_address'] \
                                    + '/' \
                                    + str(dc_self_segment['netmask'])),
                        'nexthop_address': dc_other_segment['next_hop'],
                        'netmask_cidr': dc_self_segment['netmask'],
                    }

                    # otherDC CE#1 - selfDC
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        static_route_dst_name_self,
                        msa_option_params
                    )
                    # otherDC CE#2 - selfDC
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        static_route_dst_name_self,
                        msa_option_params
                    )

                    # Create Tunnel Interface Gre IPv4(MSA)
                    msa_client_name \
                        = 'create_csr1000v_tunnel_interface_gre_ipv4'

                    dc_other_ce1_tunnel_interface_name \
                        = prefix_tunnel \
                                + str(dc_other_list['dc_number']) \
                                + '1' \
                                + str(dc_self_list['dc_number'])

                    dc_other_ce2_tunnel_interface_name \
                        = prefix_tunnel \
                                + str(dc_other_list['dc_number']) \
                                + '2' \
                                + str(dc_self_list['dc_number'])

                    # otherDC CE#1 - selfDC CE#1
                    tunnel_netmask = self.utils.get_subnet_mask_from_cidr_ipv6(
                                dc_other1_self1_tenant_v4['network'] \
                                + '/' \
                                + str(dc_other1_self1_tenant_v4['netmask']))
                    msa_option_params = {
                        'destination_ip_address': dc_self_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'interface': bgp_wan_interface,
                        'segment': dc_other1_self1_tenant_v4['network'],
                        'ip_address': dc_other1_self1_tenant_v4['ip'],
                        'netmask': tunnel_netmask,
                        'netmask_cidr': dc_other1_self1_tenant_v4['netmask'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_other_ce1_tunnel_interface_name + '1',
                        msa_option_params
                    )

                    # otherDC CE#1 - selfDC CE#2
                    tunnel_netmask = self.utils.get_subnet_mask_from_cidr_ipv6(
                                dc_other1_self2_tenant_v4['network'] \
                                + '/' \
                                + str(dc_other1_self2_tenant_v4['netmask']))
                    msa_option_params = {
                        'destination_ip_address': dc_self_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'interface': bgp_wan_interface,
                        'segment': dc_other1_self2_tenant_v4['network'],
                        'ip_address': dc_other1_self2_tenant_v4['ip'],
                        'netmask': tunnel_netmask,
                        'netmask_cidr': dc_other1_self2_tenant_v4['netmask'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_other_ce1_tunnel_interface_name + '2',
                        msa_option_params
                    )

                    # otherDC CE#2 - selfDC CE#1
                    tunnel_netmask = self.utils.get_subnet_mask_from_cidr_ipv6(
                                dc_other2_self1_tenant_v4['network'] \
                                + '/' \
                                + str(dc_other2_self1_tenant_v4['netmask']))
                    msa_option_params = {
                        'destination_ip_address': dc_self_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'interface': bgp_wan_interface,
                        'segment': dc_other2_self1_tenant_v4['network'],
                        'ip_address': dc_other2_self1_tenant_v4['ip'],
                        'netmask': tunnel_netmask,
                        'netmask_cidr': dc_other2_self1_tenant_v4['netmask'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_other_ce2_tunnel_interface_name + '1',
                        msa_option_params
                    )

                    # otherDC CE#2 - selfDC CE#2
                    tunnel_netmask = self.utils.get_subnet_mask_from_cidr_ipv6(
                                dc_other2_self2_tenant_v4['network'] \
                                + '/' \
                                + str(dc_other2_self2_tenant_v4['netmask']))
                    msa_option_params = {
                        'destination_ip_address': dc_self_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                        'interface': bgp_wan_interface,
                        'segment': dc_other2_self2_tenant_v4['network'],
                        'ip_address': dc_other2_self2_tenant_v4['ip'],
                        'netmask': tunnel_netmask,
                        'netmask_cidr': dc_other2_self2_tenant_v4['netmask'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_other_ce2_tunnel_interface_name + '2',
                        msa_option_params
                    )

                    # Create IPsec Peer(MSA)
                    msa_client_name = 'create_csr1000v_ipsec_peer_gre_ipv4'

                    dc_other_ce1_seqnumber = str(dc_other_list['dc_number']) \
                                        + '1' \
                                        + str(dc_self_list['dc_number'])

                    dc_other_ce2_seqnumber = str(dc_other_list['dc_number']) \
                                        + '2' \
                                        + str(dc_self_list['dc_number'])

                    # otherDC CE#1 - selfDC CE#1
                    msa_option_params = {
                        'ip_address': dc_other_ce1_wan_ip_address[
                                                    self.utils.IP_VER_V4],
                        'peer_ip_address': dc_self_ce1_wan_ip_address[
                                                    self.utils.IP_VER_V4],
                        'pre_shared_key': authkey,
                        'acl_number': dc_self_ce1_host_name,
                        'sequence_number': dc_other_ce1_seqnumber + '1',
                        'transform_set': ipsec_transform_set,
                        'interface': bgp_wan_interface,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_self_ce1_host_name,
                        msa_option_params
                    )

                    # otherDC CE#1 - selfDC CE#2
                    msa_option_params = {
                        'ip_address': dc_other_ce1_wan_ip_address[
                                                    self.utils.IP_VER_V4],
                        'peer_ip_address': dc_self_ce2_wan_ip_address[
                                                    self.utils.IP_VER_V4],
                        'pre_shared_key': authkey,
                        'acl_number': dc_self_ce2_host_name,
                        'sequence_number': dc_other_ce1_seqnumber + '2',
                        'transform_set': ipsec_transform_set,
                        'interface': bgp_wan_interface,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )

                    # otherDC CE#2 - selfDC CE#1
                    msa_option_params = {
                        'ip_address': dc_other_ce2_wan_ip_address[
                                                    self.utils.IP_VER_V4],
                        'peer_ip_address': dc_self_ce1_wan_ip_address[
                                                    self.utils.IP_VER_V4],
                        'pre_shared_key': authkey,
                        'acl_number': dc_self_ce1_host_name,
                        'sequence_number': dc_other_ce2_seqnumber + '1',
                        'transform_set': ipsec_transform_set,
                        'interface': bgp_wan_interface,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce1_host_name,
                        msa_option_params
                    )

                    # otherDC CE#2 - selfDC CE#2
                    msa_option_params = {
                        'ip_address': dc_other_ce2_wan_ip_address[
                                                    self.utils.IP_VER_V4],
                        'peer_ip_address': dc_self_ce2_wan_ip_address[
                                                    self.utils.IP_VER_V4],
                        'pre_shared_key': authkey,
                        'acl_number': dc_self_ce2_host_name,
                        'sequence_number': dc_other_ce2_seqnumber + '2',
                        'transform_set': ipsec_transform_set,
                        'interface': bgp_wan_interface,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )

                    # Create BGP Peer(MSA)
                    dc_other_ce1_prefix_tunnel = \
                                        prefix_tunnel \
                                        + str(dc_other_list['dc_number']) \
                                        + '1' \
                                        + str(dc_self_list['dc_number'])

                    dc_other_ce2_prefix_tunnel = \
                                        prefix_tunnel \
                                        + str(dc_other_list['dc_number']) \
                                        + '2' \
                                        + str(dc_self_list['dc_number'])

                    # Create BGP Peer IPv4(MSA)
                    msa_client_name = 'create_csr1000v_bgp_peer_ipv4'

                    # otherDC CE#1 - selfDC CE#1
                    msa_option_params = {
                        'ip_address': dc_peer_other1_self1_tenant_v4['ip'],
                        'authkey': authkey,
                        'interface': dc_other_ce1_prefix_tunnel + '1',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_self_ce1_host_name,
                        msa_option_params
                    )

                    # otherDC CE#1 - selfDC CE#2
                    msa_option_params = {
                        'ip_address': dc_peer_other1_self2_tenant_v4['ip'],
                        'authkey': authkey,
                        'interface': dc_other_ce1_prefix_tunnel + '2',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )

                    # otherDC CE#2 - selfDC CE#1
                    msa_option_params = {
                        'ip_address': dc_peer_other2_self1_tenant_v4['ip'],
                        'authkey': authkey,
                        'interface': dc_other_ce2_prefix_tunnel + '1',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce1_host_name,
                        msa_option_params
                    )
                    # otherDC CE#2 - selfDC CE#2
                    msa_option_params = {
                        'ip_address': dc_peer_other2_self2_tenant_v4['ip'],
                        'authkey': authkey,
                        'interface': dc_other_ce2_prefix_tunnel + '2',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )

                if len(dc_member['IaaS_subnet_id_v6']) > 0:
                    ip_ver_list = ['4', '6']
                else:
                    ip_ver_list = [dc_self_lan_ip_ver]

                for ip_ver in ip_ver_list:
                    # Create HSRP Tracking
                    msa_client_name = 'create_csr1000v_hsrp_tracking'

                    loop_hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                    'hsrp_group_id'][ip_ver]

                    dc_self_hsrp_netmask = \
                        self.utils.get_subnet_mask_from_cidr_ipv6(
                                        dc_self_loopback_seg + '/' \
                                        + str(dc_self_loopback_netmask))

                    dc_self_ce1_hsrp_track_id = \
                        self.__get_hsrp_tracking_track_id(
                                        dc_other_ce1_nic.replace(prefix, ''),
                                        dc_self_list['dc_number'],
                                        ip_ver)

                    dc_self_ce2_hsrp_track_id = \
                        self.__get_hsrp_tracking_track_id(
                                        dc_other_ce2_nic.replace(prefix, ''),
                                        dc_self_list['dc_number'],
                                        ip_ver)

                    # oherDC CE#1
                    msa_option_params = {
                        'interface': dc_other_ce1_nic,
                        'group_id': loop_hsrp_group_id,
                        'segment': dc_self_loopback_seg,
                        'netmask': dc_self_hsrp_netmask,
                        'prioritycost': dc_self_hsrp_track_prioritycost,
                        'track_id': dc_self_ce1_hsrp_track_id,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_other_ce1_nic + '-' + dc_self_list['dc_name'],
                        msa_option_params
                    )

                    # oherDC CE#2
                    msa_option_params = {
                        'interface': dc_other_ce2_nic,
                        'group_id': loop_hsrp_group_id,
                        'segment': dc_self_loopback_seg,
                        'netmask': dc_self_hsrp_netmask,
                        'prioritycost': dc_self_hsrp_track_prioritycost,
                        'track_id': dc_self_ce2_hsrp_track_id,
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_other_ce2_nic + '-' + dc_self_list['dc_name'],
                        msa_option_params
                    )

    def __dc_disconnect_firefly_vm(self, job_input):

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        tenant_lan_list = job_input['tenant_lan_list']
        dc_member_myself_list = job_input['dc_member_myself_list']
        dc_member_other_list = job_input['dc_member_other_list']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        myself_nic = tenant_lan_list[0]['nic']
        myself_tracking_name = myself_nic + '-' + dc_id

        for dc_myself in dc_member_myself_list:

            myself_loopbak_seg = dc_myself['ce1_info']['loopback_seg']
            myself_loopbak_netmask = dc_myself['ce1_info']['loopback_netmask']

            for dc_other in dc_member_other_list:

                # Create Instance(MSA Soap Client)
                msa = fireflyvmordercmdws.FireflyVmOrderCommandWs(
                                    self.job_config, self.nal_endpoint_config,
                                    dc_other['pod_id'], dc_other['dc_id'])

                try:
                    # Delete VRRP Tracking(DC_OTHER-CE#1)
                    msa.delete_firefly_vm_vrrp_tracking(
                                    dc_other['ce1_info']['MSA_device_id'],
                                    myself_tracking_name,
                                    myself_nic,
                                    dc_other['ce1_info']['lan_ip_address'],
                                    dc_other['ce1_info']['lan_netmask'],
                                    1,
                                    myself_loopbak_seg,
                                    myself_loopbak_netmask)
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#1)
                    msa.delete_firefly_vm_bgp_peer(
                                dc_other['ce1_info']['MSA_device_id'],
                                dc_myself['ce1_info']['host_name'],
                                dc_myself['ce1_info']['wan_ip_address'])
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#1)
                    msa.delete_firefly_vm_bgp_peer(
                                dc_other['ce1_info']['MSA_device_id'],
                                dc_myself['ce2_info']['host_name'],
                                dc_myself['ce2_info']['wan_ip_address'])
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete VRRP Tracking(DC_OTHER-CE#2)
                    msa.delete_firefly_vm_vrrp_tracking(
                                        dc_other['ce2_info']['MSA_device_id'],
                                        myself_tracking_name,
                                        myself_nic,
                                        dc_other['ce2_info']['lan_ip_address'],
                                        dc_other['ce2_info']['lan_netmask'],
                                        1,
                                        myself_loopbak_seg,
                                        myself_loopbak_netmask)
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#2)
                    msa.delete_firefly_vm_bgp_peer(
                            dc_other['ce2_info']['MSA_device_id'],
                            dc_myself['ce1_info']['host_name'],
                            dc_myself['ce1_info']['wan_ip_address'])
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#2)
                    msa.delete_firefly_vm_bgp_peer(
                            dc_other['ce2_info']['MSA_device_id'],
                            dc_myself['ce2_info']['host_name'],
                            dc_myself['ce2_info']['wan_ip_address'])
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

    def __dc_disconnect_csr1000v_vm(self, job_input):

        # Get JOB Input Parameters
        dc_member_myself_list = job_input['dc_member_myself_list']
        dc_member_other_list = job_input['dc_member_other_list']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        for dc_myself in dc_member_myself_list:

            dc_self_id = dc_myself['dc_id']
            dc_self_list = self.__get_dc_info(dc_self_id)

            device_name = self.device_type_to_name(apl_type,
                                           nf_type,
                                           device_type,
                                           dc_self_id)
            msa_config_for_device = \
                self.get_msa_config_for_device(pod_id, device_name, dc_self_id)
            prefix = msa_config_for_device['nic_prefix']
            nic_for_first_lan = msa_config_for_device['nic_for_first_lan']

            dc_myself_ce1_nic = str(dc_myself['ce1_info']['nic'])
            if dc_myself_ce1_nic == prefix + nic_for_first_lan:
                break

        # Set IPv6 delete flg
        group_id = job_input['group_id']
        ipv6_self_flg = "0"
        self_dc_member_list = self.__get_dc_member_list(group_id, dc_self_id)
        for self_dc_member in self_dc_member_list:
            if self_dc_member['vrrp_address_v6'] != '':
                ipv6_self_flg = "1"

        for dc_other in dc_member_other_list:

            dc_other_id = dc_other['dc_id']

            device_name = self.device_type_to_name(apl_type,
                                           nf_type,
                                           device_type,
                                           dc_other_id)
            msa_config_for_device = \
                self.get_msa_config_for_device(pod_id, device_name,
                                               dc_other_id)
            prefix = msa_config_for_device['nic_prefix']
            nic_for_first_lan = msa_config_for_device['nic_for_first_lan']

            # Create Instance(MSA Soap Client)
            msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                self.job_config, self.nal_endpoint_config,
                                dc_other['pod_id'], dc_other_id)

            dc_other_ce1_nic = str(dc_other['ce1_info']['nic'])
            dc_other_ce2_nic = str(dc_other['ce2_info']['nic'])

            dc_other_ip_ver_list = [self.utils.IP_VER_V4]
            if len(dc_other['ce1_address_v6']) > 0:
                dc_other_ip_ver_list.append(self.utils.IP_VER_V6)

            for dc_self_ip_ver in dc_other_ip_ver_list:

                dc_self_hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                'hsrp_group_id'][dc_self_ip_ver]

                dc_self_ce1_hsrp_track_id = \
                                self.__get_hsrp_tracking_track_id(
                                    dc_other_ce1_nic.replace(prefix, ''),
                                    dc_self_list['dc_number'],
                                    dc_self_ip_ver)

                dc_self_ce2_hsrp_track_id = \
                                self.__get_hsrp_tracking_track_id(
                                    dc_other_ce2_nic.replace(prefix, ''),
                                    dc_self_list['dc_number'],
                                    dc_self_ip_ver)

                try:
                    # Delete HSRP Tracking(DC_OTHER-CE#1)
                    msa.delete_csr1000v_hsrp_tracking(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_other_ce1_nic + '-' + str(
                                                dc_self_list['dc_name']),
                        {
                            'interface': dc_other_ce1_nic,
                            'group_id': dc_self_hsrp_group_id,
                            'track_id': dc_self_ce1_hsrp_track_id,
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                        __name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete HSRP Tracking(DC_OTHER-CE#2)
                    msa.delete_csr1000v_hsrp_tracking(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_other_ce2_nic + '-' + str(
                                                dc_self_list['dc_name']),
                        {
                            'interface': dc_other_ce2_nic,
                            'group_id': dc_self_hsrp_group_id,
                            'track_id': dc_self_ce2_hsrp_track_id,
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                        __name__, traceback.format_exc())
                    else:
                        raise

            if dc_other_ce1_nic == prefix + nic_for_first_lan:

                # Delete BGP Peer IPv4
                dc_myself_ce1_info_wan_ip_address_v4 = dc_myself[
                            'ce1_info']['wan_ip_address'][self.utils.IP_VER_V4]
                dc_myself_ce2_info_wan_ip_address_v4 = dc_myself[
                            'ce2_info']['wan_ip_address'][self.utils.IP_VER_V4]

                try:
                    # Delete BGP Peer(DC_OTHER-CE#1)
                    msa.delete_csr1000v_bgp_peer_ipv4(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_myself['ce1_info']['host_name'],
                        {
                            'ip_address': dc_myself_ce1_info_wan_ip_address_v4
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                            __name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#1)
                    msa.delete_csr1000v_bgp_peer_ipv4(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_myself['ce2_info']['host_name'],
                        {
                            'ip_address': dc_myself_ce2_info_wan_ip_address_v4
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                            __name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#2)
                    msa.delete_csr1000v_bgp_peer_ipv4(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_myself['ce1_info']['host_name'],
                        {
                            'ip_address': dc_myself_ce1_info_wan_ip_address_v4
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                            __name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#2)
                    msa.delete_csr1000v_bgp_peer_ipv4(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_myself['ce2_info']['host_name'],
                        {
                            'ip_address': dc_myself_ce2_info_wan_ip_address_v4
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                            __name__, traceback.format_exc())
                    else:
                        raise

                # Delete BGP Peer IPv6
                dc_myself_ce1_info_wan_ip_address_v6 = dc_myself[
                            'ce1_info']['wan_ip_address'][self.utils.IP_VER_V6]
                dc_myself_ce2_info_wan_ip_address_v6 = dc_myself[
                            'ce2_info']['wan_ip_address'][self.utils.IP_VER_V6]

                # Set IPv6 delete flg
                ipv6_other_flg = "0"
                other_dc_member_list = self.__get_dc_member_list(group_id,
                                                                 dc_other_id)
                for other_dc_member in other_dc_member_list:
                    if other_dc_member['vrrp_address_v6'] != '':
                        ipv6_other_flg = "1"

                if ipv6_self_flg == "1" and ipv6_other_flg == "1":
                    try:
                        # Delete BGP Peer(DC_OTHER-CE#1)
                        msa.delete_csr1000v_bgp_peer_ipv6(
                            dc_other['ce1_info']['MSA_device_id'],
                            dc_myself['ce1_info']['host_name'],
                            {
                                'ipv6_address': \
                                    dc_myself_ce1_info_wan_ip_address_v6
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(
                                            __name__, traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete BGP Peer(DC_OTHER-CE#1)
                        msa.delete_csr1000v_bgp_peer_ipv6(
                            dc_other['ce1_info']['MSA_device_id'],
                            dc_myself['ce2_info']['host_name'],
                            {
                                'ipv6_address': \
                                    dc_myself_ce2_info_wan_ip_address_v6
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(
                                            __name__, traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete BGP Peer(DC_OTHER-CE#2)
                        msa.delete_csr1000v_bgp_peer_ipv6(
                            dc_other['ce2_info']['MSA_device_id'],
                            dc_myself['ce1_info']['host_name'],
                            {
                                'ipv6_address': \
                                    dc_myself_ce1_info_wan_ip_address_v6
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(
                                            __name__, traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete BGP Peer(DC_OTHER-CE#2)
                        msa.delete_csr1000v_bgp_peer_ipv6(
                            dc_other['ce2_info']['MSA_device_id'],
                            dc_myself['ce2_info']['host_name'],
                            {
                                'ipv6_address': \
                                    dc_myself_ce2_info_wan_ip_address_v6
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(
                                            __name__, traceback.format_exc())
                        else:
                            raise

    def __dc_disconnect_csr1000v_vm_for_tunnel(self, job_input):

        # Get JOB Input Parameters
        group_id = job_input['group_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        group_rec_id = job_input['group_rec_id']
        dc_member_myself_list = job_input['dc_member_myself_list']
        dc_member_other_list = job_input['dc_member_other_list']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        rtname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rtname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        for dc_myself in dc_member_myself_list:

            dc_self_id = dc_myself['dc_id']
            dc_self_list = self.__get_dc_info(dc_self_id)

            device_name = self.device_type_to_name(apl_type,
                                           nf_type,
                                           device_type,
                                           dc_self_id)
            msa_config_for_device = \
                self.get_msa_config_for_device(pod_id, device_name, dc_self_id)
            prefix = msa_config_for_device['nic_prefix']
            nic_for_first_lan = msa_config_for_device['nic_for_first_lan']

            dc_self_ce1_wan_ip_address = \
                                dc_myself['ce1_info']['wan_ip_address']
            dc_self_ce2_wan_ip_address = \
                                dc_myself['ce2_info']['wan_ip_address']

            # Get MSA Config
            device_name = self.device_type_to_name(apl_type,
                                                   nf_type,
                                                   device_type,
                                                   dc_self_id)

            msa_config_for_device = \
                self.get_msa_config_for_device(
                                        pod_id, device_name, dc_self_id)

            bgp_wan_interface = msa_config_for_device['nic_prefix'] \
                                + msa_config_for_device['nic_for_wan']

            # Get DC Segment(SelfDC)
            dc_self_segment = self._get_dc_segment(dc_self_id, group_id)

            dc_myself_ce1_nic = str(dc_myself['ce1_info']['nic'])
            if dc_myself_ce1_nic == prefix + nic_for_first_lan:
                break

        # Set IPv6 delete flg
        group_id = job_input['group_id']
        ipv6_self_flg = "0"
        self_dc_member_list = self.__get_dc_member_list(group_id, dc_self_id)
        for self_dc_member in self_dc_member_list:
            if self_dc_member['vrrp_address_v6'] != '':
                ipv6_self_flg = "1"

        for dc_other in dc_member_other_list:

            dc_other_id = dc_other['dc_id']
            dc_other_list = self.__get_dc_info(dc_other_id)

            device_name = self.device_type_to_name(apl_type,
                                           nf_type,
                                           device_type,
                                           dc_other_id)
            msa_config_for_device = \
                self.get_msa_config_for_device(pod_id, device_name,
                                               dc_other_id)
            prefix = msa_config_for_device['nic_prefix']
            nic_for_first_lan = msa_config_for_device['nic_for_first_lan']

            # Create Instance(MSA Soap Client)
            msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                self.job_config, self.nal_endpoint_config,
                                dc_other['pod_id'], dc_other['dc_id'])

            dc_other_ce1_nic = str(dc_other['ce1_info']['nic'])
            dc_other_ce2_nic = str(dc_other['ce2_info']['nic'])

            dc_other_ce1_hsrp_track_name = \
                dc_other_ce1_nic + '-' + str(dc_self_list['dc_name'])

            dc_other_ce2_hsrp_track_name = \
                dc_other_ce2_nic + '-' + str(dc_self_list['dc_name'])

            dc_other_ip_ver_list = [self.utils.IP_VER_V4]
            if len(dc_myself['ce1_address_v6']) > 0:
                dc_other_ip_ver_list.append(self.utils.IP_VER_V6)

            for dc_self_ip_ver in dc_other_ip_ver_list:

                dc_self_hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                    'hsrp_group_id'][dc_self_ip_ver]

                dc_self_ce1_hsrp_track_id \
                                = self.__get_hsrp_tracking_track_id(
                                    dc_other_ce1_nic.replace(prefix, ''),
                                    dc_self_list['dc_number'],
                                    dc_self_ip_ver)

                dc_self_ce2_hsrp_track_id \
                                = self.__get_hsrp_tracking_track_id(
                                    dc_other_ce2_nic.replace(prefix, ''),
                                    dc_self_list['dc_number'],
                                    dc_self_ip_ver)

                # Delete HSRP Tracking
                try:
                    # Delete HSRP Tracking(DC_OTHER-CE#1)
                    msa.delete_csr1000v_hsrp_tracking(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_other_ce1_hsrp_track_name,
                        {
                            'interface': dc_other_ce1_nic,
                            'group_id': dc_self_hsrp_group_id,
                            'track_id': dc_self_ce1_hsrp_track_id,
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                        __name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete HSRP Tracking(DC_OTHER-CE#2)
                    msa.delete_csr1000v_hsrp_tracking(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_other_ce2_hsrp_track_name,
                        {
                            'interface': dc_other_ce2_nic,
                            'group_id': dc_self_hsrp_group_id,
                            'track_id': dc_self_ce2_hsrp_track_id,
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                        __name__, traceback.format_exc())
                    else:
                        raise

            if dc_other_ce1_nic == prefix + nic_for_first_lan:

                # Set IPv6 delete flg
                ipv6_other_flg = "0"
                other_dc_member_list = self.__get_dc_member_list(group_id,
                                                                 dc_other_id)
                for other_dc_member in other_dc_member_list:
                    if other_dc_member['vrrp_address_v6'] != '':
                        ipv6_other_flg = "1"

                wan_allocation_info_other \
                    = self.get_wan_allocation_info_for_tunnel(dc_other_id)

                # OtherDC-SelfDC Tenant Setting(IPv4)
                dc_other1_self1_tenant_v4 \
                    = wan_allocation_info_other[rtname1]['tenant'][
                            dc_self_id][rtname1][self.utils.IP_VER_V4]

                dc_other1_self2_tenant_v4 \
                    = wan_allocation_info_other[rtname1]['tenant'][
                            dc_self_id][rtname2][self.utils.IP_VER_V4]

                dc_other2_self1_tenant_v4 \
                    = wan_allocation_info_other[rtname2]['tenant'][
                            dc_self_id][rtname1][self.utils.IP_VER_V4]

                dc_other2_self2_tenant_v4 \
                    = wan_allocation_info_other[rtname2]['tenant'][
                            dc_self_id][rtname2][self.utils.IP_VER_V4]

                # OtherDC-SelfDC Tenant Setting(IPv6)
                dc_other1_self1_tenant_v6 \
                    = wan_allocation_info_other[rtname1]['tenant'][
                            dc_self_id][rtname1][self.utils.IP_VER_V6]

                dc_other1_self2_tenant_v6 \
                    = wan_allocation_info_other[rtname1]['tenant'][
                            dc_self_id][rtname2][self.utils.IP_VER_V6]

                dc_other2_self1_tenant_v6 \
                    = wan_allocation_info_other[rtname2]['tenant'][
                            dc_self_id][rtname1][self.utils.IP_VER_V6]

                dc_other2_self2_tenant_v6 \
                    = wan_allocation_info_other[rtname2]['tenant'][
                            dc_self_id][rtname2][self.utils.IP_VER_V6]

                wan_allocation_info_self \
                    = self.get_wan_allocation_info_for_tunnel(dc_self_id)

                # OtherDC-SelfDC Peer Tenant Setting(IPv4)
                dc_peer_other1_self1_tenant_v4 \
                    = wan_allocation_info_self[rtname1]['tenant'][
                            dc_other_id][rtname1][self.utils.IP_VER_V4]

                dc_peer_other1_self2_tenant_v4 \
                    = wan_allocation_info_self[rtname2]['tenant'][
                            dc_other_id][rtname1][self.utils.IP_VER_V4]

                dc_peer_other2_self1_tenant_v4 \
                    = wan_allocation_info_self[rtname1]['tenant'][
                            dc_other_id][rtname2][self.utils.IP_VER_V4]

                dc_peer_other2_self2_tenant_v4 \
                    = wan_allocation_info_self[rtname2]['tenant'][
                            dc_other_id][rtname2][self.utils.IP_VER_V4]

                # OtherDC-SelfDC Peer Tenant Setting(IPv6)
                dc_peer_other1_self1_tenant_v6 \
                    = wan_allocation_info_self[rtname1]['tenant'][
                            dc_other_id][rtname1][self.utils.IP_VER_V6]

                dc_peer_other1_self2_tenant_v6 \
                    = wan_allocation_info_self[rtname2]['tenant'][
                            dc_other_id][rtname1][self.utils.IP_VER_V6]

                dc_peer_other2_self1_tenant_v6 \
                    = wan_allocation_info_self[rtname1]['tenant'][
                            dc_other_id][rtname2][self.utils.IP_VER_V6]

                dc_peer_other2_self2_tenant_v6 \
                    = wan_allocation_info_self[rtname2]['tenant'][
                            dc_other_id][rtname2][self.utils.IP_VER_V6]

                # Delete BGP Peer IPv4
                try:
                    # Delete BGP Peer(DC_OTHER-CE#1 DC_SELF-CE#1)
                    msa.delete_csr1000v_bgp_peer_ipv4(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_myself['ce1_info']['host_name'],
                        {
                            'ip_address': dc_peer_other1_self1_tenant_v4['ip'],
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                        __name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#1 DC_SELF-CE#2)
                    msa.delete_csr1000v_bgp_peer_ipv4(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_myself['ce2_info']['host_name'],
                        {
                            'ip_address': dc_peer_other1_self2_tenant_v4['ip'],
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(
                                        __name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#2 DC_SELF-CE#1)
                    msa.delete_csr1000v_bgp_peer_ipv4(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_myself['ce1_info']['host_name'],
                        {
                            'ip_address': dc_peer_other2_self1_tenant_v4['ip'],
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete BGP Peer(DC_OTHER-CE#2 DC_SELF-CE#2)
                    msa.delete_csr1000v_bgp_peer_ipv4(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_myself['ce2_info']['host_name'],
                        {
                            'ip_address': dc_peer_other2_self2_tenant_v4['ip'],
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                # Delete BGP Peer IPv6
                if ipv6_self_flg == "1" and ipv6_other_flg == "1":
                    try:
                        # Delete BGP Peer(DC_OTHER-CE#1 DC_SELF-CE#1)
                        msa.delete_csr1000v_bgp_peer_ipv6(
                            dc_other['ce1_info']['MSA_device_id'],
                            dc_myself['ce1_info']['host_name'],
                            {
                                'ipv6_address': dc_peer_other1_self1_tenant_v6[
                                                                        'ip'],
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete BGP Peer(DC_OTHER-CE#1 DC_SELF-CE#2)
                        msa.delete_csr1000v_bgp_peer_ipv6(
                            dc_other['ce1_info']['MSA_device_id'],
                            dc_myself['ce2_info']['host_name'],
                            {
                                'ipv6_address': dc_peer_other1_self2_tenant_v6[
                                                                        'ip'],
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete BGP Peer(DC_OTHER-CE#2 DC_SELF-CE#1)
                        msa.delete_csr1000v_bgp_peer_ipv6(
                            dc_other['ce2_info']['MSA_device_id'],
                            dc_myself['ce1_info']['host_name'],
                            {
                                'ipv6_address': dc_peer_other2_self1_tenant_v6[
                                                                        'ip'],
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete BGP Peer(DC_OTHER-CE#2 DC_SELF-CE#2)
                        msa.delete_csr1000v_bgp_peer_ipv6(
                            dc_other['ce2_info']['MSA_device_id'],
                            dc_myself['ce2_info']['host_name'],
                            {
                                'ipv6_address': dc_peer_other2_self2_tenant_v6[
                                                                        'ip'],
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                # Delete Ipsec Peer
                dc_other1_seqnumber = str(dc_other_list['dc_number']) \
                                        + '1' \
                                        + str(dc_self_list['dc_number'])

                dc_other2_seqnumber = str(dc_other_list['dc_number']) \
                                        + '2' \
                                        + str(dc_self_list['dc_number'])

                dc_other_ce1_wan_ip_address = dc_other['ce1_info'][
                                                        'wan_ip_address']

                dc_other_ce2_wan_ip_address = dc_other['ce2_info'][
                                                        'wan_ip_address']

                try:
                    # Delete Ipsec Peer(DC_OTHER-CE#1 DC_SELF-CE#1)
                    msa.delete_csr1000v_ipsec_peer_gre_ipv4(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_myself['ce1_info']['host_name'],
                        {
                            'ip_address': dc_other_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                            'peer_ip_address': dc_self_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                            'pre_shared_key': authkey,
                            'acl_number': dc_myself['ce1_info']['host_name'],
                            'sequence_number': dc_other1_seqnumber + '1',
                            'interface': bgp_wan_interface,
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete Ipsec Peer(DC_OTHER-CE#1 DC_SELF-CE#2)
                    msa.delete_csr1000v_ipsec_peer_gre_ipv4(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_myself['ce2_info']['host_name'],
                        {
                            'ip_address': dc_other_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                            'peer_ip_address': dc_self_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                            'pre_shared_key': authkey,
                            'acl_number': dc_myself['ce2_info']['host_name'],
                            'sequence_number': dc_other1_seqnumber + '2',
                            'interface': bgp_wan_interface,
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete Ipsec Peer(DC_OTHER-CE#2 DC_SELF-CE#1)
                    msa.delete_csr1000v_ipsec_peer_gre_ipv4(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_myself['ce1_info']['host_name'],
                        {
                            'ip_address': dc_other_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                            'peer_ip_address': dc_self_ce1_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                            'pre_shared_key': authkey,
                            'acl_number': dc_myself['ce1_info']['host_name'],
                            'sequence_number': dc_other2_seqnumber + '1',
                            'interface': bgp_wan_interface,
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete Ipsec Peer(DC_OTHER-CE#2 DC_SELF-CE#2)
                    msa.delete_csr1000v_ipsec_peer_gre_ipv4(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_myself['ce2_info']['host_name'],
                        {
                            'ip_address': dc_other_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                            'peer_ip_address': dc_self_ce2_wan_ip_address[
                                                        self.utils.IP_VER_V4],
                            'pre_shared_key': authkey,
                            'acl_number': dc_myself['ce2_info']['host_name'],
                            'sequence_number': dc_other2_seqnumber + '2',
                            'interface': bgp_wan_interface,
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                # Delete Tunnel Interface
                dc_other_ce1_tunnel_interface_name = \
                    msa_config_for_device['nic_prefix_tunnel'] \
                                + str(dc_other_list['dc_number']) \
                                + '1' \
                                + str(dc_self_list['dc_number'])

                dc_other_ce2_tunnel_interface_name = \
                    msa_config_for_device['nic_prefix_tunnel'] \
                                + str(dc_other_list['dc_number']) \
                                + '2' \
                                + str(dc_self_list['dc_number'])

                try:
                    # Delete Tunnel Interface(DC_OTHER-CE#1 DC_SELF-CE#1)
                    msa.delete_csr1000v_tunnel_interface_gre_ipv4(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_other_ce1_tunnel_interface_name + '1',
                        {
                            'segment': dc_other1_self1_tenant_v4['network'],
                            'ip_address': dc_other1_self1_tenant_v4['ip'],
                            'netmask_cidr': dc_other1_self1_tenant_v4[
                                                                'netmask'],
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete Tunnel Interface(DC_OTHER-CE#1 DC_SELF-CE#2)
                    msa.delete_csr1000v_tunnel_interface_gre_ipv4(
                        dc_other['ce1_info']['MSA_device_id'],
                        dc_other_ce1_tunnel_interface_name + '2',
                        {
                            'segment': dc_other1_self2_tenant_v4['network'],
                            'ip_address': dc_other1_self2_tenant_v4['ip'],
                            'netmask_cidr': dc_other1_self2_tenant_v4[
                                                                'netmask'],
                         }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete Tunnel Interface(DC_OTHER-CE#2 DC_SELF-CE#1)
                    msa.delete_csr1000v_tunnel_interface_gre_ipv4(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_other_ce2_tunnel_interface_name + '1',
                        {
                            'segment': dc_other2_self1_tenant_v4['network'],
                            'ip_address': dc_other2_self1_tenant_v4['ip'],
                            'netmask_cidr': dc_other2_self1_tenant_v4[
                                                                'netmask'],
                         }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # Delete Tunnel Interface(DC_OTHER-CE#2 DC_SELF-CE#2)
                    msa.delete_csr1000v_tunnel_interface_gre_ipv4(
                        dc_other['ce2_info']['MSA_device_id'],
                        dc_other_ce2_tunnel_interface_name + '2',
                        {
                            'segment': dc_other2_self2_tenant_v4['network'],
                            'ip_address': dc_other2_self2_tenant_v4['ip'],
                            'netmask_cidr': dc_other2_self2_tenant_v4[
                                                                'netmask'],
                         }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                # Delete Tunnel Interface v6
                if ipv6_self_flg == "1" and ipv6_other_flg == "1":
                    try:
                        # Delete Tunnel Interface(DC_OTHER-CE#1 DC_SELF-CE#1)
                        msa.delete_csr1000v_tunnel_interface_gre_ipv6(
                            dc_other['ce1_info']['MSA_device_id'],
                            dc_other_ce1_tunnel_interface_name + '1',
                            {
                                'ipv6_address': dc_other1_self1_tenant_v6[
                                                                        'ip'],
                                'prefix': dc_other1_self1_tenant_v6['netmask'],
                                'ipv6_segment': dc_other1_self1_tenant_v6[
                                                                    'network'],
                            }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete Tunnel Interface(DC_OTHER-CE#1 DC_SELF-CE#2)
                        msa.delete_csr1000v_tunnel_interface_gre_ipv6(
                            dc_other['ce1_info']['MSA_device_id'],
                            dc_other_ce1_tunnel_interface_name + '2',
                            {
                                'ipv6_address': dc_other1_self2_tenant_v6[
                                                                        'ip'],
                                'prefix': dc_other1_self2_tenant_v6['netmask'],
                                'ipv6_segment': dc_other1_self2_tenant_v6[
                                                                    'network'],
                             }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete Tunnel Interface(DC_OTHER-CE#2 DC_SELF-CE#1)
                        msa.delete_csr1000v_tunnel_interface_gre_ipv6(
                            dc_other['ce2_info']['MSA_device_id'],
                            dc_other_ce2_tunnel_interface_name + '1',
                            {
                                'ipv6_address': dc_other2_self1_tenant_v6[
                                                                        'ip'],
                                'prefix': dc_other2_self1_tenant_v6['netmask'],
                                'ipv6_segment': dc_other2_self1_tenant_v6[
                                                                    'network'],
                             }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete Tunnel Interface(DC_OTHER-CE#2 DC_SELF-CE#2)
                        msa.delete_csr1000v_tunnel_interface_gre_ipv6(
                            dc_other['ce2_info']['MSA_device_id'],
                            dc_other_ce2_tunnel_interface_name + '2',
                            {
                                'ipv6_address': dc_other2_self2_tenant_v6[
                                                                        'ip'],
                                'prefix': dc_other2_self2_tenant_v6['netmask'],
                                'ipv6_segment': dc_other2_self2_tenant_v6[
                                                                    'network'],
                             }
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                # Get DC Segment(OtherDC)
                dc_other_segment = self._get_dc_segment(dc_other_id,
                                                            group_id)
                # Delete Static Route For DC(MSA)
                try:
                    # otherDC CE#1 - selfDC
                    msa.delete_csr1000v_static_route_for_dc(
                        dc_other['ce1_info']['MSA_device_id'],
                        msa_config_for_device['static_route_for_dc']
                                                         + dc_self_id,
                        {
                            'ip_address': dc_self_segment['network_address'],
                            'netmask': \
                                self.utils.get_subnet_mask_from_cidr_ipv6(
                                    dc_self_segment['network_address'] \
                                    + '/' + \
                                    str(dc_self_segment['netmask'])),
                            'nexthop_address': dc_other_segment['next_hop'],
                            'netmask_cidr': dc_self_segment['netmask'],
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                try:
                    # otherDC CE#2 - selfDC
                    msa.delete_csr1000v_static_route_for_dc(
                        dc_other['ce2_info']['MSA_device_id'],
                        msa_config_for_device['static_route_for_dc']
                                                         + dc_self_id,
                        {
                            'ip_address': dc_self_segment['network_address'],
                            'netmask': \
                                self.utils.get_subnet_mask_from_cidr_ipv6(
                                    dc_self_segment['network_address'] \
                                    + '/' + \
                                    str(dc_self_segment['netmask'])),
                            'nexthop_address': dc_other_segment['next_hop'],
                            'netmask_cidr': dc_self_segment['netmask'],
                        }
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

    def __create_db_dc_member(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        group_id = job_input['group_id']
        nal_tenant_id = job_input['nal_tenant_id']
        wan_network_id = job_input.get('wan_network_id')
        iaas_region_id = job_input['IaaS_region_id']
        iaas_network_type = job_input['IaaS_network_type']
        iaas_network_id = job_input['IaaS_network_id']
        network_name = job_input['network_name']
        iaas_subnet_id = job_input['IaaS_subnet_id']
        iaas_segmentation_id = job_input['IaaS_segmentation_id']
        fw_ip_address = job_input.get('fw_ip_address', '')
        iaas_subnet_id_v6 = job_input.get('IaaS_subnet_id_v6', '')
        ce_info = job_input['ce_info']

        ce1_node_id = job_input['server_id'][
                                        self.job_config.VM_ROUTER_NODE_NAME1]
        ce2_node_id = job_input['server_id'][
                                        self.job_config.VM_ROUTER_NODE_NAME2]
        port_list_ce1 = job_input['tenant_port_info'][
                                        self.job_config.VM_ROUTER_NODE_NAME1]
        port_list_ce2 = job_input['tenant_port_info'][
                                        self.job_config.VM_ROUTER_NODE_NAME2]
        port_list_vrrp = job_input['tenant_port_info']['vrrp']

        bandwidth = job_input.get('bandwidth', '')

        # Get Endpoint(DB Client)
        db_endpoint_dc_member = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_MEMBER)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        vrrp_address_cidr = port_list_vrrp['ip_address'] \
                                         + '/' + port_list_vrrp['netmask']
        ce1_address_cidr = port_list_ce1['ip_address'] \
                                         + '/' + port_list_ce1['netmask']
        ce2_address_cidr = port_list_ce2['ip_address'] \
                                         + '/' + port_list_ce2['netmask']

        if self.utils.get_ipaddress_version(
                    port_list_ce1['ip_address']) == self.utils.IP_VER_V4:

            # Create Instance(DB Client)
            db_create_instance = create.CreateClient(self.job_config)

            # Create WIM_DC_CONNECT_MEMBER_MNG(DB Client)
            params = {}
            params['create_id'] = operation_id
            params['update_id'] = operation_id
            params['delete_flg'] = 0
            params['tenant_name'] = tenant_name
            params['group_id'] = group_id
            params['dc_id'] = dc_id
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['wan_network_id'] = wan_network_id
            params['ce1_info'] = json.dumps(ce_info[0])
            params['ce2_info'] = json.dumps(ce_info[1])
            params['ce1_node_id'] = ce1_node_id
            params['ce2_node_id'] = ce2_node_id
            params['IaaS_region_id'] = iaas_region_id
            params['IaaS_network_type'] = iaas_network_type
            params['IaaS_network_id'] = iaas_network_id
            params['IaaS_network_name'] = network_name
            params['IaaS_subnet_id'] = iaas_subnet_id
            params['IaaS_segmentation_id'] = iaas_segmentation_id
            params['default_gateway'] = fw_ip_address
            params['vrrp_address'] = vrrp_address_cidr
            params['ce1_address'] = ce1_address_cidr
            params['ce2_address'] = ce2_address_cidr
            params['IaaS_subnet_id_v6'] = ''
            params['vrrp_address_v6'] = ''
            params['ce1_address_v6'] = ''
            params['ce2_address_v6'] = ''
            if len(bandwidth) > 0:
                params['bandwidth'] = bandwidth

            db_create_instance.set_context(db_endpoint_dc_member, params)
            db_create_instance.execute()

        else:

            # Create Instance(DB Client)
            db_list_instance = list.ListClient(self.job_config)
            db_update_instance = update.UpdateClient(self.job_config)

            # List WIM_DC_CONNECT_MEMBER_MNG(DB Client)
            params = {}
            params['dc_id'] = dc_id
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['IaaS_subnet_id'] = iaas_subnet_id
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_dc_member, params)
            db_list_instance.execute()
            dc_member_list = db_list_instance.get_return_param()

            # Update WIM_DC_CONNECT_MEMBER_MNG(DB Client)
            keys = [dc_member_list[0]['ID']]
            params = {}
            params['update_id'] = operation_id
            params['IaaS_subnet_id_v6'] = iaas_subnet_id_v6
            params['vrrp_address_v6'] = vrrp_address_cidr
            params['ce1_address_v6'] = ce1_address_cidr
            params['ce2_address_v6'] = ce2_address_cidr
            db_update_instance.set_context(
                                        db_endpoint_dc_member, keys, params)
            db_update_instance.execute()

    def __get_dc_info(self, dc_id):

        # Get Endpoint(DB Client)
        db_endpoint_dc = self.get_db_endpoint(self.job_config.REST_URI_WIM_DC)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['dc_id'] = dc_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_dc, params)
        db_list.execute()
        dc_list = db_list.get_return_param()

        return dc_list[0]

    def __get_hsrp_tracking_track_id(self,
                                    interface_number, dc_number, ip_version):

            return int(
                interface_number \
                + self.CSR1000V_VARIABLE_CONFIG[
                        'hsrp_track_id_prefix'][ip_version] \
                + '{0:02d}'.format(int(dc_number))[-1:]
            )

    def __get_dc_member_list(self, group_id, dc_id):

        # Get Endpoint(DB Client)
        db_endpoint_dc_member = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_MEMBER)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # List WIM_DC_CONNECT_MEMBER_MNG(DB Client)
        params = {}
        params['group_id'] = group_id
        params['dc_id'] = dc_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc_member, params)
        db_list_instance.execute()
        dc_member_list = db_list_instance.get_return_param()

        return dc_member_list
