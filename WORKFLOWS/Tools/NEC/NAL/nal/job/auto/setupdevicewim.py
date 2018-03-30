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
import time
import traceback

from job.auto import base
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import ciscocsrstdiosxeordercmdws
from job.lib.soap.msa import fireflyvmordercmdws


class SetupDeviceWim(base.JobAutoBase):

    FIREFLY_VM_STATIC_ROUTE_DST_NAME = 'default'
    FIREFLY_VM_STATIC_DESTINATION_IP_ADDRESS = '0.0.0.0'
    FIREFLY_VM_STATIC_DESTINATION_NETMASK = 0
    FIREFLY_VARIABLE_CONFIG = {
        'ce01': {
            'bgp_local_preference': 200,
            'vrrp_priority': 254,
        },
        'ce02': {
            'bgp_local_preference': 110,
            'vrrp_priority': 250,
        },
    }

    CSR1000V_VM_STATICROUTE_OBJECT_ID = 'default'
    CSR1000V_VM_STATIC_DESTINATION_IP_ADDRESS = '0.0.0.0'
    CSR1000V_VM_STATIC_DESTINATION_NETMASK = '0.0.0.0'
    CSR1000V_VM_STATICROUTE_OBJECT_ID_V6 = 'default'

    CSR1000V_VARIABLE_CONFIG = {
        'msa_object_name_hsrp': {
            'ce01': 'create_csr1000v_hsrp_primary_ipv',
            'ce02': 'create_csr1000v_hsrp_secondary_ipv',
        },
        'hsrp_group_id': {
            '4': 1,
            '6': 1000,
        },
        'hsrp_track_id_prefix': {
            '4': '',
            '6': '1',
        },
    }

    CSR1000V_MSA_CLIENT_CONFIG = {
        '3': {
            'ipsec_basic_create': 'create_csr1000v_ipsec_basic_esp_gre_ipv4',
        },
        '4': {
            'ipsec_basic_create': 'create_csr1000v_ipsec_basic_ah_gre_ipv4',
        },
    }

    def device_setup_create_csr1000v_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        rname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Device SetUp
        ret1 = self.__device_setup_create_csr1000v_vm(job_input, rname1)
        ret2 = self.__device_setup_create_csr1000v_vm(job_input, rname2)

        job_output = {
            'apl_wk': {
                    rname1: ret1['apl_wk'],
                    rname2: ret2['apl_wk'],
            },
            'msa_port_wk': {
                    rname1: ret1['msa_port_wk'],
                    rname2: ret2['msa_port_wk'],
            },
            'wan_port_wk': {
                    rname1: ret1['wan_port_wk'],
                    rname2: ret2['wan_port_wk'],
            },
            'tenant_lan_port_wk': {
                    rname1: ret1['tenant_lan_port_wk'],
                    rname2: ret2['tenant_lan_port_wk'],
                    'vrrp': job_input['tenant_lan_port_wk']['vrrp']
            },
            'ce_info': {
                    rname1: ret1['ce_info'],
                    rname2: ret2['ce_info'],
            },
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_device_setup_create_csr1000v_for_tunnel(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        rname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get DC Segment
        dc_segment = self._get_dc_segment(
                                    job_input['dc_id'], job_input['group_id'])

        # Device SetUp
        ret1 = self.__device_setup_create_csr1000v_vm_for_tunnel(
                                                job_input, rname1, dc_segment)

        ret2 = self.__device_setup_create_csr1000v_vm_for_tunnel(
                                                job_input, rname2, dc_segment)

        job_output = {
            'apl_wk': {
                    rname1: ret1['apl_wk'],
                    rname2: ret2['apl_wk'],
            },
            'msa_port_wk': {
                    rname1: ret1['msa_port_wk'],
                    rname2: ret2['msa_port_wk'],
            },
            'wan_port_wk': {
                    rname1: ret1['wan_port_wk'],
                    rname2: ret2['wan_port_wk'],
            },
            'tenant_lan_port_wk': {
                    rname1: ret1['tenant_lan_port_wk'],
                    rname2: ret2['tenant_lan_port_wk'],
                    'vrrp': job_input['tenant_lan_port_wk']['vrrp']
            },
            'ce_info': {
                    rname1: ret1['ce_info'],
                    rname2: ret2['ce_info'],
            },
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_device_setup_create_csr1000v_extra(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        rname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Device SetUp
        ret1 = self.__device_setup_create_csr1000v_vm_extra(job_input, rname1)
        ret2 = self.__device_setup_create_csr1000v_vm_extra(job_input, rname2)

        job_output = {
            'apl_wk': {
                    rname1: ret1['apl_wk'],
                    rname2: ret2['apl_wk']
            }
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_msa_license_create_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        rname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create License(MSA)
        ret1 = self.__create_msa_license_csr1000v(job_input, rname1)
        ret2 = self.__create_msa_license_csr1000v(job_input, rname2)

        virtual_apl_list = []
        virtual_apl_list.append(ret1['apl_wk'])
        virtual_apl_list.append(ret2['apl_wk'])

        apl_port_list = []
        apl_port_list.append(job_input['msa_port_wk'][rname1])
        apl_port_list.append(job_input['wan_port_wk'][rname1])
        apl_port_list.append(job_input['msa_port_wk'][rname2])
        apl_port_list.append(job_input['wan_port_wk'][rname2])

        update_apl_port_list = []
        update_apl_port_list.append(job_input['tenant_lan_port_wk'][rname1])
        update_apl_port_list.append(job_input['tenant_lan_port_wk'][rname2])
        update_apl_port_list.append(job_input['tenant_lan_port_wk']['vrrp'])

        ce_info = []
        ce_info.append(job_input['ce_info'][rname1])
        ce_info.append(job_input['ce_info'][rname2])

        job_output = {
            'virtual_apl_list': virtual_apl_list,
            'apl_port_list': apl_port_list,
            'update_apl_port_list': update_apl_port_list,
            'ce_info': ce_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_msa_license_delete_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        rname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create License(MSA)
        self.__delete_msa_license_csr1000v(job_input, rname1)
        self.__delete_msa_license_csr1000v(job_input, rname2)

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_bandwidth_update_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        rname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Update Throughput(MSA)
        ret1 = self.__update_msa_throughput_csr1000v(job_input, rname1)
        ret2 = self.__update_msa_throughput_csr1000v(job_input, rname2)

        # Update WIM_DC_CONNECT_MEMBER_MNG(DB)
        self.__update_db_dc_member_bandwidth(job_input)

        virtual_apl_list = []
        virtual_apl_list.append(ret1['apl_wk'])
        virtual_apl_list.append(ret2['apl_wk'])

        job_output = {
            'virtual_apl_list': virtual_apl_list,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_setting_update_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        rname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Update Throughput(MSA)
        ret1 = self.__update_msa_setting_csr1000v(job_input, rname1)
        ret2 = self.__update_msa_setting_csr1000v(job_input, rname2)

        virtual_apl_list = []
        virtual_apl_list.append(ret1['apl_wk'])
        virtual_apl_list.append(ret2['apl_wk'])

        job_output = {
            'virtual_apl_list': virtual_apl_list,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_create_firefly_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Device SetUp
        ret1 = self.__device_setup_create_firefly_vm(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__device_setup_create_firefly_vm(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME2)

        virtual_apl_list = []
        virtual_apl_list.append(ret1['apl_wk'])
        virtual_apl_list.append(ret2['apl_wk'])

        apl_port_list = []
        apl_port_list.append(ret1['msa_port_wk'])
        apl_port_list.append(ret1['wan_port_wk'])
        apl_port_list.append(ret2['msa_port_wk'])
        apl_port_list.append(ret2['wan_port_wk'])

        update_apl_port_list = []
        update_apl_port_list.append(ret1['tenant_lan_port_wk'])
        update_apl_port_list.append(ret2['tenant_lan_port_wk'])
        update_apl_port_list.append(job_input['tenant_lan_port_wk']['vrrp'])

        ce_info = []
        ce_info.append(ret1['ce_info'])
        ce_info.append(ret2['ce_info'])

        job_output = {
            'virtual_apl_list': virtual_apl_list,
            'apl_port_list': apl_port_list,
            'update_apl_port_list': update_apl_port_list,
            'ce_info': ce_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_update_firefly_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Device SetUp
        ret1 = self.__device_setup_update_firefly_vm(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__device_setup_update_firefly_vm(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME2)

        virtual_apl_list = []
        apl_port_list = []

        update_apl_port_list = []
        update_apl_port_list.append(ret1['tenant_lan_port_wk'])
        update_apl_port_list.append(ret2['tenant_lan_port_wk'])
        update_apl_port_list.append(job_input['tenant_lan_port_wk']['vrrp'])

        ce_info = []
        ce_info.append(ret1['ce_info'])
        ce_info.append(ret2['ce_info'])

        job_output = {
            'virtual_apl_list': virtual_apl_list,
            'apl_port_list': apl_port_list,
            'update_apl_port_list': update_apl_port_list,
            'ce_info': ce_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_update_csr1000v_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Device SetUp
        ret1 = self.__device_setup_update_csr1000v_vm(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__device_setup_update_csr1000v_vm(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME2)

        virtual_apl_list = []
        apl_port_list = []

        update_apl_port_list = []
        update_apl_port_list.append(ret1['tenant_lan_port_wk'])
        update_apl_port_list.append(ret2['tenant_lan_port_wk'])
        update_apl_port_list.append(job_input['tenant_lan_port_wk']['vrrp'])

        ce_info = []
        ce_info.append(ret1['ce_info'])
        ce_info.append(ret2['ce_info'])

        job_output = {
            'virtual_apl_list': virtual_apl_list,
            'apl_port_list': apl_port_list,
            'update_apl_port_list': update_apl_port_list,
            'ce_info': ce_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_device_setup_update_csr1000v_for_tunnel(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Device SetUp
        ret1 = self.__device_setup_update_csr1000v_vm_for_tunnel(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME1)

        ret2 = self.__device_setup_update_csr1000v_vm_for_tunnel(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME2)

        virtual_apl_list = []
        apl_port_list = []

        update_apl_port_list = []
        update_apl_port_list.append(ret1['tenant_lan_port_wk'])
        update_apl_port_list.append(ret2['tenant_lan_port_wk'])
        update_apl_port_list.append(job_input['tenant_lan_port_wk']['vrrp'])

        ce_info = []
        ce_info.append(ret1['ce_info'])
        ce_info.append(ret2['ce_info'])

        job_output = {
            'virtual_apl_list': virtual_apl_list,
            'apl_port_list': apl_port_list,
            'update_apl_port_list': update_apl_port_list,
            'ce_info': ce_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_device_setup_add_ipv6_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Device SetUp
        self_dc_member_list = self.__get_dc_member_list(job_input['group_id'],
                                                        job_input['dc_id'])
        for self_dc_member in self_dc_member_list:
            if self_dc_member['vrrp_address_v6'] != '':
                break
        else:
            self.__device_setup_add_ipv6_dc(job_input)

        # Device SetUp
        ret1 = self.__device_setup_add_ipv6_csr1000v(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__device_setup_add_ipv6_csr1000v(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME2)

        update_apl_port_list = []
        update_apl_port_list.append(ret1['tenant_lan_port_wk'])
        update_apl_port_list.append(ret2['tenant_lan_port_wk'])

        update_apl_wan_port_list = []
        update_apl_wan_port_list.append(ret1['wan_lan_port_wk'])
        update_apl_wan_port_list.append(ret2['wan_lan_port_wk'])

        ce_info = []
        ce_info.append(ret1['ce_info'])
        ce_info.append(ret2['ce_info'])

        job_output = {
            'virtual_apl_list': [],
            'apl_port_list': [],
            'update_apl_port_list': update_apl_port_list,
            'update_apl_wan_port_list': update_apl_wan_port_list,
            'ce_info': ce_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_device_setup_add_ipv6_csr1000v_for_tunnel(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Device SetUp
        self_dc_member_list = self.__get_dc_member_list(job_input['group_id'],
                                                        job_input['dc_id'])
        for self_dc_member in self_dc_member_list:
            if self_dc_member['vrrp_address_v6'] != '':
                break
        else:
            self.__device_setup_add_ipv6_dc_for_tunnel(job_input)

        ret1 = self.__device_setup_add_ipv6_csr1000v_for_tunnel(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__device_setup_add_ipv6_csr1000v_for_tunnel(
                                       job_input,
                                       self.job_config.VM_ROUTER_NODE_NAME2)

        update_apl_port_list = []
        update_apl_port_list.append(ret1['tenant_lan_port_wk'])
        update_apl_port_list.append(ret2['tenant_lan_port_wk'])

        update_apl_wan_port_list = []
        update_apl_wan_port_list.append(ret1['wan_lan_port_wk'])
        update_apl_wan_port_list.append(ret2['wan_lan_port_wk'])

        ce_info = []
        ce_info.append(ret1['ce_info'])
        ce_info.append(ret2['ce_info'])

        job_output = {
            'virtual_apl_list': [],
            'apl_port_list': [],
            'update_apl_port_list': update_apl_port_list,
            'update_apl_wan_port_list': update_apl_wan_port_list,
            'ce_info': ce_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __device_setup_create_firefly_vm(self, job_input, router_name):

        # Get JOB Input Parameters
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        fw_ip_address = job_input['fw_ip_address']

        wan_ip_address = job_input['msa_wan_port_info'][
                                    router_name]['wan_ip_address']
        msa_port_wk = job_input['msa_port_wk'][router_name]
        wan_port_wk = job_input['wan_port_wk'][router_name]
        tenant_lan_port_wk = \
            job_input['tenant_lan_port_wk'][router_name]
        apl_wk = job_input['apl_wk'][router_name]
        msa_device_id = apl_wk['MSA_device_id']
        node_name = apl_wk['node_name']

        port_list = job_input['tenant_port_info'][router_name]
        port_list_vrrp = job_input['tenant_port_info']['vrrp']

        firefly_config = self.FIREFLY_VARIABLE_CONFIG[router_name]
        bgp_local_preference = firefly_config['bgp_local_preference']
        vrrp_priority = firefly_config['vrrp_priority']

        firefly_vm_authkey = 'T' + '{0:05d}'.format(group_rec_id)

        node_detail = {}
        wan_port_msa_info = {}
        tenant_lan_port_msa_info = {}

        wan_ip_ver = self.utils.IP_VER_V4

        # Get Allocation Info(WAN)
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Create Instance(MSA Soap Client)
        msa = fireflyvmordercmdws.FireflyVmOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        # Create System Common(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_firefly_vm_system_common',
            msa_device_id,
            node_name,
            msa_config_for_device['default_timezone']
        )
        node_detail['create_firefly_vm_system_common'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Create WAN Interface(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_firefly_vm_wan_interface',
            msa_device_id,
            msa_config_for_device['nic_prefix']
                + msa_config_for_device['nic_for_wan'],
            wan_ip_address,
            wan_allocation_info['wan'][wan_ip_ver]['netmask'],
            msa_config_for_device['default_wan_interface_mtu']
        )
        wan_port_msa_info['create_firefly_vm_wan_interface'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Create BGP Basic(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_firefly_vm_bgp_basic',
            msa_device_id,
            node_name,
            wan_ip_address,
            bgp_local_preference,
            firefly_vm_authkey
        )
        wan_port_msa_info['create_firefly_vm_bgp_basic'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Create Loopback Interface(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_firefly_vm_loopback_interface',
            msa_device_id,
            'lo0',
            wan_allocation_info['loopback_ip'],
            wan_allocation_info['loopback_netmask'],
            wan_allocation_info['loopback_seg']
        )
        wan_port_msa_info['create_firefly_vm_loopback_interface'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Create LAN Interface(MSA)
        tenant_nic = msa_config_for_device['nic_prefix']\
                                 + msa_config_for_device['nic_for_first_lan']

        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_firefly_vm_lan_interface',
            msa_device_id,
            tenant_nic,
            port_list['ip_address'],
            port_list['netmask'],
            port_list_vrrp['ip_address'],
            port_list['subnet_ip_address']
        )
        tenant_lan_port_msa_info['create_firefly_vm_lan_interface'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Create VRRP(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_firefly_vm_vrrp',
            msa_device_id,
            tenant_nic,
            port_list_vrrp['ip_address'],
            port_list['ip_address'],
            port_list['netmask'],
            vrrp_priority,
            1,
            firefly_vm_authkey
        )
        tenant_lan_port_msa_info['create_firefly_vm_vrrp'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Create Static Route(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_firefly_vm_static_route',
            msa_device_id,
            self.FIREFLY_VM_STATIC_ROUTE_DST_NAME,
            self.FIREFLY_VM_STATIC_DESTINATION_IP_ADDRESS,
            self.FIREFLY_VM_STATIC_DESTINATION_NETMASK,
            fw_ip_address
        )
        tenant_lan_port_msa_info['create_firefly_vm_static_route'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Set Output Parameters
        apl_wk['node_detail'] = json.dumps(node_detail)
        wan_port_wk['msa_info'] = json.dumps(wan_port_msa_info)
        tenant_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(tenant_lan_port_msa_info)
        ce_info = {
                'MSA_device_id': msa_device_id,
                'host_name': node_name,
                'wan_ip_address': wan_ip_address,
                'lan_ip_address': port_list['ip_address'],
                'lan_netmask': port_list['netmask'],
                'nic': tenant_nic,
                'loopback_ip_address': wan_allocation_info['loopback_ip'],
                'loopback_seg': wan_allocation_info['loopback_seg'],
                'loopback_netmask': wan_allocation_info['loopback_netmask'],
        }

        # Set JOB Output Parameters
        job_output = {
            'ce_info': ce_info,
            'apl_wk': apl_wk,
            'msa_port_wk': msa_port_wk,
            'wan_port_wk': wan_port_wk,
            'tenant_lan_port_wk': tenant_lan_port_wk,
        }

        return job_output

    def __device_setup_create_csr1000v_vm(self, job_input, router_name):

        node_detail = {}
        wan_port_msa_info = {}
        tenant_lan_port_msa_info = {}

        # Get JOB Input Parameters
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        fw_ip_address = self.utils.get_ipaddress_compressed(
                                                job_input['fw_ip_address'])

        msa_port_wk = job_input['msa_port_wk'][router_name]
        wan_port_wk = job_input['wan_port_wk'][router_name]
        tenant_lan_port_wk = \
            job_input['tenant_lan_port_wk'][router_name]
        apl_wk = job_input['apl_wk'][router_name]
        msa_device_id = apl_wk['MSA_device_id']
        node_name = apl_wk['node_name']

        port_list = job_input['tenant_port_info'][router_name]
        port_list_vrrp = job_input['tenant_port_info']['vrrp']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Set Parameters(MSA)
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        wan_ip_address_v4 = wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V4]['ip']
        wan_subnet_ip_v4 = wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V4]['subnet_ip']
        wan_prefix_v4 = wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V4]['netmask']
        wan_netmask_v4 = self.utils.get_subnet_mask_from_cidr_ipv6(
                                wan_subnet_ip_v4 + '/' + str(wan_prefix_v4))

        wan_ip_address_v6 = wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V6]['ip']

        wan_interface_name = msa_config_for_device['nic_prefix'] \
                                    + msa_config_for_device['nic_for_wan']

        wan_loopback_netmask = self.utils.get_subnet_mask_from_cidr_ipv6(
                                wan_allocation_info['loopback_ip'] + '/' +
                                str(wan_allocation_info['loopback_netmask']))

        tenant_lan_ip_address = port_list['ip_address']
        tenant_lan_cidr = port_list['netmask']
        tenant_lan_seg = port_list['subnet_ip_address']
        tenant_lan_netmask = self.utils.get_subnet_mask_from_cidr_ipv6(
                                tenant_lan_seg + '/' + str(tenant_lan_cidr))
        tenant_lan_vip = port_list_vrrp['ip_address']

        msa_object_name_hsrp = self.CSR1000V_VARIABLE_CONFIG[
                                        'msa_object_name_hsrp'][router_name]

        bgp_local_preference = \
            msa_config_for_device[router_name]['bgp_local_preference']

        hsrp_priority = \
            msa_config_for_device[router_name]['hsrp_priority']

        hsrp_track_prioritycost = \
            msa_config_for_device[router_name]['hsrp_track_prioritycost']

        tenant_lan_interface_name \
            = str(msa_config_for_device['nic_prefix']) \
                  + str(msa_config_for_device['nic_for_first_lan'])

        tenant_lan_interface_track_name = tenant_lan_interface_name \
                                    + '_track_' + tenant_lan_interface_name

        hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][self.utils.IP_VER_V4]

        hsrp_track_id = self.__get_hsrp_interface_tracking_track_id(
                            self.utils.IP_VER_V4,
                            str(msa_config_for_device['nic_for_first_lan']),
                            str(msa_config_for_device['nic_for_first_lan']))

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        # Create System Common(MSA)
        msa_client_name = 'create_csr1000v_system_common_ipv6'
        msa_option_params = {
            'timezone': msa_config_for_device['default_timezone'],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create WAN Interface IPv4(MSA)
        msa_client_name = 'create_csr1000v_wan_interface_ipv4'
        msa_option_params = {
            'ip_address': wan_ip_address_v4,
            'netmask': wan_netmask_v4,
            'mtu': msa_config_for_device['default_wan_interface_mtu'],
            'segment': wan_subnet_ip_v4,
            'netmask_cidr': wan_prefix_v4,
            'tcp_mss': msa_config_for_device['default_wan_interface_tcp_mss'],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            wan_interface_name,
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create BGP Basic IPv4(MSA)
        msa_client_name = 'create_csr1000v_bgp_basic_ipv4'
        msa_option_params = {
            'ip_address': wan_ip_address_v4,
            'local_preference': bgp_local_preference,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create Loopback Interface(MSA)
        msa_client_name = 'create_csr1000v_loopback_interface'
        msa_option_params = {
            'ip_address': wan_allocation_info['loopback_ip'],
            'netmask': wan_loopback_netmask,
            'segment': wan_allocation_info['loopback_seg'],
            'netmask_cidr': wan_allocation_info['loopback_netmask'],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            msa_config_for_device['loopback_interface_name'],
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create LAN Interface IPv4(MSA)
        msa_client_name = 'create_csr1000v_lan_interface_ipv4'
        msa_option_params = {
            'ip_address': tenant_lan_ip_address,
            'hsrp_ip_address': tenant_lan_vip,
            'segment': tenant_lan_seg,
            'netmask_cidr': tenant_lan_cidr,
            'netmask': tenant_lan_netmask,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_interface_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP IPv4(MSA)
        msa_client_name = msa_object_name_hsrp + self.utils.IP_VER_V4
        msa_option_params = {
            'ip_address': tenant_lan_vip,
            'priority': hsrp_priority,
            'group_id': hsrp_group_id,
            'authkey': authkey,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_interface_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP Interface Tracking(MSA)
        msa_client_name = 'create_csr1000v_hsrp_interface_tracking'
        msa_option_params = {
            'interface': tenant_lan_interface_name,
            'group_id': hsrp_group_id,
            'track_interface': tenant_lan_interface_name,
            'prioritycost': hsrp_track_prioritycost,
            'track_id': hsrp_track_id,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_interface_track_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create Default Route IPv4 or IPv6(MSA)
        msa_client_name = 'create_csr1000v_default_route_ipv4'
        msa_option_params = {
            'ip_address': self.CSR1000V_VM_STATIC_DESTINATION_IP_ADDRESS,
            'netmask': self.CSR1000V_VM_STATIC_DESTINATION_NETMASK,
            'nexthop_address': fw_ip_address,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            self.CSR1000V_VM_STATICROUTE_OBJECT_ID,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Set Output Parameters
        apl_wk['node_detail'] = json.dumps(node_detail)
        wan_port_wk['msa_info'] = json.dumps(wan_port_msa_info)
        tenant_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(tenant_lan_port_msa_info)
        ce_info = {
            'MSA_device_id': msa_device_id,
            'host_name': node_name,
            'wan_ip_address': {
                self.utils.IP_VER_V4: wan_ip_address_v4,
                self.utils.IP_VER_V6: wan_ip_address_v6,
            },
            'lan_ip_address': port_list['ip_address'],
            'lan_netmask': port_list['netmask'],
            'loopback_ip_address': wan_allocation_info['loopback_ip'],
            'loopback_seg': wan_allocation_info['loopback_seg'],
            'loopback_netmask': wan_allocation_info['loopback_netmask'],
            'nic': tenant_lan_interface_name,
            'csr1000v': {
                'hsrp_track_prioritycost': hsrp_track_prioritycost,
                'hsrp_track_group_id': hsrp_track_id,
            },
        }

        # Set JOB Output Parameters
        job_output = {
            'ce_info': ce_info,
            'apl_wk': apl_wk,
            'msa_port_wk': msa_port_wk,
            'wan_port_wk': wan_port_wk,
            'tenant_lan_port_wk': tenant_lan_port_wk,
        }

        return job_output

    def __device_setup_create_csr1000v_vm_for_tunnel(
                            self, job_input, router_name, dc_segment):

        node_detail = {}
        wan_port_msa_info = {}
        tenant_lan_port_msa_info = {}

        # Get JOB Input Parameters
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        group_type = job_input['group_type']
        fw_ip_address = self.utils.get_ipaddress_compressed(
                                        job_input['fw_ip_address'])

        msa_port_wk = job_input['msa_port_wk'][router_name]
        wan_port_wk = job_input['wan_port_wk'][router_name]
        tenant_lan_port_wk = \
            job_input['tenant_lan_port_wk'][router_name]
        apl_wk = job_input['apl_wk'][router_name]
        msa_device_id = apl_wk['MSA_device_id']
        node_name = apl_wk['node_name']

        port_list = job_input['tenant_port_info'][router_name]
        port_list_vrrp = job_input['tenant_port_info']['vrrp']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Set Parameters(MSA)
        wan_ip_address_v4 = dc_segment[router_name + '_ip_address']
        wan_subnet_ip_v4 = dc_segment['network_address']
        wan_prefix_v4 = dc_segment['netmask']

        wan_netmask_v4 = self.utils.get_subnet_mask_from_cidr_ipv6(
                                wan_subnet_ip_v4 + '/' + str(wan_prefix_v4))

        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        wan_interface_name = msa_config_for_device['nic_prefix'] \
                                    + msa_config_for_device['nic_for_wan']

        tenant_lan_ip_address = port_list['ip_address']
        tenant_lan_cidr = port_list['netmask']
        tenant_lan_seg = port_list['subnet_ip_address']
        tenant_lan_netmask = self.utils.get_subnet_mask_from_cidr_ipv6(
                                tenant_lan_seg + '/' + str(tenant_lan_cidr))
        tenant_lan_vip = port_list_vrrp['ip_address']

        bgp_local_preference = \
            msa_config_for_device[router_name]['bgp_local_preference']

        hsrp_priority = \
            msa_config_for_device[router_name]['hsrp_priority']

        hsrp_track_prioritycost = \
            msa_config_for_device[router_name]['hsrp_track_prioritycost']

        msa_object_name_hsrp = self.CSR1000V_VARIABLE_CONFIG[
                                        'msa_object_name_hsrp'][router_name]

        msa_ipsec_basic_client = self.CSR1000V_MSA_CLIENT_CONFIG[
                                    str(group_type)]['ipsec_basic_create']

        tenant_lan_interface_name \
            = str(msa_config_for_device['nic_prefix']) \
                  + str(msa_config_for_device['nic_for_first_lan'])

        tenant_lan_interface_track_name = tenant_lan_interface_name \
                                    + '_track_' + tenant_lan_interface_name

        hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][self.utils.IP_VER_V4]

        hsrp_track_id \
            = int(self.CSR1000V_VARIABLE_CONFIG[
                            'hsrp_track_id_prefix'][self.utils.IP_VER_V4] \
                + str(msa_config_for_device['nic_for_first_lan']) \
                  + str(msa_config_for_device['nic_for_first_lan']))

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        # Create System Common(MSA)
        msa_client_name = 'create_csr1000v_system_common_ipv6'
        msa_option_params = {
            'timezone': msa_config_for_device['default_timezone'],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create WAN Interface Gre IPv4(MSA)
        msa_client_name = 'create_csr1000v_wan_interface_gre_ipv4'
        msa_option_params = {
            'ip_address': wan_ip_address_v4,
            'netmask': wan_netmask_v4,
            'mtu': msa_config_for_device['default_wan_interface_mtu'],
            'segment': wan_subnet_ip_v4,
            'netmask_cidr': wan_prefix_v4,
            'tcp_mss': msa_config_for_device[
                                'default_wan_interface_tcp_mss_tunnel'],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            wan_interface_name,
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create BGP Basic IPv4(MSA)
        msa_client_name = 'create_csr1000v_bgp_basic_ipv4'
        msa_option_params = {
            'ip_address': wan_ip_address_v4,
            'local_preference': bgp_local_preference,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create Loopback Interface(MSA)
        msa_client_name = 'create_csr1000v_loopback_interface'
        msa_option_params = {
            'ip_address': wan_allocation_info['loopback_ip'],
            'netmask': self.utils.get_subnet_mask_from_cidr_ipv6(
                        wan_allocation_info['loopback_ip'] + '/' +
                        str(wan_allocation_info['loopback_netmask'])),
            'segment': wan_allocation_info['loopback_seg'],
            'netmask_cidr': wan_allocation_info['loopback_netmask'],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            msa_config_for_device['loopback_interface_name'],
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create IPSec Basic Gre IPv4(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_ipsec_basic_client,
            msa_device_id,
            node_name,
            msa_config_for_device['msa_client_params'][
                    str(group_type)][msa_ipsec_basic_client][router_name]
        )
        node_detail[msa_ipsec_basic_client] = msa_res[msa.RES_KEY_IN]

        # Create LAN Interface IPv4(MSA)
        msa_client_name = 'create_csr1000v_lan_interface_ipv4'
        msa_option_params = {
            'ip_address': tenant_lan_ip_address,
            'hsrp_ip_address': tenant_lan_vip,
            'segment': tenant_lan_seg,
            'netmask_cidr': tenant_lan_cidr,
            'netmask': tenant_lan_netmask,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_interface_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP IPv4(MSA)
        msa_client_name = msa_object_name_hsrp + self.utils.IP_VER_V4
        msa_option_params = {
            'ip_address': tenant_lan_vip,
            'priority': hsrp_priority,
            'group_id': hsrp_group_id,
            'authkey': authkey,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_interface_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP Interface Tracking(MSA)
        msa_client_name = 'create_csr1000v_hsrp_interface_tracking'
        msa_option_params = {
            'interface': tenant_lan_interface_name,
            'group_id': hsrp_group_id,
            'track_interface': tenant_lan_interface_name,
            'prioritycost': hsrp_track_prioritycost,
            'track_id': hsrp_track_id,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_interface_track_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create Default Route IPv4 or IPv6(MSA)
        msa_client_name = 'create_csr1000v_default_route_ipv' \
                        + self.utils.get_ipaddress_version(fw_ip_address)
        msa_option_params = {
            'ip_address': self.CSR1000V_VM_STATIC_DESTINATION_IP_ADDRESS,
            'netmask': self.CSR1000V_VM_STATIC_DESTINATION_NETMASK,
            'nexthop_address': fw_ip_address,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            self.CSR1000V_VM_STATICROUTE_OBJECT_ID,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Set Output Parameters
        apl_wk['node_detail'] = json.dumps(node_detail)
        wan_port_wk['msa_info'] = json.dumps(wan_port_msa_info)
        tenant_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(tenant_lan_port_msa_info)
        ce_info = {
            'MSA_device_id': msa_device_id,
            'host_name': node_name,
            'wan_ip_address': {
                self.utils.IP_VER_V4: wan_ip_address_v4,
            },
            'lan_ip_address': port_list['ip_address'],
            'lan_netmask': port_list['netmask'],
            'loopback_ip_address': wan_allocation_info['loopback_ip'],
            'loopback_seg': wan_allocation_info['loopback_seg'],
            'loopback_netmask': wan_allocation_info['loopback_netmask'],
            'nic': tenant_lan_interface_name,
            'csr1000v': {
                'hsrp_track_prioritycost': hsrp_track_prioritycost,
                'hsrp_track_group_id': hsrp_track_id,
            },
        }

        # Set JOB Output Parameters
        job_output = {
            'ce_info': ce_info,
            'apl_wk': apl_wk,
            'msa_port_wk': msa_port_wk,
            'wan_port_wk': wan_port_wk,
            'tenant_lan_port_wk': tenant_lan_port_wk,
        }

        return job_output

    def __device_setup_create_csr1000v_vm_extra(self, job_input, router_name):

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        apl_wk = job_input['apl_wk'][router_name]
        msa_device_id = apl_wk['MSA_device_id']
        node_name = apl_wk['node_name']
        node_detail = json.loads(apl_wk['node_detail'])

        dns_server_ip_address = job_input['dns_server_ip_address']
        ntp_server_ip_address = job_input['ntp_server_ip_address']
        snmp_server_ip_address = job_input['snmp_server_ip_address']
        syslog_server_ip_address = job_input['syslog_server_ip_address']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        # Create DNS IPv4(MSA)
        dns_server_ip_address = self.utils.get_ipaddress_compressed(
                                                    dns_server_ip_address)
        msa_client_name = 'create_csr1000v_dns_ipv4'
        msa_option_params = {
            'ip_address': dns_server_ip_address,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params,
        )
        node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]
        apl_wk['dns_server_ip_address'] = dns_server_ip_address

        # Set MSA Parameters(NTP IP Address)
        ntp_server_interface = msa_config_for_device['nic_prefix'] \
            + msa_config_for_device['nic_for_first_lan']

        # Create NTP IPv4(MSA)
        ntp_server_ip_address = self.utils.get_ipaddress_compressed(
                                                    ntp_server_ip_address)
        msa_client_name = 'create_csr1000v_ntp_ipv4'
        msa_option_params = {
            'ip_address': ntp_server_ip_address,
            'interface': ntp_server_interface,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]
        apl_wk['ntp_server_ip_address'] = ntp_server_ip_address

        # Set MSA Parameters(SNMP IP Address)
        if len(snmp_server_ip_address) != 0:
            snmp_server_interface = msa_config_for_device['nic_prefix'] \
                + msa_config_for_device['nic_for_first_lan']

            # Create SNMP IPv4(MSA)
            ntp_server_ip_address = self.utils.get_ipaddress_compressed(
                                                    snmp_server_ip_address)
            msa_client_name = 'create_csr1000v_snmp_ipv4'
            msa_option_params = {
                'community_name': \
                        msa_config_for_device['snmp_community_name'],
                'interface': snmp_server_interface,
                'ip_address': snmp_server_ip_address,
                'version': msa_config_for_device['snmp_trap_version'],
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name,
                msa_device_id,
                node_name,
                msa_option_params
            )
            node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]
            apl_wk['snmp_server_ip_address'] = snmp_server_ip_address

        # Set MSA Parameters(Syslog IP Address)
        if len(syslog_server_ip_address) != 0:
            syslog_server_interface = msa_config_for_device['nic_prefix'] \
                + msa_config_for_device['nic_for_first_lan']

            # Create Syslog IPv4(MSA)
            syslog_server_ip_address = self.utils.get_ipaddress_compressed(
                                                    syslog_server_ip_address)
            msa_client_name = 'create_csr1000v_syslog_ipv4'
            msa_option_params = {
                'ip_address': syslog_server_ip_address,
                'interface': syslog_server_interface,
                'facility': msa_config_for_device['syslog_facility'],
                'severity': msa_config_for_device['syslog_severity'],
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name,
                msa_device_id,
                node_name,
                msa_option_params
            )
            node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]
            apl_wk['syslog_server_ip_address'] = syslog_server_ip_address

        # Set Output Parameters
        apl_wk['node_detail'] = json.dumps(node_detail)

        # Set JOB Output Parameters
        job_output = {
            'apl_wk': apl_wk
        }

        return job_output

    def __device_setup_update_firefly_vm(self, job_input, router_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        msa_device_id = job_input['apl_info'][router_name]['MSA_device_id']
        node_id = job_input['apl_info'][router_name]['node_id']
        node_name = job_input['apl_info'][router_name]['node_name']
        port_list = job_input['tenant_port_info'][router_name]
        port_list_vrrp = job_input['tenant_port_info']['vrrp']
        new_nic_name = job_input['new_nic_name']

        firefly_config = self.FIREFLY_VARIABLE_CONFIG[router_name]
        vrrp_priority = firefly_config['vrrp_priority']

        firefly_vm_authkey = 'T' + '{0:05d}'.format(group_rec_id)

        tenant_lan_port_msa_info = {}

        # Get Allocation Info(WAN)
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Create Instance(MSA Soap Client)
        msa = fireflyvmordercmdws.FireflyVmOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        # Create LAN Interface(MSA)
        msa_res = msa.create_firefly_vm_lan_interface(
                                    msa_device_id,
                                    new_nic_name,
                                    port_list['ip_address'],
                                    port_list['netmask'],
                                    port_list_vrrp['ip_address'],
                                    port_list['subnet_ip_address'])
        tenant_lan_port_msa_info['create_firefly_vm_lan_interface'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Create VRRP(MSA)
        msa_res = msa.create_firefly_vm_vrrp(
                                    msa_device_id,
                                    new_nic_name,
                                    port_list_vrrp['ip_address'],
                                    port_list['ip_address'],
                                    port_list['netmask'],
                                    vrrp_priority,
                                    1,
                                    firefly_vm_authkey)
        tenant_lan_port_msa_info['create_firefly_vm_vrrp'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Set Output Parameters
        tenant_lan_port_wk = {'params': {}, 'keys': {}}
        tenant_lan_port_wk['params']['update_id'] = operation_id
        tenant_lan_port_wk['params']['node_id'] = node_id
        tenant_lan_port_wk['params']['nic'] = new_nic_name
        tenant_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(tenant_lan_port_msa_info)
        tenant_lan_port_wk['keys'] = {'ID': port_list['rec_id']}

        ce_info = {
                'MSA_device_id': msa_device_id,
                'host_name': node_name,
                'wan_ip_address': '',
                'lan_ip_address': port_list['ip_address'],
                'lan_netmask': port_list['netmask'],
                'nic': new_nic_name,
                'loopback_ip_address': wan_allocation_info['loopback_ip'],
                'loopback_seg': wan_allocation_info['loopback_seg'],
                'loopback_netmask': wan_allocation_info['loopback_netmask'],
        }

        # Set JOB Output Parameters
        job_output = {
            'tenant_lan_port_wk': tenant_lan_port_wk,
            'ce_info': ce_info,
        }

        return job_output

    def __device_setup_update_csr1000v_vm(self, job_input, router_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        new_nic_name = job_input['new_nic_name']
        dc_group_id = job_input['group_id']

        node_id = job_input['apl_info'][router_name]['node_id']
        node_name = job_input['apl_info'][router_name]['node_name']
        msa_device_id = job_input['apl_info'][router_name]['MSA_device_id']

        port_list = job_input['tenant_port_info'][router_name]
        tenant_lan_ip_address = port_list['ip_address']
        tenant_lan_cidr = port_list['netmask']
        tenant_lan_seg = port_list['subnet_ip_address']
        tenant_lan_netmask = self.utils.get_subnet_mask_from_cidr_len(
                                                        tenant_lan_cidr)

        port_list_vrrp = job_input['tenant_port_info']['vrrp']
        tenant_lan_vip = port_list_vrrp['ip_address']

        tenant_lan_port_msa_info = {}

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Get WAN Config
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)
        hsrp_priority = \
            msa_config_for_device[router_name]['hsrp_priority']
        hsrp_track_prioritycost = \
            msa_config_for_device[router_name]['hsrp_track_prioritycost']

        msa_object_name_hsrp = self.CSR1000V_VARIABLE_CONFIG[
                                        'msa_object_name_hsrp'][router_name]

        hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][self.utils.IP_VER_V4]

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                                self.job_config,
                                                self.nal_endpoint_config,
                                                pod_id,
                                                dc_id)

        # Create LAN Interface(MSA)
        msa_client_name = 'create_csr1000v_lan_interface_ipv4'
        msa_option_params = {
            'ip_address': tenant_lan_ip_address,
            'netmask': tenant_lan_netmask,
            'hsrp_ip_address': tenant_lan_vip,
            'segment': tenant_lan_seg,
            'netmask_cidr': tenant_lan_cidr,
        }

        for count in range(int(self.job_config.MSA_AFTER_ATTACH_COUNT)):
            try:
                msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    msa_client_name,
                    msa_device_id,
                    new_nic_name,
                    msa_option_params
                )
                tenant_lan_port_msa_info[msa_client_name] = \
                    msa_res[msa.RES_KEY_IN]
                break

            except SystemError as e:
                time.sleep(int(self.job_config.MSA_AFTER_ATTACH_INTERVAL))
                count += 1

                if count == int(self.job_config.MSA_AFTER_ATTACH_COUNT):
                    raise e

        # Create HSRP(MSA)
        msa_client_name = msa_object_name_hsrp + self.utils.IP_VER_V4
        msa_option_params = {
            'ip_address': tenant_lan_vip,
            'priority': hsrp_priority,
            'group_id': hsrp_group_id,
            'authkey': authkey,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            new_nic_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP Interface Tracking(MSA)
        msa_wk = []

        nic_num = new_nic_name.replace(msa_config_for_device['nic_prefix'], '')
        self_min = int(msa_config_for_device['nic_for_first_lan'])
        self_max = int(nic_num)
        other_min = int(msa_config_for_device['nic_for_first_lan'])
        other_max = int(nic_num)

        msa_client_name = 'create_csr1000v_hsrp_interface_tracking'
        for other_num in range(other_min, other_max + 1):
            interface = new_nic_name
            track_interface = \
                msa_config_for_device['nic_prefix'] + str(other_num)
            hsrp_track_id = self.__get_hsrp_interface_tracking_track_id(
                                                self.utils.IP_VER_V4,
                                                str(nic_num), str(other_num))
            msa_option_params = {
                'interface': interface,
                'group_id': hsrp_group_id,
                'track_interface': track_interface,
                'prioritycost': hsrp_track_prioritycost,
                'track_id': hsrp_track_id,
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name,
                msa_device_id,
                track_interface + '_track_' + interface,
                msa_option_params
            )
            msa_wk.append(msa_res[msa.RES_KEY_IN])

        for self_num in range(self_min, self_max):

            interface = msa_config_for_device['nic_prefix'] + str(self_num)
            track_interface = new_nic_name
            hsrp_track_id = self.__get_hsrp_interface_tracking_track_id(
                                                self.utils.IP_VER_V4,
                                                str(self_num), str(nic_num))
            msa_option_params = {
                'interface': interface,
                'group_id': hsrp_group_id,
                'track_interface': track_interface,
                'prioritycost': hsrp_track_prioritycost,
                'track_id': hsrp_track_id,
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name,
                msa_device_id,
                track_interface + '_track_' + interface,
                msa_option_params
            )
            msa_wk.append(msa_res[msa.RES_KEY_IN])

        # Other Interface -> Self InterFace (IPv6)
        dc_member_list = self.__get_dc_member_list(dc_group_id, dc_id)

        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_id:

                ce1_info = json.loads(dc_member['ce1_info'])
                other_lan_nic = ce1_info['nic']

                if other_lan_nic != new_nic_name \
                    and len(dc_member['ce1_address_v6']) > 0:

                    other_nic_num = other_lan_nic.replace(
                                msa_config_for_device['nic_prefix'], '')

                    interface = other_lan_nic
                    track_interface = new_nic_name
                    hsrp_track_id = \
                        self.__get_hsrp_interface_tracking_track_id(
                                                    self.utils.IP_VER_V6,
                                                    str(other_nic_num),
                                                    str(nic_num))
                    msa_option_params = {
                        'interface': interface,
                        'group_id': self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][self.utils.IP_VER_V6],
                        'track_interface': track_interface,
                        'prioritycost': hsrp_track_prioritycost,
                        'track_id': hsrp_track_id,
                    }
                    msa_res = self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        msa_client_name,
                        msa_device_id,
                        interface + '_track_' + track_interface,
                        msa_option_params
                    )
                    msa_wk.append(msa_res[msa.RES_KEY_IN])

        tenant_lan_port_msa_info[msa_client_name] = msa_wk

        # Set Output Parameters
        update_apl_port_list = []
        tenant_lan_port_wk = {'params': {}, 'keys': {}}
        tenant_lan_port_wk['params']['update_id'] = operation_id
        tenant_lan_port_wk['params']['node_id'] = node_id
        tenant_lan_port_wk['params']['nic'] = new_nic_name
        tenant_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(tenant_lan_port_msa_info)
        tenant_lan_port_wk['keys'] = {'ID': port_list['rec_id']}

        update_apl_port_list.append(tenant_lan_port_wk)

        ce_info = {
            'MSA_device_id': msa_device_id,
            'host_name': node_name,
            'wan_ip_address': {},
            'lan_ip_address': port_list['ip_address'],
            'lan_netmask': port_list['netmask'],
            'loopback_ip_address': wan_allocation_info['loopback_ip'],
            'loopback_seg': wan_allocation_info['loopback_seg'],
            'loopback_netmask': wan_allocation_info['loopback_netmask'],
            'nic': new_nic_name,
            'csr1000v': {
                'hsrp_track_prioritycost': hsrp_track_prioritycost,
                'hsrp_track_group_id': '',
            },
        }

        # Set JOB Output Parameters
        job_output = {
            'tenant_lan_port_wk': tenant_lan_port_wk,
            'update_apl_port_list': update_apl_port_list,
            'ce_info': ce_info,
        }

        return job_output

    def __device_setup_update_csr1000v_vm_for_tunnel(
                                            self, job_input, router_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        new_nic_name = job_input['new_nic_name']
        dc_group_id = job_input['group_id']

        node_id = job_input['apl_info'][router_name]['node_id']
        node_name = job_input['apl_info'][router_name]['node_name']
        msa_device_id = job_input['apl_info'][router_name]['MSA_device_id']

        port_list = job_input['tenant_port_info'][router_name]
        tenant_lan_ip_address = port_list['ip_address']
        tenant_lan_cidr = port_list['netmask']
        tenant_lan_seg = port_list['subnet_ip_address']
        tenant_lan_netmask = self.utils.get_subnet_mask_from_cidr_len(
                                                        tenant_lan_cidr)

        port_list_vrrp = job_input['tenant_port_info']['vrrp']
        tenant_lan_vip = port_list_vrrp['ip_address']

        tenant_lan_port_msa_info = {}

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Get WAN Config
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)
        hsrp_priority = \
            msa_config_for_device[router_name]['hsrp_priority']
        hsrp_track_prioritycost = \
            msa_config_for_device[router_name]['hsrp_track_prioritycost']

        msa_object_name_hsrp = self.CSR1000V_VARIABLE_CONFIG[
                                        'msa_object_name_hsrp'][router_name]

        hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][self.utils.IP_VER_V4]

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                                self.job_config,
                                                self.nal_endpoint_config,
                                                pod_id,
                                                dc_id)

        # Create LAN Interface(MSA)
        msa_client_name = 'create_csr1000v_lan_interface_ipv4'
        msa_option_params = {
            'ip_address': tenant_lan_ip_address,
            'netmask': tenant_lan_netmask,
            'hsrp_ip_address': tenant_lan_vip,
            'segment': tenant_lan_seg,
            'netmask_cidr': tenant_lan_cidr,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            new_nic_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP(MSA)
        msa_client_name = msa_object_name_hsrp + self.utils.IP_VER_V4
        msa_option_params = {
            'ip_address': tenant_lan_vip,
            'priority': hsrp_priority,
            'group_id': hsrp_group_id,
            'authkey': authkey,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            new_nic_name,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP Interface Tracking(MSA)
        msa_wk = []

        nic_num = new_nic_name.replace(msa_config_for_device['nic_prefix'], '')
        self_min = int(msa_config_for_device['nic_for_first_lan'])
        self_max = int(nic_num)
        other_min = int(msa_config_for_device['nic_for_first_lan'])
        other_max = int(nic_num)

        msa_client_name = 'create_csr1000v_hsrp_interface_tracking'
        for other_num in range(other_min, other_max + 1):
            track_interface = \
                        msa_config_for_device['nic_prefix'] + str(other_num)
            msa_option_params = {
                'interface': new_nic_name,
                'group_id': hsrp_group_id,
                'track_interface': track_interface,
                'prioritycost': hsrp_track_prioritycost,
                'track_id': str(nic_num) + str(other_num),
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name,
                msa_device_id,
                track_interface + '_track_' + new_nic_name,
                msa_option_params
            )
            msa_wk.append(msa_res[msa.RES_KEY_IN])

        for self_num in range(self_min, self_max):

            interface = msa_config_for_device['nic_prefix'] + str(self_num)
            msa_option_params = {
                'interface': interface,
                'group_id': hsrp_group_id,
                'track_interface': new_nic_name,
                'prioritycost': hsrp_track_prioritycost,
                'track_id': str(self_num) + str(nic_num),
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name,
                msa_device_id,
                interface + '_track_' + new_nic_name,
                msa_option_params
            )
            msa_wk.append(msa_res[msa.RES_KEY_IN])

        # Other Interface -> Self InterFace (IPv6)
        dc_member_list = self.__get_dc_member_list(dc_group_id, dc_id)

        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_id:

                ce1_info = json.loads(dc_member['ce1_info'])
                other_lan_nic = ce1_info['nic']

                if other_lan_nic != new_nic_name \
                    and len(dc_member['ce1_address_v6']) > 0:

                    other_nic_num = other_lan_nic.replace(
                                msa_config_for_device['nic_prefix'], '')

                    interface = other_lan_nic
                    track_interface = new_nic_name
                    hsrp_track_id = \
                        self.__get_hsrp_interface_tracking_track_id(
                                                    self.utils.IP_VER_V6,
                                                    str(other_nic_num),
                                                    str(nic_num))
                    msa_option_params = {
                        'interface': interface,
                        'group_id': self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][self.utils.IP_VER_V6],
                        'track_interface': track_interface,
                        'prioritycost': hsrp_track_prioritycost,
                        'track_id': hsrp_track_id,
                    }
                    msa_res = self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        msa_client_name,
                        msa_device_id,
                        interface + '_track_' + track_interface,
                        msa_option_params
                    )
                    msa_wk.append(msa_res[msa.RES_KEY_IN])

        tenant_lan_port_msa_info[msa_client_name] = msa_wk

        # Set Output Parameters
        update_apl_port_list = []
        tenant_lan_port_wk = {'params': {}, 'keys': {}}
        tenant_lan_port_wk['params']['update_id'] = operation_id
        tenant_lan_port_wk['params']['node_id'] = node_id
        tenant_lan_port_wk['params']['nic'] = new_nic_name
        tenant_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(tenant_lan_port_msa_info)
        tenant_lan_port_wk['keys'] = {'ID': port_list['rec_id']}

        update_apl_port_list.append(tenant_lan_port_wk)

        ce_info = {
            'MSA_device_id': msa_device_id,
            'host_name': node_name,
            'wan_ip_address': {},
            'lan_ip_address': port_list['ip_address'],
            'lan_netmask': port_list['netmask'],
            'loopback_ip_address': wan_allocation_info['loopback_ip'],
            'loopback_seg': wan_allocation_info['loopback_seg'],
            'loopback_netmask': wan_allocation_info['loopback_netmask'],
            'nic': new_nic_name,
            'csr1000v': {
                'hsrp_track_prioritycost': hsrp_track_prioritycost,
                'hsrp_track_group_id': '',
            },
#             'wan_subnet_ip': dc_segment['network_address'],
#             'wan_netmask_cidr': dc_segment['netmask'],
#             'wan_netmask': self.utils.get_subnet_mask_from_cidr_ipv6(
#                                 dc_segment['network_address'] \
#                                 + '/' + str(dc_segment['netmask'])),
        }

        # Set JOB Output Parameters
        job_output = {
            'tenant_lan_port_wk': tenant_lan_port_wk,
            'update_apl_port_list': update_apl_port_list,
            'ce_info': ce_info,
        }

        return job_output

    def __device_setup_add_ipv6_csr1000v(self, job_input, router_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        dc_group_id = job_input['group_id']
        fw_ip_v6_address = job_input['fw_ip_v6_address']

        node_id = job_input['apl_info'][router_name]['node_id']
        node_name = job_input['apl_info'][router_name]['node_name']
        msa_device_id = job_input['apl_info'][router_name]['MSA_device_id']

        port_list = job_input['tenant_port_info'][router_name]
        tenant_lan_nic = port_list['nic']
        tenant_lan_ip_address = port_list['ip_address']
        tenant_lan_cidr = port_list['netmask']
        tenant_lan_seg = port_list['subnet_ip_address']

        port_list_vrrp = job_input['tenant_port_info']['vrrp']
        tenant_lan_vip = port_list_vrrp['ip_address']

        tenant_lan_port_msa_info = {}

        wan_port_info = job_input['wan_port_info'][router_name]

        # Get msa_info(WAN)
        for wan_lan in job_input['wan_lan_list']:
            if wan_lan['node_id'] == node_id:
                wan_port_rec_id = wan_lan['rec_id']
                wan_port_msa_info = json.loads(wan_lan['msa_info'])
                break

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Get WAN Config
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)
        hsrp_priority = \
            msa_config_for_device[router_name]['hsrp_priority']
        hsrp_track_prioritycost = \
            msa_config_for_device[router_name]['hsrp_track_prioritycost']

        msa_object_name_hsrp = self.CSR1000V_VARIABLE_CONFIG[
                                        'msa_object_name_hsrp'][router_name]

        hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][self.utils.IP_VER_V6]

        wan_ip_address_v6 = wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V6]['ip']
        wan_subnet_ip_v6 = wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V6]['subnet_ip']
        wan_prefix_v6 = wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V6]['netmask']

        wan_interface_name = msa_config_for_device['nic_prefix'] \
                                    + msa_config_for_device['nic_for_wan']

        bgp_local_preference = msa_config_for_device[router_name][
                                                    'bgp_local_preference']

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                                self.job_config,
                                                self.nal_endpoint_config,
                                                pod_id,
                                                dc_id)

        # Create WAN Interface IPv6(MSA)
        msa_client_name = 'create_csr1000v_wan_interface_ipv6'
        msa_option_params = {
            'ipv6_address': wan_ip_address_v6,
            'prefix': wan_prefix_v6,
            'segment': wan_subnet_ip_v6,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            wan_interface_name,
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create BGP Basic IPv6(MSA)
        msa_client_name = 'create_csr1000v_bgp_basic_ipv6'
        msa_option_params = {
            'local_preference': bgp_local_preference,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create LAN Interface(MSA)
        msa_client_name = 'create_csr1000v_lan_interface_ipv6'
        msa_option_params = {
            'ipv6_address': tenant_lan_ip_address,
            'prefix': tenant_lan_cidr,
            'hsrp_ipv6_address': tenant_lan_vip,
            'segment': tenant_lan_seg,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_nic,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        if len(fw_ip_v6_address) > 0:
            # Create Default Route IPv6(MSA)
            msa_client_name = 'create_csr1000v_default_route_ipv6'
            msa_option_params = {
                'nexthop_address': fw_ip_v6_address,
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name,
                msa_device_id,
                self.CSR1000V_VM_STATICROUTE_OBJECT_ID_V6,
                msa_option_params
            )
            tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP(MSA)
        msa_client_name = msa_object_name_hsrp + self.utils.IP_VER_V6
        msa_option_params = {
            'ipv6_address': tenant_lan_vip,
            'priority': hsrp_priority,
            'group_id': hsrp_group_id,
            'authkey': authkey,

        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_nic,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP Interface Tracking(MSA)
        msa_client_name = 'create_csr1000v_hsrp_interface_tracking'
        msa_wk = []

        # Self InterFace -> Self Interface
        self_nic_num = tenant_lan_nic.replace(
                            msa_config_for_device['nic_prefix'], '')

        interface = tenant_lan_nic
        track_interface = tenant_lan_nic
        hsrp_track_id = self.__get_hsrp_interface_tracking_track_id(
                                                self.utils.IP_VER_V6,
                                                str(self_nic_num),
                                                str(self_nic_num))
        msa_option_params = {
            'interface': interface,
            'group_id': hsrp_group_id,
            'track_interface': track_interface,
            'prioritycost': hsrp_track_prioritycost,
            'track_id': hsrp_track_id,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            interface + '_track_' + track_interface,
            msa_option_params
        )
        msa_wk.append(msa_res[msa.RES_KEY_IN])

        # Self InterFace -> Other Interface
        dc_member_list = self.__get_dc_member_list(dc_group_id, dc_id)

        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_id:

                ce1_info = json.loads(dc_member['ce1_info'])
                other_lan_nic = ce1_info['nic']

                if other_lan_nic != tenant_lan_nic:

                    other_nic_num = other_lan_nic.replace(
                                msa_config_for_device['nic_prefix'], '')

                    interface = tenant_lan_nic
                    track_interface = other_lan_nic
                    hsrp_track_id = \
                        self.__get_hsrp_interface_tracking_track_id(
                                                    self.utils.IP_VER_V6,
                                                    str(self_nic_num),
                                                    str(other_nic_num))
                    msa_option_params = {
                        'interface': interface,
                        'group_id': hsrp_group_id,
                        'track_interface': track_interface,
                        'prioritycost': hsrp_track_prioritycost,
                        'track_id': hsrp_track_id,
                    }
                    msa_res = self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        msa_client_name,
                        msa_device_id,
                        interface + '_track_' + track_interface,
                        msa_option_params
                    )
                    msa_wk.append(msa_res[msa.RES_KEY_IN])

        tenant_lan_port_msa_info[msa_client_name] = msa_wk

        # Set Output Parameters
        tenant_lan_port_wk = {'params': {}, 'keys': {}}
        tenant_lan_port_wk['params']['update_id'] = operation_id
        tenant_lan_port_wk['params']['node_id'] = node_id
        tenant_lan_port_wk['params']['nic'] = tenant_lan_nic
        tenant_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(tenant_lan_port_msa_info)
        tenant_lan_port_wk['keys'] = {'ID': port_list['rec_id']}

        wan_lan_port_wk = {'params': {}, 'keys': {}}
        wan_lan_port_wk['params']['update_id'] = operation_id
        wan_lan_port_wk['params']['ip_address_v6'] = wan_ip_address_v6
        wan_lan_port_wk['params']['netmask_v6'] = wan_prefix_v6
        wan_lan_port_wk['params']['port_info'] \
                                    = json.dumps(wan_port_info['port_info'])
        wan_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(wan_port_msa_info)
        wan_lan_port_wk['keys'] = {'ID': wan_port_rec_id}

        ce_info = {
            'MSA_device_id': msa_device_id,
            'host_name': node_name,
            'wan_ip_address': {},
            'lan_ip_address': port_list['ip_address'],
            'lan_netmask': port_list['netmask'],
            'loopback_ip_address': wan_allocation_info['loopback_ip'],
            'loopback_seg': wan_allocation_info['loopback_seg'],
            'loopback_netmask': wan_allocation_info['loopback_netmask'],
            'nic': tenant_lan_nic,
            'csr1000v': {
                'hsrp_track_prioritycost': hsrp_track_prioritycost,
                'hsrp_track_group_id': '',
            },
        }

        # Set JOB Output Parameters
        job_output = {
            'tenant_lan_port_wk': tenant_lan_port_wk,
            'wan_lan_port_wk': wan_lan_port_wk,
            'ce_info': ce_info,
        }

        return job_output

    def __device_setup_add_ipv6_csr1000v_for_tunnel(
                                            self, job_input, router_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        dc_group_id = job_input['group_id']
        fw_ip_v6_address = job_input['fw_ip_v6_address']

        node_id = job_input['apl_info'][router_name]['node_id']
        node_name = job_input['apl_info'][router_name]['node_name']
        msa_device_id = job_input['apl_info'][router_name]['MSA_device_id']

        port_list = job_input['tenant_port_info'][router_name]
        tenant_lan_nic = port_list['nic']
        tenant_lan_ip_address = port_list['ip_address']
        tenant_lan_cidr = port_list['netmask']
        tenant_lan_seg = port_list['subnet_ip_address']

        port_list_vrrp = job_input['tenant_port_info']['vrrp']
        tenant_lan_vip = port_list_vrrp['ip_address']

        tenant_lan_port_msa_info = {}

        # Get msa_info(WAN)
        for wan_lan in job_input['wan_lan_list']:
            if wan_lan['node_id'] == node_id:
                wan_port_rec_id = wan_lan['rec_id']
                wan_port_msa_info = json.loads(wan_lan['msa_info'])
                break

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Get WAN Config
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)
        hsrp_priority = \
            msa_config_for_device[router_name]['hsrp_priority']
        hsrp_track_prioritycost = \
            msa_config_for_device[router_name]['hsrp_track_prioritycost']

        msa_object_name_hsrp = self.CSR1000V_VARIABLE_CONFIG[
                                        'msa_object_name_hsrp'][router_name]

        hsrp_group_id = self.CSR1000V_VARIABLE_CONFIG[
                                        'hsrp_group_id'][self.utils.IP_VER_V6]

        bgp_local_preference = \
            msa_config_for_device[router_name]['bgp_local_preference']

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                                self.job_config,
                                                self.nal_endpoint_config,
                                                pod_id,
                                                dc_id)

        # Create BGP Basic IPv6(MSA)
        msa_client_name = 'create_csr1000v_bgp_basic_ipv6'
        msa_option_params = {
            'local_preference': bgp_local_preference,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        wan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create LAN Interface(MSA)
        msa_client_name = 'create_csr1000v_lan_interface_ipv6'
        msa_option_params = {
            'ipv6_address': tenant_lan_ip_address,
            'prefix': tenant_lan_cidr,
            'hsrp_ipv6_address': tenant_lan_vip,
            'segment': tenant_lan_seg,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_nic,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        if len(fw_ip_v6_address) > 0:
            # Create Default Route IPv6(MSA)
            msa_client_name = 'create_csr1000v_default_route_ipv6'
            msa_option_params = {
                'nexthop_address': fw_ip_v6_address,
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name,
                msa_device_id,
                self.CSR1000V_VM_STATICROUTE_OBJECT_ID_V6,
                msa_option_params
            )
            tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP(MSA)
        msa_client_name = msa_object_name_hsrp + self.utils.IP_VER_V6
        msa_option_params = {
            'ipv6_address': tenant_lan_vip,
            'priority': hsrp_priority,
            'group_id': hsrp_group_id,
            'authkey': authkey,

        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            tenant_lan_nic,
            msa_option_params
        )
        tenant_lan_port_msa_info[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create HSRP Interface Tracking(MSA)
        msa_client_name = 'create_csr1000v_hsrp_interface_tracking'
        msa_wk = []

        # Self InterFace -> Self Interface
        self_nic_num = tenant_lan_nic.replace(
                            msa_config_for_device['nic_prefix'], '')

        interface = tenant_lan_nic
        track_interface = tenant_lan_nic
        hsrp_track_id = self.__get_hsrp_interface_tracking_track_id(
                                                self.utils.IP_VER_V6,
                                                str(self_nic_num),
                                                str(self_nic_num))
        msa_option_params = {
            'interface': interface,
            'group_id': hsrp_group_id,
            'track_interface': track_interface,
            'prioritycost': hsrp_track_prioritycost,
            'track_id': hsrp_track_id,
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            interface + '_track_' + track_interface,
            msa_option_params
        )
        msa_wk.append(msa_res[msa.RES_KEY_IN])

        # Self InterFace -> Other Interface
        dc_member_list = self.__get_dc_member_list(dc_group_id, dc_id)

        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_id:

                ce1_info = json.loads(dc_member['ce1_info'])
                other_lan_nic = ce1_info['nic']

                if other_lan_nic != tenant_lan_nic:

                    other_nic_num = \
                        other_lan_nic.replace(
                                    msa_config_for_device['nic_prefix'], '')

                    interface = tenant_lan_nic
                    track_interface = other_lan_nic
                    hsrp_track_id = \
                        self.__get_hsrp_interface_tracking_track_id(
                                                    self.utils.IP_VER_V6,
                                                    str(self_nic_num),
                                                    str(other_nic_num))
                    msa_option_params = {
                        'interface': interface,
                        'group_id': hsrp_group_id,
                        'track_interface': track_interface,
                        'prioritycost': hsrp_track_prioritycost,
                        'track_id': hsrp_track_id,
                    }
                    msa_res = self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        msa_client_name,
                        msa_device_id,
                        interface + '_track_' + track_interface,
                        msa_option_params
                    )
                    msa_wk.append(msa_res[msa.RES_KEY_IN])

        tenant_lan_port_msa_info[msa_client_name] = msa_wk

        # Set Output Parameters
        tenant_lan_port_wk = {'params': {}, 'keys': {}}
        tenant_lan_port_wk['params']['update_id'] = operation_id
        tenant_lan_port_wk['params']['node_id'] = node_id
        tenant_lan_port_wk['params']['nic'] = tenant_lan_nic
        tenant_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(tenant_lan_port_msa_info)
        tenant_lan_port_wk['keys'] = {'ID': port_list['rec_id']}

        wan_lan_port_wk = {'params': {}, 'keys': {}}
        wan_lan_port_wk['params']['update_id'] = operation_id
        wan_lan_port_wk['params']['msa_info'] \
                                        = json.dumps(wan_port_msa_info)
        wan_lan_port_wk['keys'] = {'ID': wan_port_rec_id}

        ce_info = {
            'MSA_device_id': msa_device_id,
            'host_name': node_name,
            'wan_ip_address': {},
            'lan_ip_address': port_list['ip_address'],
            'lan_netmask': port_list['netmask'],
            'loopback_ip_address': wan_allocation_info['loopback_ip'],
            'loopback_seg': wan_allocation_info['loopback_seg'],
            'loopback_netmask': wan_allocation_info['loopback_netmask'],
            'nic': tenant_lan_nic,
            'csr1000v': {
                'hsrp_track_prioritycost': hsrp_track_prioritycost,
                'hsrp_track_group_id': '',
            },
        }

        # Set JOB Output Parameters
        job_output = {
            'tenant_lan_port_wk': tenant_lan_port_wk,
            'wan_lan_port_wk': wan_lan_port_wk,
            'ce_info': ce_info,
        }

        return job_output

    def get_new_nic_name(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        dc_member_list = job_input['dc_member_list']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type,
                                               device_type, dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        array_prot_number = []
        for dc_member in dc_member_list:

            if dc_member['dc_id'] != dc_id:
                continue

            ce1_info = json.loads(dc_member['ce1_info'])
            nic = ce1_info.get('nic')

            if isinstance(nic, str) and len(nic) > 0:
                nic = nic.replace(msa_config_for_device['nic_prefix'], '')
                array_prot_number.append(int(nic))

        if len(array_prot_number) == 0:
            number = msa_config_for_device['nic_for_first_lan']
        else:
            number = max(array_prot_number) + 1

        # Set JOB Output Parameters
        job_output = {
            'new_nic_name': msa_config_for_device['nic_prefix'] + str(number)
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __device_setup_add_ipv6_dc(self, job_input):

        rtname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rtname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        group_rec_id = job_input['group_rec_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        dc_member_list = job_input['dc_member_list']
        wan_allocation_info = job_input['wan_allocation_info']

        dc_self_ce1_msa_device_id = \
            job_input['apl_info'][rtname1]['MSA_device_id']
        dc_self_ce2_msa_device_id = \
            job_input['apl_info'][rtname2]['MSA_device_id']
        dc_self_ce1_host_name = job_input['apl_info'][rtname1]['node_name']
        dc_self_ce2_host_name = job_input['apl_info'][rtname2]['node_name']
        dc_self_ce1_wan_ip_address = \
            wan_allocation_info[rtname1]['wan'][self.utils.IP_VER_V6]['ip']
        dc_self_ce2_wan_ip_address = \
            wan_allocation_info[rtname2]['wan'][self.utils.IP_VER_V6]['ip']

        dc_self_id = dc_id

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_self_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_self_id)

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

            bgp_wan_interface = \
                            msa_config_for_device['nic_prefix'] \
                                + msa_config_for_device['nic_for_wan']

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_ce1_host_name = ce1_info['host_name']
            dc_other_ce1_wan_ip_address = ce1_info['wan_ip_address']

            dc_other_ce2_host_name = ce2_info['host_name']
            dc_other_ce2_wan_ip_address = ce2_info['wan_ip_address']

            if dc_member['dc_id'] not in dc_uniq_list:
                if dc_member['vrrp_address_v6'] != '':

                    dc_uniq_list.append(dc_member['dc_id'])

                    # Create BGP Peer IPv6(MSA)
                    msa_client_name = 'create_csr1000v_bgp_peer_ipv6'
                    msa_option_params = {
                        'authkey': authkey,
                        'interface': bgp_wan_interface,
                    }

                    # selfDC CE#1 - otherDC CE#1
                    msa_option_params['ipv6_address'] \
                        = dc_other_ce1_wan_ip_address[self.utils.IP_VER_V6]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_other_ce1_host_name,
                        msa_option_params
                    )
                    # selfDC CE#1 - otherDC CE#2
                    msa_option_params['ipv6_address'] \
                        = dc_other_ce2_wan_ip_address[self.utils.IP_VER_V6]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce1_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )
                    # selfDC CE#2 - otherDC CE#1
                    msa_option_params['ipv6_address'] \
                        = dc_other_ce1_wan_ip_address[self.utils.IP_VER_V6]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce1_host_name,
                        msa_option_params
                    )
                    # selfDC CE#2 - otherDC CE#2
                    msa_option_params['ipv6_address'] \
                        = dc_other_ce2_wan_ip_address[self.utils.IP_VER_V6]
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )

        # -----------------------------------------------------------------
        # Other DC Setting
        # -----------------------------------------------------------------
        dc_uniq_list = []
        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_self_id:
                continue

            dc_other_id = dc_member['dc_id']

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_ce1_msa_device_id = ce1_info['MSA_device_id']
            dc_other_ce2_msa_device_id = ce2_info['MSA_device_id']

            # Create Instance(MSA Soap Client)(DC_OTHER)
            msa_other = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                self.job_config,
                                self.nal_endpoint_config, pod_id, dc_other_id)

            if dc_member['dc_id'] not in dc_uniq_list:
                if dc_member['vrrp_address_v6'] != '':

                    dc_uniq_list.append(dc_member['dc_id'])

                    # Create BGP Peer IPv6(MSA)
                    msa_client_name = 'create_csr1000v_bgp_peer_ipv6'
                    msa_option_params = {
                        'authkey': authkey,
                        'interface': bgp_wan_interface,
                    }

                    # otherDC CE#1 - selfDC CE#1
                    msa_option_params['ipv6_address'] \
                        = dc_self_ce1_wan_ip_address
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_self_ce1_host_name,
                        msa_option_params
                    )
                    # otherDC CE#1 - selfDC CE#2
                    msa_option_params['ipv6_address'] \
                        = dc_self_ce2_wan_ip_address
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce1_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )
                    # otherDC CE#2 - selfDC CE#1
                    msa_option_params['ipv6_address'] \
                        = dc_self_ce1_wan_ip_address
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce1_host_name,
                        msa_option_params
                    )
                    # otherDC CE#2 - selfDC CE#2
                    msa_option_params['ipv6_address'] \
                        = dc_self_ce2_wan_ip_address
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )

    def __device_setup_add_ipv6_dc_for_tunnel(self, job_input):

        rtname1 = self.job_config.VM_ROUTER_NODE_NAME1
        rtname2 = self.job_config.VM_ROUTER_NODE_NAME2

        # Get JOB Input Parameters
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        group_rec_id = job_input['group_rec_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        dc_member_list = job_input['dc_member_list']
        wan_allocation_info_self = job_input['wan_allocation_info']

        dc_self_ce1_msa_device_id = \
            job_input['apl_info'][rtname1]['MSA_device_id']
        dc_self_ce2_msa_device_id = \
            job_input['apl_info'][rtname2]['MSA_device_id']
        dc_self_ce1_host_name = job_input['apl_info'][rtname1]['node_name']
        dc_self_ce2_host_name = job_input['apl_info'][rtname2]['node_name']

        # Auth Key
        authkey = 'T' + '{0:05d}'.format(group_rec_id)

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)
        prefix_tunnel = msa_config_for_device['nic_prefix_tunnel']

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                                self.job_config,
                                                self.nal_endpoint_config,
                                                pod_id,
                                                dc_id)

        dc_self_id = dc_id
        dc_self_list = self.__get_dc_info(dc_self_id)
        msa_self = msa

        dc_uniq_list = []
        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_self_id:
                continue

            dc_other_id = dc_member['dc_id']
            dc_other_list = self.__get_dc_info(dc_other_id)

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_ce1_host_name = ce1_info['host_name']
            dc_other_ce2_host_name = ce2_info['host_name']

            # SelfDC-OtherDC Tenant Setting(IPv6)
            dc_self1_other1_tenant_v6 \
                = wan_allocation_info_self[rtname1]['tenant'][
                        dc_other_id][rtname1][self.utils.IP_VER_V6]

            dc_self1_other2_tenant_v6 \
                = wan_allocation_info_self[rtname1]['tenant'][
                        dc_other_id][rtname2][self.utils.IP_VER_V6]

            dc_self2_other1_tenant_v6 \
                = wan_allocation_info_self[rtname2]['tenant'][
                        dc_other_id][rtname1][self.utils.IP_VER_V6]

            dc_self2_other2_tenant_v6 \
                = wan_allocation_info_self[rtname2]['tenant'][
                        dc_other_id][rtname2][self.utils.IP_VER_V6]

            wan_allocation_info_other \
                = self.get_wan_allocation_info_for_tunnel(dc_other_id)

            # SelfDC-OtherDC Tenant Peer Setting(IPv6)
            dc_peer_self1_other1_tenant_v6 \
                = wan_allocation_info_other[rtname1]['tenant'][
                        dc_self_id][rtname1][self.utils.IP_VER_V6]

            dc_peer_self1_other2_tenant_v6 \
                = wan_allocation_info_other[rtname2]['tenant'][
                        dc_self_id][rtname1][self.utils.IP_VER_V6]

            dc_peer_self2_other1_tenant_v6 \
                = wan_allocation_info_other[rtname1]['tenant'][
                        dc_self_id][rtname2][self.utils.IP_VER_V6]

            dc_peer_self2_other2_tenant_v6 \
                = wan_allocation_info_other[rtname2]['tenant'][
                        dc_self_id][rtname2][self.utils.IP_VER_V6]

            if dc_other_id not in dc_uniq_list:
                if dc_member['vrrp_address_v6'] != '':

                    dc_uniq_list.append(dc_other_id)

                    # Create Tunnel Interface Gre IPv4(MSA)
                    msa_client_name \
                        = 'create_csr1000v_tunnel_interface_gre_ipv6'

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
                    msa_option_params = {
                        'ipv6_address': dc_self1_other1_tenant_v6['ip'],
                        'prefix': dc_self1_other1_tenant_v6['netmask'],
                        'ipv6_segment': dc_self1_other1_tenant_v6['network'],
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
                    msa_option_params = {
                        'ipv6_address': dc_self1_other2_tenant_v6['ip'],
                        'prefix': dc_self1_other2_tenant_v6['netmask'],
                        'ipv6_segment': dc_self1_other2_tenant_v6['network'],
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
                    msa_option_params = {
                        'ipv6_address': dc_self2_other1_tenant_v6['ip'],
                        'prefix': dc_self2_other1_tenant_v6['netmask'],
                        'ipv6_segment': dc_self2_other1_tenant_v6['network'],
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
                    msa_option_params = {
                        'ipv6_address': dc_self2_other2_tenant_v6['ip'],
                        'prefix': dc_self2_other2_tenant_v6['netmask'],
                        'ipv6_segment': dc_self2_other2_tenant_v6['network'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_self_ce2_tunnel_interface_name + '2',
                        msa_option_params
                    )

                    # Create BGP Peer IPv6(MSA)
                    msa_client_name = 'create_csr1000v_bgp_peer_ipv6'

                    # selfDC CE#1 - otherDC CE#1
                    msa_option_params = {
                        'ipv6_address': dc_peer_self1_other1_tenant_v6['ip'],
                        'authkey': authkey,
                        'interface': dc_self_ce1_tunnel_interface_name + '1',
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
                        'ipv6_address': dc_peer_self1_other2_tenant_v6['ip'],
                        'authkey': authkey,
                        'interface': dc_self_ce1_tunnel_interface_name + '2',
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
                        'ipv6_address': dc_peer_self2_other1_tenant_v6['ip'],
                        'authkey': authkey,
                        'interface': dc_self_ce2_tunnel_interface_name + '1',
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
                        'ipv6_address': dc_peer_self2_other2_tenant_v6['ip'],
                        'authkey': authkey,
                        'interface': dc_self_ce2_tunnel_interface_name + '2',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_self,
                        msa_client_name,
                        dc_self_ce2_msa_device_id,
                        dc_other_ce2_host_name,
                        msa_option_params
                    )

        dc_uniq_list = []
        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_self_id:
                continue

            dc_other_id = dc_member['dc_id']
            dc_other_list = self.__get_dc_info(dc_other_id)

            ce1_info = json.loads(dc_member['ce1_info'])
            ce2_info = json.loads(dc_member['ce2_info'])

            dc_other_ce1_msa_device_id = ce1_info['MSA_device_id']
            dc_other_ce2_msa_device_id = ce2_info['MSA_device_id']

            wan_allocation_info_other \
                = self.get_wan_allocation_info_for_tunnel(dc_other_id)

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

            # Create Instance(MSA Soap Client)(DC_OTHER)
            msa_other = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                                self.job_config,
                                self.nal_endpoint_config, pod_id, dc_other_id)

            if dc_other_id not in dc_uniq_list:
                if dc_member['vrrp_address_v6'] != '':

                    dc_uniq_list.append(dc_other_id)

                    # Create Tunnel Interface Gre IPv4(MSA)
                    msa_client_name \
                        = 'create_csr1000v_tunnel_interface_gre_ipv6'

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
                    msa_option_params = {
                        'ipv6_address': dc_other1_self1_tenant_v6['ip'],
                        'prefix': dc_other1_self1_tenant_v6['netmask'],
                        'ipv6_segment': dc_other1_self1_tenant_v6['network'],
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
                    msa_option_params = {
                        'ipv6_address': dc_other1_self2_tenant_v6['ip'],
                        'prefix': dc_other1_self2_tenant_v6['netmask'],
                        'ipv6_segment': dc_other1_self2_tenant_v6['network'],
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
                    msa_option_params = {
                        'ipv6_address': dc_other2_self1_tenant_v6['ip'],
                        'prefix': dc_other2_self1_tenant_v6['netmask'],
                        'ipv6_segment': dc_other2_self1_tenant_v6['network'],
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
                    msa_option_params = {
                        'ipv6_address': dc_other2_self2_tenant_v6['ip'],
                        'prefix': dc_other2_self2_tenant_v6['netmask'],
                        'ipv6_segment': dc_other2_self2_tenant_v6['network'],
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_other_ce2_tunnel_interface_name + '2',
                        msa_option_params
                    )

                    # Create BGP Peer IPv6(MSA)
                    msa_client_name = 'create_csr1000v_bgp_peer_ipv6'

                    # otherDC CE#1 - selfDC CE#1
                    msa_option_params = {
                        'ipv6_address': dc_peer_other1_self1_tenant_v6['ip'],
                        'authkey': authkey,
                        'interface': dc_other_ce1_tunnel_interface_name + '1',
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
                        'ipv6_address': dc_peer_other1_self2_tenant_v6['ip'],
                        'authkey': authkey,
                        'interface': dc_other_ce1_tunnel_interface_name + '2',
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
                        'ipv6_address': dc_peer_other2_self1_tenant_v6['ip'],
                        'authkey': authkey,
                        'interface': dc_other_ce2_tunnel_interface_name + '1',
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
                        'ipv6_address': dc_peer_other2_self2_tenant_v6['ip'],
                        'authkey': authkey,
                        'interface': dc_other_ce2_tunnel_interface_name + '2',
                    }
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa_other,
                        msa_client_name,
                        dc_other_ce2_msa_device_id,
                        dc_self_ce2_host_name,
                        msa_option_params
                    )

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

    def __create_msa_license_csr1000v(self, job_input, router_name):

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        bandwidth = job_input['bandwidth']

        apl_wk = job_input['apl_wk'][router_name]
        msa_device_id = apl_wk['MSA_device_id']
        node_name = apl_wk['node_name']
        node_detail = json.loads(apl_wk['node_detail'])

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        # Create License(MSA)
        msa_client_name = 'create_csr1000v_license'
        msa_option_params = {
            'idtoken': msa_config_for_device['license_key'],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Create Throughput(MSA)
        msa_client_name = 'create_csr1000v_throughput'
        msa_option_params = {
            'throughput': msa_config_for_device['throughput'][bandwidth],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Set Output Parameters
        apl_wk['node_detail'] = json.dumps(node_detail)

        # Set JOB Output Parameters
        job_output = {
            'apl_wk': apl_wk,
        }

        return job_output

    def __delete_msa_license_csr1000v(self, job_input, router_name):

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_wk = job_input['apl_info'][router_name]
        msa_device_id = apl_wk['MSA_device_id']
        node_name = apl_wk['node_name']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        try:
            # Delete License(MSA)
            msa.delete_csr1000v_license(
                msa_device_id,
                node_name)
            # Wait
            time.sleep(self.job_config.OS_SERVER_WAIT_TIME_CSR_LICENSE)
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

    def __update_msa_throughput_csr1000v(self, job_input, router_name):

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        bandwidth = job_input['bandwidth']

        apl_wk = job_input['apl_info'][router_name]
        msa_device_id = apl_wk['MSA_device_id']
        node_name = apl_wk['node_name']
        node_detail = json.loads(apl_wk['node_detail'])

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        # Delete Throughput(MSA)
        self.execute_msa_command(
            msa_config_for_device,
            msa,
            'delete_csr1000v_throughput',
            msa_device_id,
            node_name,
        )

        # Create Throughput(MSA)
        msa_client_name = 'create_csr1000v_throughput'
        msa_option_params = {
            'throughput': msa_config_for_device['throughput'][bandwidth],
        }
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            msa_client_name,
            msa_device_id,
            node_name,
            msa_option_params
        )
        node_detail[msa_client_name] = msa_res[msa.RES_KEY_IN]

        # Set Output Parameters
        apl_wk['node_detail'] = json.dumps(node_detail)

        # Set JOB Output Parameters
        job_output = {
            'apl_wk': apl_wk,
        }

        return job_output

    def __update_db_dc_member_bandwidth(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        bandwidth = job_input['bandwidth']
        dc_member_list = job_input['dc_member_list']

        # Get Endpoint(DB Client)
        db_endpoint_dc_member = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_MEMBER)

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)

        for dc_member in dc_member_list:

            if dc_member['dc_id'] == dc_id and dc_member['pod_id'] == pod_id \
                and dc_member['tenant_id'] == nal_tenant_id:

                # Update WIM_DC_CONNECT_MEMBER_MNG(DB Client)
                keys = [dc_member['ID']]
                params = {}
                params['update_id'] = operation_id
                params['bandwidth'] = bandwidth
                db_update_instance.set_context(
                                        db_endpoint_dc_member, keys, params)
                db_update_instance.execute()

    def __update_msa_setting_csr1000v(self, job_input, router_name):

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        dns_server_ip_address = job_input.get('dns_server_ip_address', '')

        ntp_server_ip_address = job_input.get('ntp_server_ip_address', '')
        ntp_server_interface = job_input.get('ntp_server_interface', '')

        snmp_server_ip_address = job_input.get('snmp_server_ip_address', '')
        snmp_server_interface = job_input.get('snmp_server_interface', '')

        syslog_server_ip_address \
                            = job_input.get('syslog_server_ip_address', '')
        syslog_server_interface = job_input.get('syslog_server_interface', '')

        snmp_server_delete_flg = job_input['snmp_server_delete_flg']
        syslog_server_delete_flg = job_input['syslog_server_delete_flg']

        apl_wk = job_input['apl_info'][router_name]
        msa_device_id = apl_wk['MSA_device_id']
        node_name = apl_wk['node_name']
        node_detail = json.loads(apl_wk['node_detail'])
        apl_dns_server_ip_address = apl_wk['old_dns_server_ip_address']
        apl_ntp_server_ip_address = apl_wk['old_ntp_server_ip_address']
        apl_snmp_server_ip_address = apl_wk['old_snmp_server_ip_address']
        apl_syslog_server_ip_address = apl_wk['old_syslog_server_ip_address']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Create Instance(MSA Soap Client)
        msa = ciscocsrstdiosxeordercmdws.CsrStdIosXeOrderCommandWs(
                    self.job_config, self.nal_endpoint_config, pod_id, dc_id)

        # Update DNS(MSA)
        if len(dns_server_ip_address) == 0:
            pass
        else:

            if len(apl_dns_server_ip_address) > 0:

                # Delete DNS(MSA)
                ip_version_old = self.utils.get_ipaddress_version(
                                            apl_dns_server_ip_address)

                msa_client_name_create_old = 'create_csr1000v_dns_ipv' + \
                                                            ip_version_old

                msa_client_name_delete = 'delete_csr1000v_dns_ipv' + \
                                                            ip_version_old

                msa_option_params = {
                    'ip_address': apl_dns_server_ip_address,
                    'ipv6_address': apl_dns_server_ip_address,
                }
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    msa_client_name_delete,
                    msa_device_id,
                    node_name,
                    msa_option_params
                )
                del node_detail[msa_client_name_create_old]

            # Create DNS(MSA)
            dns_server_ip_address = self.utils.get_ipaddress_compressed(
                                                    dns_server_ip_address)
            msa_client_name_create = 'create_csr1000v_dns_ipv' + \
                    self.utils.get_ipaddress_version(dns_server_ip_address)

            msa_option_params = {
                'ip_address': dns_server_ip_address,
                'ipv6_address': dns_server_ip_address,
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name_create,
                msa_device_id,
                node_name,
                msa_option_params
            )
            node_detail[msa_client_name_create] = msa_res[msa.RES_KEY_IN]
            apl_wk['dns_server_ip_address'] = dns_server_ip_address

        # Update NTP(MSA)
        if len(ntp_server_ip_address) == 0 or len(ntp_server_interface) == 0:
            pass
        else:

            if len(apl_ntp_server_ip_address) > 0:

                # Delete DNS(MSA)
                ip_version_old = self.utils.get_ipaddress_version(
                                            apl_ntp_server_ip_address)

                msa_client_name_create_old = 'create_csr1000v_ntp_ipv' + \
                                                            ip_version_old

                apl_msa_input_params = self.get_apl_msa_input_params(
                                    apl_wk['node_detail'],
                                    msa_client_name_create_old,
                                    msa.OBJECT_FILE_NAME[
                                                msa_client_name_create_old])

                msa_client_name_delete = 'delete_csr1000v_ntp_ipv' + \
                                                            ip_version_old

                msa_option_params = {
                    'interface': apl_msa_input_params['interface'],
                    'ip_address': apl_ntp_server_ip_address,
                    'ipv6_address': apl_ntp_server_ip_address,
                }
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    msa_client_name_delete,
                    msa_device_id,
                    node_name,
                    msa_option_params
                )
                del node_detail[msa_client_name_create_old]

            # Create NTP(MSA)
            ntp_server_ip_address = self.utils.get_ipaddress_compressed(
                                                    ntp_server_ip_address)
            msa_client_name_create = 'create_csr1000v_ntp_ipv' + \
                    self.utils.get_ipaddress_version(ntp_server_ip_address)

            msa_option_params = {
                'interface': ntp_server_interface,
                'ip_address': ntp_server_ip_address,
                'ipv6_address': ntp_server_ip_address,
            }
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                msa_client_name_create,
                msa_device_id,
                node_name,
                msa_option_params
            )
            node_detail[msa_client_name_create] = msa_res[msa.RES_KEY_IN]
            apl_wk['ntp_server_ip_address'] = ntp_server_ip_address

        # Update SNMP(MSA)
        if len(apl_snmp_server_ip_address) > 0:
            ip_version_old = self.utils.get_ipaddress_version(
                                                apl_snmp_server_ip_address)

            msa_client_name_create_snmp_old = 'create_csr1000v_snmp_ipv' \
                                                            + ip_version_old

            msa_client_name_delete_snmp = 'delete_csr1000v_snmp_ipv' \
                                                            + ip_version_old

            apl_msa_input_params = self.get_apl_msa_input_params(
                                    apl_wk['node_detail'],
                                    msa_client_name_create_snmp_old,
                                    msa.OBJECT_FILE_NAME[
                                            msa_client_name_create_snmp_old])

            msa_option_params_delete_snmp = {
                'community_name': apl_msa_input_params['community_name'],
                'version': apl_msa_input_params['version'],
                'ip_address': apl_snmp_server_ip_address,
                'ipv6_address': apl_snmp_server_ip_address,
            }

        if str(snmp_server_delete_flg) == '1':

            if len(apl_snmp_server_ip_address) > 0:

                # Delete SNMP(MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    msa_client_name_delete_snmp,
                    msa_device_id,
                    node_name,
                    msa_option_params_delete_snmp
                )
                del node_detail[msa_client_name_create_snmp_old]
                apl_wk['snmp_server_ip_address'] = ''

        else:
            if len(snmp_server_ip_address) == 0 or \
                    len(snmp_server_interface) == 0:
                pass
            else:
                if len(apl_snmp_server_ip_address) > 0:

                    # Delete SNMP(MSA)
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        msa_client_name_delete_snmp,
                        msa_device_id,
                        node_name,
                        msa_option_params_delete_snmp
                    )
                    del node_detail[msa_client_name_create_snmp_old]

                # Create SNMP(MSA)
                snmp_server_ip_address \
                = self.utils.get_ipaddress_compressed(snmp_server_ip_address)

                msa_client_name_create = 'create_csr1000v_snmp_ipv' + \
                    self.utils.get_ipaddress_version(snmp_server_ip_address)

                msa_option_params = {
                    'community_name': msa_config_for_device[
                                                    'snmp_community_name'],
                    'version': msa_config_for_device['snmp_trap_version'],
                    'interface': snmp_server_interface,
                    'ip_address': snmp_server_ip_address,
                    'ipv6_address': snmp_server_ip_address,
                }
                msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    msa_client_name_create,
                    msa_device_id,
                    node_name,
                    msa_option_params
                )
                node_detail[msa_client_name_create] = msa_res[msa.RES_KEY_IN]
                apl_wk['snmp_server_ip_address'] = snmp_server_ip_address

        # Update Syslog(MSA)
        if len(apl_syslog_server_ip_address) > 0:

            ip_version_old = self.utils.get_ipaddress_version(
                                                apl_syslog_server_ip_address)

            msa_client_name_delete_syslog = 'delete_csr1000v_syslog_ipv' \
                                                            + ip_version_old

            msa_client_name_create_syslog_old = 'create_csr1000v_syslog_ipv' \
                                                            + ip_version_old

            msa_option_params_delete_syslog = {
                'ip_address': apl_syslog_server_ip_address,
                'ipv6_address': apl_syslog_server_ip_address,
            }

        if str(syslog_server_delete_flg) == '1':

            if len(apl_syslog_server_ip_address) > 0:

                # Delete Syslog(MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    msa_client_name_delete_syslog,
                    msa_device_id,
                    node_name,
                    msa_option_params_delete_syslog
                )
                del node_detail[msa_client_name_create_syslog_old]
                apl_wk['syslog_server_ip_address'] = ''

        else:
            if len(syslog_server_ip_address) == 0 or \
                    len(syslog_server_interface) == 0:
                pass
            else:

                if len(apl_syslog_server_ip_address) > 0:

                    # Delete Syslog(MSA)
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        msa_client_name_delete_syslog,
                        msa_device_id,
                        node_name,
                        msa_option_params_delete_syslog
                    )
                    del node_detail[msa_client_name_create_syslog_old]

                # Create Syslog(MSA)
                syslog_server_ip_address \
                                = self.utils.get_ipaddress_compressed(
                                                syslog_server_ip_address)

                msa_client_name_create = 'create_csr1000v_syslog_ipv' + \
                                        self.utils.get_ipaddress_version(
                                                syslog_server_ip_address)

                msa_option_params = {
                    'facility': msa_config_for_device['syslog_facility'],
                    'severity': msa_config_for_device['syslog_severity'],
                    'interface': syslog_server_interface,
                    'ip_address': syslog_server_ip_address,
                    'ipv6_address': syslog_server_ip_address,
                }
                msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    msa_client_name_create,
                    msa_device_id,
                    node_name,
                    msa_option_params
                )
                node_detail[msa_client_name_create] = msa_res[msa.RES_KEY_IN]
                apl_wk['syslog_server_ip_address'] = syslog_server_ip_address

        # Set Output Parameters
        apl_wk['node_detail'] = json.dumps(node_detail)

        # Set JOB Output Parameters
        job_output = {
            'apl_wk': apl_wk,
        }

        return job_output

    def __get_hsrp_interface_tracking_track_id(self,
                        ip_version, interface_number, track_interface_number):

            return int(
                self.CSR1000V_VARIABLE_CONFIG[
                    'hsrp_track_id_prefix'][ip_version] \
                + interface_number \
                + track_interface_number
            )
