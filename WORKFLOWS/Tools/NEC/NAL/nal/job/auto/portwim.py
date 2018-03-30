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
from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import ports
from job.lib.openstack.quantum import subnets
from job.lib.soap.msa import msaordercmdws


class PortWim(base.JobAutoBase):

    def virtual_msa_lan_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']

        # Get msa network info
        assign_network_info = self.__get_msa_network_info(tenant_name, pod_id)
        if len(assign_network_info) == 0:
            assign_network_info = self.__assign_msa_network(tenant_name,
                                                            pod_id,
                                                            nal_tenant_id,
                                                            operation_id,
                                                            job_input)
        msa_network_info = assign_network_info[0]

        # Set JOB Output Parameters
        job_output['msa_network_info'] = msa_network_info

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def port_create_wim(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create Port
        ret1 = self.__msa_port_create_wim(job_input,
                                          self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__msa_port_create_wim(job_input,
                                          self.job_config.VM_ROUTER_NODE_NAME2)

        # Set JOB Output Parameters
        job_output = {}
        job_output['msa_wan_port_info'] = {}
        job_output['msa_wan_port_info'][
                            self.job_config.VM_ROUTER_NODE_NAME1] = ret1
        job_output['msa_wan_port_info'][
                            self.job_config.VM_ROUTER_NODE_NAME2] = ret2

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_port_create_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create Port
        ret1 = self.__msa_port_create_wim_csr1000v(job_input,
                                          self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__msa_port_create_wim_csr1000v(job_input,
                                          self.job_config.VM_ROUTER_NODE_NAME2)

        # Set JOB Output Parameters
        job_output = {}
        job_output['msa_wan_port_info'] = {}
        job_output['msa_wan_port_info'][
                            self.job_config.VM_ROUTER_NODE_NAME1] = ret1
        job_output['msa_wan_port_info'][
                            self.job_config.VM_ROUTER_NODE_NAME2] = ret2

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_port_create_csr1000v_for_tunnel(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get DC Segment
        dc_segment = self._get_dc_segment(
                                    job_input['dc_id'], job_input['group_id'])

        # Create Port
        ret1 = self.__msa_port_create_wim_csr1000v_for_tunnel(job_input,
                                        dc_segment,
                                        self.job_config.VM_ROUTER_NODE_NAME1)

        ret2 = self.__msa_port_create_wim_csr1000v_for_tunnel(job_input,
                                        dc_segment,
                                        self.job_config.VM_ROUTER_NODE_NAME2)

        # Set JOB Output Parameters
        job_output = {}
        job_output['msa_wan_port_info'] = {}
        job_output['msa_wan_port_info'][
                            self.job_config.VM_ROUTER_NODE_NAME1] = ret1
        job_output['msa_wan_port_info'][
                            self.job_config.VM_ROUTER_NODE_NAME2] = ret2

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_port_create_add_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Update Port(Add IPv6 Address)
        ret1 = self.__wan_port_add_ipv6_wim(job_input,
                                          self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__wan_port_add_ipv6_wim(job_input,
                                          self.job_config.VM_ROUTER_NODE_NAME2)

        # Set JOB Output Parameters
        job_output = {}
        job_output['wan_port_info'] = {}
        job_output['wan_port_info'][
                            self.job_config.VM_ROUTER_NODE_NAME1] = ret1
        job_output['wan_port_info'][
                            self.job_config.VM_ROUTER_NODE_NAME2] = ret2

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __msa_port_create_wim(self, job_input, router_name):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        msa_network_info = job_input['msa_network_info']
        nal_tenant_id = job_input['nal_tenant_id']
        wan_network_id = job_input['wan_network_id']

        # Get Allocation Info(WAN)
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_subnets = subnets.OscQuantumSubnets(self.job_config)
        osc_ports = ports.OscQuantumPorts(self.job_config)

        # Create Port(OpenStack:VIM)(MSA)
        port_res_msa = osc_ports.create_port(os_endpoint_vim,
                                            msa_network_info['network_id'],
                                            '',
                                            True,
                                            msa_network_info['subnet_id'])

        msa_port_id = port_res_msa['port']['id']
        msa_ip_address = port_res_msa['port']['fixed_ips'][0]['ip_address']
        msa_port_info = port_res_msa

        wan_ip_ver = self.utils.IP_VER_V4
        wan_subnet_id = ''
        wan_cidr = wan_allocation_info['wan'][wan_ip_ver]['subnet_ip'] \
                + '/' + str(wan_allocation_info['wan'][wan_ip_ver]['netmask'])

        subnet_exists_flg = False

        # List Subnets(OpenStack:VIM)
        subnet_list = osc_subnets.list_subnets(os_endpoint_vim)

        for rec in subnet_list['subnets']:
            if rec['network_id'] == wan_network_id \
                            and rec['cidr'] == wan_cidr:
                subnet_exists_flg = True
                wan_subnet_id = rec['id']
                break

        if subnet_exists_flg == False:

            # Create Subnet(OpenStack:VIM)(WAN)
            subnet_res_wan = osc_subnets.create_subnet(os_endpoint_vim,
                                            wan_network_id,
                                            wan_cidr,
                                            '',
                                            nal_tenant_id)
            wan_subnet_id = subnet_res_wan['subnet']['id']

        # Create Port(OpenStack:VIM)(WAN)
        port_res_wan = osc_ports.create_port(os_endpoint_vim,
                                            wan_network_id,
                                            '',
                                            True,
                                            wan_subnet_id,
                                wan_allocation_info['wan'][wan_ip_ver]['ip'])

        wan_port_id = port_res_wan['port']['id']
        wan_ip_address = port_res_wan['port']['fixed_ips'][0]['ip_address']
        wan_port_info = port_res_wan

        # Set JOB Output Parameters
        job_output = {
            'msa_netmask': msa_network_info['netmask'],
            'msa_port_id': msa_port_id,
            'msa_ip_address': msa_ip_address,
            'msa_port_info': msa_port_info,
            'wan_subnet_id': wan_subnet_id,
            'wan_port_id': wan_port_id,
            'wan_ip_address': wan_ip_address,
            'wan_port_info': wan_port_info,
            'wan_info': {
                self.utils.IP_VER_V4: {
                    'ip': wan_allocation_info[
                                        'wan'][self.utils.IP_VER_V4]['ip'],
                    'netmask': wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V4]['netmask'],
                },
            }
        }

        return job_output

    def __msa_port_create_wim_csr1000v(self, job_input, router_name):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        msa_network_info = job_input['msa_network_info']
        nal_tenant_id = job_input['nal_tenant_id']
        wan_network_id = job_input['wan_network_id']

        # Get Allocation Info(WAN)
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_subnets = subnets.OscQuantumSubnets(self.job_config)
        osc_ports = ports.OscQuantumPorts(self.job_config)

        # Create Port(OpenStack:VIM)(MSA)
        port_res_msa = osc_ports.create_port(os_endpoint_vim,
                                            msa_network_info['network_id'],
                                            '',
                                            True,
                                            msa_network_info['subnet_id'])

        msa_port_id = port_res_msa['port']['id']
        msa_ip_address = port_res_msa['port']['fixed_ips'][0]['ip_address']
        msa_port_info = port_res_msa

        fixed_ips = []
        for ip_ver in [self.utils.IP_VER_V4]:

            wan_cidr = wan_allocation_info['wan'][ip_ver]['subnet_ip'] \
                    + '/' + str(wan_allocation_info['wan'][ip_ver]['netmask'])

            wan_subnet_id = ''
            subnet_exists_flg = False

            # List Subnets(OpenStack:VIM)
            subnet_list = osc_subnets.list_subnets(os_endpoint_vim)

            for rec in subnet_list['subnets']:

                vim_cidr = self.utils.get_cidr_compressed(rec['cidr'])

                if rec['network_id'] == wan_network_id \
                                and vim_cidr['cidr'] == wan_cidr:
                    subnet_exists_flg = True
                    wan_subnet_id = rec['id']
                    break

            if subnet_exists_flg == False:

                # Create Subnet(OpenStack:VIM)(WAN)
                subnet_res_wan = osc_subnets.create_subnet(os_endpoint_vim,
                                                wan_network_id,
                                                wan_cidr,
                                                '',
                                                nal_tenant_id,
                                                ip_ver)
                wan_subnet_id = subnet_res_wan['subnet']['id']

            fixed_ips.append(
                {
                    'subnet_id': wan_subnet_id,
                    'ip_address': wan_allocation_info['wan'][ip_ver]['ip'],
                }
            )

        # Create Port(OpenStack:VIM)(WAN)
        port_res_wan = osc_ports.create_port_dual_stack(os_endpoint_vim,
                                            wan_network_id,
                                            '',
                                            True,
                                            fixed_ips)

        # Set JOB Output Parameters
        job_output = {
            'msa_netmask': msa_network_info['netmask'],
            'msa_port_id': msa_port_id,
            'msa_ip_address': msa_ip_address,
            'msa_port_info': msa_port_info,
            'wan_port_id': port_res_wan['port']['id'],
            'wan_port_info': port_res_wan,
            'wan_info': {
                self.utils.IP_VER_V4: {
                    'ip': wan_allocation_info[
                                        'wan'][self.utils.IP_VER_V4]['ip'],
                    'netmask': wan_allocation_info[
                                    'wan'][self.utils.IP_VER_V4]['netmask'],
                },
            }
        }

        return job_output

    def __msa_port_create_wim_csr1000v_for_tunnel(
                                self, job_input, dc_segment, router_name):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        msa_network_info = job_input['msa_network_info']
        nal_tenant_id = job_input['nal_tenant_id']
        wan_network_id = job_input['wan_network_id']

        # Get DC Segment Info
        dc_segment_ip_address = dc_segment[router_name + '_ip_address']
        dc_segment_netmask = dc_segment['netmask']

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_ports = ports.OscQuantumPorts(self.job_config)

        # Create Port(OpenStack:VIM)(MSA)
        port_res_msa = osc_ports.create_port(os_endpoint_vim,
                                            msa_network_info['network_id'],
                                            '',
                                            True,
                                            msa_network_info['subnet_id'])

        msa_port_id = port_res_msa['port']['id']
        msa_ip_address = port_res_msa['port']['fixed_ips'][0]['ip_address']
        msa_port_info = port_res_msa

        # Get Network Info(IDC)
        idc_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_IDC,
                                            '',
                                            dc_id)

        # Create Port(OpenStack:VIM)(WAN)
        port_res_wan = osc_ports.create_port(os_endpoint_vim,
                                             wan_network_id,
                                             '',
                                             True,
                                             idc_network_info['subnet_id'],
                                             dc_segment_ip_address)

        # Set JOB Output Parameters
        job_output = {
            'msa_netmask': msa_network_info['netmask'],
            'msa_port_id': msa_port_id,
            'msa_ip_address': msa_ip_address,
            'msa_port_info': msa_port_info,
            'wan_port_id': port_res_wan['port']['id'],
            'wan_port_info': port_res_wan,
            'wan_info': {
                self.utils.IP_VER_V4: {
                    'ip': dc_segment_ip_address,
                    'netmask': dc_segment_netmask,
                },
            }
        }

        return job_output

    def __wan_port_add_ipv6_wim(self, job_input, router_name):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['apl_info'][router_name]['node_id']
        wan_lan_list = job_input['wan_lan_list']

        # Get Allocation Info(WAN)
        wan_allocation_info = job_input['wan_allocation_info'][router_name]

        # Get port_id(WAN)
        for wan_lan in wan_lan_list:
            if wan_lan['node_id'] == node_id:
                wan_network_id = wan_lan['network_id']
                wan_port_id = wan_lan['port_id']
                break

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_subnets = subnets.OscQuantumSubnets(self.job_config)
        osc_ports = ports.OscQuantumPorts(self.job_config)

        wan_ip = wan_allocation_info['wan'][self.utils.IP_VER_V6]['ip']
        wan_ip_subnet = wan_allocation_info['wan'][self.utils.IP_VER_V6][
                                                                'subnet_ip']
        wan_netmask = wan_allocation_info['wan'][self.utils.IP_VER_V6][
                                                                'netmask']
        wan_cidr = wan_ip_subnet + '/' + str(wan_netmask)

        wan_subnet_id = ''
        subnet_exists_flg = False

        # List Subnets(OpenStack:VIM)
        subnet_list = osc_subnets.list_subnets(os_endpoint_vim)

        for rec in subnet_list['subnets']:

            vim_cidr = self.utils.get_cidr_compressed(rec['cidr'])

            if rec['network_id'] == wan_network_id \
                            and vim_cidr['cidr'] == wan_cidr:
                subnet_exists_flg = True
                wan_subnet_id = rec['id']
                break

        if subnet_exists_flg == False:

            # Create Subnet(OpenStack:VIM)(WAN)
            subnet_res_wan = osc_subnets.create_subnet(os_endpoint_vim,
                                            wan_network_id,
                                            wan_cidr,
                                            '',
                                            nal_tenant_id,
                                            self.utils.IP_VER_V6)
            wan_subnet_id = subnet_res_wan['subnet']['id']

        # Get Port(OpenStack:VIM)
        os_port_res = osc_ports.get_port(os_endpoint_vim, wan_port_id)

        fixed_ips_update = os_port_res['port']['fixed_ips']
        fixed_ips_update.append(
                    {'subnet_id': wan_subnet_id, 'ip_address': wan_ip})

        # Update Port(OpenStack:VIM)
        os_port_upd = osc_ports.update_port(os_endpoint_vim,
                                                    wan_port_id,
                                                    None,
                                                    None,
                                                    fixed_ips_update)

        # Set JOB Output Parameters
        job_output = {
            'port_info': os_port_upd,
        }

        return job_output

    def msa_port_delete_wim(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        msa_port_id1 = job_input['apl_info'][
                        self.job_config.VM_ROUTER_NODE_NAME1]['msa_port_id']
        msa_port_id2 = job_input['apl_info'][
                        self.job_config.VM_ROUTER_NODE_NAME2]['msa_port_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        logical_delete_apl_port_list \
                = job_input['logical_delete_apl_port_list']

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_ports = ports.OscQuantumPorts(self.job_config)

        # Delete Port(OpenStack Client)(MSA)
        try:
            osc_ports.delete_port(os_endpoint_vim, msa_port_id1)
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            osc_ports.delete_port(os_endpoint_vim, msa_port_id2)
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Set Delete Info
        logical_delete_apl_port_list.append(
            {
                'search': {
                    'delete_flg': 0,
                    'tenant_id': nal_tenant_id,
                    'apl_type': self.job_config.APL_TYPE_VR,
                    'port_id': msa_port_id1,
                },
                'params': {
                    'update_id': operation_id,
                    'delete_flg': 1,
                },
            }
        )
        logical_delete_apl_port_list.append(
            {
                'search': {
                    'delete_flg': 0,
                    'tenant_id': nal_tenant_id,
                    'apl_type': self.job_config.APL_TYPE_VR,
                    'port_id': msa_port_id2,
                },
                'params': {
                    'update_id': operation_id,
                    'delete_flg': 1,
                },
            }
        )

        # Output Log(Job Output)
        job_output = {
            'logical_delete_apl_port_list': logical_delete_apl_port_list
        }
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __get_msa_network_info(self, tenant_name, pod_id):

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = self.get_db_endpoint(
                                    self.job_config.REST_URI_MSA_VLAN)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_MSA_VLAN_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['pod_id'] = pod_id
        params['tenant_name'] = tenant_name
        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        msa_network_info = db_list.get_return_param()

        return msa_network_info

    def __assign_msa_network(self, tenant_name, pod_id,
                             nal_tenant_id, operation_id, job_input):

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = self.get_db_endpoint(
                                    self.job_config.REST_URI_MSA_VLAN)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id, '', nal_tenant_id)

        IaaS_tenant_id = job_input['IaaS_tenant_id']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Create Instance(OpenStack Client)
        osc_networks = networks.OscQuantumNetworks(self.job_config)
        os_subnets_instance = subnets.OscQuantumSubnets(self.job_config)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_MSA_VLAN_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['status'] = 0
        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        msa_vlan_list = db_list.get_return_param()

        msa_network_info = {}
        if len(msa_vlan_list) != 0:

            rec = msa_vlan_list[0]

            # Update NAL_MSA_VLAN_MNG(DB Client)
            keys = [rec['ID']]
            params = {}
            params['update_id'] = operation_id
            params['pod_id'] = pod_id
            params['tenant_name'] = tenant_name
            params['status'] = 1
            params['tenant_id'] = nal_tenant_id
            db_update.set_context(db_endpoint_msa_vlan, keys, params)
            db_update.execute()

            cidr = rec['network_address'] + '/' + rec['netmask']

            if vim_iaas_with_flg == 0:
                # Create Network(OpenStack:VIM)
                network_name = 'MSA_for_' + nal_tenant_id
                physical_network_name = None
            else:
                # Create Network(OpenStack:VIM)
                network_name = 'MSA_for_' + IaaS_tenant_id
                physical_network_name = self.get_os_physical_network_name()

            os_cre_network_vim = osc_networks.create_network(
                                                    os_endpoint_vim,
                                                    network_name,
                                                    True,
                                                    False,
                                                    rec['vlan_id'],
                                                    physical_network_name)
            network_info = os_cre_network_vim['network']
            network_id = network_info['id']

            # Get Network Data(id)
            os_cre_subnet_vim = os_subnets_instance.create_subnet(
                                                    os_endpoint_vim,
                                                    network_id,
                                                    cidr,
                                                    '',
                                                    nal_tenant_id)
            subnet_info = os_cre_subnet_vim['subnet']
            subnet_id = subnet_info['id']

            # Create Port(OpenStack:VIM)
            os_cre_port_vim = os_ports_instance.create_port(os_endpoint_vim,
                                                            network_id)

            # Get Port Info
            port_info = os_cre_port_vim['port']
            port_id = port_info['id']
            ip_address = port_info['fixed_ips'][0]['ip_address']

            # MSA setup
            self.__setup_msa_network_vlan(pod_id,
                                          rec['vlan_id'],
                                          ip_address,
                                          rec['netmask'])

            # Update NAL_MSA_VLAN_MNG(DB Client)
            keys = [rec['ID']]
            params = {}
            params['update_id'] = operation_id
            params['msa_ip_address'] = ip_address
            params['network_id'] = network_id
            params['subnet_id'] = subnet_id
            params['port_id'] = port_id
            params['network_info'] = json.dumps(network_info)
            params['subnet_info'] = json.dumps(subnet_info)
            params['port_info'] = json.dumps(port_info)
            db_update.set_context(db_endpoint_msa_vlan, keys, params)
            db_update.execute()

            # List NAL_MSA_VLAN_MNG(DB Client)
            params = {}
            params['delete_flg'] = 0
            params['pod_id'] = pod_id
            params['tenant_name'] = tenant_name
            db_list.set_context(db_endpoint_msa_vlan, params)
            db_list.execute()
            msa_network_info = db_list.get_return_param()

        else:
            raise SystemError('vlan for MSA not Found.')

        return msa_network_info

    def __setup_msa_network_vlan(self, pod_id, vlan_id, ip_address, netmask):

        # Create Instance(MSA Soap Client)
        msa = msaordercmdws.MsaOrderCommandWs(self.job_config,
                                              self.nal_endpoint_config,
                                              pod_id)

        # get config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)

        msa_mask = self.utils.get_subnet_mask_from_cidr_len(netmask)

        # Create System Common(MSA)
        msa_res = msa.create_msa_network_vlan(
                          msa_config_for_common['msa_server_device_id'],
                          vlan_id,
                          ip_address,
                          msa_mask)

        return msa_res

    def __insert_db_port(self, operation_id,
                               tenant_name,
                               pod_id,
                               tenant_id,
                               apl_type,
                               network_id,
                               network_type,
                               network_type_detail,
                               port_id,
                               ip_address,
                               port_info,
                               subnet_mask):

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create NAL_PORT_MNG(DB)
        params = {}
        params['create_id'] = operation_id
        params['update_id'] = operation_id
        params['delete_flg'] = 0
        params['port_id'] = port_id
        params['tenant_name'] = tenant_name
        params['pod_id'] = pod_id
        params['tenant_id'] = tenant_id
        params['network_id'] = network_id
        params['network_type'] = network_type
        params['network_type_detail'] = network_type_detail
        params['apl_type'] = apl_type
        params['node_id'] = ''
        params['IaaS_region_id'] = ' '
        params['IaaS_tenant_id'] = ' '
        params['IaaS_network_id'] = ' '
        params['IaaS_port_id'] = ' '
        params['nic'] = ''
        params['ip_address'] = ip_address
        params['netmask'] = subnet_mask
        params['port_info'] = json.dumps(port_info)
        params['msa_info'] = json.dumps({})

        db_create_instance.set_context(db_endpoint_port, params)
        db_create_instance.execute()

    def __get_dc_segment(self, dc_id, group_id):

        # Get Endpoint(DB Client)
        db_endpoint_dc_segment = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_SEGMENT_MNG)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['dc_id'] = dc_id
        params['group_id'] = group_id
        params['status'] = '1'
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_dc_segment, params)
        db_list.execute()
        dc_segment_list = db_list.get_return_param()

        return dc_segment_list[0]
