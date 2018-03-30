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
from job.lib.soap.msa import fortigateordercmdws


class SetupDeviceFortigate(base.JobAutoBase):

    def device_setup_create_for_fortigate(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        master_msa_device_id = apl_data['master_MSA_device_id']
        vdom_name = apl_data['device_user_name']

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup System Common Setting
        self.__setup_system_common_fortigate(job_input,
                                             pod_id,
                                             master_msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)

        # Setup Pub LAN Setting
        self.__setup_pub_lan_fortigate(job_input,
                                       pod_id,
                                       master_msa_device_id,
                                       msa_config_for_common,
                                       msa_config_for_device,
                                       apl_data['nic_public'])

        # Setup Ext LAN Setting
        self.__setup_ext_lan_fortigate(job_input,
                                       pod_id,
                                       master_msa_device_id,
                                       msa_config_for_common,
                                       msa_config_for_device,
                                       apl_data['nic_external'])

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_fortigate(job_input,
                                           pod_id,
                                           master_msa_device_id,
                                           vdom_name,
                                           msa_config_for_common,
                                           msa_config_for_device,
                                           apl_data['nic_tenant'])

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_add_port_for_fortigate(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        master_msa_device_id = apl_data['master_MSA_device_id']
        vdom_name = apl_data['device_user_name']

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_fortigate(job_input,
                                           pod_id,
                                           master_msa_device_id,
                                           vdom_name,
                                           msa_config_for_common,
                                           msa_config_for_device,
                                           apl_data['nic_tenant'])

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_add_ipv6_for_fortigate(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        msa_device_id = apl_data['master_MSA_device_id']
        vdom_name = apl_data['device_user_name']
        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup Device(IPv6)
        self.__setup_fortigate_add_ipv6(job_input,
                                             pod_id,
                                             vdom_name,
                                             msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device,
                                             apl_data)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_delete_for_fortigate(self, job_input):

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

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        msa_device_id = apl_data['master_MSA_device_id']
        vdom_name = apl_data['device_user_name']

        user_account_id = self.get_apl_msa_input_params(
                                        apl_data['device_detail_master'],
                                        'create_fortigate_admin_user',
                                        'FortiAdminUserProvPNF',
                                        'user_name',
                                        job_cleaning_mode)

        admin_prof = self.get_apl_msa_input_params(
                                        apl_data['device_detail_master'],
                                        'create_fortigate_admin_user',
                                        'FortiAdminUserProvPNF',
                                        'admin_prof',
                                        job_cleaning_mode)

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # UnSetup Tenant VLAN Setting
        self.__unsetup_tenant_vlan_fortigate(job_input,
                                           pod_id,
                                           msa_device_id,
                                           vdom_name,
                                           msa_config_for_common,
                                           msa_config_for_device)

        # UnSetup Ext LAN Setting
        self.__unsetup_ext_lan_fortigate(job_input,
                                       pod_id,
                                       msa_device_id,
                                       vdom_name,
                                       msa_config_for_common,
                                       msa_config_for_device,
                                       apl_data['nic_external'])

        # UnSetup Pub LAN Setting
        self.__unsetup_pub_lan_fortigate(job_input,
                                       pod_id,
                                       msa_device_id,
                                       vdom_name,
                                       msa_config_for_common,
                                       msa_config_for_device,
                                       apl_data['nic_public'])

        # UnSetup System Common Setting
        self.__unsetup_system_common_fortigate(job_input,
                                             pod_id,
                                             msa_device_id,
                                             vdom_name,
                                             msa_config_for_common,
                                             msa_config_for_device,
                                             user_account_id,
                                             admin_prof)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_delete_port_for_fortigate(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        iaas_network_id = job_input['IaaS_network_id']

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        msa_device_id = apl_data['master_MSA_device_id']
        vdom_name = apl_data['device_user_name']

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # UnSetup Tenant VLAN Setting
        self.__unsetup_tenant_vlan_fortigate(job_input,
                                           pod_id,
                                           msa_device_id,
                                           vdom_name,
                                           msa_config_for_common,
                                           msa_config_for_device,
                                           iaas_network_id)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __setup_fortigate_add_ipv6(self,
                                job_input,
                                pod_id,
                                vdom_name,
                                msa_device_id,
                                msa_config_for_common,
                                msa_config_for_device,
                                db_apl_data):

        # Get JOB Input Parameters
        node_id = job_input['node_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id = job_input['port_id']
        port_id_pub_ipv6 = job_input['port_id_pub_ipv6']
        port_id_ext_ipv6 = job_input['port_id_ext_ipv6']
        management_flg = 'yes'
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Network Info
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
        # Create Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                        self.job_config,
                                        self.nal_endpoint_config,
                                        pod_id)

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
        if len(port_id) != 0:
            params['port_id'] = port_id

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        for rec in port_list:

            if rec['network_id'] != pub_network_info['network_id'] \
                    and rec['network_id'] != ext_network_info['network_id']:

                params = {}
                params['delete_flg'] = 0
                params['tenant_id'] = nal_tenant_id
                params['network_id'] = rec['network_id']
                db_list.set_context(db_endpoint_vlan, params)
                db_list.execute()
                vlan_list = db_list.get_return_param()
                iaas_net_type = vlan_list[0]['IaaS_network_type']

                # Get VLAN_ID
                if vim_iaas_with_flg == 1 and \
                        iaas_net_type.upper() == self.job_config.NW_TYPE_VXLAN:
                    # List NAL_PNF_VLAN_MNG(DB Client)
                    params = {}
                    params['delete_flg'] = 0
                    params['status'] = 1
                    params['network_id'] = rec['network_id']
                    db_list.set_context(db_endpoint_pnf_vlan, params)
                    db_list.execute()
                    pnf_vlan_list = db_list.get_return_param()
                    vlan_id = pnf_vlan_list[0]['vlan_id']
                else:
                    vlan_id = vlan_list[0]['vlan_id']

            if len(port_id_pub_ipv6) > 0:

                # Get NAL_PORT_MNG(Pub)
                port_res_pub = self.__get_db_port(
                                        nal_tenant_id, '', port_id_pub_ipv6)

                msa_info_pub = json.loads(port_res_pub[0]['msa_info'])

                # Create Interface IPv6(MSA) Pub
                msa_res = self.execute_msa_command(
                            msa_config_for_device,
                            msa,
                            'create_fortigate_vlan_ipv6_interface',
                            msa_device_id,
                            vdom_name + '_' + str(pub_network_info['vlan_id']),
                            vdom_name,
                            str(pub_network_info['vlan_id']),
                            db_apl_data['nic_public'],
                            'no',
                            port_res_pub[0]['ip_address_v6'],
                            port_res_pub[0]['netmask_v6'],
                )
                msa_info_pub['create_fortigate_vlan_ipv6_interface']\
                                = msa_res[msa.RES_KEY_IN]

                # Update NAL_PORT_MNG(DB) Pub
                self.__update_db_port(job_input, port_id_pub_ipv6,
                                      msa_info_pub)

            if len(port_id_ext_ipv6) > 0:

                # Get NAL_PORT_MNG(Ext)
                port_res_ext = self.__get_db_port(
                                        nal_tenant_id, '', port_id_ext_ipv6)

                msa_info_ext = json.loads(port_res_ext[0]['msa_info'])

                # Create Interface IPv6(MSA) Ext
                msa_res = self.execute_msa_command(
                            msa_config_for_device,
                            msa,
                            'create_fortigate_vlan_ipv6_interface',
                            msa_device_id,
                            vdom_name + '_' + str(ext_network_info['vlan_id']),
                            vdom_name,
                            str(ext_network_info['vlan_id']),
                            db_apl_data['nic_external'],
                            'no',
                            port_res_ext[0]['ip_address_v6'],
                            port_res_ext[0]['netmask_v6'],
                )
                msa_info_ext['create_fortigate_vlan_ipv6_interface']\
                         = msa_res[msa.RES_KEY_IN]

                # Update NAL_PORT_MNG(DB) Ext
                self.__update_db_port(job_input, port_id_ext_ipv6,
                                      msa_info_ext)

            # Get NAL_PORT_MNG(Tenant VLAN)
            port_res_tenant = self.__get_db_port(nal_tenant_id, '', port_id)

            msa_info_tenant = json.loads(port_res_tenant[0]['msa_info'])

            # Create Interface IPv6(MSA) Tenant
            msa_res = self.execute_msa_command(
                                msa_config_for_device,
                                msa,
                                'create_fortigate_vlan_ipv6_interface',
                                msa_device_id,
                                vdom_name + '_' + str(vlan_id),
                                vdom_name,
                                str(vlan_id),
                                db_apl_data['nic_tenant'],
                                management_flg,
                                port_res_tenant[0]['ip_address_v6'],
                                port_res_tenant[0]['netmask_v6'],
            )
            msa_info_tenant['create_fortigate_vlan_ipv6_interface']\
                     = msa_res[msa.RES_KEY_IN]

            # Update NAL_PORT_MNG(DB) Tenant VLAN
            self.__update_db_port(job_input, port_id, msa_info_tenant)

    def __get_db_port(self, nal_tenant_id, node_id, port_id=''):

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_PORT_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id

        if len(node_id) > 0:
            params['node_id'] = node_id

        if len(port_id) > 0:
            params['port_id'] = port_id

        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        return port_list

    def __setup_system_common_fortigate(self,
                                        job_input,
                                        pod_id,
                                        msa_device_id,
                                        msa_config_for_common,
                                        msa_config_for_device):

        node_detail = {}

        # Create Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create System Common(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_vdom',
                                    msa_device_id,
                                    job_input['vdom_name']
        )
        node_detail[
            'create_fortigate_vdom'] = msa_res[msa.RES_KEY_IN]

        # Create Admin Profile(MSA)
        management_name = job_input['vdom_name'] + '_' \
                                            + job_input['admin_prof_name']
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_admin_profile',
                                    msa_device_id,
                                    management_name,
                                    job_input['admin_prof_name']
        )
        node_detail[
            'create_fortigate_admin_profile'] = msa_res[msa.RES_KEY_IN]

        # Create Admin User(MSA)
        management_name = job_input['vdom_name'] + '_' \
                                            + job_input['user_account_id']
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_admin_user',
                                    msa_device_id,
                                    management_name,
                                    job_input['vdom_name'],
                                    job_input['user_account_id'],
                                    job_input['account_password'],
                                    job_input['admin_prof_name']
        )
        node_detail[
            'create_fortigate_admin_user'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, 'act', node_detail)

    def __setup_pub_lan_fortigate(self,
                                  job_input,
                                  pod_id,
                                  msa_device_id,
                                  msa_config_for_common,
                                  msa_config_for_device,
                                  nic_public):

        msa_info = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id2 = job_input['port_id2']

        # List NAL_VNF_MNG(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id2
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        # Get Network Info
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            '')

        # Create Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create Intergace(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_fortigate_vlan_interface',
            msa_device_id,
            job_input['vdom_name'] + '_' + str(pub_network_info['vlan_id']),
            job_input['vdom_name'],
            str(pub_network_info['vlan_id']),
            port_list[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(port_list[0]['netmask']),
            nic_public,
            'no'
        )
        msa_info['create_fortigate_vlan_interface'] = \
            msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id2, msa_info)

    def __setup_ext_lan_fortigate(self,
                                  job_input,
                                  pod_id,
                                  msa_device_id,
                                  msa_config_for_common,
                                  msa_config_for_device,
                                  nic_external):

        msa_info = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id3 = job_input['port_id3']

        # List NAL_VNF_MNG(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id3
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            '')

        # Create Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create Interface(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_fortigate_vlan_interface',
            msa_device_id,
            job_input['vdom_name'] + '_' + str(ext_network_info['vlan_id']),
            job_input['vdom_name'],
            str(ext_network_info['vlan_id']),
            port_list[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(port_list[0]['netmask']),
            nic_external,
            'no'
        )
        msa_info['create_fortigate_vlan_interface'] = \
            msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id3, msa_info)

    def __setup_tenant_vlan_fortigate(self,
                                      job_input,
                                      pod_id,
                                      msa_device_id,
                                      vdom_name,
                                      msa_config_for_common,
                                      msa_config_for_device,
                                      nic_tenant):

        msa_info = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input['port_id4']
        iaas_network_type = job_input['IaaS_network_type']
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

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
            params = {}
            params['delete_flg'] = 0
            params['tenant_id'] = nal_tenant_id
            params['network_id'] = port_list[0]['network_id']
            db_list.set_context(db_endpoint_vlan, params)
            db_list.execute()
            vlan_list = db_list.get_return_param()
            vlan_id = vlan_list[0]['vlan_id']

        # Create Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create Interface(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_fortigate_vlan_interface',
            msa_device_id,
            vdom_name + '_' + str(vlan_id),
            vdom_name,
            str(vlan_id),
            port_list[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(
                                port_list[0]['netmask']),
            nic_tenant,
            'yes'
        )
        msa_info['create_fortigate_vlan_interface'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id4, msa_info)

    def __unsetup_system_common_fortigate(self,
                                        job_input,
                                        pod_id,
                                        msa_device_id,
                                        vdom_name,
                                        msa_config_for_common,
                                        msa_config_for_device,
                                        user_account_id,
                                        admin_prof):

        node_detail = {}

        # Create Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        try:
            # Delete Admin User(MSA)
            management_name = vdom_name + '_' + user_account_id
            msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_fortigate_admin_user',
                                    msa_device_id,
                                    management_name,
                                    user_account_id
            )

            node_detail[
                'delete_fortigate_admin_user'] = msa_res[msa.RES_KEY_IN]

        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete Admin Profile(MSA)
            management_name = vdom_name + '_' + admin_prof
            msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_fortigate_admin_profile',
                                    msa_device_id,
                                    management_name,
                                    admin_prof
            )

            node_detail[
                'delete_fortigate_admin_profile'] = msa_res[msa.RES_KEY_IN]

        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete Vdom(MSA)
            msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_fortigate_vdom',
                                    msa_device_id,
                                    vdom_name
            )

            node_detail[
                'delete_fortigate_vdom'] = msa_res[msa.RES_KEY_IN]

        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, 'act', node_detail)

    def __unsetup_pub_lan_fortigate(self,
                                  job_input,
                                  pod_id,
                                  msa_device_id,
                                  vdom_name,
                                  msa_config_for_common,
                                  msa_config_for_device,
                                  nic_public):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get Network Info
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            '')

        # List NAL_VNF_MNG(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        # Get Network Info pub
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = pub_network_info['network_id']
        params['node_id'] = node_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()
        ip_address_v6 = port_list[0].get('ip_address_v6', '')

        # Create Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        if ip_address_v6 != '':
            try:
                # Delete Interface(MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_fortigate_vlan_ipv6_interface',
                    msa_device_id,
                    vdom_name + '_' + str(pub_network_info['vlan_id'])
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

        try:
            # Delete Interface(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_fortigate_vlan_interface',
                msa_device_id,
                vdom_name + '_' + str(pub_network_info['vlan_id'])
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

    def __unsetup_ext_lan_fortigate(self,
                                  job_input,
                                  pod_id,
                                  msa_device_id,
                                  vdom_name,
                                  msa_config_for_common,
                                  msa_config_for_device,
                                  nic_external):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get Network Info
        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            '')

        # List NAL_VNF_MNG(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        # Get Network Info pub
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = ext_network_info['network_id']
        params['node_id'] = node_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()
        ip_address_v6 = port_list[0].get('ip_address_v6', '')

        # Create Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        if ip_address_v6 != '':
            try:
                # Delete Interface(MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_fortigate_vlan_ipv6_interface',
                    msa_device_id,
                    vdom_name + '_' + str(ext_network_info['vlan_id'])
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

        try:
            # Delete Interface(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_fortigate_vlan_interface',
                msa_device_id,
                vdom_name + '_' + str(ext_network_info['vlan_id'])
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

    def __unsetup_tenant_vlan_fortigate(self,
                                      job_input,
                                      pod_id,
                                      msa_device_id,
                                      vdom_name,
                                      msa_config_for_common,
                                      msa_config_for_device,
                                      iaas_network_id=''):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        port_id = job_input.get('port_id', '')
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Network Info
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
        if len(iaas_network_id) != 0:
            params['IaaS_network_id'] = iaas_network_id
        if len(port_id) != 0:
            params['port_id'] = port_id

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        # Delete Instance(MSA Soap Client)
        msa = fortigateordercmdws.FortigateOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        for rec in port_list:

            if rec['network_id'] != pub_network_info['network_id'] \
                    and rec['network_id'] != ext_network_info['network_id']:

                params = {}
                params['delete_flg'] = 0
                params['tenant_id'] = nal_tenant_id
                params['network_id'] = rec['network_id']
                db_list.set_context(db_endpoint_vlan, params)
                db_list.execute()
                vlan_list = db_list.get_return_param()
                iaas_net_type = vlan_list[0]['IaaS_network_type']

                # Get VLAN_ID
                if vim_iaas_with_flg == 1 and \
                        iaas_net_type.upper() == self.job_config.NW_TYPE_VXLAN:
                    # List NAL_PNF_VLAN_MNG(DB Client)
                    params = {}
                    params['delete_flg'] = 0
                    params['status'] = 1
                    params['network_id'] = rec['network_id']
                    db_list.set_context(db_endpoint_pnf_vlan, params)
                    db_list.execute()
                    pnf_vlan_list = db_list.get_return_param()
                    vlan_id = pnf_vlan_list[0]['vlan_id']
                else:
                    vlan_id = vlan_list[0]['vlan_id']

                if rec.get('ip_address_v6', '') != '':
                    try:
                        # Delete IPv6Vlan
                        self.execute_msa_command(
                            msa_config_for_device,
                            msa,
                            'delete_fortigate_vlan_ipv6_interface',
                            msa_device_id,
                            vdom_name + '_' + str(vlan_id),
                        )

                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise
                else:
                    pass

                try:
                    # Create Interface(MSA)
                    # Delete IPv4Vlan
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_fortigate_vlan_interface',
                        msa_device_id,
                        vdom_name + '_' + str(vlan_id)
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__,
                                              traceback.format_exc())
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

    def __update_db_port(self, job_input, port_id, msa_info):

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

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['msa_info'] = json.dumps(msa_info)
        db_update.set_context(db_endpoint, keys, params)
        db_update.execute()
