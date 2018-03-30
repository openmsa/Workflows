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

from job.auto import base
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import fortigatevm541ordercmdws


class SetupDeviceFortigateVm541(base.JobAutoBase):

    def device_setup_create_for_fortigate_vm(self, job_input):

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
        self.__setup_system_common_fortigate(job_input,
                                             pod_id,
                                             msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)

        # Setup Pub LAN Setting
        self.__setup_pub_lan_fortigate(job_input,
                                       pod_id,
                                       msa_device_id,
                                       msa_config_for_common,
                                       msa_config_for_device)

        # Setup Ext LAN Setting
        self.__setup_ext_lan_fortigate(job_input,
                                       pod_id,
                                       msa_device_id,
                                       msa_config_for_common,
                                       msa_config_for_device)

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_fortigate(job_input,
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

    def device_add_port_for_fortigate_vm(self, job_input):

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
        self.__setup_tenant_vlan_fortigate(job_input,
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

    def device_setup_add_ipv6_for_fortigate_vm(self, job_input):

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

        # Setup Device(IPv6)
        self.__setup_fortigate_add_ipv6(job_input,
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

    def __setup_system_common_fortigate(self,
                                        job_input,
                                        pod_id,
                                        msa_device_id,
                                        msa_config_for_common,
                                        msa_config_for_device):

        node_detail = {}

        # Create Instance(MSA Soap Client)
        msa = fortigatevm541ordercmdws.FortigateVm541OrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create System Common(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_vm_system_common',
                                    msa_device_id,
                                    job_input['host_name'],
                                    msa_config_for_device['default_language'],
                                    msa_config_for_device['default_timezone']
        )
        node_detail[
            'create_fortigate_vm_system_common'] = msa_res[msa.RES_KEY_IN]

        # Create Admin Account(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_vm_admin_account',
                                    msa_device_id,
                                    job_input['admin_id'],
                                    job_input['admin_pw'],
                                    msa_config_for_device['admin_profile']
        )
        node_detail[
            'create_fortigate_vm_admin_account'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, node_detail)

    def __setup_pub_lan_fortigate(self,
                                  job_input,
                                  pod_id,
                                  msa_device_id,
                                  msa_config_for_common,
                                  msa_config_for_device):

        node_detail = {}
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
        msa = fortigatevm541ordercmdws.FortigateVm541OrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create DNS(MSA)
        msa_dns_address = self.set_msa_dns_address(
                                            job_input, msa_config_for_common)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_fortigate_vm_dns',
                    msa_device_id,
                    job_input['host_name'],
                    msa_dns_address['dns_server_primary'],
                    msa_dns_address['dns_server_secondary']
        )
        node_detail['create_fortigate_vm_dns'] = msa_res[msa.RES_KEY_IN]

        # Create NTP(MSA)
        msa_ntp_address = self.set_msa_ntp_address(
                                            job_input, msa_config_for_common)
        msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_fortigate_vm_ntp',
                    msa_device_id,
                    job_input['host_name'],
                    msa_config_for_device['default_ntp_action'],
                    msa_config_for_device['default_ntp_sync_interval'],
                    msa_ntp_address['ntp_server_primary'],
                    msa_ntp_address['ntp_server_secondary']
        )
        node_detail['create_fortigate_vm_ntp'] = msa_res[msa.RES_KEY_IN]

        # Create Static Route(MSA)
        msa_res = self.execute_msa_command(
                            msa_config_for_device,
                            msa,
                            'create_fortigate_vm_router_static',
                            msa_device_id,
                            msa_config_for_device['router_static_num'],
                            None,
                            'no',
                            msa_config_for_common['pub_vlan_gateway'],
                            msa_config_for_common['svc_vlan_network_address'],
                            self.utils.get_subnet_mask_from_cidr_len(
                              msa_config_for_common['svc_vlan_network_mask']),
                            port_list[0]['nic']
        )
        msa_info[
                'create_fortigate_vm_router_static'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, node_detail)

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, job_input['port_id2'], msa_info)

    def __setup_ext_lan_fortigate(self,
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
        msa = fortigatevm541ordercmdws.FortigateVm541OrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Create Interface(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_fortigate_vm_interface',
            msa_device_id,
            port_list[0]['nic'],
            port_list[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(
                                port_list[0]['netmask']),
            'Enable',
            'Disable',
            'Disable'
        )
        msa_info['create_fortigate_vm_interface'] = msa_res[msa.RES_KEY_IN]

        # Create Static Route(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_fortigate_vm_router_static',
            msa_device_id,
            2,
            None,
            'yes',
            msa_config_for_common['ext_vlan_gateway'],
            '',
            '',
            port_list[0]['nic']
        )
        msa_info[
                'create_fortigate_vm_router_static'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id3, msa_info)

    def __setup_tenant_vlan_fortigate(self,
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
        msa = fortigatevm541ordercmdws.FortigateVm541OrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        for count in range(int(self.job_config.MSA_AFTER_ATTACH_COUNT)):
            try:
                # Create Interface(MSA)
                msa_res = self.execute_msa_command(
                    msa_config_for_device,
                    msa,
                    'create_fortigate_vm_interface',
                    msa_device_id,
                    port_list[0]['nic'],
                    port_list[0]['ip_address'],
                    self.utils.get_subnet_mask_from_cidr_len(
                                        port_list[0]['netmask']),
                    'Enable',
                    'Enable',
                    'Enable'
                )
                msa_info['create_fortigate_vm_interface'] = \
                    msa_res[msa.RES_KEY_IN]
                break

            except SystemError as e:
                time.sleep(int(self.job_config.MSA_AFTER_ATTACH_INTERVAL))
                count += 1

                if count == int(self.job_config.MSA_AFTER_ATTACH_COUNT):
                    raise e

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id4, msa_info)

    def __setup_fortigate_add_ipv6(self,
                                        job_input,
                                        pod_id,
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

        # Get DB APL Data
        node_name = db_apl_data['node_name']
        node_detail = json.loads(db_apl_data['node_detail'])

        # Create Instance(MSA Soap Client)
        msa = fortigatevm541ordercmdws.FortigateVm541OrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Get DB PORT LIST(Tenant Vlan)
        port_list_tenant = self.__get_db_port(nal_tenant_id, node_id)

        tenant_ipv6_count = 0
        for port_tenant in port_list_tenant:
            if len(port_tenant['ip_address_v6']) > 0:
                tenant_ipv6_count = tenant_ipv6_count + 1

        if tenant_ipv6_count == 1:

            # Create System Common(MSA)
            msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_vm_system_common',
                                    msa_device_id,
                                    node_name,
                                    msa_config_for_device['default_language'],
                                    msa_config_for_device['default_timezone']
            )
            node_detail[
                'create_fortigate_vm_system_common'] = msa_res[msa.RES_KEY_IN]

            # Create GUI Enable IPv6(MSA)
            msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_vm_ipv6_gui_enable',
                                    msa_device_id,
                                    node_name
            )
            node_detail[
            'create_fortigate_vm_ipv6_gui_enable'] = msa_res[msa.RES_KEY_IN]

            # Update NAL_APL_MNG(DB)
            self.__update_db_apl(job_input, node_detail)

        if len(port_id_pub_ipv6) > 0:

            # Get NAL_PORT_MNG(Pub)
            port_res_pub = self.__get_db_port(
                                        nal_tenant_id, '', port_id_pub_ipv6)

            msa_info_pub = json.loads(port_res_pub[0]['msa_info'])

            # Create Interface IPv6(MSA) Pub
            msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_vm_ipv6_interface',
                                    msa_device_id,
                                    port_res_pub[0]['nic'],
                                    port_res_pub[0]['ip_address_v6'],
                                    port_res_pub[0]['netmask_v6'],
                                    'enable',
                                    'enable',
                                    'enable'
            )
            msa_info_pub[
                'create_fortigate_vm_ipv6_interface'] = msa_res[msa.RES_KEY_IN]

            # Create Static Route IPv6(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_fortigate_vm_ipv6_staticroute',
                msa_device_id,
                '3',
                'no',
                self.utils.get_ipaddress_compressed(
                    msa_config_for_common['pub_vlan_gateway_ipv6']),
                self.utils.get_ipaddress_compressed(
                    msa_config_for_common['svc_vlan_network_address_ipv6']),
                msa_config_for_common['svc_vlan_network_mask_ipv6'],
                port_res_pub[0]['nic']
            )
            msa_info_pub[
            'create_fortigate_vm_ipv6_staticroute'] = msa_res[msa.RES_KEY_IN]

            # Update NAL_PORT_MNG(DB) Pub
            self.__update_db_port(job_input, port_id_pub_ipv6, msa_info_pub)

        if len(port_id_ext_ipv6) > 0:

            # Get NAL_PORT_MNG(Ext)
            port_res_ext = self.__get_db_port(
                                        nal_tenant_id, '', port_id_ext_ipv6)

            msa_info_ext = json.loads(port_res_ext[0]['msa_info'])

            # Create Interface IPv6(MSA) Ext
            msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_vm_ipv6_interface',
                                    msa_device_id,
                                    port_res_ext[0]['nic'],
                                    port_res_ext[0]['ip_address_v6'],
                                    port_res_ext[0]['netmask_v6'],
                                    'enable',
                                    'disable',
                                    'disable'
            )
            msa_info_ext[
                'create_fortigate_vm_ipv6_interface'] = msa_res[msa.RES_KEY_IN]

            # Create Static Route IPv6(MSA)
            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_fortigate_vm_ipv6_staticroute',
                msa_device_id,
                '4',
                'yes',
                self.utils.get_ipaddress_compressed(
                    msa_config_for_common['ext_vlan_gateway_ipv6']),
                '',
                '',
                port_res_ext[0]['nic']
            )
            msa_info_ext[
            'create_fortigate_vm_ipv6_staticroute'] = msa_res[msa.RES_KEY_IN]

            # Update NAL_PORT_MNG(DB) Ext
            self.__update_db_port(job_input, port_id_ext_ipv6, msa_info_ext)

        # Get NAL_PORT_MNG(Tenant VLAN)
        port_res_tenant = self.__get_db_port(nal_tenant_id, '', port_id)

        msa_info_tenant = json.loads(port_res_tenant[0]['msa_info'])

        # Create Interface IPv6(MSA) Tenant
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_fortigate_vm_ipv6_interface',
                                    msa_device_id,
                                    port_res_tenant[0]['nic'],
                                    port_res_tenant[0]['ip_address_v6'],
                                    port_res_tenant[0]['netmask_v6'],
                                    'enable',
                                    'enable',
                                    'enable'
        )
        msa_info_tenant[
                'create_fortigate_vm_ipv6_interface'] = msa_res[msa.RES_KEY_IN]

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
