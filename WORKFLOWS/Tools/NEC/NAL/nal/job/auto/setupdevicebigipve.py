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

from job.auto import base
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import bigipveordercmdws


class SetupDeviceBigIpVe(base.JobAutoBase):

    def device_setup_create_bigip_ve(self, job_input):

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
        msa_device_id = apl_data['MSA_device_id']

        # Get MSA Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup System Common Setting
        self.__setup_system_common_bigip_ve(job_input,
                                             pod_id,
                                             msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_bigip_ve(job_input,
                                          pod_id,
                                          msa_device_id,
                                          msa_config_for_common,
                                          msa_config_for_device)

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [job_input['apl_table_rec_id']]
        params = {}
        params['update_id'] = job_input['operation_id']
        params['default_gateway'] = job_input['fw_ip_address']
        db_update.set_context(db_endpoint, keys, params)
        db_update.execute()

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_add_ipv6_for_bigip_ve(self, job_input):

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

        # Get DeviceID
        apl_data = self.__get_db_apl(job_input)
        msa_device_id = apl_data['MSA_device_id']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup IPv6 Setting
        self.__setup_add_ipv6_bigip_ve(job_input,
                                          pod_id,
                                          msa_device_id,
                                          msa_config_for_device)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, {})

        return job_output

    def __setup_system_common_bigip_ve(self,
                                       job_input,
                                       pod_id,
                                       msa_device_id,
                                       msa_config_for_common,
                                       msa_config_for_device):

        node_detail = {}

        # Create Instance(MSA Soap Client)
        msa = bigipveordercmdws.BigIpVeOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create System Common(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_big_ip_ve_system_common',
                                    msa_device_id,
                                    job_input['host_name'],
                                    job_input['domain_name']
        )
        node_detail[
            'create_big_ip_ve_system_common'] = msa_res[msa.RES_KEY_IN]

        # Create Admin Account(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_big_ip_system_admin_account',
                                    msa_device_id,
                                    job_input['admin_id'],
                                    job_input['admin_pw']
        )
        node_detail[
            'create_big_ip_system_admin_account'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, node_detail)

    def __setup_tenant_vlan_bigip_ve(self,
                                      job_input,
                                      pod_id,
                                      msa_device_id,
                                      msa_config_for_common,
                                      msa_config_for_device):

        msa_info = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input['port_id4']

        # List NAL_VNF_MNG(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id4
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()

        port_list = db_list.get_return_param()

        # Create Instance(MSA Soap Client)
        msa = bigipveordercmdws.BigIpVeOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create VLAN(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_ve_network_vlan',
            msa_device_id,
            job_input['network_name'],
            port_list[0]['nic']
        )
        msa_info['create_big_ip_ve_network_vlan'] = \
                                                msa_res[msa.RES_KEY_IN]

        # Setting SelfIP(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_network_self_ip',
            msa_device_id,
            job_input['self_ip_name'],
            port_list[0]['ip_address'],
            port_list[0]['netmask'],
            job_input['network_name']
        )
        msa_info['create_big_ip_network_self_ip'] = msa_res[msa.RES_KEY_IN]

        # Setting Static Route(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_network_routes',
            msa_device_id,
            'defaultGW',
            'yes',
            job_input['fw_ip_address'],
            '',
            ''
        )
        msa_info['create_big_ip_network_routes'] = msa_res[msa.RES_KEY_IN]

        # Setting DNS(MSA Soap Client)
        msa_dns_address = self.set_msa_dns_address(
                                            job_input, msa_config_for_common)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_system_dns',
            msa_device_id,
            job_input['host_name'],
            msa_dns_address['dns_server_primary'],
            msa_dns_address['dns_server_secondary']
        )
        msa_info['create_big_ip_system_dns'] = msa_res[msa.RES_KEY_IN]

        # Setting NTP(MSA Soap Client)
        msa_ntp_address = self.set_msa_ntp_address(
                                            job_input, msa_config_for_common)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_big_ip_system_ntp',
            msa_device_id,
            job_input['host_name'],
            msa_ntp_address['ntp_server_primary'],
            msa_ntp_address['ntp_server_secondary'],
            job_input['timezone']
        )
        msa_info['create_big_ip_system_ntp'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id4, msa_info)

    def __setup_add_ipv6_bigip_ve(self,
                                      job_input,
                                      pod_id,
                                      msa_device_id,
                                      msa_config_for_device):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id = job_input['port_id']
        vlan_name = job_input['network_name']
        fw_ip_v6_address = self.utils.get_ipaddress_compressed(
                                            job_input['fw_ip_v6_address'])

        # List NAL_PORT_MNG(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()

        port_list = db_list.get_return_param()

        msa_info = json.loads(port_list[0]['msa_info'])

        # Create Instance(MSA Soap Client)
        msa = bigipveordercmdws.BigIpVeOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Setting SelfIP IPv6(MSA Soap Client)
        object_params_v4 = json.loads(
            msa_info['create_big_ip_network_self_ip']['objectParameters'])

        for key in object_params_v4[
            msa.OBJECT_FILE_NAME['create_big_ip_network_self_ip']].keys():
            self_ip_name_v4 = key
            break

        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_f5_bigipve_ipv6_selfip',
            msa_device_id,
            self_ip_name_v4 + 'v6',
            port_list[0]['ip_address_v6'],
            port_list[0]['netmask_v6'],
            vlan_name
        )
        msa_info['create_f5_bigipve_ipv6_selfip'] = msa_res[msa.RES_KEY_IN]

        # Setting Static Route(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_f5_bigipve_ipv6_staticroute',
            msa_device_id,
            'defaultGWv6',
            'yes',
            fw_ip_v6_address,
            '',
            ''
        )
        msa_info['create_f5_bigipve_ipv6_staticroute'] = msa_res[
                                                            msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id, msa_info)

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

    def __update_db_apl(self, job_input, node_detail_update):

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

        node_detail_dict = json.loads(apl_list[0]['node_detail'])
        node_detail_dict.update(node_detail_update)

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [apl_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['node_detail'] = json.dumps(node_detail_dict)
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
