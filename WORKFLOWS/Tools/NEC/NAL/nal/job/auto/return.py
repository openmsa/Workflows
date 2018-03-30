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
from job.lib.db import list
from job.lib.db import update


class Return(base.JobAutoBase):

    def terminate_create_apl(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Update to complete the status of the APL
        self.__update_db_server_task_status_end(job_input)

        # Set Return Value
        result = {
            'status': 0,
            'error-code': '',
            'message': '',
        }
        data = {}

        # Set JOB Output Parameters
        job_output = {
            'result': result,
            'data': data
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def terminate_update_apl(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Update to complete the status of the APL
        self.__update_db_server_task_status_end_for_update(job_input)

        # Set Return Value
        result = {
            'status': 0,
            'error-code': '',
            'message': '',
        }
        data = {}

        # Set JOB Output Parameters
        job_output = {
            'result': result,
            'data': data
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def get_job_return_value(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Set Return Value
        result = {
            'status': 0,
            'error-code': '',
            'message': '',
        }
        data = job_input.get('job_ret_data', {})

        # Set JOB Output Parameters
        job_output = {
            'result': result,
            'data': data
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def get_job_return_value_wim(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # task status update
        self.__update_db_service_task_status_end_for_update(job_input)

        # Set Return Value
        result = {
            'status': 0,
            'error-code': '',
            'message': '',
        }
        data = job_input.get('job_ret_data', {})

        # Set JOB Output Parameters
        job_output = {
            'result': result,
            'data': data
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_physical_pt_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'node_id': job_input['node_id'],
            'ip_address': job_input['free_ip_iaas']['ip'],
            'netmask': job_input['free_ip_iaas']['netmask'],
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_connect_prepare(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'operation_id': job_input['operation_id'],
            'group_id': job_input.get('group_id', ''),
            'group_type': job_input['service_type'],
            'group_name': job_input['service_name'],
            'apl_type': job_input['apl_type'],
            'type': job_input['type'],
            'device_type': job_input['device_type'],
            'IaaS_region_id': job_input['IaaS_region_id'],
            'IaaS_tenant_id': job_input['IaaS_tenant_id'],
            'IaaS_tenant_name': job_input['IaaS_tenant_name'],
            'IaaS_network_id': job_input['IaaS_network_id'],
            'IaaS_network_type': job_input['IaaS_network_type'],
            'IaaS_segmentation_id': job_input['IaaS_segmentation_id'],
            'IaaS_subnet_id': job_input['IaaS_subnet_id'],
            'network_name': job_input['network_name'],
            'tenant_name': job_input['tenant_name'],
            'dc_id': job_input['dc_id'],
            'pod_id': job_input['pod_id'],
            'nal_tenant_id': job_input['nal_tenant_id'],
            'nal_tenant_name': job_input['tenant_name'],
            'msa_customer_id': job_input['msa_customer_id'],
            'fw_ip_address': job_input['fw_ip_address'],
            'tenant_port_info': {'vrrp': job_input['vrrp'],
                                 'ce01': job_input['ce01'],
                                 'ce02': job_input['ce02'],
            },
            'msa_network_info': job_input['msa_network_info'],
            'bandwidth': job_input.get('bandwidth', ''),
            'dns_server_ip_address': job_input.get(
                                                'dns_server_ip_address', ''),
            'ntp_server_ip_address': job_input.get(
                                                'ntp_server_ip_address', ''),
            'snmp_server_ip_address': job_input.get(
                                                'snmp_server_ip_address', ''),
            'syslog_server_ip_address': job_input.get(
                                            'syslog_server_ip_address', ''),
            'license_list': job_input.get('license_list', '')
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_connect_update_prepare(self,
                                                              job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'operation_id': job_input['operation_id'],
            'group_type': job_input['service_type'],
            'apl_type': job_input['apl_type'],
            'type': job_input['type'],
            'device_type': job_input['device_type'],
            'IaaS_region_id': job_input['IaaS_region_id'],
            'IaaS_tenant_id': job_input['IaaS_tenant_id'],
            'IaaS_network_type': job_input['IaaS_network_type'],
            'network_name': job_input['network_name'],
            'IaaS_network_id': job_input['IaaS_network_id'],
            'IaaS_subnet_id': job_input['IaaS_subnet_id'],
            'IaaS_segmentation_id': job_input['IaaS_segmentation_id'],
            'tenant_name': job_input['tenant_name'],
            'dc_id': job_input['dc_id'],
            'pod_id': job_input['pod_id'],
            'nal_tenant_id': job_input['nal_tenant_id'],
            'apl_info': job_input['apl_info'],
            'tenant_lan_list': job_input['tenant_lan_list'],
            'wan_lan_list': job_input['wan_lan_list'],
            'tenant_port_info': {'vrrp': job_input['vrrp'],
                                 'ce01': job_input['ce01'],
                                 'ce02': job_input['ce02'],
            },
            'IaaS_subnet_id_v6': job_input.get('IaaS_subnet_id_v6', ''),
            'fw_ip_v6_address': job_input.get('fw_ip_v6_address', ''),
#             'router_name_list': job_input['router_name_list'],
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_disconnect_prepare(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'operation_id': job_input['operation_id'],
            'group_type': job_input['service_type'],
            'apl_type': job_input['apl_type'],
            'type': job_input['type'],
            'device_type': job_input['device_type'],
            'IaaS_region_id': job_input['IaaS_region_id'],
            'IaaS_tenant_id': job_input['IaaS_tenant_id'],
            'tenant_name': job_input['tenant_name'],
            'dc_id': job_input['dc_id'],
            'pod_id': job_input['pod_id'],
            'nal_tenant_id': job_input['nal_tenant_id'],
            'apl_info': job_input['apl_info'],
            'tenant_lan_list': job_input['tenant_lan_list'],
            'wan_lan_list': job_input['wan_lan_list'],
            'pub_port_list': job_input['pub_port_list'],
            'msa_network_id': job_input['msa_network_id'],
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_connect_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'virtual_apl_list': job_input['virtual_apl_list'],
            'virtual_lan_list': job_input['virtual_lan_list'],
            'apl_port_list': job_input['apl_port_list'],
            'update_apl_port_list': job_input['update_apl_port_list'],
            'license_list': job_input['license_list']
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_connect_update(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'virtual_apl_list': [],
            'virtual_lan_list': [],
            'apl_port_list': [],
            'update_apl_port_list': job_input['update_apl_port_list'],
            'update_apl_wan_port_list': job_input.get(
                                        'update_apl_wan_port_list', []),
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_disconnect_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'operation_id': job_input['operation_id'],
            'IaaS_region_id': job_input['IaaS_region_id'],
            'IaaS_tenant_id': job_input['IaaS_tenant_id'],
            'dc_id': job_input['dc_id'],
            'pod_id': job_input['pod_id'],
            'nal_tenant_id': job_input['nal_tenant_id'],
            'tenant_lan_list': job_input['tenant_lan_list'],
            'logical_delete_apl_list': job_input['logical_delete_apl_list'],
            'logical_delete_vlan_list': job_input['logical_delete_vlan_list'],
            'logical_delete_apl_port_list': job_input[
                                            'logical_delete_apl_port_list'],
            'msa_network_id': job_input['msa_network_id'],
            'group_type': job_input['group_type']
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_bandwidth_update_prepare(self,
                                                                job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'operation_id': job_input['operation_id'],
            'group_type': job_input['service_type'],
            'apl_type': job_input['apl_type'],
            'type': job_input['type'],
            'device_type': job_input['device_type'],
            'IaaS_tenant_id': job_input['IaaS_tenant_id'],
            'tenant_name': job_input['tenant_name'],
            'dc_id': job_input['dc_id'],
            'pod_id': job_input['pod_id'],
            'nal_tenant_id': job_input['nal_tenant_id'],
            'apl_info': job_input['apl_info'],
            'bandwidth': job_input['bandwidth'],
            'license_list': job_input['license_list'],
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_bandwidth_update(self,
                                                                job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'operation_id': job_input['operation_id'],
            'tenant_name': job_input['tenant_name'],
            'bandwidth': job_input['bandwidth'],
            'virtual_apl_list': job_input['virtual_apl_list'],
            'license_list': job_input['license_list'],
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_setting_update_prepare(self,
                                                              job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        dns_server_ip_address = job_input.get('dns_server_ip_address', '')
        ntp_server_ip_address = job_input.get('ntp_server_ip_address', '')
        snmp_server_ip_address = job_input.get('snmp_server_ip_address', '')
        syslog_server_ip_address = job_input.get(
                                            'syslog_server_ip_address', '')

        ntp_subnet_id = job_input.get('ntp_server_interface', '')
        snmp_subnet_id = job_input.get('snmp_server_interface', '')
        syslog_subnet_id = job_input.get('syslog_server_interface', '')

        ntp_server_interface = self.__get_port_nic_name(job_input,
                                                    ntp_server_ip_address,
                                                    ntp_subnet_id)

        snmp_server_interface = self.__get_port_nic_name(job_input,
                                                    snmp_server_ip_address,
                                                    snmp_subnet_id)

        syslog_server_interface = self.__get_port_nic_name(job_input,
                                                    syslog_server_ip_address,
                                                    syslog_subnet_id)

        job_output['job_ret_data'] = {
            'operation_id': job_input['operation_id'],
            'group_type': job_input['service_type'],
            'apl_type': job_input['apl_type'],
            'type': job_input['type'],
            'device_type': job_input['device_type'],
            'IaaS_tenant_id': job_input['IaaS_tenant_id'],
            'tenant_name': job_input['tenant_name'],
            'dc_id': job_input['dc_id'],
            'pod_id': job_input['pod_id'],
            'nal_tenant_id': job_input['nal_tenant_id'],
            'apl_info': job_input['apl_info'],
            'dns_server_ip_address': dns_server_ip_address,
            'ntp_server_ip_address': ntp_server_ip_address,
            'ntp_server_interface': ntp_server_interface,
            'snmp_server_ip_address': snmp_server_ip_address,
            'snmp_server_interface': snmp_server_interface,
            'snmp_server_delete_flg': job_input['snmp_server_delete_flg'],
            'syslog_server_ip_address': syslog_server_ip_address,
            'syslog_server_interface': syslog_server_interface,
            'syslog_server_delete_flg': job_input['syslog_server_delete_flg']
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def set_job_return_data_virtual_rt_setting_update(self,
                                                                job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output['job_ret_data'] = {
            'operation_id': job_input['operation_id'],
            'tenant_name': job_input['tenant_name'],
            'virtual_apl_list': job_input['virtual_apl_list']
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __update_db_server_task_status_end(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_table_rec_id = job_input['apl_table_rec_id']
        license_key = job_input.get('license_key', '')
        apl_type = job_input['apl_type']

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        if license_key == '' and \
                str(apl_type) == str(self.job_config.APL_TYPE_VR):
            params = {}
            params['task_status'] = 2
            params['update_id'] = operation_id
            keys = [apl_table_rec_id]
            db_update.set_context(db_endpoint_apl, keys, params)
            db_update.execute()
        else:
            params = {}
            params['task_status'] = 1
            params['update_id'] = operation_id
            keys = [apl_table_rec_id]
            db_update.set_context(db_endpoint_apl, keys, params)
            db_update.execute()

    def __update_db_server_task_status_end_for_update(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_table_rec_id = job_input['apl_table_rec_id']

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        params = {}
        params['task_status'] = 1
        params['update_id'] = operation_id
        keys = [apl_table_rec_id]
        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()

    def __update_db_service_task_status_end_for_update(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        group_rec_id = job_input['group_rec_id']

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_GROUP)

        params = {}
        params['task_status'] = 1
        params['update_id'] = operation_id
        keys = [group_rec_id]
        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()

    def __get_port_nic_name(self, job_input, subnet_ip, subnet_id):

        # Get JOB Input Parameters
        node_id = job_input['apl_info'][
                        self.job_config.VM_ROUTER_NODE_NAME1]['node_id']

        nic_name = ''
        if len(subnet_ip) > 0 and len(subnet_id) > 0:
            # Create Instance(DB Client)
            db_list = list.ListClient(self.job_config)

            # Get Endpoint(DB Client)
            db_endpoint_port = \
                self.get_db_endpoint(self.job_config.REST_URI_PORT)

            params = {}
            params['node_id'] = node_id

            if self.utils.get_ipaddress_version(subnet_ip) \
                                            == self.utils.IP_VER_V4:
                params['IaaS_subnet_id'] = subnet_id
            else:
                params['IaaS_subnet_id_v6'] = subnet_id

            db_list.set_context(db_endpoint_port, params)
            db_list.execute()
            apl_list = db_list.get_return_param()

            nic_name = apl_list[0]['nic']

        return nic_name
