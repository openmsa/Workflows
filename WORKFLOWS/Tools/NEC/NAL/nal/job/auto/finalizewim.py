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

from job.auto import base
from job.lib.db import create
from job.lib.db import list
from job.lib.db import update


class FinalizeWim(base.JobAutoBase):

    def finalize_dc_connect_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        virtual_apl_list = job_input['data']['virtual_apl_list']
        virtual_lan_list = job_input['data']['virtual_lan_list']
        apl_port_list = job_input['data']['apl_port_list']
        update_apl_port_list = job_input['data']['update_apl_port_list']
        license_list = job_input['data'].get('license_list', [])
        update_apl_wan_port_list = job_input['data'].get(
                                            'update_apl_wan_port_list', [])

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_endpoint_license = \
            self.get_db_endpoint(self.job_config.REST_URI_LICENSE)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # Create NAL_APL_MNG(DB Client)
        for virtual_apl_data in virtual_apl_list:
            params = {}
            params['create_id'] = virtual_apl_data['create_id']
            params['update_id'] = virtual_apl_data['update_id']
            params['delete_flg'] = virtual_apl_data['delete_flg']
            params['tenant_name'] = virtual_apl_data['tenant_name']
            params['apl_type'] = virtual_apl_data['apl_type']
            params['type'] = virtual_apl_data['type']
            params['device_type'] = virtual_apl_data['device_type']
            params['tenant_id'] = virtual_apl_data['tenant_id']
            params['pod_id'] = virtual_apl_data['pod_id']
            params['node_id'] = virtual_apl_data['node_id']
            params['node_name'] = virtual_apl_data['node_name']
            params['node_detail'] = virtual_apl_data['node_detail']
            params['server_id'] = virtual_apl_data['server_id']
            params['server_info'] = virtual_apl_data['server_info']
            params['MSA_device_id'] = virtual_apl_data['MSA_device_id']
            params['dns_server_ip_address'] = \
                virtual_apl_data.get('dns_server_ip_address', '')
            params['ntp_server_ip_address'] = \
                virtual_apl_data.get('ntp_server_ip_address', '')
            params['snmp_server_ip_address'] = \
                virtual_apl_data.get('snmp_server_ip_address', '')
            params['syslog_server_ip_address'] = \
                virtual_apl_data.get('syslog_server_ip_address', '')
            db_create_instance.set_context(db_endpoint_apl, params)
            db_create_instance.execute()

        # Create NAL_VIRTUAL_LAN_MNG(DB Client)
        for virtual_lan_data in virtual_lan_list:
            params = {}
            params['create_id'] = virtual_lan_data['create_id']
            params['update_id'] = virtual_lan_data['update_id']
            params['delete_flg'] = virtual_lan_data['delete_flg']
            params['tenant_name'] = virtual_lan_data['tenant_name']
            params['tenant_id'] = virtual_lan_data['tenant_id']
            params['network_id'] = virtual_lan_data['network_id']
            params['pod_id'] = virtual_lan_data['pod_id']
            params['vlan_id'] = virtual_lan_data['vlan_id']
            params['IaaS_network_type'] \
                                = virtual_lan_data['IaaS_network_type']
            params['IaaS_network_id'] \
                                = virtual_lan_data['IaaS_network_id']
            params['IaaS_segmentation_id'] \
                                = virtual_lan_data['IaaS_segmentation_id']
            params['rule_id'] = virtual_lan_data['rule_id']
            params['nal_vlan_info'] = virtual_lan_data['nal_vlan_info']
            db_create_instance.set_context(db_endpoint_vlan, params)
            db_create_instance.execute()

        # Create NAL_PORT_MNG(DB Client)
        for apl_port_data in apl_port_list:
            params = {}
            params['create_id'] = apl_port_data['create_id']
            params['update_id'] = apl_port_data['update_id']
            params['delete_flg'] = apl_port_data['delete_flg']
            params['tenant_name'] = apl_port_data['tenant_name']
            params['tenant_id'] = apl_port_data['tenant_id']
            params['apl_type'] = apl_port_data['apl_type']
            params['port_id'] = apl_port_data['port_id']
            params['IaaS_port_id'] = apl_port_data['IaaS_port_id']
            params['node_id'] = apl_port_data['node_id']
            params['network_id'] = apl_port_data['network_id']
            params['nic'] = apl_port_data['nic']
            params['ip_address'] = apl_port_data['ip_address']
            params['netmask'] = apl_port_data['netmask']
            params['ip_address_v6'] = apl_port_data.get('ip_address_v6', '')
            params['netmask_v6'] = apl_port_data.get('netmask_v6', '')
            params['port_info'] = apl_port_data['port_info']
            params['msa_info'] = apl_port_data['msa_info']
            params['network_type'] = apl_port_data['network_type']
            params['network_type_detail'] = apl_port_data[
                                                    'network_type_detail']
            db_create_instance.set_context(db_endpoint_port, params)
            db_create_instance.execute()

        # Update NAL_PORT_MNG(DB Client)
        for apl_port_data in update_apl_port_list:
            params = {}
            params['update_id'] = apl_port_data['params']['update_id']
            params['node_id'] = apl_port_data['params']['node_id']
            params['nic'] = apl_port_data['params']['nic']
            params['msa_info'] = apl_port_data['params']['msa_info']
            keys = [apl_port_data['keys']['ID']]
            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

        for apl_port_data in update_apl_wan_port_list:
            params = {}
            params['update_id'] = apl_port_data['params']['update_id']
            params['msa_info'] = apl_port_data['params']['msa_info']

            if 'ip_address_v6' in apl_port_data['params']:
                params['ip_address_v6'] = apl_port_data['params'][
                                                            'ip_address_v6']
            if 'netmask_v6' in apl_port_data['params']:
                params['netmask_v6'] = apl_port_data['params']['netmask_v6']

            if 'port_info' in apl_port_data['params']:
                params['port_info'] = apl_port_data['params']['port_info']

            keys = [apl_port_data['keys']['ID']]
            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

        # Update NAL_LICENSE_MNG(DB Client)
        for (license_id, apl_info) in zip(license_list, virtual_apl_list):

            # Update NAL_LICENSE_MNG
            keys = [license_id]
            params = {}
            params['node_id'] = apl_info['node_id']
            db_update_instance.set_context(db_endpoint_license,
                                           keys, params)
            db_update_instance.execute()

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def finalize_dc_disconnect_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        logical_delete_apl_list = job_input['data']['logical_delete_apl_list']
        logical_delete_apl_port_list \
                        = job_input['data']['logical_delete_apl_port_list']
        logical_delete_vlan_list \
                        = job_input['data']['logical_delete_vlan_list']

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # Update NAL_APL_MNG(DB Client)
        for apl_data in logical_delete_apl_list:

            params = {}
            params['delete_flg'] = apl_data['search']['delete_flg']
            params['tenant_id'] = apl_data['search']['tenant_id']
            params['apl_type'] = apl_data['search']['apl_type']
            params['type'] = apl_data['search']['type']
            params['device_type'] = apl_data['search']['device_type']
            params['node_id'] = apl_data['search']['node_id']
            db_list_instance.set_context(db_endpoint_apl, params)
            db_list_instance.execute()
            apl_list = db_list_instance.get_return_param()

            params = {}
            params['update_id'] = apl_data['params']['update_id']
            params['delete_flg'] = apl_data['params']['delete_flg']
            keys = [apl_list[0]['ID']]
            db_update_instance.set_context(db_endpoint_apl, keys, params)
            db_update_instance.execute()

        # Update NAL_PORT_MNG(DB Client)
        for port_data in logical_delete_apl_port_list:

            params = {}
            params['delete_flg'] = port_data['search']['delete_flg']
            params['tenant_id'] = port_data['search']['tenant_id']
            params['apl_type'] = port_data['search']['apl_type']
            params['port_id'] = port_data['search']['port_id']
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list = db_list_instance.get_return_param()

            params = {}
            params['update_id'] = port_data['params']['update_id']
            params['delete_flg'] = port_data['params']['delete_flg']
            keys = [port_list[0]['ID']]
            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

        # Update NAL_VIRTUAL_LAN_MNG(DB Client)
        for vlan_data in logical_delete_vlan_list:

            params = {}
            params['delete_flg'] = vlan_data['search']['delete_flg']
            params['tenant_id'] = vlan_data['search']['tenant_id']
            params['network_id'] = vlan_data['search']['network_id']
            db_list_instance.set_context(db_endpoint_vlan, params)
            db_list_instance.execute()
            vlan_list = db_list_instance.get_return_param()

            params = {}
            params['update_id'] = vlan_data['params']['update_id']
            params['delete_flg'] = vlan_data['params']['delete_flg']
            keys = [vlan_list[0]['ID']]
            db_update_instance.set_context(db_endpoint_vlan, keys, params)
            db_update_instance.execute()

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_finalize_bandwidth(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['data']['operation_id']
        tenant_name = job_input['data']['tenant_name']
        bandwidth = job_input['data']['bandwidth']
        virtual_apl_list = job_input['data']['virtual_apl_list']
        license_list = job_input['data']['license_list']

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_license = self.get_db_endpoint(
                                    self.job_config.REST_URI_LICENSE)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        for (license_id, apl_data) in zip(license_list, virtual_apl_list):

            # Update NAL_APL_MNG(DB Client)
            params = {}
            params['update_id'] = operation_id
            params['node_detail'] = apl_data['node_detail']
            keys = [apl_data['apl_rec_id']]
            db_update_instance.set_context(db_endpoint_apl, keys, params)
            db_update_instance.execute()

            # List NAL_LICENSE_MNG(DB Client)
            params = {}
            params['node_id'] = apl_data['node_id']
            params['tenant_name'] = tenant_name
            params['status'] = '2'
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_license, params)
            db_list_instance.execute()
            license_list = db_list_instance.get_return_param()

            # Update NAL_LICENSE_MNG(DB Client)
            keys = [license_list[0]['ID']]
            params = {}
            params['update_id'] = operation_id
            params['node_id'] = ''
            params['tenant_name'] = ''
            params['status'] = '3'
            db_update_instance.set_context(db_endpoint_license, keys, params)
            db_update_instance.execute()

            # Update NAL_LICENSE_MNG(DB Client)
            keys = [license_id]
            params = {}
            params['update_id'] = operation_id
            params['node_id'] = apl_data['node_id']
            db_update_instance.set_context(db_endpoint_license, keys, params)
            db_update_instance.execute()

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_rt_finalize_setting_update(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['data']['operation_id']
        virtual_apl_list = job_input['data']['virtual_apl_list']

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)

        for apl_data in virtual_apl_list:

            # Update NAL_APL_MNG(DB Client)
            params = {}
            params['update_id'] = operation_id
            params['node_detail'] = apl_data['node_detail']
            if 'dns_server_ip_address' in apl_data:
                params['dns_server_ip_address'] = \
                    apl_data['dns_server_ip_address']
            if 'ntp_server_ip_address' in apl_data:
                params['ntp_server_ip_address'] = \
                    apl_data['ntp_server_ip_address']
            if 'snmp_server_ip_address' in apl_data:
                params['snmp_server_ip_address'] = \
                    apl_data['snmp_server_ip_address']
            if 'syslog_server_ip_address' in apl_data:
                params['syslog_server_ip_address'] = \
                    apl_data['syslog_server_ip_address']
            keys = [apl_data['apl_rec_id']]
            db_update_instance.set_context(db_endpoint_apl, keys, params)
            db_update_instance.execute()

        # Output Log(Job Output)
        job_output = {}
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output
