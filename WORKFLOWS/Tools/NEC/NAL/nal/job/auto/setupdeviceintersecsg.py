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
from job.lib.soap.msa import intersecordercmdws


class SetupDeviceInterSecSg(base.JobAutoBase):

    def device_setup_intersec(self, job_input):

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
        self.__setup_system_common_intersec(job_input,
                                             pod_id,
                                             msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)

        # Setup Ext LAN Setting
        self.__setup_ext_lan_intersec(job_input,
                                             pod_id,
                                             msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_intersec(job_input,
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
        params['default_gateway'] = msa_config_for_common['ext_vlan_gateway']
        db_update.set_context(db_endpoint, keys, params)
        db_update.execute()

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_add_port_intersec(self, job_input):

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

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_add(job_input,
                                     pod_id,
                                     msa_device_id,
                                     msa_config_for_common,
                                     msa_config_for_device)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def msa_configuration_add_ipv6_for_intersec_sg_pub(self, job_input):

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

        # Setup MSA(Intersec SG IPv6)
        self.__setup_msa_intersec_sg_ipv6_pub(job_input,
                                                 msa_device_id,
                                                 msa_config_for_common,
                                                 msa_config_for_device)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, {})

        return {}

    def msa_configuration_add_ipv6_for_intersec_sg_internet(self, job_input):

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

        # Setup MSA(Intersec SG IPv6)
        self.__setup_msa_intersec_sg_ipv6_ext(job_input,
                                                 msa_device_id,
                                                 msa_config_for_common,
                                                 msa_config_for_device)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, {})

        return {}

    def device_del_port_intersec(self, job_input):

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

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_del(job_input,
                                     pod_id,
                                     msa_device_id,
                                     msa_config_for_common,
                                     msa_config_for_device)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_intersec_pub(self, job_input):

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
        self.__setup_system_common_intersec(job_input,
                                             pod_id,
                                             msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)

        # Setup Pub LAN Setting
        self.__setup_pub_lan_intersec_pub(job_input,
                                             pod_id,
                                             msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_intersec_pub(job_input,
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
        params['default_gateway'] = msa_config_for_common['pub_vlan_gateway']
        db_update.set_context(db_endpoint, keys, params)
        db_update.execute()

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __setup_system_common_intersec(self,
                                  job_input,
                                  pod_id,
                                  msa_device_id,
                                  msa_config_for_common,
                                  msa_config_for_device):

        node_detail = {}

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Create System Common(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_intersec_sg_startup',
                                    msa_device_id,
                                    job_input['host_name'],
                                    job_input['license_key']
        )
        node_detail['create_intersec_sg_startup'] = msa_res[msa.RES_KEY_IN]

        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, node_detail)

    def __setup_pub_lan_intersec_pub(self,
                                  job_input,
                                  pod_id,
                                  msa_device_id,
                                  msa_config_for_common,
                                  msa_config_for_device):

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

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        for count in range(int(self.job_config.MSA_AFTER_ATTACH_COUNT)):
            try:
                # Create Network(MSA)
                msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_intersec_sg_nw',
                    msa_device_id,
                    port_list[0]['nic'],
                    port_list[0]['ip_address'],
                    self.utils.get_subnet_mask_from_cidr_len(
                                                port_list[0]['netmask'])
                )
                msa_info['create_intersec_sg_nw'] = msa_res[msa.RES_KEY_IN]
                break

            except SystemError as e:
                time.sleep(int(self.job_config.MSA_AFTER_ATTACH_INTERVAL))
                count += 1

                if count == int(self.job_config.MSA_AFTER_ATTACH_COUNT):
                    raise e

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Create NTP(MSA)
        msa_ntp_address = self.set_msa_ntp_address(
                                            job_input, msa_config_for_common)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_ntp',
            msa_device_id,
            msa_ntp_address['ntp_server_primary']
        )
        msa_info['create_intersec_sg_ntp'] = msa_res[msa.RES_KEY_IN]

        # Create Default Gateway(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_default_gw',
            msa_device_id,
            msa_config_for_common['pub_vlan_gateway']
        )
        msa_info['create_intersec_sg_default_gw'] = msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, job_input['port_id2'], msa_info)

    def __setup_ext_lan_intersec(self,
                                  job_input,
                                  pod_id,
                                  msa_device_id,
                                  msa_config_for_common,
                                  msa_config_for_device):

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

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create Network(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_nw',
            msa_device_id,
            port_list[0]['nic'],
            port_list[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(port_list[0]['netmask'])
        )
        msa_info['create_intersec_sg_nw'] = msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Create NTP(MSA)
        msa_ntp_address = self.set_msa_ntp_address(
                                            job_input, msa_config_for_common)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_ntp',
            msa_device_id,
            msa_ntp_address['ntp_server_primary']
        )
        msa_info['create_intersec_sg_ntp'] = msa_res[msa.RES_KEY_IN]

        # Create Default Gateway(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_default_gw',
            msa_device_id,
            msa_config_for_common['ext_vlan_gateway']
        )
        msa_info['create_intersec_sg_default_gw'] = msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, job_input['port_id3'], msa_info)

    def __setup_tenant_vlan_intersec(self,
                                     job_input,
                                     pod_id,
                                     msa_device_id,
                                     msa_config_for_common,
                                     msa_config_for_device):

        # Setup Tenant VLAN Setting
        result = self.__setup_tenant_vlan_intersec_base(job_input,
                                                        pod_id,
                                                        msa_device_id,
                                                        msa_config_for_common,
                                                        msa_config_for_device)
        node_detail = result['node_detail']
        msa_info = result['msa_info']

        # Create Static Route(MSA)
        static_route_ip = job_input.get('static_route_ip')

        if len(static_route_ip) > 0:

            msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_static_route',
                msa_device_id,
                msa_config_for_common['svc_vlan_network_address'],
                self.utils.get_subnet_mask_from_cidr_len(
                            msa_config_for_common['svc_vlan_network_mask']),
                static_route_ip
            )
            node_detail['create_intersec_sg_static_route'] = \
                                                    msa_res[msa.RES_KEY_IN]

            # Reboot(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
            # Wait(MSA)
            self.__wait_for_reboot(
                            pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, node_detail)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, job_input['port_id4'], msa_info)

    def __setup_tenant_vlan_intersec_pub(self,
                                         job_input,
                                         pod_id,
                                         msa_device_id,
                                         msa_config_for_common,
                                         msa_config_for_device):

        # Setup Tenant VLAN Setting
        result = self.__setup_tenant_vlan_intersec_base(job_input,
                                                        pod_id,
                                                        msa_device_id,
                                                        msa_config_for_common,
                                                        msa_config_for_device)
        node_detail = result['node_detail']
        msa_info = result['msa_info']

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, node_detail)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, job_input['port_id4'], msa_info)

    def __setup_tenant_vlan_intersec_base(self,
                                          job_input,
                                          pod_id,
                                          msa_device_id,
                                          msa_config_for_common,
                                          msa_config_for_device):

        msa_info = {}
        node_detail = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input['port_id4']

        # List NAL_VNF_MNG(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id4
        db_list.set_context(db_endpoint, params)
        db_list.execute()

        port_list = db_list.get_return_param()

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create Network(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_nw',
            msa_device_id,
            port_list[0]['nic'],
            port_list[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(port_list[0]['netmask'])
        )
        msa_info['create_intersec_sg_nw'] = msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Create Zabbix Setting(MSA)
        zabbixVIPipAddress = job_input.get('zabbix_vip_ip')
        zabbix01ipAddress = job_input.get('zabbix_01_ip')
        zabbix02ipAddress = job_input.get('zabbix_02_ip')

        if len(zabbixVIPipAddress) > 0 \
                and len(zabbix01ipAddress) > 0 \
                and len(zabbix02ipAddress) > 0:

            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_zabbix',
                msa_device_id,
                job_input['host_name'],
                zabbixVIPipAddress,
                zabbix01ipAddress,
                zabbix02ipAddress
            )
            node_detail['create_intersec_sg_zabbix'] = msa_res[msa.RES_KEY_IN]

        return {'node_detail': node_detail, 'msa_info': msa_info}

    def __setup_tenant_vlan_add(self,
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
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id4
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create Network(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_nw',
            msa_device_id,
            port_list[0]['nic'],
            port_list[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(port_list[0]['netmask'])
        )
        msa_info['create_intersec_sg_nw'] = msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, job_input['port_id4'], msa_info)

    def __setup_msa_intersec_sg_ipv6_pub(self,
                                job_input,
                                msa_device_id,
                                msa_config_for_common,
                                msa_config_for_device):

        # Get JOB Input Parameters
        port_id_pub_ipv6 = job_input['port_id_pub_ipv6']
        port_id = job_input['port_id']
        pod_id = job_input['pod_id']
        node_id = job_input['node_id']
        nal_tenant_id = job_input['nal_tenant_id']

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        if len(port_id_pub_ipv6) > 0:

            # List NAL_APL_MNG(DB)
            params = {}
            params['node_id'] = node_id
            params['delete_flg'] = 0
            db_list.set_context(db_endpoint_apl, params)
            db_list.execute()
            apl_db_res = db_list.get_return_param()

            node_name = apl_db_res[0]['node_name']

            # List NAL_PORT_MNG(DB)
            params = {}
            params['tenant_id'] = nal_tenant_id
            params['port_id'] = port_id_pub_ipv6
            params['delete_flg'] = 0
            db_list.set_context(db_endpoint_port, params)
            db_list.execute()
            port_db_pub_res = db_list.get_return_param()

            msa_info_pub = json.loads(port_db_pub_res[0]['msa_info'])

            # Create Interface IPv6(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_nec_intersecvmsg_ipv6_interface',
                msa_device_id,
                port_db_pub_res[0]['nic'],
                port_db_pub_res[0]['ip_address_v6'],
                port_db_pub_res[0]['netmask_v6']
            )
            msa_info_pub['create_nec_intersecvmsg_ipv6_interface'] \
                                                    = msa_res[msa.RES_KEY_IN]

            # Reboot(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
            # Wait(MSA)
            self.__wait_for_reboot(
                                pod_id, msa_device_id, msa_config_for_device)

            # Create Default Gateway IPv6(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_nec_intersecvmsg_ipv6_defaultgw',
                msa_device_id,
                node_name,
                self.utils.get_ipaddress_compressed(
                            msa_config_for_common['pub_vlan_gateway_ipv6']),
                msa_config_for_device['defaultgw_source_interface_ipv6']
            )
            msa_info_pub['create_nec_intersecvmsg_ipv6_defaultgw'] \
                                                    = msa_res[msa.RES_KEY_IN]

            # Reboot(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
            # Wait(MSA)
            self.__wait_for_reboot(
                                pod_id, msa_device_id, msa_config_for_device)

            # Update NAL_PORT_MNG(DB)
            self.__update_db_port(job_input, port_id_pub_ipv6, msa_info_pub)

        # List NAL_PORT_MNG(DB)
        params = {}
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_db_tenant_res = db_list.get_return_param()

        msa_info_tenant = json.loads(port_db_tenant_res[0]['msa_info'])

        # Create Interface IPv6(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_nec_intersecvmsg_ipv6_interface',
            msa_device_id,
            port_db_tenant_res[0]['nic'],
            port_db_tenant_res[0]['ip_address_v6'],
            port_db_tenant_res[0]['netmask_v6']
        )
        msa_info_tenant['create_nec_intersecvmsg_ipv6_interface'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
        # Wait(MSA)
        self.__wait_for_reboot(
                                pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id, msa_info_tenant)

    def __setup_msa_intersec_sg_ipv6_ext(self,
                                job_input,
                                msa_device_id,
                                msa_config_for_common,
                                msa_config_for_device):

        # Get JOB Input Parameters
        port_id_ext_ipv6 = job_input['port_id_ext_ipv6']
        port_id = job_input['port_id']
        pod_id = job_input['pod_id']
        node_id = job_input['node_id']
        nal_tenant_id = job_input['nal_tenant_id']

        static_route_ip_ipv6 = job_input.get('static_route_ip_ipv6', '')

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        if len(port_id_ext_ipv6) > 0:

            # List NAL_APL_MNG(DB)
            params = {}
            params['node_id'] = node_id
            params['delete_flg'] = 0
            db_list.set_context(db_endpoint_apl, params)
            db_list.execute()
            apl_db_res = db_list.get_return_param()

            node_name = apl_db_res[0]['node_name']

            # List NAL_PORT_MNG(DB)
            params = {}
            params['tenant_id'] = nal_tenant_id
            params['port_id'] = port_id_ext_ipv6
            params['delete_flg'] = 0
            db_list.set_context(db_endpoint_port, params)
            db_list.execute()
            port_db_ext_res = db_list.get_return_param()

            msa_info_ext = json.loads(port_db_ext_res[0]['msa_info'])

            # Create Interface IPv6(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_nec_intersecvmsg_ipv6_interface',
                msa_device_id,
                port_db_ext_res[0]['nic'],
                port_db_ext_res[0]['ip_address_v6'],
                port_db_ext_res[0]['netmask_v6']
            )
            msa_info_ext['create_nec_intersecvmsg_ipv6_interface'] \
                                                    = msa_res[msa.RES_KEY_IN]

            # Reboot(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
            # Wait(MSA)
            self.__wait_for_reboot(
                                pod_id, msa_device_id, msa_config_for_device)

            # Create Default Gateway IPv6(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_nec_intersecvmsg_ipv6_defaultgw',
                msa_device_id,
                node_name,
                self.utils.get_ipaddress_compressed(
                            msa_config_for_common['ext_vlan_gateway_ipv6']),
                msa_config_for_device['defaultgw_source_interface_ipv6']
            )
            msa_info_ext['create_nec_intersecvmsg_ipv6_defaultgw'] \
                                                    = msa_res[msa.RES_KEY_IN]

            # Reboot(MSA)
            self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
            # Wait(MSA)
            self.__wait_for_reboot(
                                pod_id, msa_device_id, msa_config_for_device)

            # Update NAL_PORT_MNG(DB)
            self.__update_db_port(job_input, port_id_ext_ipv6, msa_info_ext)

        # List NAL_PORT_MNG(DB)
        params = {}
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_db_tenant_res = db_list.get_return_param()

        msa_info_tenant = json.loads(port_db_tenant_res[0]['msa_info'])

        # Create Interface IPv6(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_nec_intersecvmsg_ipv6_interface',
            msa_device_id,
            port_db_tenant_res[0]['nic'],
            port_db_tenant_res[0]['ip_address_v6'],
            port_db_tenant_res[0]['netmask_v6']
        )
        msa_info_tenant['create_nec_intersecvmsg_ipv6_interface'] \
                                                    = msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        if len(static_route_ip_ipv6) > 0:

            static_route_ip_ipv6 = self.utils.get_ipaddress_compressed(
                                                        static_route_ip_ipv6)

            # Create Static Route IPv6(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_nec_intersecvmsg_ipv6_staticroute',
                msa_device_id,
                '1',
                self.utils.get_ipaddress_compressed(
                    msa_config_for_common['svc_vlan_network_address_ipv6']),
                msa_config_for_common['svc_vlan_network_mask_ipv6'],
                static_route_ip_ipv6
            )
            msa_info_tenant['create_nec_intersecvmsg_ipv6_staticroute'] \
                                                    = msa_res[msa.RES_KEY_IN]

            # Reboot(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
            # Wait(MSA)
            self.__wait_for_reboot(
                                pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id, msa_info_tenant)

    def __setup_tenant_vlan_del(self,
                                job_input,
                                pod_id,
                                msa_device_id,
                                msa_config_for_common,
                                msa_config_for_device):

        msa_info = {}
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input['port_id']

        # List NAL_VNF_MNG(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id4
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        ip_address_v6 = port_list[0]['ip_address_v6']

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        if len(ip_address_v6) > 0:

            try:
                # Delete Interface IPv6(MSA)
                msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'delete_nec_intersecvmsg_ipv6_interface',
                    msa_device_id,
                    port_list[0]['nic']
                )
                msa_info['delete_nec_intersecvmsg_ipv6_interface'] \
                                                = msa_res[msa.RES_KEY_IN]
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            # Reboot(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_sg_reboot',
                msa_device_id
            )
            # Wait(MSA)
            self.__wait_for_reboot(
                            pod_id, msa_device_id, msa_config_for_device)

        try:
            # Delete Interface IPv4(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'delete_intersec_sg_nw',
                msa_device_id,
                port_list[0]['nic']
            )
            msa_info['delete_intersec_sg_nw'] = msa_res[msa.RES_KEY_IN]
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_sg_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, job_input['port_id'], msa_info)

    def __wait_for_reboot(self,
                      pod_id,
                      msa_device_id,
                      msa_config_for_device):

        # Create Instance(MSA Soap Client)
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        if len(msa_config_for_device) != 0:
            retry_count = msa_config_for_device.get('retry_count', '18')
            sleep_time_sec = msa_config_for_device.get('sleep_time_sec', '10')
        else:
            retry_count = '18'
            sleep_time_sec = '10'

        for count in range(int(retry_count)):

            # Reboot(MSA)
            msa_res = msa.check_boot_complete_sg(msa_device_id)

            if msa_res['out']['status'] == 'OK':
                break

            time.sleep(int(sleep_time_sec))
            count += 1

        if str(count) == str(retry_count):
            raise SystemError('Waitting for MSA Reboot is TimeOver.')

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
