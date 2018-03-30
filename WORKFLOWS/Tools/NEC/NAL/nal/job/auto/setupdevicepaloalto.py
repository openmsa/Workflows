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
from job.lib.soap.msa import paloaltoordercmdws


class SetupDevicePaloAlto(base.JobAutoBase):

    INTERFACE_MANAGEMENT_PROFILE_NAME_PUB = 'Pub_profile'
    INTERFACE_MANAGEMENT_PROFILE_NAME_EXT = 'Ext_profile'
    INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT = 'TenantVlan_profile'

    IPv4 = '4'
    IPv6 = '6'

    def device_setup_create_for_paloalto(self, job_input):

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
        vsys_id_seq = apl_data['vsys_id_seq']

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup System Common Setting
        self.__setup_system_common_paloalto(job_input,
                                             pod_id,
                                             master_msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device,
                                             vsys_id_seq)

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [job_input['apl_table_rec_id']]
        params = {}
        params['update_id'] = job_input['operation_id']
        params['default_gateway'] = msa_config_for_common['ext_vlan_gateway']
        db_update.set_context(db_endpoint, keys, params)
        db_update.execute()

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_add_ipv6_for_paloalto(self, job_input):

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

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup Device(IPv6)
        self.__setup_paloalto_add_ipv6(job_input,
                                             pod_id,
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

    def device_setup_delete_for_paloalto(self, job_input):

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
        vsys_name = apl_data['device_user_name']
        vsys_id_seq = apl_data['vsys_id_seq']
        device_detail_master = json.loads(apl_data['device_detail_master'])

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # UnSetup Pub LAN Setting
        self.__unsetup_system_common_paloalto(job_input,
                                       pod_id,
                                       msa_device_id,
                                       vsys_name,
                                       device_detail_master,
                                       msa_config_for_common,
                                       msa_config_for_device,
                                       vsys_id_seq)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_add_port_for_paloalto(self, job_input):

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
        vsys_name = apl_data['device_user_name']
        vsys_id_seq = apl_data['vsys_id_seq']

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup System Common Setting
        self.__add_port_paloalto(job_input,
                                 pod_id,
                                 msa_device_id,
                                 vsys_name,
                                 msa_config_for_common,
                                 msa_config_for_device,
                                 vsys_id_seq)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_delete_port_for_paloalto(self, job_input):

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
        vsys_name = apl_data['device_user_name']
        vsys_id_seq = apl_data['vsys_id_seq']

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # UnSetup Pub LAN Setting
        self.__delete_port_paloalto(job_input,
                                       pod_id,
                                       msa_device_id,
                                       vsys_name,
                                       msa_config_for_common,
                                       msa_config_for_device,
                                       vsys_id_seq)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __setup_system_common_paloalto(self,
                                        job_input,
                                        pod_id,
                                        msa_device_id,
                                        msa_config_for_common,
                                        msa_config_for_device,
                                        vsys_id_seq):

        node_detail = {}
        msa_info2 = {}
        msa_info3 = {}
        msa_info4 = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id2 = job_input['port_id2']
        port_id3 = job_input['port_id3']
        port_id4 = job_input['port_id4']
        iaas_network_type = job_input['IaaS_network_type']
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # List NAL_VNF_MNG(DB Client)
        db_vlan_endpoint = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_pnf_vlan = self.get_db_endpoint(
                                            self.job_config.REST_URI_PNF_VLAN)
        db_list = list.ListClient(self.job_config)

        port_list2 = self.__get_db_port(nal_tenant_id, '', port_id2)

        # Get Network Info
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            '')

        port_list3 = self.__get_db_port(nal_tenant_id, '', port_id3)

        # Get Network Info
        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            '')

        port_list4 = self.__get_db_port(nal_tenant_id, '', port_id4)

        # Get VLAN_ID
        if vim_iaas_with_flg == 1 and \
                iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:
            # List NAL_PNF_VLAN_MNG(DB Client)
            params = {}
            params['delete_flg'] = 0
            params['status'] = 1
            params['network_id'] = port_list4[0]['network_id']
            db_list.set_context(db_endpoint_pnf_vlan, params)
            db_list.execute()
            pnf_vlan_list = db_list.get_return_param()
            vlan_id = pnf_vlan_list[0]['vlan_id']
        else:
            params = {}
            params['delete_flg'] = 0
            params['tenant_id'] = nal_tenant_id
            params['network_id'] = port_list4[0]['network_id']
            db_list.set_context(db_vlan_endpoint, params)
            db_list.execute()
            vlan_list = db_list.get_return_param()
            vlan_id = vlan_list[0]['vlan_id']

        # Create Instance(MSA Soap Client)
        msa = paloaltoordercmdws.PaloaltoOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create System Common(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_paloalto_vsys',
                                    msa_device_id,
                                    int(vsys_id_seq),
                                    job_input['vsys_name']
        )
        node_detail[
            'create_paloalto_vsys'] = msa_res[msa.RES_KEY_IN]

        # Create admin user(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_paloalto_system_vsys_users',
                                    msa_device_id,
                                    job_input['admin_id'],
                                    self.utils.get_hash_value('',
                                      self.job_config.CHAR_SET,
                                      self.job_config.SCRIPT_STDOUT_SEPARATER,
                                      job_input['admin_pw']),
                                    'vsys' + str(vsys_id_seq)
        )
        node_detail[
            'create_paloalto_system_vsys_users'] = msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------
        # port2
        # -----------------------------------------------------------------
        # Create interface_mngprofile(MSA)
        msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_network_interface_mngprofile',
                msa_device_id,
                self.INTERFACE_MANAGEMENT_PROFILE_NAME_PUB + str(vsys_id_seq),
                'yes',
                'yes',
                'yes',
                'yes'
        )
        msa_info2['create_paloalto_network_interface_mngprofile'] = \
                                                msa_res[msa.RES_KEY_IN]
        # Create subinterface(MSA)
        msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_network_subinterface',
                msa_device_id,
                port_list2[0]['nic'],
                port_list2[0]['nic'].split(".")[0],
                port_list2[0]['ip_address'],
                port_list2[0]['netmask'],
                str(pub_network_info['vlan_id']),
                self.INTERFACE_MANAGEMENT_PROFILE_NAME_PUB + str(vsys_id_seq)
        )
        msa_info2['create_paloalto_network_subinterface'] = \
                                                msa_res[msa.RES_KEY_IN]
        # Create Zone(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_zone',
                    msa_device_id,
                    'Pub',
                    'vsys' + str(vsys_id_seq)
        )
        msa_info2['create_paloalto_vsys_zone'] = msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------
        # port3
        # -----------------------------------------------------------------
        # Create interface_mngprofile(MSA)
        msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_network_interface_mngprofile',
                msa_device_id,
                self.INTERFACE_MANAGEMENT_PROFILE_NAME_EXT + str(vsys_id_seq),
                'no',
                'no',
                'no',
                'yes'
        )
        msa_info3['create_paloalto_network_interface_mngprofile'] = \
                                                msa_res[msa.RES_KEY_IN]
        # Create subinterface(MSA)
        msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_network_subinterface',
                msa_device_id,
                port_list3[0]['nic'],
                port_list3[0]['nic'].split(".")[0],
                port_list3[0]['ip_address'],
                port_list3[0]['netmask'],
                str(ext_network_info['vlan_id']),
                self.INTERFACE_MANAGEMENT_PROFILE_NAME_EXT + str(vsys_id_seq)
        )
        msa_info3['create_paloalto_network_subinterface'] = \
                                                msa_res[msa.RES_KEY_IN]
        # Create Zone(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_zone',
                    msa_device_id,
                    'Ext',
                    'vsys' + str(vsys_id_seq)
        )
        msa_info3['create_paloalto_vsys_zone'] = msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------
        # port4
        # -----------------------------------------------------------------
        # Create interface_mngprofile(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_paloalto_network_interface_mngprofile',
            msa_device_id,
            self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT + str(vsys_id_seq),
            'yes',
            'yes',
            'yes',
            'yes'
        )
        msa_info4['create_paloalto_network_interface_mngprofile'] = \
                                                msa_res[msa.RES_KEY_IN]
        # Create subinterface(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_paloalto_network_subinterface',
            msa_device_id,
            port_list4[0]['nic'],
            port_list4[0]['nic'].split(".")[0],
            port_list4[0]['ip_address'],
            port_list4[0]['netmask'],
            vlan_id,
            self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT + str(vsys_id_seq)
        )
        msa_info4['create_paloalto_network_subinterface'] = \
                                                msa_res[msa.RES_KEY_IN]
        # Create Zone(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_zone',
                    msa_device_id,
                    job_input['zone_name'],
                    'vsys' + str(vsys_id_seq)
        )
        msa_info4['create_paloalto_vsys_zone'] = msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------

        # Create virtualrouter(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_network_virtualrouter',
                    msa_device_id,
                    'VRouter_' + job_input['vsys_name']
        )
        node_detail['create_paloalto_network_virtualrouter'] = \
                                                msa_res[msa.RES_KEY_IN]

        # Create vrouter_mapping(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_network_vrouter_mapping',
                    msa_device_id,
                    'VRouter_' + job_input['vsys_name'],
                    [port_list2[0]['nic'],
                         port_list3[0]['nic'],
                         port_list4[0]['nic']]
        )
        node_detail['create_paloalto_network_vrouter_mapping'] = \
                                                msa_res[msa.RES_KEY_IN]

        # -----------------------------------------------------------------
        # port2
        # -----------------------------------------------------------------
        # Create taticroute'(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_network_staticroute',
                    msa_device_id,
                    'Pub_StaticRoute_' + job_input['vsys_name'],
                    'VRouter_' + job_input['vsys_name'],
                    msa_config_for_common['svc_vlan_network_address'],
                    msa_config_for_common['svc_vlan_network_mask'],
                    msa_config_for_common['pub_vlan_gateway'],
                    port_list2[0]['nic']
        )
        msa_info2['create_paloalto_network_staticroute'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------
        # port3
        # -----------------------------------------------------------------
        # Create staticroute(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_network_staticroute',
                    msa_device_id,
                    'defaultGW_' + job_input['vsys_name'],
                    'VRouter_' + job_input['vsys_name'],
                    '0.0.0.0',
                    '0',
                    msa_config_for_common['ext_vlan_gateway'],
                    port_list3[0]['nic']
        )
        msa_info3['create_paloalto_network_staticroute'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------

        # Create interface_importing(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_interface_importing',
                    msa_device_id,
                    'vsys' + str(vsys_id_seq),
                    [port_list2[0]['nic'],
                         port_list3[0]['nic'],
                         port_list4[0]['nic']]
        )
        node_detail['create_paloalto_vsys_interface_importing'] = \
                                                msa_res[msa.RES_KEY_IN]

        # Create vrouter_importing(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_vrouter_importing',
                    msa_device_id,
                    'vsys' + str(vsys_id_seq),
                    ['VRouter_' + job_input['vsys_name']]
        )
        node_detail['create_paloalto_vsys_vrouter_importing'] = \
                                                msa_res[msa.RES_KEY_IN]

        # -----------------------------------------------------------------
        # port2
        # -----------------------------------------------------------------
        # Create zone_mapping(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_zone_mapping',
                    msa_device_id,
                    'Pub',
                    'vsys' + str(vsys_id_seq),
                    [port_list2[0]['nic']]
        )
        msa_info2['create_paloalto_vsys_zone_mapping'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------
        # port3
        # -----------------------------------------------------------------
        # Create zone_mapping(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_zone_mapping',
                    msa_device_id,
                    'Ext',
                    'vsys' + str(vsys_id_seq),
                    [port_list3[0]['nic']]
        )
        msa_info3['create_paloalto_vsys_zone_mapping'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------
        # port4
        # -----------------------------------------------------------------
        # Create zone_mapping(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_zone_mapping',
                    msa_device_id,
                    job_input['zone_name'],
                    'vsys' + str(vsys_id_seq),
                    [port_list4[0]['nic']]
        )
        msa_info4['create_paloalto_vsys_zone_mapping'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------

        # Set Node Detail(ObjectList)
        node_detail["InterFaceList"] = [port_list2[0]['nic'],
                                        port_list3[0]['nic'],
                                        port_list4[0]['nic']]
        node_detail['ZoneNameList'] = [
                                'Pub', 'Ext', job_input['zone_name']]

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, 'act', node_detail)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id2, msa_info2)
        self.__update_db_port(job_input, port_id3, msa_info3)
        self.__update_db_port(job_input, port_id4, msa_info4)

    def __unsetup_system_common_paloalto(self,
                                        job_input,
                                        pod_id,
                                        msa_device_id,
                                        vsys_name,
                                        device_detail_master,
                                        msa_config_for_common,
                                        msa_config_for_device,
                                        vsys_id_seq):

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
        params['network_id'] = pub_network_info['network_id']
        params['node_id'] = node_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list2 = db_list.get_return_param()

        pub_ip_address_v6 = ''
        if len(port_list2) != 0:
            pub_ip_address_v6 = port_list2[0].get('ip_address_v6', '')
            pub_object_id_nic = port_list2[0]['nic']
            pub_interface = pub_object_id_nic.split('.')[0]
            pub_net_work_id_list = pub_object_id_nic.split('/')[1].split('.')
            pub_net_work_id = pub_net_work_id_list[0] + pub_net_work_id_list[1]
            pub_object_id_ipv4 = pub_net_work_id + self.IPv4
            pub_object_id_ipv6 = pub_net_work_id + self.IPv6

        # Get Network Info ext
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = ext_network_info['network_id']
        params['node_id'] = node_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list3 = db_list.get_return_param()

        ext_ip_address_v6 = ''
        if len(port_list3) != 0:
            ext_ip_address_v6 = port_list3[0].get('ip_address_v6', '')
            ext_object_id_nic = port_list3[0]['nic']
            ext_interface = ext_object_id_nic.split('.')[0]
            ext_net_work_id_list = ext_object_id_nic.split('/')[1].split('.')
            ext_net_work_id = ext_net_work_id_list[0] + ext_net_work_id_list[1]
            ext_object_id_ipv4 = ext_net_work_id + self.IPv4
            ext_object_id_ipv6 = ext_net_work_id + self.IPv6

        # Get Network Info tenant LAN
        port_list = self.__get_db_port(nal_tenant_id, node_id, '')

        # Delete Instance(MSA Soap Client)
        msa = paloaltoordercmdws.PaloaltoOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)
        # pub
        if pub_ip_address_v6 != '':
            try:
                # Delete permitted ipv6 (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_permitted_ip',
                    msa_device_id,
                    pub_object_id_ipv6,
                    self.INTERFACE_MANAGEMENT_PROFILE_NAME_PUB \
                        + str(vsys_id_seq),
                    port_list2[0]['ip_address_v6'],
                    port_list2[0]['netmask_v6']
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete permitted ipv4 (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_permitted_ip',
                    msa_device_id,
                    pub_object_id_ipv4,
                    self.INTERFACE_MANAGEMENT_PROFILE_NAME_PUB \
                        + str(vsys_id_seq),
                    '0.0.0.0',
                    '0'
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete ipv6 static route (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_ipv6_static_route',
                    msa_device_id,
                    'Pub_StaticRoutev6_' + vsys_name,
                    'VRouter_' + vsys_name
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete ipv6 interface enable (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_ipv6_interface_enable',
                    msa_device_id,
                    pub_object_id_nic,
                    pub_interface
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete ipv6 interface (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_ipv6_interface',
                    msa_device_id,
                    pub_object_id_nic,
                    pub_interface
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        else:
            pass

        # ext
        if ext_ip_address_v6 != '':
            try:
                # Delete permitted ipv6 (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_permitted_ip',
                    msa_device_id,
                    ext_object_id_ipv6,
                    self.INTERFACE_MANAGEMENT_PROFILE_NAME_EXT \
                        + str(vsys_id_seq),
                    port_list3[0]['ip_address_v6'],
                    port_list3[0]['netmask_v6']
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete permitted ipv4 (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_permitted_ip',
                    msa_device_id,
                    ext_object_id_ipv4,
                    self.INTERFACE_MANAGEMENT_PROFILE_NAME_EXT \
                        + str(vsys_id_seq),
                    '0.0.0.0',
                    '0'
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete ipv6 static route (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_ipv6_static_route',
                    msa_device_id,
                    'defaultGWv6_' + vsys_name,
                    'VRouter_' + vsys_name
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete ipv6 interface enable (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_ipv6_interface_enable',
                    msa_device_id,
                    ext_object_id_nic,
                    ext_interface
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete ipv6 interface (MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_paloalto_ipv6_interface',
                    msa_device_id,
                    ext_object_id_nic,
                    ext_interface
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        else:
            pass

        # tenant LAN
        for lan_port_dict in port_list:
            if (lan_port_dict['network_id'] !=
                                    pub_network_info['network_id'])\
                and (lan_port_dict['network_id'] !=
                                    ext_network_info['network_id']):
                if lan_port_dict.get('ip_address_v6', '') != '':
                    lan_object_id_nic = lan_port_dict['nic']
                    lan_interface = lan_object_id_nic.split('.')[0]
                    lan_net_work_id_list = \
                            lan_object_id_nic.split('/')[1].split('.')
                    lan_net_work_id = \
                            lan_net_work_id_list[0] + lan_net_work_id_list[1]
                    lan_object_id_ipv4 = lan_net_work_id + self.IPv4
                    lan_object_id_ipv6 = lan_net_work_id + self.IPv6

                    # get value of permitted_ip_info
                    permitted_ip_info = ''
                    msa_info = lan_port_dict['msa_info']
                    msa_info_dict = json.loads(msa_info)
                    if 'create_paloalto_paloalto_permitted_ip' \
                            in msa_info_dict:
                        api_permitted_ip = msa_info_dict[
                                    'create_paloalto_paloalto_permitted_ip']
                        object_params = api_permitted_ip['objectParameters']
                        object_params_dict = json.loads(object_params)
                        for key in object_params_dict[
                                        'PaloaltoPaloaltoPermittedip'].keys():
                            permitted_ip_info = object_params_dict[
                                        'PaloaltoPaloaltoPermittedip'][key]

                    try:
                        # Delete permitted ipv6 (MSA)
                        self.execute_msa_command(
                            msa_config_for_device,
                            msa,
                            'delete_paloalto_paloalto_permitted_ip',
                            msa_device_id,
                            lan_object_id_ipv6,
                            self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT \
                                + str(vsys_id_seq),
                            permitted_ip_info['ip_address'],
                            permitted_ip_info['netmask']
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete permitted ipv4 (MSA)
                        self.execute_msa_command(
                            msa_config_for_device,
                            msa,
                            'delete_paloalto_paloalto_permitted_ip',
                            msa_device_id,
                            lan_object_id_ipv4,
                            self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT \
                                + str(vsys_id_seq),
                            '0.0.0.0',
                            '0'
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete ipv6 interface enable (MSA)
                        self.execute_msa_command(
                            msa_config_for_device,
                            msa,
                            'delete_paloalto_paloalto_ipv6_interface_enable',
                            msa_device_id,
                            lan_object_id_nic,
                            lan_interface
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                    try:
                        # Delete ipv6 interface (MSA)
                        self.execute_msa_command(
                            msa_config_for_device,
                            msa,
                            'delete_paloalto_paloalto_ipv6_interface',
                            msa_device_id,
                            lan_object_id_nic,
                            lan_interface
                        )
                    except:
                        if job_cleaning_mode == '1':
                            self.output_log_fatal(__name__,
                                                  traceback.format_exc())
                        else:
                            raise

                else:
                    pass
            else:
                pass

        try:
            # Delete virtualrouter(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_paloalto_vsys_interface_importing',
                msa_device_id,
                'vsys' + str(vsys_id_seq)
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete virtualrouter(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_paloalto_vsys_vrouter_importing',
                msa_device_id,
                'vsys' + str(vsys_id_seq)
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete virtualrouter(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_paloalto_network_virtualrouter',
                msa_device_id,
                'VRouter_' + vsys_name
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete vsys_zone(MSA)
            for zone_name in device_detail_master['ZoneNameList']:
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_vsys_zone',
                    msa_device_id,
                    zone_name,
                    'vsys' + str(vsys_id_seq)
                )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete vsys_users(MSA)
            param = json.loads(device_detail_master[
                                        'create_paloalto_system_vsys_users'][
                                        'objectParameters'])
            user_dict = param['PaloAlto_System_Vsys_Users']
            for key in user_dict:
                user_name = key
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_paloalto_system_vsys_users',
                msa_device_id,
                user_name
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete vsys(MSA)
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_paloalto_vsys',
                                    msa_device_id,
                                    int(vsys_id_seq)
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # -----------------------------------------------------------------
        # port2
        # -----------------------------------------------------------------
        if len(port_list2) != 0:
            try:
                # Delete subinterface(MSA)
                self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_network_subinterface',
                        msa_device_id,
                        port_list2[0]['nic'],
                        port_list2[0]['nic'].split(".")[0]
                        )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        # -----------------------------------------------------------------
        # port3
        # -----------------------------------------------------------------
        if len(port_list3) != 0:
            try:
                # Delete subinterface(MSA)
                self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_network_subinterface',
                    msa_device_id,
                    port_list3[0]['nic'],
                    port_list3[0]['nic'].split(".")[0],
                    )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        # -----------------------------------------------------------------
        # port4 -
        # -----------------------------------------------------------------
        for rec in port_list:

            if rec['network_id'] != pub_network_info['network_id'] \
                    and rec['network_id'] != ext_network_info['network_id']:

                try:
                    # Delete subinterface(MSA)
                    self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_network_subinterface',
                        msa_device_id,
                        rec['nic'],
                        rec['nic'].split(".")[0],
                    )
                except:
                    if job_cleaning_mode == '1':
                        self.output_log_fatal(__name__, traceback.format_exc())
                    else:
                        raise
        # -----------------------------------------------------------------
        # Delete mngprofile(MSA)
        try:
            self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_network_interface_mngprofile',
                        msa_device_id,
                        self.INTERFACE_MANAGEMENT_PROFILE_NAME_PUB \
                            + str(vsys_id_seq)
                        )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_network_interface_mngprofile',
                        msa_device_id,
                        self.INTERFACE_MANAGEMENT_PROFILE_NAME_EXT \
                            + str(vsys_id_seq)
                        )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_network_interface_mngprofile',
                        msa_device_id,
                        self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT \
                            + str(vsys_id_seq)
                        )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

    def __add_port_paloalto(self,
                            job_input,
                            pod_id,
                            msa_device_id,
                            vsys_name,
                            msa_config_for_common,
                            msa_config_for_device,
                            vsys_id_seq):

        node_detail = {}
        msa_info = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input['port_id4']
        iaas_network_type = job_input['IaaS_network_type']
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # List NAL_VNF_MNG(DB Client)
        db_vlan_endpoint = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_pnf_vlan = self.get_db_endpoint(
                                            self.job_config.REST_URI_PNF_VLAN)
        db_list = list.ListClient(self.job_config)

        port_list = self.__get_db_port(nal_tenant_id, '', port_id4)

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
            db_list.set_context(db_vlan_endpoint, params)
            db_list.execute()
            vlan_list = db_list.get_return_param()
            vlan_id = vlan_list[0]['vlan_id']

        # Create Instance(MSA Soap Client)
        msa = paloaltoordercmdws.PaloaltoOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # -----------------------------------------------------------------
        # port4
        # -----------------------------------------------------------------
        # Create Zone(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_zone',
                    msa_device_id,
                    job_input['zone_name'],
                    'vsys' + str(vsys_id_seq)
        )
        msa_info['create_paloalto_vsys_zone'] = msa_res[msa.RES_KEY_IN]
        zone_list = self.__get_nodedetail_objlist(job_input, 'act', 'zone')
        zone_list.append(job_input['zone_name'])
        node_detail["ZoneNameList"] = zone_list
        # -----------------------------------------------------------------
        # Create subinterface(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_network_subinterface',
                    msa_device_id,
                    port_list[0]['nic'],
                    port_list[0]['nic'].split(".")[0],
                    port_list[0]['ip_address'],
                    port_list[0]['netmask'],
                    vlan_id,
                    self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT \
                        + str(vsys_id_seq)
        )
        msa_info['create_paloalto_network_subinterface'] = \
                                                msa_res[msa.RES_KEY_IN]
        interface_list = self.__get_nodedetail_objlist(job_input,
                                                       'act',
                                                       'interface')
        interface_list.append(port_list[0]['nic'])
        node_detail["InterFaceList"] = interface_list
        # -----------------------------------------------------------------
        # Delete vrouter_mapping(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_network_vrouter_mapping',
                    msa_device_id,
                    'VRouter_' + vsys_name
        )
        # Create vrouter_mapping(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_network_vrouter_mapping',
                    msa_device_id,
                    'VRouter_' + vsys_name,
                    interface_list
        )
        # Delete interface_importing(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'delete_paloalto_vsys_interface_importing',
            msa_device_id,
            'vsys' + str(vsys_id_seq)
        )
        # Create interface_importing(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_interface_importing',
                    msa_device_id,
                    'vsys' + str(vsys_id_seq),
                    interface_list
        )
        node_detail['create_paloalto_vsys_interface_importing'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------
        # port4
        # -----------------------------------------------------------------
        # Create zone_mapping(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_zone_mapping',
                    msa_device_id,
                    job_input['zone_name'],
                    'vsys' + str(vsys_id_seq),
                    [port_list[0]['nic']]
        )
        msa_info['create_paloalto_vsys_zone_mapping'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------
        # Delete vrouter_importing(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'delete_paloalto_vsys_vrouter_importing',
            msa_device_id,
            'vsys' + str(vsys_id_seq)
        )
        node_detail['create_paloalto_network_vrouter_mapping'] = \
                                                msa_res[msa.RES_KEY_IN]
        # Create vrouter_importing(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_vrouter_importing',
                    msa_device_id,
                    'vsys' + str(vsys_id_seq),
                    ['VRouter_' + vsys_name]
        )
        node_detail['create_paloalto_vsys_vrouter_importing'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, 'act', node_detail)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id4, msa_info)

    def __delete_port_paloalto(self,
                               job_input,
                               pod_id,
                               msa_device_id,
                               vsys_name,
                               msa_config_for_common,
                               msa_config_for_device,
                               vsys_id_seq):

        node_detail = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        iaas_network_id = job_input['IaaS_network_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # List NAL_VNF_MNG(DB Client)
        db_port_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['IaaS_network_id'] = iaas_network_id
        params['node_id'] = node_id
        db_list.set_context(db_port_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()
        ip_address_v6 = port_list[0].get('ip_address_v6', '')

        # Get interface list
        interface_list = \
                self.__get_nodedetail_objlist(job_input, 'act', 'interface')
        interface_list.remove(port_list[0]['nic'])

        # Get zone name & delete zone name from zone list
        msa_info = json.loads(port_list[0]['msa_info'])
        obj_params = json.loads(
            msa_info['create_paloalto_vsys_zone']['objectParameters'])
        zone_dict = obj_params['PaloAlto_Vsys_Zone']
        for key in zone_dict:
            zone_name = key

        zone_list = \
                self.__get_nodedetail_objlist(job_input, 'act', 'zone')
        zone_list.remove(zone_name)

        # Create Instance(MSA Soap Client)
        msa = paloaltoordercmdws.PaloaltoOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        if ip_address_v6 != '':
            lan_object_id_nic = port_list[0]['nic']
            lan_net_work_id_list = \
                    lan_object_id_nic.split('/')[1].split('.')
            lan_net_work_id = \
                    lan_net_work_id_list[0] + lan_net_work_id_list[1]
            lan_object_id_ipv4 = lan_net_work_id + self.IPv4
            lan_object_id_ipv6 = lan_net_work_id + self.IPv6

            # get value of permitted_ip_info
            permitted_ip_info = ''
            msa_info = port_list[0]['msa_info']
            msa_info_dict = json.loads(msa_info)
            if 'create_paloalto_paloalto_permitted_ip' \
                    in msa_info_dict:
                api_permitted_ip = msa_info_dict[
                                'create_paloalto_paloalto_permitted_ip']
                object_params = api_permitted_ip['objectParameters']
                object_params_dict = json.loads(object_params)
                for key in object_params_dict[
                                    'PaloaltoPaloaltoPermittedip'].keys():
                    permitted_ip_info = object_params_dict[
                                    'PaloaltoPaloaltoPermittedip'][key]

            try:
                # Delete permitted ip ipv6(MSA)
                self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_paloalto_permitted_ip',
                        msa_device_id,
                        lan_object_id_ipv6,
                        self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT \
                            + str(vsys_id_seq),
                        permitted_ip_info['ip_address'],
                        permitted_ip_info['netmask']
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete permitted ip ipv4(MSA)
                self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_paloalto_permitted_ip',
                        msa_device_id,
                        lan_object_id_ipv4,
                        self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT \
                            + str(vsys_id_seq),
                        '0.0.0.0',
                        '0'
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete ipv6 interface enable(MSA)
                self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_paloalto_ipv6_interface_enable',
                        msa_device_id,
                        port_list[0]['nic'],
                        port_list[0]['nic'].split(".")[0],
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            try:
                # Delete ipv6 interface (MSA)
                self.execute_msa_command(
                        msa_config_for_device,
                        msa,
                        'delete_paloalto_paloalto_ipv6_interface',
                        msa_device_id,
                        port_list[0]['nic'],
                        port_list[0]['nic'].split(".")[0]
                )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

        # -----------------------------------------------------------------
        try:
            # Delete vrouter_mapping(MSA)
            self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_paloalto_network_vrouter_mapping',
                    msa_device_id,
                    'VRouter_' + vsys_name
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Create vrouter_mapping(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_network_vrouter_mapping',
                    msa_device_id,
                    'VRouter_' + vsys_name,
                    interface_list
        )
        node_detail['create_paloalto_network_vrouter_mapping'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------

        try:
            # Delete interface_importing(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_paloalto_vsys_zone_mapping',
                msa_device_id,
                zone_name,
                'vsys' + str(vsys_id_seq)
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        try:
            # Delete interface_importing(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_paloalto_vsys_interface_importing',
                msa_device_id,
                'vsys' + str(vsys_id_seq)
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Create interface_importing(MSA)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_paloalto_vsys_interface_importing',
                    msa_device_id,
                    'vsys' + str(vsys_id_seq),
                    interface_list
        )
        node_detail['create_paloalto_vsys_interface_importing'] = \
                                                msa_res[msa.RES_KEY_IN]
        # -----------------------------------------------------------------

        # -----------------------------------------------------------------
        # port4
        # -----------------------------------------------------------------
        try:
            # Delete subinterface(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_paloalto_network_subinterface',
                msa_device_id,
                port_list[0]['nic'],
                port_list[0]['nic'].split(".")[0]
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # -----------------------------------------------------------------
        # Delete vrouter_mapping(MSA)
        try:
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_paloalto_vsys_zone',
                msa_device_id,
                zone_name,
                'vsys' + str(vsys_id_seq)
            )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        node_detail["InterFaceList"] = interface_list

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, 'act', node_detail)

    def __setup_paloalto_add_ipv6(self,
                                        job_input,
                                        pod_id,
                                        msa_device_id,
                                        msa_config_for_common,
                                        msa_config_for_device,
                                        db_apl_data):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id = job_input['port_id']
        port_id_pub_ipv6 = job_input['port_id_pub_ipv6']
        port_id_ext_ipv6 = job_input['port_id_ext_ipv6']
        network_address_ipv6 = job_input['network_address_ipv6']
        vsys_name = db_apl_data['device_user_name']
        vsys_id_seq = db_apl_data['vsys_id_seq']

        # Get Network Info
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            self.utils.IP_VER_V6)

        # Get Network Info
        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            self.utils.IP_VER_V6)

        # Create Instance(MSA Soap Client)
        msa = paloaltoordercmdws.PaloaltoOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        if len(port_id_pub_ipv6) > 0:

            # Get NAL_PORT_MNG(Pub)
            port_res_pub = self.__get_db_port(
                                    nal_tenant_id, '', port_id_pub_ipv6)
            msa_info_pub = json.loads(port_res_pub[0]['msa_info'])

            object_id_nic = port_res_pub[0]['nic']
            interface = object_id_nic.split('.')[0]

            net_work_id_list = object_id_nic.split('/')[1].split('.')
            net_work_id = net_work_id_list[0] + net_work_id_list[1]
            object_id_ipv4 = net_work_id + self.IPv4
            object_id_ipv6 = net_work_id + self.IPv6

            # Create Interface IPv6(MSA) Pub
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_ipv6_interface',
                msa_device_id,
                object_id_nic,
                interface,
                port_res_pub[0]['ip_address_v6'],
                port_res_pub[0]['netmask_v6']
            )
            msa_info_pub['create_paloalto_paloalto_ipv6_interface'] = \
                msa_res[msa.RES_KEY_IN]

            # Create Enable IPv6(MSA) Pub
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_ipv6_interface_enable',
                msa_device_id,
                object_id_nic,
                interface
            )
            msa_info_pub['create_paloalto_paloalto_ipv6_interface_enable'] = \
                msa_res[msa.RES_KEY_IN]

            # Create Static Route IPv6(MSA) Pub
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_ipv6_static_route',
                msa_device_id,
                'Pub_StaticRoutev6_' + vsys_name,
                'VRouter_' + vsys_name,
                msa_config_for_common['svc_vlan_network_address_ipv6'],
                msa_config_for_common['svc_vlan_network_mask_ipv6'],
                msa_config_for_common['pub_vlan_gateway_ipv6'],
                port_res_pub[0]['nic']
            )
            msa_info_pub['create_paloalto_paloalto_ipv6_static_route'] = \
                msa_res[msa.RES_KEY_IN]

            # Create Permitted Ip IPv4(MSA) Pub
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_permitted_ip',
                msa_device_id,
                object_id_ipv4,
                self.INTERFACE_MANAGEMENT_PROFILE_NAME_PUB + str(vsys_id_seq),
                '0.0.0.0',
                '0'
            )
            msa_info_pub['create_paloalto_paloalto_permitted_ip'] = \
                msa_res[msa.RES_KEY_IN]

            # Create Permitted Ip IPv6(MSA) Pub
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_permitted_ip',
                msa_device_id,
                object_id_ipv6,
                self.INTERFACE_MANAGEMENT_PROFILE_NAME_PUB + str(vsys_id_seq),
                pub_network_info['network_address'],
                port_res_pub[0]['netmask_v6']
            )
            msa_info_pub['create_paloalto_paloalto_permitted_ip'] = \
                msa_res[msa.RES_KEY_IN]

            # Update NAL_PORT_MNG(DB) Pub
            self.__update_db_port(job_input, port_id_pub_ipv6, msa_info_pub)

        if len(port_id_ext_ipv6) > 0:

            # Get NAL_PORT_MNG(Ext)
            port_res_ext = self.__get_db_port(
                                    nal_tenant_id, '', port_id_ext_ipv6)
            msa_info_ext = json.loads(port_res_ext[0]['msa_info'])

            object_id_nic = port_res_ext[0]['nic']
            interface = object_id_nic.split('.')[0]
            net_work_id_list = object_id_nic.split('/')[1].split('.')
            net_work_id = net_work_id_list[0] + net_work_id_list[1]
            object_id_ipv4 = net_work_id + self.IPv4
            object_id_ipv6 = net_work_id + self.IPv6

            # Create Interface IPv6(MSA) Ext
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_ipv6_interface',
                msa_device_id,
                object_id_nic,
                interface,
                port_res_ext[0]['ip_address_v6'],
                port_res_ext[0]['netmask_v6']
            )
            msa_info_ext['create_paloalto_paloalto_ipv6_interface'] = \
                msa_res[msa.RES_KEY_IN]

            # Create Enable IPv6(MSA) Ext
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_ipv6_interface_enable',
                msa_device_id,
                object_id_nic,
                interface
            )
            msa_info_ext['create_paloalto_paloalto_ipv6_interface_enable'] = \
                msa_res[msa.RES_KEY_IN]

            # Create Static Route IPv6(MSA) Ext
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_ipv6_static_route',
                msa_device_id,
                'defaultGWv6_' + vsys_name,
                'VRouter_' + vsys_name,
                '::',
                '0',
                msa_config_for_common['ext_vlan_gateway_ipv6'],
                port_res_ext[0]['nic']
            )
            msa_info_ext['create_paloalto_paloalto_ipv6_static_route'] = \
                msa_res[msa.RES_KEY_IN]

            # Create Permitted Ip IPv4(MSA) Ext
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_permitted_ip',
                msa_device_id,
                object_id_ipv4,
                self.INTERFACE_MANAGEMENT_PROFILE_NAME_EXT + str(vsys_id_seq),
                '0.0.0.0',
                '0'
            )
            msa_info_ext['create_paloalto_paloalto_permitted_ip'] = \
                msa_res[msa.RES_KEY_IN]

            # Create Permitted Ip IPv6(MSA) Ext
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_paloalto_paloalto_permitted_ip',
                msa_device_id,
                object_id_ipv6,
                self.INTERFACE_MANAGEMENT_PROFILE_NAME_EXT + str(vsys_id_seq),
                ext_network_info['network_address'],
                port_res_ext[0]['netmask_v6']
            )
            msa_info_ext['create_paloalto_paloalto_permitted_ip'] = \
                msa_res[msa.RES_KEY_IN]

            # Update NAL_PORT_MNG(DB) Ext
            self.__update_db_port(job_input, port_id_ext_ipv6, msa_info_ext)

        # Get NAL_PORT_MNG(DB) Tenant VLAN
        port_res_tenant = self.__get_db_port(nal_tenant_id, '', port_id)
        msa_info_tenant = json.loads(port_res_tenant[0]['msa_info'])
        lan_object_id_nic = port_res_tenant[0]['nic']
        lan_interface = lan_object_id_nic.split('.')[0]
        lan_net_work_id_list = lan_object_id_nic.split('/')[1].split('.')
        lan_net_work_id = lan_net_work_id_list[0] + lan_net_work_id_list[1]
        lan_object_id_ipv4 = lan_net_work_id + self.IPv4
        lan_object_id_ipv6 = lan_net_work_id + self.IPv6

        # Create Interface IPv6(MSA) Tenant VLAN
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_paloalto_paloalto_ipv6_interface',
            msa_device_id,
            lan_object_id_nic,
            lan_interface,
            port_res_tenant[0]['ip_address_v6'],
            port_res_tenant[0]['netmask_v6']
        )
        msa_info_tenant['create_paloalto_paloalto_ipv6_interface'] = \
            msa_res[msa.RES_KEY_IN]

        # Create Enable IPv6(MSA) Tenant VLAN
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_paloalto_paloalto_ipv6_interface_enable',
            msa_device_id,
            lan_object_id_nic,
            lan_interface
        )
        msa_info_tenant['create_paloalto_paloalto_ipv6_interface_enable'] = \
            msa_res[msa.RES_KEY_IN]

        # Create Permitted Ip IPv4(MSA) Tenant VLAN
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_paloalto_paloalto_permitted_ip',
            msa_device_id,
            lan_object_id_ipv4,
            self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT + str(vsys_id_seq),
            '0.0.0.0',
            '0'
        )
        msa_info_tenant['create_paloalto_paloalto_permitted_ip'] = \
            msa_res[msa.RES_KEY_IN]

        # Create Permitted Ip IPv6(MSA) Tenant VLAN
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_paloalto_paloalto_permitted_ip',
            msa_device_id,
            lan_object_id_ipv6,
            self.INTERFACE_MANAGEMENT_PROFILE_NAME_TENANT + str(vsys_id_seq),
            network_address_ipv6.split('/')[0],
            network_address_ipv6.split('/')[1]
        )
        msa_info_tenant['create_paloalto_paloalto_permitted_ip'] = \
            msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB) Tenant VLAN
        self.__update_db_port(job_input, port_id, msa_info_tenant)

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

    def __get_nodedetail_objlist(self, job_input, act_sby, list_type):

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

        if act_sby == 'act':
            node_detail_dict = json.loads(apl_list[0]['device_detail_master'])
        else:
            node_detail_dict = json.loads(apl_list[0]['device_detail_slave'])

        if list_type == 'zone':
            obj_list = node_detail_dict.get('ZoneNameList', [])
        else:
            obj_list = node_detail_dict.get('InterFaceList', [])

        return obj_list

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
