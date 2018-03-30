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
import socket
import struct
import time

from job.auto import base
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import intersecordercmdws


class SetupDeviceInterSecLb(base.JobAutoBase):

    def device_setup_create_intersec_lb(self, job_input):

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
        self.__setup_system_common_intersec_lb(job_input,
                                             pod_id,
                                             msa_device_id,
                                             msa_config_for_common,
                                             msa_config_for_device)

        # Setup Tenant VLAN Setting
        self.__setup_tenant_vlan_intersec_lb(job_input,
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

    def __setup_system_common_intersec_lb(self,
                                       job_input,
                                       pod_id,
                                       msa_device_id,
                                       msa_config_for_common,
                                       msa_config_for_device):

        node_detail = {}

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id1 = job_input['port_id1']

        # List NAL_VNF_MNG(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_list = list.ListClient(self.job_config)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id1
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()

        port_list = db_list.get_return_param()

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
                                    'create_intersec_lb_startup',
                                    msa_device_id,
                                    job_input['host_name'],
                                    port_list[0]['ip_address'],
                                    job_input['license_key']
        )
        node_detail[
            'create_intersec_lb_startup'] = msa_res[msa.RES_KEY_IN]

        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, node_detail)

    def __setup_tenant_vlan_intersec_lb(self,
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
        msa = intersecordercmdws.IntersecOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Calc BoadCastAddress
        ret = self.utils.get_network_range_from_cidr(
                    port_list[0]['ip_address'] + '/' + port_list[0]['netmask'])
        broadcastAddress = \
                socket.inet_ntoa(struct.pack(r'!l', ret['broadcast']))

        # Create Network(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_lb_nw',
            msa_device_id,
            port_list[0]['nic'],
            port_list[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(port_list[0]['netmask']),
            broadcastAddress
        )
        msa_info['create_intersec_lb_nw'] = \
                                                msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_lb_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Setting NTP(MSA Soap Client)
        msa_ntp_address = self.set_msa_ntp_address(
                                            job_input, msa_config_for_common)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_lb_ntp',
            msa_device_id,
            msa_ntp_address['ntp_server_primary']
        )
        msa_info['create_intersec_lb_ntp'] = msa_res[msa.RES_KEY_IN]

        # Setting Default Gateway(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_lb_default_gw',
            msa_device_id,
            job_input['fw_ip_address'],
            port_list[0]['nic']
        )
        msa_info['create_intersec_lb_default_gw'] = msa_res[msa.RES_KEY_IN]

        # Reboot(MSA)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_intersec_lb_reboot',
            msa_device_id
        )
        # Wait(MSA)
        self.__wait_for_reboot(pod_id, msa_device_id, msa_config_for_device)

        # Setting Zabbix(MSA Soap Client)
        zabbix_vip_ipaddress = job_input.get('zabbix_vip_ip', '')
        zabbix_01_ipaddress = job_input.get(' zabbix_01_ip', '')
        zabbix_02_ipaddress = job_input.get('zabbix_02_ip', '')

        if len(zabbix_vip_ipaddress) > 0 and \
                    len(zabbix_01_ipaddress) > 0 and \
                    len(zabbix_02_ipaddress) > 0:

            msa_res = self.execute_msa_command(
                msa_config_for_device,
                msa,
                'create_intersec_lb_zabbix',
                msa_device_id,
                job_input['host_name'],
                zabbix_vip_ipaddress,
                zabbix_01_ipaddress,
                zabbix_02_ipaddress
            )
            msa_info['create_intersec_lb_zabbix'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, port_id4, msa_info)

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
            msa_res = msa.check_boot_complete_lb(msa_device_id)

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
