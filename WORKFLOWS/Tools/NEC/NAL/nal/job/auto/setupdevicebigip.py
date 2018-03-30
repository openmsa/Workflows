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
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import bigipordercmdws


class SetupDeviceBigIp(base.JobAutoBase):

    def device_setup_create_bigip(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        redundant_configuration_flg = job_input['redundant_configuration_flg']
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        master_msa_device_id = apl_data['master_MSA_device_id']
        slave_msa_device_id = apl_data['slave_MSA_device_id']
        partition_id = apl_data['device_user_name']

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup System Common Setting
        self.__setup_system_common_bigip(job_input,
                                             'act',
                                             pod_id,
                                             master_msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)
        if redundant_configuration_flg == '0':
            self.__setup_system_common_bigip(job_input,
                                                 'sby',
                                                 pod_id,
                                                 slave_msa_device_id,
                                                 msa_config_for_common,
                                                 msa_config_for_device)

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_bigip(job_input,
                                         'act',
                                          pod_id,
                                          master_msa_device_id,
                                          partition_id,
                                          msa_config_for_common,
                                          msa_config_for_device,
                                          apl_data['nic_tenant'])
        if redundant_configuration_flg == '0':
            self.__setup_tenant_vlan_bigip(job_input,
                                             'sby',
                                              pod_id,
                                              slave_msa_device_id,
                                              partition_id,
                                              msa_config_for_common,
                                              msa_config_for_device,
                                              apl_data['nic_tenant'])

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_add_ipv6_for_bigip(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        redundant_configuration_flg = job_input['redundant_configuration_flg']
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        msa_device_id = apl_data['master_MSA_device_id']
        partition_id = apl_data['device_user_name']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup IPv6 Setting
        self.__setup_add_ipv6_bigip(job_input,
                                          'act',
                                          pod_id,
                                          msa_device_id,
                                          partition_id,
                                          msa_config_for_device)
        if redundant_configuration_flg == '0':
            # Setup IPv6 Setting
            self.__setup_add_ipv6_bigip(job_input,
                                          'sby',
                                          pod_id,
                                          msa_device_id,
                                          partition_id,
                                          msa_config_for_device)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, {})

        return job_output

    def device_setup_delete_bigip(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')
        redundant_configuration_flg = job_input['redundant_configuration_flg']
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        master_msa_device_id = apl_data['master_MSA_device_id']
        slave_msa_device_id = apl_data['slave_MSA_device_id']
        partition_id = apl_data['device_user_name']

        master_route_domain_id = self.get_apl_msa_input_params(
                                        apl_data['device_detail_master'],
                                        'create_big_ip_route_domain',
                                        'BIGIP_route_domain',
                                        'rtdomain_id',
                                        job_cleaning_mode)

        if redundant_configuration_flg == '0':
            slave_route_domain_id = self.get_apl_msa_input_params(
                                        apl_data['device_detail_slave'],
                                        'create_big_ip_route_domain',
                                        'BIGIP_route_domain',
                                        'rtdomain_id',
                                        job_cleaning_mode)

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup Tenant VLAN Setting
        self.__unsetup_tenant_vlan_bigip(job_input,
                                         'act',
                                          pod_id,
                                          master_msa_device_id,
                                          partition_id,
                                          master_route_domain_id,
                                          msa_config_for_common,
                                          msa_config_for_device)
        if redundant_configuration_flg == '0':
            self.__unsetup_tenant_vlan_bigip(job_input,
                                             'sby',
                                              pod_id,
                                              slave_msa_device_id,
                                              partition_id,
                                              slave_route_domain_id,
                                              msa_config_for_common,
                                              msa_config_for_device)

        # Setup System Common Setting
        mng_user_account_id = self.get_apl_msa_input_params(
                                        apl_data['device_detail_master'],
                                        'create_big_ip_user_manager',
                                        'BIGIP_User_Manager',
                                        'user_id',
                                        job_cleaning_mode)

        certificate_user_account_id = self.get_apl_msa_input_params(
                                    apl_data['device_detail_master'],
                                    'create_big_ip_user_certificate_manager',
                                    'BIGIP_User_Certificate_Manager',
                                    'user_id',
                                    job_cleaning_mode)

        self.__unsetup_system_common_bigip(job_input,
                                           'act',
                                           pod_id,
                                           master_msa_device_id,
                                           partition_id,
                                           master_route_domain_id,
                                           msa_config_for_common,
                                           msa_config_for_device,
                                           mng_user_account_id,
                                           certificate_user_account_id)

        if redundant_configuration_flg == '0':

            mng_user_account_id_slave = self.get_apl_msa_input_params(
                                        apl_data['device_detail_slave'],
                                        'create_big_ip_user_manager',
                                        'BIGIP_User_Manager',
                                        'user_id',
                                        job_cleaning_mode)

            certificate_user_account_id_slave = self.get_apl_msa_input_params(
                                    apl_data['device_detail_slave'],
                                    'create_big_ip_user_certificate_manager',
                                    'BIGIP_User_Certificate_Manager',
                                    'user_id',
                                    job_cleaning_mode)

            self.__unsetup_system_common_bigip(job_input,
                                            'sby',
                                            pod_id,
                                            slave_msa_device_id,
                                            partition_id,
                                            slave_route_domain_id,
                                            msa_config_for_common,
                                            msa_config_for_device,
                                            mng_user_account_id_slave,
                                            certificate_user_account_id_slave)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __setup_system_common_bigip(self,
                                       job_input,
                                       act_sby,
                                       pod_id,
                                       msa_device_id,
                                       msa_config_for_common,
                                       msa_config_for_device):

        node_detail = {}

        # Create Instance(MSA Soap Client)
        msa = bigipordercmdws.BigIpOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create Partition(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_big_ip_partition',
                                    msa_device_id,
                                    job_input['partition_id']
        )
        node_detail[
            'create_big_ip_partition'] = msa_res[msa.RES_KEY_IN]

        # Create RouteDomain(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_big_ip_route_domain',
                                    msa_device_id,
                                    job_input['partition_id'],
                                    job_input['route_domain_id']
        )
        node_detail[
            'create_big_ip_route_domain'] = msa_res[msa.RES_KEY_IN]

        # Create DefaultRouteDomain(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_big_ip_default_route_domain',
                                    msa_device_id,
                                    job_input['partition_id'],
                                    job_input['route_domain_id']
        )
        node_detail[
            'create_big_ip_default_route_domain'] = msa_res[msa.RES_KEY_IN]

        # Create User Manager(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_big_ip_user_manager',
                                    msa_device_id,
                                    job_input['partition_id'],
                                    job_input['mng_user_account_id'],
                                    'manager',
                                    job_input['mng_account_password']
        )
        node_detail[
            'create_big_ip_user_manager'] = msa_res[msa.RES_KEY_IN]

        # Create User Certificate Manager(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_big_ip_user_certificate_manager',
                                    msa_device_id,
                                    job_input['partition_id'],
                                    job_input['certificate_user_account_id'],
                                    'certificate-manager',
                                    job_input['certificate_account_password']
        )
        node_detail[
            'create_big_ip_user_certificate_manager'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, act_sby, node_detail)

    def __setup_add_ipv6_bigip(self,
                                    job_input,
                                    act_sby,
                                    pod_id,
                                    msa_device_id,
                                    partition_id,
                                    msa_config_for_device):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id = job_input['port_id']
        ipv6_route = '::/0'
        gateway_ipv6_address = job_input['fw_ip_v6_address']
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)
        is_default_gateway = 'yes'
        route_name = 'defaultGWv6'
        destination_ipv6_address = '::'
        destination_ipv6_netmask = '0'

        # List NAL_PORT_MNG(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_pnf_vlan = self.get_db_endpoint(
                                            self.job_config.REST_URI_PNF_VLAN)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()

        port_list = db_list.get_return_param()

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = port_list[0]['network_id']
        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        vlan_list = db_list.get_return_param()
        iaas_network_type = vlan_list[0]['IaaS_network_type']

        # Get VLAN_ID
        if vim_iaas_with_flg == 1 and \
                iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:
            # List NAL_PNF_VLAN_MNG(DB Client)
            params = {}
            params['delete_flg'] = 0
            params['status'] = 1
            params['network_id'] = port_list[0]['network_id']
            db_list.set_context(db_endpoint_pnf_vlan, params)
            db_list.execute()
            pnf_vlan_list = db_list.get_return_param()
            vlan_id = pnf_vlan_list[0]['vlan_id']
        else:
            vlan_id = vlan_list[0]['vlan_id']

        msa_info = json.loads(port_list[0]['msa_info'])
        port_dict = json.loads(port_list[0]['port_info'])

        vip_ip_address_v6 = port_dict['IaaS_port_info']['vip']['ip_address_v6']
        vip_netmask_v6 = port_dict['IaaS_port_info']['vip']['netmask_v6']

        if act_sby == 'act':
            ip_address_v6 = port_dict['IaaS_port_info']['act']['ip_address_v6']
            netmask_v6 = port_dict['IaaS_port_info']['act']['netmask_v6']
        else:
            ip_address_v6 = port_dict['IaaS_port_info']['sby']['ip_address_v6']
            netmask_v6 = port_dict['IaaS_port_info']['sby']['netmask_v6']

        # Create Instance(MSA Soap Client)
        msa = bigipordercmdws.BigIpOrderCommandWs(
                                                  self.job_config,
                                                  self.nal_endpoint_config,
                                                  pod_id)
        # Setting F5BigipPhysicalIpv6
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_f5_big_ip_physical_ipv6',
            msa_device_id,
            partition_id + '_' + vlan_id + '_IP',
            partition_id,
            ip_address_v6,
            netmask_v6,
            partition_id + '_' + vlan_id
        )
        msa_info['create_f5_big_ip_physical_ipv6'] = msa_res[msa.RES_KEY_IN]

        # Setting F5BigipVipIpv6
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_f5_big_ip_ipv6',
            msa_device_id,
            partition_id + '_' + vlan_id + '_VIP',
            partition_id,
            vip_ip_address_v6,
            vip_netmask_v6,
            partition_id + '_' + vlan_id,
            'traffic-group-1'
        )
        msa_info['create_f5_big_ip_ipv6'] = msa_res[msa.RES_KEY_IN]

        # Setting F5BigipIpv6Staticroute
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_f5_big_ip_ipv6_static_route',
            msa_device_id,
            partition_id,
            ipv6_route,
            gateway_ipv6_address,
            is_default_gateway,
            route_name,
            destination_ipv6_address,
            destination_ipv6_netmask
        )
        msa_info[
            'create_f5_big_ip_ipv6_static_route'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, act_sby, port_id, msa_info)

    def __setup_tenant_vlan_bigip(self,
                                      job_input,
                                      act_sby,
                                      pod_id,
                                      msa_device_id,
                                      partition_id,
                                      msa_config_for_common,
                                      msa_config_for_device,
                                      nic_tenant):

        msa_info = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input['port_id4']
        gateway = job_input['fw_ip_address']
        iaas_network_type = job_input['IaaS_network_type']
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)
        route = '0.0.0.0/0'

        # List NAL_VNF_MNG(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_pnf_vlan = self.get_db_endpoint(
                                            self.job_config.REST_URI_PNF_VLAN)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id4
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = port_list[0]['network_id']
        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        vlan_list = db_list.get_return_param()

        # Get VLAN_ID
        if vim_iaas_with_flg == 1 and \
                iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:
            # List NAL_PNF_VLAN_MNG(DB Client)
            params = {}
            params['delete_flg'] = 0
            params['status'] = 1
            params['network_id'] = port_list[0]['network_id']
            db_list.set_context(db_endpoint_pnf_vlan, params)
            db_list.execute()
            pnf_vlan_list = db_list.get_return_param()
            vlan_id = pnf_vlan_list[0]['vlan_id']
        else:
            vlan_id = vlan_list[0]['vlan_id']

        # Create Instance(MSA Soap Client)
        msa = bigipordercmdws.BigIpOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        port_dict = json.loads(port_list[0]['port_info'])

        vip_ip_address = port_dict['IaaS_port_info']['vip']['ip_address']
        vip_netmask = port_dict['IaaS_port_info']['vip']['netmask']

        if act_sby == 'act':
            ip_address = port_dict['IaaS_port_info']['act']['ip_address']
            netmask = port_dict['IaaS_port_info']['act']['netmask']
        else:
            ip_address = port_dict['IaaS_port_info']['sby']['ip_address']
            netmask = port_dict['IaaS_port_info']['sby']['netmask']

        # Create VLAN(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_vlan',
            msa_device_id,
            partition_id,
            partition_id + '_' + vlan_id,
            nic_tenant,
            vlan_id
        )
        msa_info['create_big_ip_vlan'] = msa_res[msa.RES_KEY_IN]

        # Create PhysicalIP(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_physical_ip',
            msa_device_id,
            partition_id,
            partition_id + '_' + vlan_id + '_IP',
            ip_address,
            self.utils.get_subnet_mask_from_cidr_len(netmask),
            partition_id + '_' + vlan_id
        )
        msa_info['create_big_ip_physical_ip'] = msa_res[msa.RES_KEY_IN]

        # Create VIP(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_vip',
            msa_device_id,
            partition_id,
            partition_id + '_' + vlan_id + '_VIP',
            vip_ip_address,
            self.utils.get_subnet_mask_from_cidr_len(vip_netmask),
            partition_id + '_' + vlan_id,
            'traffic-group-1'
        )
        msa_info['create_big_ip_vip'] = msa_res[msa.RES_KEY_IN]

        # Set Staticroute(BIGIP_route)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_route',
            msa_device_id,
            partition_id,
            route,
            gateway
        )
        msa_info['create_big_ip_route'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, act_sby, port_id4, msa_info)

    def __unsetup_system_common_bigip(self,
                                       job_input,
                                       act_sby,
                                       pod_id,
                                       msa_device_id,
                                       partition_id,
                                       route_domain_id,
                                       msa_config_for_common,
                                       msa_config_for_device,
                                       mng_user_account_id,
                                       certificate_user_account_id):

        # Create Instance(MSA Soap Client)
        msa = bigipordercmdws.BigIpOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        try:
            # Delete User Certificate Manager(MSA)
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_big_ip_user_certificate_manager',
                                    msa_device_id,
                                    partition_id,
                                    certificate_user_account_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete User Manager(MSA)
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_big_ip_user_manager',
                                    msa_device_id,
                                    partition_id,
                                    mng_user_account_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete DefaultRouteDomain(MSA)
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_big_ip_default_route_domain',
                                    msa_device_id,
                                    partition_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete RouteDomain(MSA)
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_big_ip_route_domain',
                                    msa_device_id,
                                    partition_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete Partition(MSA)
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_big_ip_partition',
                                    msa_device_id,
                                    partition_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

    def __unsetup_tenant_vlan_bigip(self,
                                      job_input,
                                      act_sby,
                                      pod_id,
                                      msa_device_id,
                                      partition_id,
                                      route_domain_id,
                                      msa_config_for_common,
                                      msa_config_for_device):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)
        route_name = 'defaultGWv6'
        route = '0.0.0.0/0'
        self_ipv6_end_number = 1

        # List NAL_VNF_MNG(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_pnf_vlan = self.get_db_endpoint(
                                            self.job_config.REST_URI_PNF_VLAN)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['node_id'] = node_id
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        ip_address_v6 = port_list[0].get('ip_address_v6', '')

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = port_list[0]['network_id']
        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        vlan_list = db_list.get_return_param()
        iaas_network_type = vlan_list[0]['IaaS_network_type']

        # Get VLAN_ID
        if vim_iaas_with_flg == 1 and \
                iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:
            # List NAL_PNF_VLAN_MNG(DB Client)
            params = {}
            params['delete_flg'] = 0
            params['status'] = 1
            params['network_id'] = port_list[0]['network_id']
            db_list.set_context(db_endpoint_pnf_vlan, params)
            db_list.execute()
            pnf_vlan_list = db_list.get_return_param()
            vlan_id = pnf_vlan_list[0]['vlan_id']
        else:
            vlan_id = vlan_list[0]['vlan_id']

        # Create Instance(MSA Soap Client)
        msa = bigipordercmdws.BigIpOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)
        if ip_address_v6 != '':
            try:
                # Delete IPv6Staticroute(MSA Soap Client)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_f5_big_ip_ipv6_static_route',
                    msa_device_id,
                    partition_id,
                    route_name
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        else:
            pass

        try:
            # Delete IPv4Staticroute(MSA Soap Client)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_big_ip_route',
                msa_device_id,
                partition_id,
                route
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        if ip_address_v6 != '':
            try:
                # Delete F5BigipVipIpv6(MSA Soap Client)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_f5_big_ip_ipv6',
                    msa_device_id,
                    partition_id + '_' + vlan_id + '_VIP',
                    partition_id,
                    self_ipv6_end_number,
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        else:
            pass

        if ip_address_v6 != '':
            try:
                # Delete F5BigipPhysicalIpv6(MSA Soap Client)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_f5_big_ip_physical_ipv6',
                    msa_device_id,
                    partition_id + '_' + vlan_id + '_IP',
                    partition_id,
                    self_ipv6_end_number
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        else:
            pass

        try:
            # Delete VIP(MSA Soap Client)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_big_ip_vip',
                msa_device_id,
                partition_id,
                partition_id + '_' + vlan_id + '_VIP'
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete PhysicalIP(MSA Soap Client)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_big_ip_physical_ip',
                msa_device_id,
                partition_id,
                partition_id + '_' + vlan_id + '_IP'
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete VIP(MSA Soap Client)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_big_ip_vlan',
                msa_device_id,
                partition_id,
                partition_id + '_' + vlan_id
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

    def __get_db_apl(self, job_input):

        node_id = job_input['node_id']

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_VNF_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['node_id'] = node_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        return apl_list[0]

    def __update_db_apl(self, job_input, act_sby, node_detail_update):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        node_id = job_input['node_id']

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_VNF_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['node_id'] = node_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        if act_sby == 'act':
            node_detail_dict = json.loads(apl_list[0]['device_detail_master'])
        else:
            node_detail_dict = json.loads(apl_list[0]['device_detail_slave'])
        node_detail_dict.update(node_detail_update)

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [apl_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        if act_sby == 'act':
            params['device_detail_master'] = json.dumps(node_detail_dict)
        else:
            params['device_detail_slave'] = json.dumps(node_detail_dict)
        db_update.set_context(db_endpoint, keys, params)
        db_update.execute()

    def __update_db_port(self, job_input, act_sby, port_id, msa_info):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_VNF_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        wk = {}
        wk[act_sby] = msa_info
        msa_info_dict = json.loads(port_list[0]['msa_info'])
        msa_info_dict.update(msa_info_dict)

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['msa_info'] = json.dumps(msa_info_dict)
        db_update.set_context(db_endpoint, keys, params)
        db_update.execute()
