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


class PrepareWim(base.JobAutoBase):

    def get_rt_dc_connected_info_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        router_name_list = [
            self.job_config.VM_ROUTER_NODE_NAME1,
            self.job_config.VM_ROUTER_NODE_NAME2
        ]

        # Get NAL_APL_MNG(DB)
        apl_list_res = self.__get_db_apl(job_input)

        if len(apl_list_res) == 0:
            raise SystemError('server not exists.')

        if len(apl_list_res) != len(router_name_list):
            raise SystemError('server too many or too few.')

        pod_id = apl_list_res[0]['pod_id']
        nal_tenant_id = apl_list_res[0]['tenant_id']
        apl_type = apl_list_res[0]['apl_type']
        nf_type = apl_list_res[0]['type']

        # Get MSA Info(network_id)
        msa_vlan_info = self.__get_db_msa_vlan(job_input, pod_id)
        msa_network_id = msa_vlan_info[0]['network_id']

        apl_list = {}
        for router_name in router_name_list:

            for apl_res in apl_list_res:
                if apl_res['node_name'].find(router_name) > -1:
                    apl_list[router_name] = {
                        'node_id': apl_res['server_id'],
                        'node_name': apl_res['node_name'],
                        'type': apl_res['type'],
                        'device_type': apl_res['device_type'],
                        'MSA_device_id': apl_res['MSA_device_id'],
                        'ID': apl_res['ID'],
                        'node_detail': apl_res['node_detail'],
                        'dns_server_ip_address': apl_res[
                                                'dns_server_ip_address'],
                        'ntp_server_ip_address': apl_res[
                                                'ntp_server_ip_address'],
                        'snmp_server_ip_address': apl_res[
                                                'snmp_server_ip_address'],
                        'syslog_server_ip_address': apl_res[
                                                'syslog_server_ip_address'],
                    }

            if router_name not in apl_list:
                raise SystemError('server matched router_name not exists..')

        apl_info = {}
        tenant_lan_list = []
        wan_lan_list = []
        pub_port_list = []
        for key, value in apl_list.items():

            # Get NAL_PORT_MNG(DB)
            port_list_res = self.__get_db_port(job_input, value['node_id'])

            if len(port_list_res) == 0:
                raise SystemError('port not exists.')

            for port_res in port_list_res:

                if port_res['network_id'] == msa_network_id:

                    apl_info[key] = {
                        'node_id': value['node_id'],
                        'node_name': value['node_name'],
                        'device_type': value['device_type'],
                        'MSA_device_id': value['MSA_device_id'],
                        'msa_nw_id': port_res['network_id'],
                        'msa_port_id': port_res['port_id'],
                        'msa_nic': port_res['nic'],
                        'msa_ip_address': port_res['ip_address'],
                        'apl_rec_id': value['ID'],
                        'node_detail': value['node_detail'],
                        'old_dns_server_ip_address': value[
                                                'dns_server_ip_address'],
                        'old_ntp_server_ip_address': value[
                                                'ntp_server_ip_address'],
                        'old_snmp_server_ip_address': value[
                                                'snmp_server_ip_address'],
                        'old_syslog_server_ip_address': value[
                                                'syslog_server_ip_address'],
                    }

                else:
                    lan_info = {
                        'node_id': value['node_id'],
                        'network_id': port_res['network_id'],
                        'port_id': port_res['port_id'],
                        'IaaS_port_id': port_res['IaaS_port_id'],
                        'nic': port_res['nic'],
                        'msa_info': port_res['msa_info'],
                        'rec_id': port_res['ID'],
                    }

                    if port_res['network_type'] \
                                == str(self.job_config.NW_TYPE_IN):
                        tenant_lan_list.append(lan_info)
                    else:
                        if port_res['network_type_detail'] \
                                    == str(self.job_config.NW_TYPE_PUBLIC):
                            pub_port_list.append(port_res)
                        else:
                            wan_lan_list.append(lan_info)

        # Set JOB Output Parameters
        job_output = {
            'nal_tenant_id': nal_tenant_id,
            'pod_id': pod_id,
            'apl_type': apl_type,
            'type': nf_type,
            'apl_info': apl_info,
            'tenant_lan_list': tenant_lan_list,
            'wan_lan_list': wan_lan_list,
            'pub_port_list': pub_port_list,
            'msa_network_id': msa_network_id,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __get_db_apl(self, job_input):

        # Get Input Parameters
        tenant_name = job_input['tenant_name']
        device_type = job_input['device_type']

        apl_type = self.job_config.APL_TYPE_VR
        hard_type = self.job_config.TYPE_RT

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_name'] = tenant_name
        params['apl_type'] = apl_type
        params['type'] = hard_type
        params['device_type'] = device_type
        db_list_instance.set_context(db_endpoint_apl, params)
        db_list_instance.execute()
        apl_list = db_list_instance.get_return_param()

        return apl_list

    def __get_db_port(self, job_input, node_id):

        # Get Input Parameters
        tenant_name = job_input['tenant_name']

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # List NAL_PORT_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_name'] = tenant_name
        params['node_id'] = node_id
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        return port_list

    def __get_db_msa_vlan(self, job_input, pod_id):

        # Get Input Parameters
        tenant_name = job_input['tenant_name']

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(
                            self.job_config.REST_URI_MSA_VLAN)

        # List NAL_PORT_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['pod_id'] = pod_id
        params['tenant_name'] = tenant_name
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        return port_list
