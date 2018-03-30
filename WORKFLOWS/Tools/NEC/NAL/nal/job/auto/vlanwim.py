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

from job.auto import base
from job.auto.extension import routingpod
from job.lib.db import create
from job.lib.db import list
from job.lib.db import update
from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import ports
from job.lib.openstack.quantum import subnets
from job.lib.script import vxlangw


class VlanWim(base.JobAutoBase):

    IAAS_PORT_NAME = '#used-NFVI#'

    def tenant_vlan_port_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get VLAN
        vlan_list = self.__get_vlan(job_input)

        if vim_iaas_with_flg == 0:
            # Create VLAN
            if len(vlan_list) == 0:
                vlan_res = self.__create_vlan(job_input)
                network_id = vlan_res['network_id']
                vlan_id = vlan_res['vlan_id']
            else:
                network_id = vlan_list[0]['network_id']
                vlan_id = vlan_list[0]['vlan_id']

            # Create Port(ce2)
            ce02 = self.__create_port_tenant(job_input, network_id, vlan_id)
            # Create Port(ce1)
            ce01 = self.__create_port_tenant(job_input, network_id, vlan_id)
            # Create Port(vrrp)
            vrrp = self.__create_port_tenant(job_input, network_id, vlan_id)

            # Set JOB Output Parameters
            job_output = {}
            job_output['vrrp'] = vrrp
            job_output['ce01'] = ce01
            job_output['ce02'] = ce02
        else:
            # Create VLAN
            if len(vlan_list) == 0:
                vlan_res = self.__login_vlan(job_input)
                IaaS_network_id = vlan_res['IaaS_network_id']
                vlan_id = vlan_res['vlan_id']
            else:
                IaaS_network_id = vlan_list[0]['IaaS_network_id']
                vlan_id = vlan_list[0]['vlan_id']

            # Create Port(ce2)
            ce02 = self.__create_port_tenant_iaas(job_input,
                                             IaaS_network_id, vlan_id)
            # Create Port(ce1)
            ce01 = self.__create_port_tenant_iaas(job_input,
                                             IaaS_network_id, vlan_id)
            # Create Port(vrrp)
            vrrp = self.__create_port_tenant_iaas(job_input,
                                             IaaS_network_id, vlan_id)

            # Set JOB Output Parameters
            job_output = {}
            job_output['vrrp'] = vrrp
            job_output['ce01'] = ce01
            job_output['ce02'] = ce02

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_tenant_vlan_add_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get VLAN
        vlan_list = self.__get_vlan(job_input)

        if len(vlan_list) == 0:
            raise SystemError('Tenant VLAN not Found.')

        network_id = vlan_list[0]['network_id']
        vlan_id = vlan_list[0]['vlan_id']

        # Create Port
        job_output = self.__add_port_tenant_ipv6(
                                            job_input, network_id, vlan_id)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def tenant_vlan_port_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Delete Port
        logical_delete_apl_port_list = self.__delete_port_tenant(job_input)

        # Set JOB Output Parameters
        job_output = {
            'logical_delete_apl_port_list': logical_delete_apl_port_list
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def tenant_vlan_port_iaas_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        dc_id = job_input['data']['dc_id']
        pod_id = job_input['data']['pod_id']

        job_input2 = {
            'dc_id': dc_id,
            'pod_id': pod_id
        }

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input2)

        if vim_iaas_with_flg == 0:
            # Delete Port(IaaS)
            target_network_list = self.__delete_port_tenant_iaas(job_input)

            # Delete VLAN
            self.__delete_vlan(job_input, target_network_list)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def wan_vlan_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        virtual_lan_list = []
        # Create Network
        if job_input['group_type'] in [
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
            ]:

            idc_network_info = self.get_os_network_info(
                                            job_input['pod_id'],
                                            job_input['nal_tenant_id'],
                                            self.job_config.NW_NAME_IDC,
                                            '',
                                            job_input['dc_id'])

            network_id = idc_network_info['network_id']
        else:
            virtual_lan_wan = self.__create_network_wan(job_input)
            network_id = virtual_lan_wan['network_id']
            virtual_lan_list.append(virtual_lan_wan)

        # Set JOB Output Parameters
        job_output = {
            'wan_network_id': network_id,
            'virtual_lan_list': virtual_lan_list
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def wan_vlan_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Delete Port
        logical_delete_apl_port_list = self.__delete_port_wan(job_input)

        # Delete Network
        logical_delete_vlan_list = []
        if job_input['group_type'] not in [
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
            ]:
            logical_delete_vlan_list = self.__delete_network_wan(job_input)

        # Set JOB Output Parameters
        job_output = {
            'logical_delete_apl_port_list': logical_delete_apl_port_list,
            'logical_delete_vlan_list': logical_delete_vlan_list
        }

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
        dc_id = job_input['dc_id']

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
        rule_id = ''

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
        params['vlan_id'] = iaas_segmentation_id
        params['network_id'] = iaas_network_id
        params['rule_id'] = rule_id
        params['nal_vlan_info'] = {}
        db_create_instance.set_context(db_endpoint_vlan, params)
        db_create_instance.execute()

        return {'IaaS_network_id': iaas_network_id,
                'vlan_id': iaas_segmentation_id}

    def __delete_vlan(self, job_input, target_network_list):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['data']['nal_tenant_id']
        operation_id = job_input['data']['operation_id']
        pod_id = job_input['data']['pod_id']
        dc_id = job_input['data'].get('dc_id', 'system')
        job_cleaning_mode = job_input['data'].get('job_cleaning_mode', '0')

        # Get MSA Info(network_id)
        msa_network_id = job_input['data']['msa_network_id']

        # Get Network Info
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            '',
                                            dc_id)

        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            '',
                                            dc_id)

        network_id_list = [msa_network_id,
                           pub_network_info['network_id'],
                           ext_network_info['network_id']]

        if job_input['data']['group_type'] in [
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
            ]:

            idc_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_IDC,
                                            '',
                                            dc_id)
            network_id_list.append(idc_network_info['network_id'])

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                            pod_id, '', nal_tenant_id, dc_id)

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

        # List NAL_VIRTUAL_LAN_MNG(DB)
        params = {}
        params['delete_flg'] = 0
        params['pod_id'] = pod_id
        params['nal_tenant_id'] = nal_tenant_id
        db_list_instance.set_context(db_endpoint_vlan, params)
        db_list_instance.execute()
        vlan_list = db_list_instance.get_return_param()

        for vlan_res in vlan_list:

            vlan_rec_id = vlan_res['ID']
            vlan_network_id = vlan_res['network_id']
            iaas_network_type = vlan_res['IaaS_network_type']
            rule_id = vlan_res['rule_id']

            if vlan_network_id in network_id_list:
                continue

            if vlan_network_id not in target_network_list:
                continue

            # List NAL_PORT_MNG(DB)
            params = {}
            params['delete_flg'] = 0
            params['pod_id'] = pod_id
            params['nal_tenant_id'] = nal_tenant_id
            params['network_id'] = vlan_network_id
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list = db_list_instance.get_return_param()

            if len(port_list) == 0:

                try:
                    # Delete Network(OpenStack:VIM)
                    osc_networks.delete_network(
                                os_endpoint_vim, vlan_network_id)
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__,
                                                traceback.format_exc())
                    else:
                        raise

                # Delete VXLAN-GW Rule
                if iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:
                    params = [rule_id, self.job_config.PROV_TIMEOUT]
                    try:
                        vxlangw_instance.delete_vxlan_gw(params)
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                traceback.format_exc())
                        else:
                            raise

                # Update NAL_VIRTUAL_LAN_MNG(DB)
                params = {}
                params['update_id'] = operation_id
                params['delete_flg'] = 1
                keys = [vlan_rec_id]
                db_update_instance.set_context(db_endpoint_vlan, keys, params)
                db_update_instance.execute()

    def __create_port_tenant(self, job_input, network_id, vlan_id):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_subnet_id = job_input['IaaS_subnet_id']
        network_name = job_input['network_name']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']

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
        db_list_instance = list.ListClient(self.job_config)

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
                                    free_ip_iaas['id'], free_ip_iaas['ip'])

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
        subnet_exists_flg = False
        subnet_id = ''
        subnet_list = os_subnets_instance.list_subnets(os_endpoint_vim)

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
        params['node_id'] = ''
        params['IaaS_region_id'] = iaas_region_id
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['IaaS_network_id'] = iaas_network_id
        params['IaaS_subnet_id'] = iaas_subnet_id
        params['IaaS_port_id'] = iaas_port_id
        params['nic'] = ''
        params['ip_address'] = ip_address
        params['netmask'] = free_ip_iaas['netmask']
        params['port_info'] = json.dumps(port_info)
        params['msa_info'] = json.dumps({})

        db_create_instance.set_context(db_endpoint_port, params)
        db_create_instance.execute()

        # List NAL_PORT_MNG(DB)
        params = {}
        params['port_id'] = port_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Set Output Parameters
        output = {}
        output['network_id'] = port_list[0]['network_id']
        output['port_id'] = port_list[0]['port_id']
        output['ip_address'] = port_list[0]['ip_address']
        output['netmask'] = port_list[0]['netmask']
        output['rec_id'] = port_list[0]['ID']
        output['subnet_ip_address'] = free_ip_iaas['subnet_ip']
        output['IaaS_subnet_id'] = free_ip_iaas['id']
        output['vlan_id'] = vlan_id

        return output

    def __create_port_tenant_iaas(self, job_input,
                                        network_id,
                                        vlan_id,
                                        mac_address=''):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_subnet_id = job_input['IaaS_subnet_id']
#         network_name = job_input['network_name']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                '',
                                                nal_tenant_id)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(OpenStack Client)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

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
        params['node_id'] = ''
        params['IaaS_region_id'] = iaas_region_id
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['IaaS_network_id'] = iaas_network_id
        params['IaaS_subnet_id'] = iaas_subnet_id
        params['IaaS_port_id'] = iaas_port_id
        params['nic'] = ''
        params['ip_address'] = ip_address
        params['netmask'] = free_ip_iaas['netmask']
        params['port_info'] = json.dumps(port_info)
        params['msa_info'] = json.dumps({})

        db_create_instance.set_context(db_endpoint_port, params)
        db_create_instance.execute()

        # List NAL_PORT_MNG(DB)
        params = {}
        params['port_id'] = port_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Set Output Parameters
        output = {}
        output['network_id'] = port_list[0]['network_id']
        output['port_id'] = port_list[0]['port_id']
        output['ip_address'] = port_list[0]['ip_address']
        output['netmask'] = port_list[0]['netmask']
        output['rec_id'] = port_list[0]['ID']
        output['subnet_ip_address'] = free_ip_iaas['subnet_ip']
        output['IaaS_subnet_id'] = free_ip_iaas['id']
        output['vlan_id'] = vlan_id

        return output

    def __add_port_tenant_ipv6(self, job_input, network_id, vlan_id):

        output = {}

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        iaas_subnet_id = job_input['IaaS_subnet_id']
        iaas_subnet_id_v6 = job_input['IaaS_subnet_id_v6']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        vrrp_address = job_input['vrrp_address']
        ce1_address = job_input['ce1_address']
        ce2_address = job_input['ce2_address']

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
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(OpenStack Client)
        os_subnets_instance = subnets.OscQuantumSubnets(self.job_config)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # Get Subnet(OpenStack:IaaS)
        iaas_subnet_res = os_subnets_instance.get_subnet(
                                os_endpoint_iaas, iaas_subnet_id_v6)

        iaas_cidr_wk = self.utils.get_cidr_compressed(
                                    iaas_subnet_res['subnet']['cidr'])
        iaas_cidr = iaas_cidr_wk['cidr']
        subnet_ip_v6 = iaas_cidr_wk['ip']
        netmask_v6 = iaas_cidr_wk['netmask']

        # List NAL_PORT_MNG(DB)
        params = {}
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['IaaS_network_id'] = iaas_network_id
        params['IaaS_subnet_id'] = iaas_subnet_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list_v4 = db_list_instance.get_return_param()

        for port_res in port_list_v4:

            if port_res['ip_address'] == vrrp_address:
                port_vrrp = port_res

            if port_res['ip_address'] == ce1_address:
                port_ce1 = port_res

            if port_res['ip_address'] == ce2_address:
                port_ce2 = port_res

        # Add IPv6 Tenant LAN(CE1,CE2)
        for router_name, port_ce in {
                self.job_config.VM_ROUTER_NODE_NAME1: port_ce1,
                self.job_config.VM_ROUTER_NODE_NAME2: port_ce2,
            }.items():
            port_id_vim = port_ce['port_id']
            port_id_iaas = port_ce['IaaS_port_id']
            if vim_iaas_with_flg == 0:
                # Get Port(OpenStack:IaaS)
                iaas_port_res = os_ports_instance.get_port(
                                                os_endpoint_iaas, port_id_iaas)

                fixed_ips_iaas = iaas_port_res['port']['fixed_ips']
                fixed_ips_iaas.append({'subnet_id': iaas_subnet_id_v6})

                # Update Port(OpenStack:IaaS)
                os_upd_port_iaas = os_ports_instance.update_port(
                                                            os_endpoint_iaas,
                                                            port_id_iaas,
                                                            None,
                                                            None,
                                                            fixed_ips_iaas)

                fixed_ips_iaas = os_upd_port_iaas['port']['fixed_ips']

                for fixed_ip in fixed_ips_iaas:
                    if fixed_ip['subnet_id'] == iaas_subnet_id_v6:
                        ip_address_v6 = self.utils.get_ipaddress_compressed(
                                                        fixed_ip['ip_address'])
                        break

                # List Subnets(OpenStack:VIM)
                subnet_list = os_subnets_instance.list_subnets(os_endpoint_vim)

                subnet_exists_flg = False
                subnet_id = ''
                for rec in subnet_list['subnets']:

                    vim_cidr = self.utils.get_cidr_compressed(rec['cidr'])

                    if rec['network_id'] == network_id \
                                            and vim_cidr['cidr'] == iaas_cidr:
                        subnet_exists_flg = True
                        subnet_id = rec['id']
                        break

                if subnet_exists_flg == False:
                    # Create Subnet(OpenStack:VIM)
                    os_subnet_cre_vim = os_subnets_instance.create_subnet(
                                                        os_endpoint_vim,
                                                        network_id,
                                                        iaas_cidr,
                                                        '',
                                                        nal_tenant_id,
                                                        self.utils.IP_VER_V6)
                    subnet_id = os_subnet_cre_vim['subnet']['id']

                # Get Port(OpenStack:VIM)
                os_port_res_vim = os_ports_instance.get_port(
                                                os_endpoint_vim, port_id_vim)

                fixed_ips_vim = os_port_res_vim['port']['fixed_ips']
                fixed_ips_vim.append(
                    {'subnet_id': subnet_id, 'ip_address': ip_address_v6})

                # Update Port(OpenStack:VIM)
                os_port_upd_vim = os_ports_instance.update_port(
                                                            os_endpoint_vim,
                                                            port_id_vim,
                                                            None,
                                                            None,
                                                            fixed_ips_vim)

            else:
                # Get Port(OpenStack:VIM)
                vim_port_res = os_ports_instance.get_port(
                                                os_endpoint_vim, port_id_vim)

                fixed_ips_vim = vim_port_res['port']['fixed_ips']
                fixed_ips_vim.append({'subnet_id': iaas_subnet_id_v6})

                # Update Port(OpenStack:IaaS)
                os_port_upd_vim = os_ports_instance.update_port(
                                                            os_endpoint_vim,
                                                            port_id_vim,
                                                            None,
                                                            None,
                                                            fixed_ips_vim)

                fixed_ips_vim = os_port_upd_vim['port']['fixed_ips']

                for fixed_ip in fixed_ips_vim:
                    if fixed_ip['subnet_id'] == iaas_subnet_id_v6:
                        ip_address_v6 = self.utils.get_ipaddress_compressed(
                                                        fixed_ip['ip_address'])
                        break

            # Update NAL_PORT_MNG(DB Client)
            keys = [port_ce['ID']]
            params = {}
            params['update_id'] = operation_id
            params['IaaS_subnet_id_v6'] = iaas_subnet_id_v6
            params['ip_address_v6'] = ip_address_v6
            params['netmask_v6'] = netmask_v6
            params['port_info'] = json.dumps(os_port_upd_vim['port'])
            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

            # Set Output Parameters
            output[router_name] = {}
            output[router_name]['network_id'] = port_ce['network_id']
            output[router_name]['port_id'] = port_id_vim
            output[router_name]['ip_address'] = ip_address_v6
            output[router_name]['netmask'] = netmask_v6
            output[router_name]['rec_id'] = port_ce['ID']
            output[router_name]['subnet_ip_address'] = subnet_ip_v6
            output[router_name]['IaaS_subnet_id'] = iaas_subnet_id_v6
            output[router_name]['vlan_id'] = vlan_id
            output[router_name]['nic'] = port_ce['nic']

        if vim_iaas_with_flg == 0:
            vrrp_address = 'fe80::f' + format(int(vlan_id), 'x')
        else:
            if int(vlan_id) <= 65535:
                vrrp_address = 'fe80::' + format(int(vlan_id), 'x')
            else:
                end_address = format(int(vlan_id), 'x')[-4:]
                second_address = format(int(vlan_id), 'x')[:-4]
                vrrp_address = 'fe80::' + second_address + ':' + end_address

        # Set Output Parameters(vrrp)
        output['vrrp'] = {}
        output['vrrp']['network_id'] = port_vrrp['network_id']
        output['vrrp']['port_id'] = port_vrrp['port_id']
        output['vrrp']['ip_address'] = self.utils.get_ipaddress_compressed(
                                                                vrrp_address)
        output['vrrp']['netmask'] = ''
        output['vrrp']['rec_id'] = port_vrrp['ID']
        output['vrrp']['subnet_ip_address'] = ''
        output['vrrp']['IaaS_subnet_id'] = ''
        output['vrrp']['vlan_id'] = vlan_id

        return output

    def __delete_port_tenant(self, job_input):

        # Get JOB Input Parameters
        tenant_lan_list = job_input['tenant_lan_list']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        operation_id = job_input['operation_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                '',
                                                nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        logical_delete_apl_port_list = []
        for tenant_lan in tenant_lan_list:

            try:
                # Delete Port(OpenStack:VIM)
                os_ports_instance.delete_port(os_endpoint_vim,
                                 tenant_lan['port_id'])
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__,
                                          traceback.format_exc())
                else:
                    raise

            logical_delete_apl_port_list.append(
                {
                    'search': {
                        'delete_flg': 0,
                        'tenant_id': nal_tenant_id,
                        'apl_type': 1,
                        'port_id': tenant_lan['port_id'],
                    },
                    'params': {
                        'update_id': operation_id,
                        'delete_flg': 1,
                    }
                }
            )

        return logical_delete_apl_port_list

    def __delete_port_tenant_iaas(self, job_input):

        # Get JOB Input Parameters
        iaas_region_id = job_input['data']['IaaS_region_id']
        iaas_tenant_id = job_input['data']['IaaS_tenant_id']
        tenant_lan_list = job_input['data']['tenant_lan_list']
        dc_id = job_input['data']['dc_id']
        job_cleaning_mode = job_input['data'].get('job_cleaning_mode', '0')

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                '',
                                                iaas_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        target_network_list = []
        for tenant_lan in tenant_lan_list:

            try:
                # Delete Port(OpenStack:VIM)
                os_ports_instance.delete_port(os_endpoint_iaas,
                                 tenant_lan['IaaS_port_id'])
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            target_network_list.append(tenant_lan['network_id'])

        return target_network_list

    def __delete_port_wan(self, job_input):

        # Get JOB Input Parameters
        wan_lan_list = job_input['wan_lan_list']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        operation_id = job_input['operation_id']
        logical_delete_apl_port_list \
                = job_input['logical_delete_apl_port_list']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id,
                                                '',
                                                nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        for wan_lan in wan_lan_list:

            wan_port_id = wan_lan['port_id']

            if len(wan_port_id) > 0:

                try:
                    # Delete Port(OpenStack:VIM)
                    os_ports_instance.delete_port(os_endpoint_vim,
                                                        wan_port_id)
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__,
                                              traceback.format_exc())
                    else:
                        raise

            logical_delete_apl_port_list.append(
                {
                    'search': {
                        'delete_flg': 0,
                        'tenant_id': nal_tenant_id,
                        'apl_type': 1,
                        'port_id': wan_port_id,
                    },
                    'params': {
                        'update_id': operation_id,
                        'delete_flg': 1,
                    }
                }
            )

        return logical_delete_apl_port_list

    def __create_network_wan(self, job_input):

        # Get JOB Input Parameters
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        operation_id = job_input['operation_id']
        tenant_name = job_input['tenant_name']

        nal_tenant_id = job_input['nal_tenant_id']
        nal_tenant_name = job_input['nal_tenant_name']
        pod_id = job_input['pod_id']

        dc_id = job_input['dc_id']
        dc_name = job_input['dc_name']
        dc_vlan_id = job_input.get('dc_vlan_id', None)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                            pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_networks = networks.OscQuantumNetworks(self.job_config)

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)
        if vim_iaas_with_flg == 0:
            physical_network_name = None
        else:
            physical_network_name = self.get_os_physical_network_name()
        # Create Network(OpenStack:VIM)
        network_name_vim = dc_name + nal_tenant_name
        os_network_res = osc_networks.create_network(os_endpoint_vim,
                                            network_name_vim, True, False,
                                            dc_vlan_id, physical_network_name)
        wan_network_id = os_network_res['network']['id']
        wan_segmentation_id \
                    = os_network_res['network']['provider:segmentation_id']

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
        params['IaaS_network_id'] = ''
        params['IaaS_network_type'] = ''
        params['IaaS_segmentation_id'] = ''
        params['vlan_id'] = wan_segmentation_id
        params['network_id'] = wan_network_id
        params['rule_id'] = ''
        params['nal_vlan_info'] = json.dumps(os_network_res['network'])

        return params

    def __delete_network_wan(self, job_input):

        # Get JOB Input Parameters
        wan_lan_list = job_input['wan_lan_list']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        operation_id = job_input['operation_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        logical_delete_vlan_list = []

        if len(wan_lan_list) > 0:

            # Get Endpoint(OpenStack:VIM)
            os_endpoint_vim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

            # Create Instance(OpenStack Client)
            osc_networks = networks.OscQuantumNetworks(self.job_config)

            # Delete Network(OpenStack:VIM)
            wan_network_id = wan_lan_list[0]['network_id']
            try:
                osc_networks.delete_network(os_endpoint_vim, wan_network_id)
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            logical_delete_vlan_list.append(
                {
                    'search': {
                        'delete_flg': 0,
                        'tenant_id': nal_tenant_id,
                        'network_id': wan_network_id,
                    },
                    'params': {
                        'update_id': operation_id,
                        'delete_flg': 1,
                    }
                }
            )

        return logical_delete_vlan_list
