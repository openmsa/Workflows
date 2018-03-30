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
import re
import time
import traceback
import uuid

from job.auto import base
from job.auto.extension import routingpod
from job.lib.db import create
from job.lib.db import list
from job.lib.db import update
from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import ports
from job.lib.openstack.quantum import subnets
from job.lib.script import vxlangw


class Vlan(base.JobAutoBase):

    IAAS_PORT_NAME = '#used-NFVI#'

    def virtual_tenant_vlan_port_create_fw(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create VLAN
        vlan_list = self.__get_vlan(job_input)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        if vim_iaas_with_flg == 0:
            # Create VLAN
            if len(vlan_list) == 0:
                vlan_res = self.__create_vlan(job_input)
                network_id = vlan_res['network_id']
            else:
                network_id = vlan_list[0]['network_id']

            # Create Port
            port_res = self.__create_port(job_input,
                                          network_id)

            # Set JOB Output Parameters
            job_output['port_id4'] = port_res['port_id4']

        else:
            # Login VLAN
            if len(vlan_list) == 0:
                vlan_res = self.__login_vlan(job_input)
                iaas_network_id = vlan_res['IaaS_network_id']
            else:
                iaas_network_id = vlan_list[0]['IaaS_network_id']

            # Create Port
            port_res = self.__create_port_iaas(job_input,
                                          iaas_network_id)
            # Set JOB Output Parameters
            job_output['port_id4'] = port_res['port_id4']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_tenant_vlan_port_create_lb(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Create VLAN
        vlan_list = self.__get_vlan(job_input)
        if len(vlan_list) == 0:
            raise SystemError('vlan for tenant  not found.')
        else:
            network_id = vlan_list[0]['network_id']

        if vim_iaas_with_flg == 0:
            # Create Port
            port_res = self.__create_port(job_input,
                                          network_id)
        else:
            port_res = self.__create_port_iaas(job_input,
                                               network_id)

        # Set JOB Output Parameters
        job_output['port_id4'] = port_res['port_id4']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_fw_tenant_vlan_port_add_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Add Port
        self.__add_port_ipv6(job_input)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, {})

        return {}

    def virtual_lb_tenant_vlan_port_add_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Add Port
        self.__add_port_ipv6(job_input)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, {})

        return {}

    def virtual_tenant_vlan_port_delete_fw(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Delete Port
        target_network_list = self.__delete_port(job_input)

        if vim_iaas_with_flg == 0:
            # Delete VLAN
            self.__delete_vlan(job_input, target_network_list)

        # Set JOB Output Parameters

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_tenant_vlan_port_delete_lb(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Delete Port
        target_network_list = self.__delete_port(job_input)

        if vim_iaas_with_flg == 0:
            # Delete VLAN
            self.__delete_vlan(job_input, target_network_list)

        # Set JOB Output Parameters

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def physical_tenant_vlan_port_create_fw(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        apl_type = job_input['apl_type']

        # Create VLAN
        vlan_list = self.__get_vlan(job_input)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        if vim_iaas_with_flg == 0:
            # Create VLAN
            if len(vlan_list) == 0:
                vlan_res = self.__create_vlan(job_input)
                network_id = vlan_res['network_id']
            else:
                network_id = vlan_list[0]['network_id']

        else:
            # Login VLAN
            if len(vlan_list) == 0:
                vlan_res = self.__login_vlan(job_input)
                network_id = vlan_res['IaaS_network_id']
            else:
                network_id = vlan_list[0]['IaaS_network_id']

        tenant_id = job_input['nal_tenant_id']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        node_id = job_input['node_id']

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(
                                        self.job_config.REST_URI_PORT)
        db_endpoint_apl = self.get_db_endpoint(
                                        self.job_config.REST_URI_APL)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['ID'] = job_input['apl_table_rec_id']
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_apl, params)
        db_list_instance.execute()
        apl_list = db_list_instance.get_return_param()

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_PORT_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = tenant_id
        params['node_id'] = node_id

        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        if len(port_list) == 0:
            nic = ''
        else:
            # Get NIC
            nic = self.assign_port(db_list_instance,
                                   db_endpoint_port,
                                   tenant_id,
                                   apl_type,
                                   node_id,
                                   apl_list[0]['nic_tenant'],
                                   nf_type,
                                   device_type,
                                   self.job_config.NW_TYPE_TENANT)

        if vim_iaas_with_flg == 0:
            # Create Port
            port_res = self.__create_port(job_input,
                                          network_id,
                                          '',
                                          '',
                                          node_id,
                                          nic)
        else:
            # Create Port
            port_res = self.__create_port_iaas(job_input,
                                               network_id,
                                               '',
                                               '',
                                               node_id,
                                               nic)

            # Create VXLAN-GW
            self.__create_pnf_vxlangw_tenant(job_input, port_res['port_id4'])

        # Set JOB Output Parameters
        job_output['port_id4'] = port_res['port_id4']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def physical_tenant_vlan_port_create_lb(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        redundant_configuration_flg = \
            job_input.get("redundant_configuration_flg", '1')
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        # Create VLAN
        vlan_list = self.__get_vlan(job_input)
        if len(vlan_list) == 0:
            raise SystemError('vlan for tenant  not found.')
        else:
            network_id = vlan_list[0]['network_id']

        # Create Port(VIP)
        vip_info = self.__create_physical_lb_port(job_input, network_id)

        # Create Port(ACT)
        act_info = self.__create_physical_lb_port(job_input, network_id)

        sby_info = {}
        if redundant_configuration_flg == '0':
            # Create Port(SBY)
            sby_info = self.__create_physical_lb_port(job_input, network_id)

        self.__inster_physical_lb_port_info(job_input,
                                            network_id,
                                            vip_info['free_ip_iaas'],
                                            act_info['free_ip_iaas'],
                                            sby_info.get('free_ip_iaas', {}),
                                            vip_info['port_id'],
                                            act_info['port_id'],
                                            sby_info.get('port_id', ''))

        # Set JOB Output Parameters
        job_output['port_id4'] = vip_info['port_id']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def physical_fw_tenant_vlan_port_add_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Add Port
        network_address_ipv6 = \
            self.__add_fortigate_tenant_vlan_port_ipv6(job_input)

        # Set JOB Output Parameters
        job_output['network_address_ipv6'] = network_address_ipv6

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def physical_lb_tenant_vlan_port_add_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Add Port
        self.__add_tenant_vlan_port_ipv6(job_input)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, {})

        return {}

    def physical_tenant_vlan_port_delete_fw(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Delete Port
        target_network_list = self.__delete_port(job_input)

        if vim_iaas_with_flg == 0:
            # Delete VLAN
            self.__delete_vlan(job_input, target_network_list)
        else:
            # Delete vxlan-gw for pnf vlan
            self.__delete_pnf_vxlangw_tenant(job_input, target_network_list)

        # Set JOB Output Parameters

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def physical_tenant_vlan_port_delete_lb(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Delete Port
        target_network_list = self.__delete_physical_lb_port(job_input)

        if vim_iaas_with_flg == 0:
            # Delete VLAN
            self.__delete_vlan(job_input, target_network_list)
        else:
            # Delete vxlan-gw for pnf vlan
            self.__delete_pnf_vxlangw_tenant(job_input, target_network_list)

        # Set JOB Output Parameters

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __get_vlan(self, job_input):

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_network_type = job_input['IaaS_network_type']

        # Get Endpoint(DB Client)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # List NAL_VIRTUAL_LAN_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['pod_id'] = pod_id
        params['tenant_id'] = nal_tenant_id
        params['IaaS_network_id'] = iaas_network_id
        params['IaaS_network_type'] = iaas_network_type
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_vlan, params)
        db_list_instance.execute()
        vlan_list = db_list_instance.get_return_param()

        return vlan_list

    def __create_vlan(self, job_input):

        # Get JOB Input Parameters
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_network_type = job_input['IaaS_network_type']
        iaas_segmentation_id = job_input['IaaS_segmentation_id']
        network_name = job_input['network_name']
        operation_id = job_input['operation_id']
        tenant_name = job_input['tenant_name']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']
        dc_id = job_input.get('dc_id', 'system')

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                            pod_id, '', nal_tenant_id, dc_id)

        # Get Endpoint(DB Client)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)

        # Create Instance(OpenStack Client)
        osc_networks = networks.OscQuantumNetworks(self.job_config)

        # Create Instance(VXLAN-GW)
        vxlangw_pod_instance = routingpod.RoutingPod()
        vxlangw_instance = vxlangw.VxlanGwClient(self.job_config)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)

        vxlangw_pod_id = ''
        rule_id = ''
        os_cre_network_vim = {}
        if iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:

            vxlangw_endpoint = self.get_os_endpoint_vxlangw(iaas_region_id)

            # Create Network(OpenStack:VIM)
            os_cre_network_vim = osc_networks.create_network(
                            os_endpoint_vim, network_name)

            vxlangw_pod_id = vxlangw_pod_instance.\
                                routing_vxlangw_pod(job_input)

            params = [
                vxlangw_endpoint['endpoint'],
                vxlangw_endpoint['user_id'],
                vxlangw_endpoint['user_password'],
                os_cre_network_vim['network']['provider:segmentation_id'],
                vxlangw_pod_id,
                iaas_network_id,
                vxlangw_endpoint['timeout'],
            ]
            vxlan_gw_res = vxlangw_instance.create_vxlan_gw(params)

            pattern = re.compile('\|\s+id\s+\|\s+(.*)\s+\|')
            for vxlan_gw in vxlan_gw_res:
                matchOB = pattern.match(vxlan_gw)
                if matchOB:
                    rule_id = matchOB.group(1)
                    break

        elif iaas_network_type.upper() == self.job_config.NW_TYPE_VLAN:

            vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)
            if vim_iaas_with_flg == 0:
                physical_network_name = None
            else:
                physical_network_name = self.get_os_physical_network_name()
            # Create Network(OpenStack:VIM)
            os_cre_network_vim = osc_networks.create_network(
                            os_endpoint_vim, network_name, True, False,
                            iaas_segmentation_id, physical_network_name)

        # Get Network Data(id)
        network_id = os_cre_network_vim['network']['id']
        vlan_id = os_cre_network_vim['network']['provider:segmentation_id']

        # Create NAL_VIRTUAL_LAN_MNG(DB Client)
        params = {}
        params['create_id'] = operation_id
        params['update_id'] = operation_id
        params['delete_flg'] = 0
        params['tenant_name'] = tenant_name
        params['pod_id'] = pod_id
        params['tenant_id'] = nal_tenant_id
        params['IaaS_region_id'] = iaas_region_id
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['IaaS_network_id'] = iaas_network_id
        params['IaaS_network_type'] = iaas_network_type
        params['IaaS_segmentation_id'] = iaas_segmentation_id
        params['vlan_id'] = vlan_id
        params['network_id'] = network_id
        params['rule_id'] = rule_id
        params['nal_vlan_info'] = json.dumps(os_cre_network_vim[
                                                            'network'])
        db_create_instance.set_context(db_endpoint_vlan, params)
        db_create_instance.execute()

        return {'network_id': network_id, 'vlan_id': vlan_id}

    def __delete_vlan(self, job_input, target_network_list):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        iaas_region_id = job_input['IaaS_region_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        # Get Endpoint(DB Client)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(OpenStack Client)
        osc_networks = networks.OscQuantumNetworks(self.job_config)

        # Create Instance(VXLAN-GW)
        vxlangw_instance = vxlangw.VxlanGwClient(self.job_config)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # List NAL_VIRTUAL_LAN_MNG(DB Client)
        params = {}
        params['pod_id'] = pod_id
        params['tenant_id'] = nal_tenant_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_vlan, params)
        db_list_instance.execute()
        vlan_list = db_list_instance.get_return_param()

        for vlan_res in vlan_list:

            if vlan_res['network_id'] not in target_network_list:
                continue

            # List NAL_PORT_MNG(DB Client)
            params = {}
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['network_id'] = vlan_res['network_id']
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list = db_list_instance.get_return_param()

            if len(port_list) == 0:
                try:
                    # Delete Network(OpenStack:VIM)
                    osc_networks.delete_network(
                                    os_endpoint_vim, vlan_res['network_id'])
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

                if vlan_res['IaaS_network_type'].upper() == \
                        self.job_config.NW_TYPE_VXLAN:

                    vxlangw_endpoint = self.get_os_endpoint_vxlangw(
                                                            iaas_region_id)
                    # Delete VXLAN-GW(Rule)
                    try:
                        vxlangw_instance.delete_vxlan_gw(
                                            [vxlangw_endpoint['endpoint'],
                                             vxlangw_endpoint['user_id'],
                                             vxlangw_endpoint['user_password'],
                                             vlan_res['rule_id'],
                                             vxlangw_endpoint['timeout']])
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                # Update NAL_VIRTUAL_LAN_MNG(DB): Set DeleteFlg On
                params = {}
                params['update_id'] = operation_id
                params['delete_flg'] = 1
                keys = [vlan_res['ID']]
                db_update_instance.set_context(db_endpoint_vlan, keys, params)
                db_update_instance.execute()

    def __create_port(self,
                      job_input,
                      network_id,
                      mac_address='',
                      del_port_rec_id='',
                      node_id='',
                      nic=''):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        network_name = job_input['network_name']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']
        apl_table_rec_id = job_input['apl_table_rec_id']
        iaas_subnet_id = job_input['IaaS_subnet_id']

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                     '',
                                                     iaas_tenant_id)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(OpenStack Client)
        os_subnets_instance = subnets.OscQuantumSubnets(self.job_config)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        iaas_port_create_count = 0
        while iaas_port_create_count <= \
                            self.job_config.OS_PORT_CREATE_RETRY_COUNT:

            # Get Free IpAddress(IaaS)
            free_ip_iaas = self.get_free_ip_max(job_input, iaas_subnet_id)

            # Create Port(OpenStack:IaaS)
            try:
                os_cre_port_iaas = os_ports_instance.create_port(
                                        os_endpoint_iaas,
                                        iaas_network_id,
                                        self.IAAS_PORT_NAME,
                                        True,
                                        free_ip_iaas['id'],
                                        free_ip_iaas['ip'],
                                        mac_address)

            except Exception as e:

                if str(e) == self.job_config.OS_ERR_MSG_PORT_DUPLICATED:

                    if iaas_port_create_count \
                                == self.job_config.OS_PORT_CREATE_RETRY_COUNT:
                        raise SystemError(
                        'Exceeded Limit Count: OpenStack Port Create(IaaS).')

                    time.sleep(self.job_config.OS_PORT_CREATE_WAIT_TIME)
                    iaas_port_create_count += 1
                    continue

                raise

            break

        iaas_port_id = os_cre_port_iaas['port']['id']
        iaas_mac_address = os_cre_port_iaas['port']['mac_address']

        # Create Subnet(OpenStack:VIM)
        if str(apl_type) == str(self.job_config.APL_TYPE_VR):

            subnet_list = os_subnets_instance.list_subnets(os_endpoint_vim)

            subnet_exists_flg = False
            subnet_id = ''
            for rec in subnet_list['subnets']:
                if rec['network_id'] == network_id \
                            and rec['cidr'] == free_ip_iaas['cidr']:
                    subnet_exists_flg = True
                    subnet_id = rec['id']
                    break

            if subnet_exists_flg == False:
                os_cre_subnet_vim = os_subnets_instance.create_subnet(
                                                        os_endpoint_vim,
                                                        network_id,
                                                        free_ip_iaas['cidr'],
                                                        '',
                                                        nal_tenant_id)
                subnet_id = os_cre_subnet_vim['subnet']['id']

            # Create Port(OpenStack:VIM)
            os_cre_port_vim = os_ports_instance.create_port(os_endpoint_vim,
                                                            network_id,
                                                            network_name,
                                                            True,
                                                            subnet_id,
                                                            free_ip_iaas['ip'],
                                                            iaas_mac_address)

            # Get Port Info
            port_info = os_cre_port_vim['port']
            port_id = port_info['id']
            ip_address = port_info['fixed_ips'][0]['ip_address']
            subnet_id = port_info['fixed_ips'][0]['subnet_id']

            # Get Subnet(OpenStack:VIM)
            os_get_subnet_res = os_subnets_instance.get_subnet(
                                                os_endpoint_vim, subnet_id)

            # Get Subnet Info(cidr)
            cidr_array = os_get_subnet_res['subnet']['cidr'].split('/')
            netmask = cidr_array[1]

        else:
            port_info = {}
            port_id = str(uuid.uuid4())
            ip_address = free_ip_iaas['ip']
            netmask = free_ip_iaas['netmask']

        if len(del_port_rec_id) == 0:
            # Create NAL_PORT_MNG(DB)
            params = {}
            params['create_id'] = operation_id
            params['update_id'] = operation_id
            params['delete_flg'] = 0
            params['port_id'] = port_id
            params['tenant_name'] = tenant_name
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['network_id'] = network_id
            params['network_type'] = self.job_config.NW_TYPE_IN
            params['network_type_detail'] = self.job_config.NW_TYPE_TENANT
            params['apl_type'] = apl_type
            params['IaaS_region_id'] = iaas_region_id
            params['IaaS_tenant_id'] = iaas_tenant_id
            params['IaaS_network_id'] = iaas_network_id
            params['IaaS_subnet_id'] = iaas_subnet_id
            params['IaaS_port_id'] = iaas_port_id
            params['ip_address'] = ip_address
            params['netmask'] = netmask
            params['port_info'] = json.dumps(port_info)
            params['msa_info'] = json.dumps({})
            params['node_id'] = ''
            params['nic'] = ''
            params['apl_table_rec_id'] = apl_table_rec_id

            # pysical server port add
            if len(node_id) != 0 and len(nic) != 0:
                params['node_id'] = node_id
                params['nic'] = nic

            db_create_instance.set_context(db_endpoint_port, params)
            db_create_instance.execute()
        else:
            # Update NAL_VIRTUAL_LAN_MNG(DB): Set DeleteFlg On
            params = {}
            params['update_id'] = operation_id
            params['delete_flg'] = 0
            params['port_id'] = port_id
            params['network_id'] = network_id
            params['IaaS_network_id'] = iaas_network_id
            params['IaaS_subnet_id'] = iaas_subnet_id
            params['IaaS_port_id'] = iaas_port_id
            params['ip_address'] = ip_address
            params['netmask'] = netmask
            params['port_info'] = json.dumps(port_info)
            params['msa_info'] = json.dumps({})
            keys = [del_port_rec_id]

            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

        return {
            'port_id4': port_id,
        }

    def __create_physical_lb_port(self, job_input, network_id):

        # Get JOB Input Parameters
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_subnet_id = job_input['IaaS_subnet_id']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']
        operation_id = job_input['operation_id']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        if vim_iaas_with_flg == 0:
            iaas_token_tenant = iaas_tenant_id
        else:
            iaas_token_tenant = nal_tenant_id

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                     '',
                                                     iaas_token_tenant)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        # Create Instance(OpenStack Client)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        iaas_port_create_count = 0
        while iaas_port_create_count <= \
                            self.job_config.OS_PORT_CREATE_RETRY_COUNT:

            # Get Free IpAddress(IaaS)
            free_ip_iaas = self.get_free_ip_max(job_input, iaas_subnet_id)

            try:
                if vim_iaas_with_flg == 0:
                    # Create Port(OpenStack:IaaS)
                    os_cre_port_iaas = os_ports_instance.create_port(
                                    os_endpoint_iaas,
                                    iaas_network_id,
                                    self.IAAS_PORT_NAME,
                                    True,
                                    free_ip_iaas['id'], free_ip_iaas['ip'])
                else:
                    # Create Port(OpenStack:VIM)
                    os_cre_port_iaas = os_ports_instance.create_port(
                                    os_endpoint_vim,
                                    iaas_network_id,
                                    self.IAAS_PORT_NAME,
                                    True,
                                    free_ip_iaas['id'], free_ip_iaas['ip'])

                    # Create VXLAN-GW
                    self.__create_pnf_vxlangw_tenant(job_input,
                                              os_cre_port_iaas['port']['id'])

            except Exception as e:

                if str(e) == self.job_config.OS_ERR_MSG_PORT_DUPLICATED:

                    if iaas_port_create_count \
                                == self.job_config.OS_PORT_CREATE_RETRY_COUNT:
                        raise SystemError(
                        'Exceeded Limit Count: OpenStack Port Create(IaaS).')

                    time.sleep(self.job_config.OS_PORT_CREATE_WAIT_TIME)
                    iaas_port_create_count += 1
                    continue

                raise

            break

        return {
                'free_ip_iaas': free_ip_iaas,
                'port_id': os_cre_port_iaas['port']['id'],
        }

    def __inster_physical_lb_port_info(self,
                                       job_input,
                                       network_id,
                                       vip_free_ip_info,
                                       act_free_ip_info,
                                       sby_free_ip_info,
                                       vip_iaas_port_id,
                                       act_iaas_port_id,
                                       sby_iaas_port_id):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_subnet_id = job_input['IaaS_subnet_id']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']
        apl_table_rec_id = job_input['apl_table_rec_id']

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)

        vip_ip_address = vip_free_ip_info['ip']
        vip_netmask = vip_free_ip_info['netmask']

        act_ip_address = act_free_ip_info['ip']
        act_netmask = act_free_ip_info['netmask']

        sby_ip_address = sby_free_ip_info.get('ip', '')
        sby_netmask = sby_free_ip_info.get('netmask', '')

        # Create NAL_PORT_MNG(DB)
        params = {}
        params['create_id'] = operation_id
        params['update_id'] = operation_id
        params['delete_flg'] = 0
        params['port_id'] = vip_iaas_port_id
        params['tenant_name'] = tenant_name
        params['pod_id'] = pod_id
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = network_id
        params['network_type'] = self.job_config.NW_TYPE_IN
        params['network_type_detail'] = self.job_config.NW_TYPE_TENANT
        params['apl_type'] = apl_type
        params['node_id'] = ''
        params['apl_table_rec_id'] = apl_table_rec_id
        params['IaaS_region_id'] = iaas_region_id
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['IaaS_network_id'] = iaas_network_id
        params['IaaS_subnet_id'] = iaas_subnet_id
        params['IaaS_port_id'] = vip_iaas_port_id
        params['nic'] = 'TENANT-TRUNK'
        params['ip_address'] = vip_ip_address
        params['netmask'] = vip_netmask
        params['port_info'] = json.dumps({'IaaS_port_info': {
                                  'vip': {'id': vip_iaas_port_id,
                                          'ip_address': vip_ip_address,
                                          'netmask': vip_netmask,
                                          },
                                  'act': {'id': act_iaas_port_id,
                                          'ip_address': act_ip_address,
                                          'netmask': act_netmask,
                                          },
                                  'sby': {'id': sby_iaas_port_id,
                                          'ip_address': sby_ip_address,
                                          'netmask': sby_netmask,
                                          },
                                  },
                              })
        params['msa_info'] = json.dumps({})

        db_create_instance.set_context(db_endpoint_port, params)
        db_create_instance.execute()

    def __delete_port(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        tenant_name = job_input['tenant_name']
        apl_table_rec_id = job_input['apl_table_rec_id']
        node_id = job_input['node_id']
        apl_type = job_input['apl_type']
        iaas_network_id = job_input.get('IaaS_network_id', '')
        port_id = job_input.get('port_id', '')
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        if vim_iaas_with_flg == 0:
            iaas_token_tenant = iaas_tenant_id
        else:
            iaas_token_tenant = nal_tenant_id

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                     '',
                                                     iaas_token_tenant)

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = \
            self.get_db_endpoint(self.job_config.REST_URI_MSA_VLAN)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(OpenStack Client)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # Get Network Info
        msa_network_info = {'network_id': ''}
        if str(apl_type) == str(self.job_config.APL_TYPE_VR):
            params = {}
            params['tenant_name'] = tenant_name
            params['pod_id'] = pod_id
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_msa_vlan, params)
            db_list_instance.execute()
            msa_network_list = db_list_instance.get_return_param()
            msa_network_info = msa_network_list[0]
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            '')
        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            '')

        # List NAL_PORT_MNG(DB)
        if node_id == '':
            params = {}
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['apl_table_rec_id'] = apl_table_rec_id
            params['delete_flg'] = 0
            if len(iaas_network_id) != 0:
                params['IaaS_network_id'] = iaas_network_id
            if len(port_id) != 0:
                params['port_id'] = port_id
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list = db_list_instance.get_return_param()

        else:
            params = {}
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['node_id'] = node_id
            params['delete_flg'] = 0
            if len(iaas_network_id) != 0:
                params['IaaS_network_id'] = iaas_network_id
            if len(port_id) != 0:
                params['port_id'] = port_id
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list = db_list_instance.get_return_param()

        if len(port_list) == 0:
            if job_cleaning_mode == '1':
                pass
            else:
                raise SystemError('port on tenant-lan not exists.')

        target_network_list = []

        for port_res in port_list:

            if port_res['network_id'] == \
                        msa_network_info['network_id'] \
                or port_res['network_id'] == \
                        pub_network_info['network_id'] \
                or port_res['network_id'] == \
                        ext_network_info['network_id']:
                continue

            if port_res['network_id'] not in target_network_list:
                target_network_list.append(port_res['network_id'])

            port_key_id = port_res['ID']
            port_id = port_res['port_id']
            iaas_port_id = port_res['IaaS_port_id']

            if vim_iaas_with_flg == 0:

                # Delete Port(OpenStack:IaaS)
                try:
                    os_ports_instance.delete_port(
                                        os_endpoint_iaas, iaas_port_id)
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise
            else:
                # Delete Port(OpenStack:Vim)
                try:
                    os_ports_instance.delete_port(
                                        os_endpoint_vim, iaas_port_id)
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

            if str(apl_type) == str(self.job_config.APL_TYPE_VR):
                if vim_iaas_with_flg == 0:
                    try:
                        # Delete Port(OpenStack:VIM)
                        os_ports_instance.delete_port(os_endpoint_vim, port_id)
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

            # Update NAL_PORT_MNG(DB): Set DeleteFlg On
            params = {}
            params['update_id'] = operation_id
            params['delete_flg'] = 1
            keys = [port_key_id]
            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

        return  target_network_list

    def __delete_physical_lb_port(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_table_rec_id = job_input['apl_table_rec_id']
        node_id = job_input['node_id']
        iaas_network_id = job_input.get('IaaS_network_id', '')
        port_id = job_input.get('port_id', '')
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        if vim_iaas_with_flg == 0:
            iaas_token_tenant = iaas_tenant_id
        else:
            iaas_token_tenant = nal_tenant_id

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                     '',
                                                     iaas_token_tenant)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(OpenStack Client)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            '')
        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            '')

        # List NAL_PORT_MNG(DB)
        if node_id == '':
            params = {}
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['apl_table_rec_id'] = apl_table_rec_id
            params['delete_flg'] = 0
            if len(iaas_network_id) != 0:
                params['IaaS_network_id'] = iaas_network_id
            if len(port_id) != 0:
                params['port_id'] = port_id
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list = db_list_instance.get_return_param()

        else:
            params = {}
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['node_id'] = node_id
            params['delete_flg'] = 0
            if len(iaas_network_id) != 0:
                params['IaaS_network_id'] = iaas_network_id
            if len(port_id) != 0:
                params['port_id'] = port_id
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list = db_list_instance.get_return_param()

        if len(port_list) == 0:
            if job_cleaning_mode == '1':
                pass
            else:
                raise SystemError('port on tenant-lan not exists.')

        target_network_list = []

        for port_res in port_list:

            if port_res['network_id'] == \
                        pub_network_info['network_id'] \
                or port_res['network_id'] == \
                        ext_network_info['network_id']:
                continue

            if port_res['network_id'] not in target_network_list:
                target_network_list.append(port_res['network_id'])

            port_key_id = port_res['ID']
            port_info = json.loads(port_res['port_info'])
            iaas_vip_port_id = port_info['IaaS_port_info']['vip']['id']
            iaas_act_port_id = port_info['IaaS_port_info']['act']['id']
            iaas_sby_port_id = port_info['IaaS_port_info']['sby']['id']

            # Delete Port(vip)(OpenStack:IaaS)
            try:
                if vim_iaas_with_flg == 0:
                    os_ports_instance.delete_port(os_endpoint_iaas,
                                                  iaas_vip_port_id)
                else:
                    os_ports_instance.delete_port(os_endpoint_vim,
                                                  iaas_vip_port_id)
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            # Delete Port(act)(OpenStack:IaaS)
            try:
                if vim_iaas_with_flg == 0:
                    os_ports_instance.delete_port(os_endpoint_iaas,
                                                  iaas_act_port_id)
                else:
                    os_ports_instance.delete_port(os_endpoint_vim,
                                                  iaas_act_port_id)
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            # Delete Port(sby)(OpenStack:IaaS)
            if len(iaas_sby_port_id) > 0:
                try:
                    if vim_iaas_with_flg == 0:
                        os_ports_instance.delete_port(os_endpoint_iaas,
                                                      iaas_sby_port_id)
                    else:
                        os_ports_instance.delete_port(os_endpoint_vim,
                                                      iaas_sby_port_id)
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise

            # Update NAL_PORT_MNG(DB): Set DeleteFlg On
            params = {}
            params['update_id'] = operation_id
            params['delete_flg'] = 1
            keys = [port_key_id]
            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

        return  target_network_list

    def __add_port_ipv6(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_subnet_id_v6 = job_input['IaaS_subnet_id']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']
        port_id = job_input['port_id']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Create Instance(OpenStack Client)
        os_subnets_instance = subnets.OscQuantumSubnets(self.job_config)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        if vim_iaas_with_flg == 0:
            iaas_token_tenant = iaas_tenant_id
        else:
            iaas_token_tenant = nal_tenant_id

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                     '',
                                                     iaas_token_tenant)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # List NAL_PORT_MNG(DB)
        params = {}
        params['nal_tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_db_res = db_list.get_return_param()

        port_rec_id = port_db_res[0]['ID']
        iaas_port_id = port_db_res[0]['IaaS_port_id']
        network_id = port_db_res[0]['network_id']

        # Get Port(OpenStack:IaaS)
        os_port_iaas_res = os_ports_instance.get_port(os_endpoint_iaas,
                                                      iaas_port_id)

        fixed_ip_add = {'subnet_id': iaas_subnet_id_v6}
        fixed_ips_update = os_port_iaas_res['port']['fixed_ips']
        fixed_ips_update.append(fixed_ip_add)

        if vim_iaas_with_flg == 0:
            # Update Port(OpenStack:IaaS)
            os_port_iaas_upd = os_ports_instance.update_port(os_endpoint_iaas,
                                                             iaas_port_id,
                                                             None,
                                                             None,
                                                             fixed_ips_update)
        else:
            # Update Port(OpenStack:Vim)
            os_port_iaas_upd = os_ports_instance.update_port(os_endpoint_vim,
                                                             iaas_port_id,
                                                             None,
                                                             None,
                                                             fixed_ips_update)

        for fixed_ip in os_port_iaas_upd['port']['fixed_ips']:
            if fixed_ip['subnet_id'] == iaas_subnet_id_v6:
                ip_address_v6 = self.utils.get_ipaddress_compressed(
                                                fixed_ip['ip_address'])

        # Get Subnet(OpenStack:IaaS)
        os_subnet_iaas_res = os_subnets_instance.get_subnet(os_endpoint_iaas,
                                                            iaas_subnet_id_v6)

        iaas_cidr = self.utils.get_cidr_compressed(
                                os_subnet_iaas_res['subnet']['cidr'])['cidr']

        iaas_netmask = iaas_cidr.split('/')

        if vim_iaas_with_flg == 0:
            # List Subnets(OpenStack:VIM)
            os_subnet_vim_list = \
                    os_subnets_instance.list_subnets(os_endpoint_vim)

            subnet_exists_flg = False
            for subnet in os_subnet_vim_list['subnets']:

                vim_cidr = \
                    self.utils.get_cidr_compressed(subnet['cidr'])['cidr']

                if subnet['network_id'] == network_id \
                    and vim_cidr == iaas_cidr:

                    subnet_exists_flg = True
                    vim_subnet_id = subnet['id']
                    break

            if subnet_exists_flg == False:

                # Create Subnet(OpenStack:VIM)
                os_subnet_vim_cre = os_subnets_instance.create_subnet(
                                                        os_endpoint_vim,
                                                        network_id,
                                                        iaas_cidr,
                                                        '',
                                                        nal_tenant_id,
                                                        self.utils.IP_VER_V6
                                                        )

                vim_subnet_id = os_subnet_vim_cre['subnet']['id']

            # Get Port(OpenStack:VIM)
            os_port_vim_res = os_ports_instance.get_port(os_endpoint_vim,
                                                         port_id)

            fixed_ip_add = {
                'subnet_id': vim_subnet_id,
                'ip_address': ip_address_v6,
            }
            fixed_ips_update = os_port_vim_res['port']['fixed_ips']
            fixed_ips_update.append(fixed_ip_add)

            # Update Port(OpenStack:VIM)
            os_port_vim_upd = os_ports_instance.update_port(os_endpoint_vim,
                                                        port_id,
                                                        None,
                                                        None,
                                                        fixed_ips_update)

            update_params = {
                'update_id': operation_id,
                'IaaS_subnet_id_v6': iaas_subnet_id_v6,
                'ip_address_v6': ip_address_v6,
                'netmask_v6': iaas_netmask[1],
                'port_info': os_port_vim_upd['port'],
            }

        else:
            update_params = {
                'update_id': operation_id,
                'IaaS_subnet_id_v6': iaas_subnet_id_v6,
                'ip_address_v6': ip_address_v6,
                'netmask_v6': iaas_netmask[1],
                'port_info': os_port_iaas_upd['port'],
            }

        # Update DB: NAL_PORT_MNG
        self._update_db_port(update_params, port_rec_id)

    def __add_tenant_vlan_port_ipv6(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_subnet_id_v6 = job_input['IaaS_subnet_id']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']
        port_id = job_input['port_id']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        if vim_iaas_with_flg == 0:
            iaas_token_tenant = iaas_tenant_id
        else:
            iaas_token_tenant = nal_tenant_id

        # Create Instance(OpenStack Client)
        os_subnets_instance = subnets.OscQuantumSubnets(self.job_config)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                     '',
                                                     iaas_token_tenant)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # List NAL_PORT_MNG(DB)
        params = {}
        params['nal_tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_db_res = db_list.get_return_param()
        port_rec_id = port_db_res[0]['ID']
        port_info = port_db_res[0]['port_info']
        port_info_dict = json.loads(port_info)
        iaas_vip_port_id = port_info_dict['IaaS_port_info']['vip']['id']
        iaas_act_port_id = port_info_dict['IaaS_port_info']['act']['id']
        iaas_sby_port_id = port_info_dict['IaaS_port_info']['sby']['id']

        # Get Port(OpenStack:IaaS)
        os_port_iaas_res = os_ports_instance.get_port(os_endpoint_iaas,
                                                      iaas_vip_port_id)

        fixed_ip_add = {'subnet_id': iaas_subnet_id_v6}
        fixed_ips_update = os_port_iaas_res['port']['fixed_ips']
        fixed_ips_update.append(fixed_ip_add)

        if vim_iaas_with_flg == 0:
            # Update Port(OpenStack:IaaS)
            os_port_iaas_upd = os_ports_instance.update_port(os_endpoint_iaas,
                                                    iaas_vip_port_id,
                                                    None,
                                                    None,
                                                    fixed_ips_update)
        else:
            # Update Port(OpenStack:VIM)
            os_port_iaas_upd = os_ports_instance.update_port(os_endpoint_vim,
                                                    iaas_vip_port_id,
                                                    None,
                                                    None,
                                                    fixed_ips_update)

        for fixed_ip in os_port_iaas_upd['port']['fixed_ips']:
            if fixed_ip['subnet_id'] == iaas_subnet_id_v6:
                ip_address_v6_vip = self.utils.get_ipaddress_compressed(
                                                fixed_ip['ip_address'])

        # Get Port(OpenStack:IaaS)
        os_port_iaas_res = os_ports_instance.get_port(os_endpoint_iaas,
                                                      iaas_act_port_id)

        fixed_ip_add = {'subnet_id': iaas_subnet_id_v6}
        fixed_ips_update = os_port_iaas_res['port']['fixed_ips']
        fixed_ips_update.append(fixed_ip_add)

        if vim_iaas_with_flg == 0:
        # Update Port(OpenStack:IaaS)
            os_port_iaas_upd = os_ports_instance.update_port(os_endpoint_iaas,
                                                    iaas_act_port_id,
                                                    None,
                                                    None,
                                                    fixed_ips_update)
        else:
            # Update Port(OpenStack:VIM)
            os_port_iaas_upd = os_ports_instance.update_port(os_endpoint_vim,
                                                    iaas_act_port_id,
                                                    None,
                                                    None,
                                                    fixed_ips_update)

        for fixed_ip in os_port_iaas_upd['port']['fixed_ips']:
            if fixed_ip['subnet_id'] == iaas_subnet_id_v6:
                ip_address_v6_act = self.utils.get_ipaddress_compressed(
                                                fixed_ip['ip_address'])

        if iaas_sby_port_id == '':
            pass
        else:
            # Get Port(OpenStack:IaaS)
            os_port_iaas_res = os_ports_instance.get_port(os_endpoint_iaas,
                                                          iaas_sby_port_id)

            fixed_ip_add = {'subnet_id': iaas_subnet_id_v6}
            fixed_ips_update = os_port_iaas_res['port']['fixed_ips']
            fixed_ips_update.append(fixed_ip_add)

            if vim_iaas_with_flg == 0:
                # Update Port(OpenStack:IaaS)
                os_port_iaas_upd = os_ports_instance.update_port(
                                                        os_endpoint_iaas,
                                                        iaas_sby_port_id,
                                                        None,
                                                        None,
                                                        fixed_ips_update)
            else:
                # Update Port(OpenStack:VIM)
                os_port_iaas_upd = os_ports_instance.update_port(
                                                        os_endpoint_vim,
                                                        iaas_sby_port_id,
                                                        None,
                                                        None,
                                                        fixed_ips_update)

            for fixed_ip in os_port_iaas_upd['port']['fixed_ips']:
                if fixed_ip['subnet_id'] == iaas_subnet_id_v6:
                    ip_address_v6_sby = self.utils.get_ipaddress_compressed(
                                                    fixed_ip['ip_address'])

        # Get Subnet(OpenStack:IaaS)
        os_subnet_iaas_res = os_subnets_instance.get_subnet(os_endpoint_iaas,
                                                           iaas_subnet_id_v6)

        iaas_cidr = self.utils.get_cidr_compressed(
                                os_subnet_iaas_res['subnet']['cidr'])['cidr']

        iaas_netmask = iaas_cidr.split('/')

        port_info_dict['IaaS_port_info']['vip']['netmask_v6'] =\
                                                        iaas_netmask[1]
        port_info_dict['IaaS_port_info']['vip']['ip_address_v6'] =\
                                                        ip_address_v6_vip
        port_info_dict['IaaS_port_info']['act']['netmask_v6'] =\
                                                        iaas_netmask[1]
        port_info_dict['IaaS_port_info']['act']['ip_address_v6'] =\
                                                        ip_address_v6_act

        if iaas_sby_port_id == '':
            pass
        else:
            port_info_dict['IaaS_port_info']['sby']['netmask_v6'] =\
                                                        iaas_netmask[1]
            port_info_dict['IaaS_port_info']['sby']['ip_address_v6'] =\
                                                        ip_address_v6_sby
        update_params = {
            'update_id': operation_id,
            'IaaS_subnet_id_v6': iaas_subnet_id_v6,
            'ip_address_v6': ip_address_v6_vip,
            'netmask_v6': iaas_netmask[1],
            'port_info': json.dumps(port_info_dict)
        }

        # Update DB: NAL_PORT_MNG
        self._update_db_port(update_params, port_rec_id)

    def __add_fortigate_tenant_vlan_port_ipv6(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_subnet_id_v6 = job_input['IaaS_subnet_id']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']
        port_id = job_input['port_id']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Create Instance(OpenStack Client)
        os_subnets_instance = subnets.OscQuantumSubnets(self.job_config)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        if vim_iaas_with_flg == 0:
            iaas_token_tenant = iaas_tenant_id
        else:
            iaas_token_tenant = nal_tenant_id

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                     '',
                                                     iaas_token_tenant)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # List NAL_PORT_MNG(DB)
        params = {}
        params['nal_tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_db_res = db_list.get_return_param()
        port_rec_id = port_db_res[0]['ID']
        iaas_port_id = port_db_res[0]['IaaS_port_id']

        # Get Port(OpenStack:IaaS)
        os_port_iaas_res = os_ports_instance.get_port(os_endpoint_iaas,
                                                      iaas_port_id)

        fixed_ip_add = {'subnet_id': iaas_subnet_id_v6}
        fixed_ips_update = os_port_iaas_res['port']['fixed_ips']
        fixed_ips_update.append(fixed_ip_add)

        if vim_iaas_with_flg == 0:
            # Update Port(OpenStack:IaaS)
            os_port_iaas_upd = os_ports_instance.update_port(os_endpoint_iaas,
                                                             iaas_port_id,
                                                             None,
                                                             None,
                                                             fixed_ips_update)
        else:
            # Update Port(OpenStack:IaaS)
            os_port_iaas_upd = os_ports_instance.update_port(os_endpoint_vim,
                                                             iaas_port_id,
                                                             None,
                                                             None,
                                                             fixed_ips_update)

        for fixed_ip in os_port_iaas_upd['port']['fixed_ips']:
            if fixed_ip['subnet_id'] == iaas_subnet_id_v6:
                ip_address_v6 = self.utils.get_ipaddress_compressed(
                                                fixed_ip['ip_address'])
        # Get Subnet(OpenStack:IaaS)
        os_subnet_iaas_res = os_subnets_instance.get_subnet(os_endpoint_iaas,
                                                            iaas_subnet_id_v6)

        iaas_cidr = self.utils.get_cidr_compressed(
                                os_subnet_iaas_res['subnet']['cidr'])['cidr']

        iaas_netmask = iaas_cidr.split('/')

        update_params = {
            'update_id': operation_id,
            'IaaS_subnet_id_v6': iaas_subnet_id_v6,
            'ip_address_v6': ip_address_v6,
            'netmask_v6': iaas_netmask[1],
            'port_info': os_port_iaas_upd['port'],
        }

        # Update DB: NAL_PORT_MNG
        self._update_db_port(update_params, port_rec_id)

        return iaas_cidr

    def __login_vlan(self, job_input):

        # Get JOB Input Parameters
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_network_type = job_input['IaaS_network_type']
        iaas_segmentation_id = job_input['IaaS_segmentation_id']
        operation_id = job_input['operation_id']
        tenant_name = job_input['tenant_name']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']

        # Get Endpoint(DB Client)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)

        vlan_id = iaas_segmentation_id

        # Create NAL_VIRTUAL_LAN_MNG(DB Client)
        params = {}
        params['create_id'] = operation_id
        params['update_id'] = operation_id
        params['delete_flg'] = 0
        params['tenant_name'] = tenant_name
        params['pod_id'] = pod_id
        params['tenant_id'] = nal_tenant_id
        params['IaaS_region_id'] = iaas_region_id
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['IaaS_network_id'] = iaas_network_id
        params['IaaS_network_type'] = iaas_network_type
        params['IaaS_segmentation_id'] = iaas_segmentation_id
        params['network_id'] = iaas_network_id
        params['vlan_id'] = vlan_id
        params['rule_id'] = ''
        params['nal_vlan_info'] = '{}'
        db_create_instance.set_context(db_endpoint_vlan, params)
        db_create_instance.execute()

        return {'IaaS_network_id': iaas_network_id, 'vlan_id': vlan_id}

    def __create_port_iaas(self,
                      job_input,
                      network_id,
                      mac_address='',
                      del_port_rec_id='',
                      node_id='',
                      nic=''):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']
        apl_table_rec_id = job_input['apl_table_rec_id']
        iaas_subnet_id = job_input['IaaS_subnet_id']

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                   '',
                                                   nal_tenant_id)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(OpenStack Client)
        os_subnets_instance = subnets.OscQuantumSubnets(self.job_config)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        iaas_port_create_count = 0
        while iaas_port_create_count <= \
                            self.job_config.OS_PORT_CREATE_RETRY_COUNT:

            # Get Free IpAddress(IaaS)
            free_ip_iaas = self.get_free_ip_max(job_input, iaas_subnet_id)

            # Create Port(OpenStack:IaaS)
            try:
                os_cre_port_iaas = os_ports_instance.create_port(
                                        os_endpoint_vim,
                                        iaas_network_id,
                                        self.IAAS_PORT_NAME,
                                        True,
                                        free_ip_iaas['id'],
                                        free_ip_iaas['ip'],
                                        mac_address)

            except Exception as e:

                if str(e) == self.job_config.OS_ERR_MSG_PORT_DUPLICATED:

                    if iaas_port_create_count \
                                == self.job_config.OS_PORT_CREATE_RETRY_COUNT:
                        raise SystemError(
                        'Exceeded Limit Count: OpenStack Port Create(IaaS).')

                    time.sleep(self.job_config.OS_PORT_CREATE_WAIT_TIME)
                    iaas_port_create_count += 1
                    continue

                raise

            break

        iaas_port_id = os_cre_port_iaas['port']['id']

        # Get Port Info
        port_info = os_cre_port_iaas['port']
        port_id = port_info['id']
        ip_address = port_info['fixed_ips'][0]['ip_address']
        subnet_id = port_info['fixed_ips'][0]['subnet_id']

        # Get Subnet(OpenStack:VIM)
        os_get_subnet_res = os_subnets_instance.get_subnet(
                                                os_endpoint_vim, subnet_id)

        # Get Subnet Info(cidr)
        cidr_array = os_get_subnet_res['subnet']['cidr'].split('/')
        netmask = cidr_array[1]

        if len(del_port_rec_id) == 0:
            # Create NAL_PORT_MNG(DB)
            params = {}
            params['create_id'] = operation_id
            params['update_id'] = operation_id
            params['delete_flg'] = 0
            params['port_id'] = port_id
            params['tenant_name'] = tenant_name
            params['pod_id'] = pod_id
            params['tenant_id'] = nal_tenant_id
            params['network_id'] = network_id
            params['network_type'] = self.job_config.NW_TYPE_IN
            params['network_type_detail'] = self.job_config.NW_TYPE_TENANT
            params['apl_type'] = apl_type
            params['IaaS_region_id'] = iaas_region_id
            params['IaaS_tenant_id'] = iaas_tenant_id
            params['IaaS_network_id'] = iaas_network_id
            params['IaaS_subnet_id'] = iaas_subnet_id
            params['IaaS_port_id'] = iaas_port_id
            params['ip_address'] = ip_address
            params['netmask'] = netmask
            params['port_info'] = json.dumps(port_info)
            params['msa_info'] = json.dumps({})
            params['node_id'] = ''
            params['nic'] = ''
            params['apl_table_rec_id'] = apl_table_rec_id

            # pysical server port add
            if len(node_id) != 0 and len(nic) != 0:
                params['node_id'] = node_id
                params['nic'] = nic

            db_create_instance.set_context(db_endpoint_port, params)
            db_create_instance.execute()
        else:
            # Update NAL_VIRTUAL_LAN_MNG(DB): Set DeleteFlg On
            params = {}
            params['update_id'] = operation_id
            params['delete_flg'] = 0
            params['port_id'] = port_id
            params['network_id'] = network_id
            params['IaaS_network_id'] = iaas_network_id
            params['IaaS_subnet_id'] = iaas_subnet_id
            params['IaaS_port_id'] = iaas_port_id
            params['ip_address'] = ip_address
            params['netmask'] = netmask
            params['port_info'] = json.dumps(port_info)
            params['msa_info'] = json.dumps({})
            keys = [del_port_rec_id]

            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

        return {
            'port_id4': port_id,
        }

    def __create_pnf_vxlangw_tenant(self, job_input, port_id):

        # Get JOB Input Parameters
        iaas_region_id = job_input['IaaS_region_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_subnet_id = job_input['IaaS_subnet_id']
        iaas_network_type = job_input['IaaS_network_type']
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        pod_id = job_input['pod_id']

        rule_id = ''
        if iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:

            # Get Endpoint(DB Client)
            db_endpoint_pnf_vlan = self.get_db_endpoint(
                                        self.job_config.REST_URI_PNF_VLAN)

            # Create Instance(VXLAN-GW)
            vxlangw_pod_instance = routingpod.RoutingPod()
            vxlangw_instance = vxlangw.VxlanGwClient(self.job_config)

            # Create Instance(DB Client)
            db_list = list.ListClient(self.job_config)
            db_update = update.UpdateClient(self.job_config)

            # List NAL_PNF_VLAN_MNG(DB Client)
            params = {}
            params['delete_flg'] = 0
            params['status'] = 1
            params['network_id'] = iaas_network_id
            db_list.set_context(db_endpoint_pnf_vlan, params)
            db_list.execute()
            pnf_vlan_list = db_list.get_return_param()

            if len(pnf_vlan_list) == 0:
                # List NAL_PNF_VLAN_MNG(DB Client)
                params = {}
                params['delete_flg'] = 0
                params['status'] = 0
                db_list.set_context(db_endpoint_pnf_vlan, params)
                db_list.execute()
                pnf_vlan_list = db_list.get_return_param()

                pnf_vlan_info = {}
                if len(pnf_vlan_list) != 0:

                    pnf_vlan_info = pnf_vlan_list[0]

                    # Update NAL_PNF_VLAN_MNG(DB Client)
                    keys = [pnf_vlan_info['ID']]
                    params = {}
                    params['update_id'] = operation_id
                    params['pod_id'] = pod_id
                    params['tenant_name'] = nal_tenant_id
                    params['status'] = 1
                    params['tenant_id'] = iaas_tenant_id
                    params['network_id'] = iaas_network_id
                    params['subnet_id'] = iaas_subnet_id
                    params['port_id'] = port_id
                    db_update.set_context(db_endpoint_pnf_vlan, keys, params)
                    db_update.execute()

                else:
                    # List NAL_PNF_VLAN_MNG(DB Client)
                    params = {}
                    params['delete_flg'] = 0
                    params['status'] = 2
                    db_list.set_context(db_endpoint_pnf_vlan, params)
                    db_list.execute()
                    pnf_vlan_list = db_list.get_return_param()

                    if len(pnf_vlan_list) != 0:

                        pnf_vlan_info = pnf_vlan_list[0]

                        # Update NAL_PNF_VLAN_MNG(DB Client)
                        keys = [pnf_vlan_info['ID']]
                        params = {}
                        params['update_id'] = operation_id
                        params['pod_id'] = pod_id
                        params['tenant_name'] = nal_tenant_id
                        params['status'] = 1
                        params['tenant_id'] = iaas_tenant_id
                        params['network_id'] = iaas_network_id
                        params['subnet_id'] = iaas_subnet_id
                        params['port_id'] = port_id
                        db_update.set_context(db_endpoint_pnf_vlan,
                                              keys, params)
                        db_update.execute()

                    else:
                        raise SystemError('vlan for PNF not Found.')

                vxlangw_endpoint = self.get_os_endpoint_vxlangw(iaas_region_id)

                vxlangw_pod_id = vxlangw_pod_instance.\
                                    routing_vxlangw_pod(job_input)

                params = [
                    vxlangw_endpoint['endpoint'],
                    vxlangw_endpoint['user_id'],
                    vxlangw_endpoint['user_password'],
                    pnf_vlan_info['vlan_id'],
                    vxlangw_pod_id,
                    iaas_network_id,
                    vxlangw_endpoint['timeout'],
                ]
                vxlan_gw_res = vxlangw_instance.create_vxlan_gw(params)

                pattern = re.compile('\|\s+id\s+\|\s+(.*)\s+\|')
                for vxlan_gw in vxlan_gw_res:
                    matchOB = pattern.match(vxlan_gw)
                    if matchOB:
                        rule_id = matchOB.group(1)
                        break

                # Update NAL_PNF_VLAN_MNG(DB Client)
                keys = [pnf_vlan_info['ID']]
                params = {}
                params['update_id'] = operation_id
                params['rule_id'] = rule_id
                db_update.set_context(db_endpoint_pnf_vlan, keys, params)
                db_update.execute()

    def __delete_pnf_vxlangw_tenant(self, job_input, target_network_list):

        # Get JOB Input Parameters
        iaas_region_id = job_input['IaaS_region_id']
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(
                                        self.job_config.REST_URI_PORT)
        db_endpoint_pnf_vlan = self.get_db_endpoint(
                                    self.job_config.REST_URI_PNF_VLAN)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_PNF_VLAN_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['status'] = 1
        db_list.set_context(db_endpoint_pnf_vlan, params)
        db_list.execute()
        pnf_vlan_list = db_list.get_return_param()

        for vlan_res in pnf_vlan_list:

            if vlan_res['network_id'] not in target_network_list:
                continue

            # List NAL_PORT_MNG(DB Client)
            params = {}
            params['network_id'] = vlan_res['network_id']
            params['delete_flg'] = 0
            db_list.set_context(db_endpoint_port, params)
            db_list.execute()
            port_list = db_list.get_return_param()

            if len(port_list) == 0:
                # Create Instance(VXLAN-GW)
                vxlangw_instance = vxlangw.VxlanGwClient(self.job_config)

                vxlangw_endpoint = self.get_os_endpoint_vxlangw(
                                                        iaas_region_id)
                # Delete VXLAN-GW(Rule)
                try:
                    vxlangw_instance.delete_vxlan_gw(
                                        [vxlangw_endpoint['endpoint'],
                                         vxlangw_endpoint['user_id'],
                                         vxlangw_endpoint['user_password'],
                                         vlan_res['rule_id'],
                                         vxlangw_endpoint['timeout']])
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__,
                                              traceback.format_exc())
                    else:
                        raise

                # Update NAL_VIRTUAL_LAN_MNG(DB): Set DeleteFlg On
                params = {}
                params['update_id'] = operation_id
                params['status'] = 2
                params['pod_id'] = ''
                params['tenant_name'] = ''
                params['tenant_id'] = ''
                params['network_id'] = ''
                params['subnet_id'] = ''
                params['port_id'] = ''
                params['rule_id'] = ''
                keys = [vlan_res['ID']]
                db_update.set_context(db_endpoint_pnf_vlan, keys, params)
                db_update.execute()
