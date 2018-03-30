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
import base64
import inspect
import json
import traceback

from job.auto import base
from job.lib.openstack.nova import servers
from job.lib.script import zerotouch
from job.lib.soap.msa import sshws
from job.lib.db import list


class ServerWim(base.JobAutoBase):

    def server_create_rt_vm_firefly(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create Server(OpenStack:WIM)
        job_output1 = self.__create_server_wim(job_input,
                                    self.job_config.VM_ROUTER_NODE_NAME1)
        # Provisioning(FireFlyVM)
        self.__provisioning_firefly_vm(job_input,
                                       job_output1['server_id'],
                                       self.job_config.VM_ROUTER_NODE_NAME1)

        # Create Server(OpenStack:WIM)
        job_output2 = self.__create_server_wim(job_input,
                                    self.job_config.VM_ROUTER_NODE_NAME2)
        # Provisioning(FireFlyVM)
        self.__provisioning_firefly_vm(job_input,
                                       job_output2['server_id'],
                                       self.job_config.VM_ROUTER_NODE_NAME2)

        ret = {}
        ret['server_id'] = {}
        ret['server_id'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    job_output1['server_id']
        ret['server_id'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    job_output2['server_id']
        ret['apl_wk'] = {}
        ret['apl_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    job_output1['apl_wk']
        ret['apl_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    job_output2['apl_wk']
        ret['msa_port_wk'] = {}
        ret['msa_port_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    job_output1['msa_port_wk']
        ret['msa_port_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    job_output2['msa_port_wk']
        ret['wan_port_wk'] = {}
        ret['wan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    job_output1['wan_port_wk']
        ret['wan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    job_output2['wan_port_wk']
        ret['tenant_lan_port_wk'] = {}
        ret['tenant_lan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                            job_output1['tenant_lan_port_wk']
        ret['tenant_lan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                            job_output2['tenant_lan_port_wk']

        port_list_vrrp = job_input['tenant_port_info']['vrrp']
        vrrp_tenant_lan_port_wk = {
            'params': {
                'update_id': job_input['operation_id'],
                'node_id': job_output1['server_id'],
                'nic': job_output1['nic'],
                'msa_info': json.dumps({}),
            },
            'keys': {'ID': port_list_vrrp['rec_id']},
        }
        ret['tenant_lan_port_wk']['vrrp'] = vrrp_tenant_lan_port_wk

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, ret)

        return ret

    def server_create_rt_vm_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Create Contents(Script For Provisioning)
        prov_contents = self.__create_prov_script_server_vm_rt_csr1000v(
                                    job_input,
                                    self.job_config.VM_ROUTER_NODE_NAME1)
        # Create Server(OpenStack:WIM)
        job_output1 = self.__create_server_wim(
                                    job_input,
                                    self.job_config.VM_ROUTER_NODE_NAME1,
                                    prov_contents
        )
        # Create Contents(Script For Provisioning)
        prov_contents = self.__create_prov_script_server_vm_rt_csr1000v(
                                    job_input,
                                    self.job_config.VM_ROUTER_NODE_NAME2)

        # Create Server(OpenStack:WIM)
        job_output2 = self.__create_server_wim(
                                    job_input,
                                    self.job_config.VM_ROUTER_NODE_NAME2,
                                    prov_contents
        )

        ret = {}
        ret['server_id'] = {}
        ret['server_id'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    job_output1['server_id']
        ret['server_id'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    job_output2['server_id']
        ret['apl_wk'] = {}
        ret['apl_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    job_output1['apl_wk']
        ret['apl_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    job_output2['apl_wk']
        ret['msa_port_wk'] = {}
        ret['msa_port_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    job_output1['msa_port_wk']
        ret['msa_port_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    job_output2['msa_port_wk']
        ret['wan_port_wk'] = {}
        ret['wan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    job_output1['wan_port_wk']
        ret['wan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    job_output2['wan_port_wk']
        ret['tenant_lan_port_wk'] = {}
        ret['tenant_lan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                            job_output1['tenant_lan_port_wk']
        ret['tenant_lan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                            job_output2['tenant_lan_port_wk']

        port_list_vrrp = job_input['tenant_port_info']['vrrp']
        vrrp_tenant_lan_port_wk = {
            'params': {
                'update_id': job_input['operation_id'],
                'node_id': job_output1['server_id'],
                'nic': job_output1['nic'],
                'msa_info': json.dumps({}),
            },
            'keys': {'ID': port_list_vrrp['rec_id']},
        }
        ret['tenant_lan_port_wk']['vrrp'] = vrrp_tenant_lan_port_wk

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, ret)

        return ret

    def server_attach_interface_rt_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Delete Server(OpenStack:WIM)
        ret1 = self.__server_attach_interface(job_input,
                                self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__server_attach_interface(job_input,
                                self.job_config.VM_ROUTER_NODE_NAME2)

        ret = {}
        ret['server_id'] = {}
        ret['server_id'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                    ret1['server_id']
        ret['server_id'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                    ret2['server_id']
        ret['tenant_lan_port_wk'] = {}
        ret['tenant_lan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                            ret1['tenant_lan_port_wk']
        ret['tenant_lan_port_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                            ret2['tenant_lan_port_wk']

        port_list_vrrp = job_input['tenant_port_info']['vrrp']
        vrrp_tenant_lan_port_wk = {
            'params': {
                'update_id': job_input['operation_id'],
                'node_id': ret1['server_id'],
                'nic': ret1['nic'],
                'msa_info': json.dumps({}),
            },
            'keys': {'ID': port_list_vrrp['rec_id']},
        }
        ret['tenant_lan_port_wk']['vrrp'] = vrrp_tenant_lan_port_wk

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, ret)

        return ret

    def virtual_rt_server_update_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        job_output = {}
        job_output['server_id'] = {}
        job_output['server_id'][self.job_config.VM_ROUTER_NODE_NAME1] = \
            job_input['apl_info'][self.job_config.VM_ROUTER_NODE_NAME1][
                                                                    'node_id']
        job_output['server_id'][self.job_config.VM_ROUTER_NODE_NAME2] = \
            job_input['apl_info'][self.job_config.VM_ROUTER_NODE_NAME2][
                                                                    'node_id']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def server_delete_rt_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Delete Server(OpenStack:WIM)
        ret1 = self.__delete_server_wim(job_input,
                                self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__delete_server_wim(job_input,
                                self.job_config.VM_ROUTER_NODE_NAME2)

        job_output = {
            'logical_delete_apl_list': [
                ret1['logical_delete_apl_list'],
                ret2['logical_delete_apl_list'],
            ]
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __create_server_wim(self, job_input, router_name, personality=None):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        group_rec_id = job_input['group_rec_id']
        tenant_name = job_input['tenant_name']
        nal_tenant_id = job_input['nal_tenant_id']
        msa_port_id = job_input['msa_wan_port_info'][
                                        router_name]['msa_port_id']
        msa_ip_address = job_input['msa_wan_port_info'][
                                        router_name]['msa_ip_address']
        msa_netmask = job_input['msa_wan_port_info'][
                                        router_name]['msa_netmask']
        msa_port_info = job_input['msa_wan_port_info'][
                                        router_name]['msa_port_info']
        wan_port_id = job_input['msa_wan_port_info'][
                                        router_name]['wan_port_id']
        wan_port_info = job_input['msa_wan_port_info'][
                                        router_name]['wan_port_info']
        wan_info = job_input['msa_wan_port_info'][
                                        router_name].get('wan_info', {})
        wan_network_id = job_input['wan_network_id']
        port_list = job_input['tenant_port_info'][router_name]
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        msa_network_info = job_input['msa_network_info']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type,
                                               device_type, dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Get MSA Info
        msa_network_id = msa_network_info['network_id']

        # Set Parameter
        os_uuid = self.get_os_uuid_image_flavor(nf_type, device_type,
                                                pod_id, nal_tenant_id, dc_id)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_wim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_servers_instance = servers.OscServers(self.job_config)

        host_name = 'T' + '{0:05d}'.format(group_rec_id) + dc_id + router_name
        network1 = {'uuid': msa_network_id,
                    'port': msa_port_id}
        network2 = {'uuid': wan_network_id,
                    'port': wan_port_id}
        network3 = {'uuid': port_list['network_id'],
                    'port': port_list['port_id']}
        networks = [network1, network2, network3]

        # Create Server(OpenStack:VIM)
        os_server_res = osc_servers_instance.create_server(
                                            os_endpoint_wim,
                                            host_name,
                                            os_uuid['image_id'],
                                            os_uuid['flavor_id'],
                                            networks,
                                            [{'name': 'default'}],
                                            None,
                                            None,
                                            None,
                                            None,
                                            True,
                                            personality)

        server_id = os_server_res['server']['id']

        # Wait Server Activated(OpenStack:VIM)
        self.wait_os_server_active(osc_servers_instance, os_endpoint_wim,
                                server_id,
                                self.job_config.OS_SERVER_BOOT_COUNT,
                                self.job_config.OS_SERVER_BOOT_INTERVAL,
                                self.job_config.OS_SERVER_WAIT_TIME)

        # Reboot Server(OpenStack)
        osc_servers_instance.action_server(
                                os_endpoint_wim,
                                os_server_res['server']['id'],
                                osc_servers_instance.SERVER_ACTION_REBOOT,
                                osc_servers_instance.SERVER_REBOOT_TYPE_SOFT)

        # Wait Server Activated(OpenStack)
        self.wait_os_server_active(
                                osc_servers_instance,
                                os_endpoint_wim,
                                os_server_res['server']['id'],
                                self.job_config.OS_SERVER_REBOOT_COUNT,
                                self.job_config.OS_SERVER_REBOOT_INTERVAL,
                                self.job_config.OS_SERVER_WAIT_TIME)

        # Set Finalize Data
        apl_wk = {}
        apl_wk['create_id'] = operation_id
        apl_wk['update_id'] = operation_id
        apl_wk['delete_flg'] = 0
        apl_wk['apl_type'] = self.job_config.APL_TYPE_VR
        apl_wk['type'] = self.job_config.TYPE_RT
        apl_wk['device_type'] = device_type
        apl_wk['tenant_id'] = nal_tenant_id
        apl_wk['node_id'] = server_id
        apl_wk['node_name'] = host_name
        apl_wk['node_detail'] = json.dumps({})
        apl_wk['server_id'] = server_id
        apl_wk['server_info'] = json.dumps(os_server_res['server'])
        apl_wk['MSA_device_id'] = 0
        apl_wk['tenant_name'] = tenant_name
        apl_wk['pod_id'] = pod_id

        msa_port_wk = {}
        msa_port_wk['create_id'] = operation_id
        msa_port_wk['update_id'] = operation_id
        msa_port_wk['delete_flg'] = 0
        msa_port_wk['tenant_id'] = nal_tenant_id
        msa_port_wk['apl_type'] = self.job_config.APL_TYPE_VR
        msa_port_wk['port_id'] = msa_port_id
        msa_port_wk['IaaS_port_id'] = ''
        msa_port_wk['node_id'] = server_id
        msa_port_wk['network_id'] = msa_network_id
        msa_port_wk['nic'] = msa_config_for_device['nic_prefix']\
                             + msa_config_for_device['nic_for_msa']
        msa_port_wk['ip_address'] = msa_ip_address
        msa_port_wk['netmask'] = msa_netmask
        msa_port_wk['port_info'] = json.dumps(msa_port_info['port'])
        msa_port_wk['msa_info'] = json.dumps({})
        msa_port_wk['network_type'] = self.job_config.NW_TYPE_EX
        msa_port_wk['network_type_detail'] = self.job_config.NW_TYPE_MSA
        msa_port_wk['tenant_name'] = tenant_name
        msa_port_wk['pod_id'] = pod_id

        wan_port_wk = {}
        wan_port_wk['create_id'] = operation_id
        wan_port_wk['update_id'] = operation_id
        wan_port_wk['delete_flg'] = 0
        wan_port_wk['tenant_id'] = nal_tenant_id
        wan_port_wk['apl_type'] = self.job_config.APL_TYPE_VR
        wan_port_wk['port_id'] = wan_port_id
        wan_port_wk['IaaS_port_id'] = ''
        wan_port_wk['node_id'] = server_id
        wan_port_wk['network_id'] = wan_network_id
        wan_port_wk['nic'] = msa_config_for_device['nic_prefix']\
                             + msa_config_for_device['nic_for_wan']
        wan_port_wk['ip_address'] = wan_info[self.utils.IP_VER_V4]['ip']
        wan_port_wk['netmask'] = wan_info[self.utils.IP_VER_V4]['netmask']
        wan_port_wk['port_info'] = json.dumps(wan_port_info['port'])
        wan_port_wk['msa_info'] = json.dumps({})
        wan_port_wk['network_type'] = self.job_config.NW_TYPE_EX
        wan_port_wk['network_type_detail'] = self.job_config.NW_TYPE_WAN
        wan_port_wk['tenant_name'] = tenant_name
        wan_port_wk['pod_id'] = pod_id

        if self.utils.IP_VER_V6 in wan_info:
            wan_port_wk['ip_address_v6'] = wan_info[
                                            self.utils.IP_VER_V6]['ip']
            wan_port_wk['netmask_v6'] = wan_info[
                                        self.utils.IP_VER_V6]['netmask']

        tenant_lan_port_wk = {'params': {}, 'keys': {}}
        tenant_lan_port_wk['params']['update_id'] = operation_id
        tenant_lan_port_wk['params']['node_id'] = server_id
        tenant_lan_port_wk['params']['nic'] =\
                        msa_config_for_device['nic_prefix']\
                             + msa_config_for_device['nic_for_first_lan']
        tenant_lan_port_wk['keys'] = {'ID': port_list['rec_id']}

        return {
            'server_id': server_id,
            'apl_wk': apl_wk,
            'msa_port_wk': msa_port_wk,
            'wan_port_wk': wan_port_wk,
            'tenant_lan_port_wk': tenant_lan_port_wk,
            'nic': msa_config_for_device['nic_prefix']\
                     + msa_config_for_device['nic_for_first_lan']
        }

    def __server_attach_interface(self, job_input, router_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_list = job_input['tenant_port_info'][router_name]
        node_id = job_input['apl_info'][router_name]['node_id']
        new_nic_name = job_input['new_nic_name']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        vnf_ip = job_input['apl_info'][router_name]['msa_ip_address']

        # Create Instance(MSA Rest Client)
        msa_sshws = sshws.SshWs(self.job_config,
                            self.nal_endpoint_config,
                            pod_id)

        # Get MSA Device Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type, device_type)
        msa_config_for_device = \
                self.get_msa_config_for_device(pod_id, device_name)

        ssh_port = msa_config_for_device.get('ssh_port', '')

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_servers = servers.OscServers(self.job_config)

        # Attach Port(Openstack)(VIM)
        osc_servers.attach_interface(os_endpoint_vim,
                                    node_id, port_list['port_id'])

        # Reboot Server(Openstack)(VIM)
        osc_servers.action_server(os_endpoint_vim,
                                    node_id,
                                    osc_servers.SERVER_ACTION_REBOOT,
                                    osc_servers.SERVER_REBOOT_TYPE_SOFT)

        # Wait Server Activated(OpenStack:VIM)
        self.wait_os_server_active(osc_servers, os_endpoint_vim,
                                node_id,
                                self.job_config.OS_SERVER_BOOT_COUNT,
                                self.job_config.OS_SERVER_BOOT_INTERVAL,
                            self.job_config.OS_SERVER_WAIT_TIME_FOR_ATTACH)

        #check_ssh_connect_possible_confirm
        self.check_ssh_connect_possible_confirm(msa_sshws,
                                                vnf_ip,
                                                ssh_port)

        tenant_lan_port_wk = {
            'params': {},
            'keys': {}
        }
        tenant_lan_port_wk['params']['update_id'] = operation_id
        tenant_lan_port_wk['params']['node_id'] = node_id
        tenant_lan_port_wk['params']['nic'] = new_nic_name
        tenant_lan_port_wk['keys'] = {'ID': port_list['rec_id']}

        return {
            'server_id': node_id,
            'tenant_lan_port_wk': tenant_lan_port_wk,
            'nic': new_nic_name
        }

    def __delete_server_wim(self, job_input, router_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        dc_id = job_input['dc_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']
        hard_type = job_input['type']
        device_type = job_input['apl_info'][router_name]['device_type']
        node_id = job_input['apl_info'][router_name]['node_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                    pod_id, '', nal_tenant_id, dc_id)

        # Create Instance(OpenStack Client)
        osc_servers_instance = servers.OscServers(self.job_config)

        try:
            # Delete Server(OpenStack:VIM)
            osc_servers_instance.delete_server(os_endpoint_vim, node_id)
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Set Delete Info
        logical_delete_apl_list = {
                'search': {
                    'delete_flg': 0,
                    'tenant_id': nal_tenant_id,
                    'apl_type': apl_type,
                    'type': hard_type,
                    'device_type': device_type,
                    'node_id': node_id,
                },
                'params': {
                    'update_id': operation_id,
                    'delete_flg': 1,
                },
        }

        return {
            'logical_delete_apl_list': logical_delete_apl_list
        }

    def __provisioning_firefly_vm(self,
                                  job_input,
                                  server_id,
                                  router_name):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        msa_ip_address = job_input['msa_wan_port_info'][
                                    router_name]['msa_ip_address']
        msa_netmask = job_input['msa_wan_port_info'][
                                    router_name]['msa_netmask']

        # Create Instance(ZeroTouchClient)
        zerotouch_instance = zerotouch.ZeroTouchClient(self.job_config)

        # Get Vim Endpoint
        vim_endpoint_data = self.nal_endpoint_config[dc_id]['vim'][pod_id]

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type,
                                               device_type, dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        zerotouch_params = [
            vim_endpoint_data['openstack_controller_node_ip_address'],
            vim_endpoint_data['openstack_controller_node_server_login_id'],
            vim_endpoint_data[
                        'openstack_controller_node_server_login_password'],
            vim_endpoint_data['openstack_keystone_ip_address'],
            vim_endpoint_data['user_id'],
            vim_endpoint_data['user_password'],
            server_id,
            msa_config_for_device['user_id'],
            msa_config_for_device['user_new_password'],
            msa_config_for_device['nic_prefix'] +
                        msa_config_for_device['nic_for_msa'],
            msa_ip_address + '/' + msa_netmask,
            vim_endpoint_data['admin_tenant_name']
        ]
        passwords = [
            vim_endpoint_data[\
                        'openstack_controller_node_server_login_password'],
            vim_endpoint_data['user_password'],
            msa_config_for_device['user_new_password'],
        ]

        # Provisioning
        zerotouch_instance.vsrx_ff_provisioning(zerotouch_params, passwords)

    def __create_prov_script_server_vm_rt_csr1000v(self,
                                                   job_input,
                                                   router_name):

        # Get JOB Input Parameters
        msa_network_info = job_input['msa_network_info']
        vnf_ip_address = job_input['msa_wan_port_info'][
                                            router_name]['msa_ip_address']

        # Get Template
        with open(self.job_config.TEMPLATE_DIR \
                  + self.job_config.TEMPLATE_INIT_PROV_IS_VM_CSR, 'r') as f:
                script_str = f.read()

        # Replace Template
        script_str = script_str.replace('%vnf_address%', vnf_ip_address)
        script_str = script_str.replace('%vnf_netmask%', \
         self.utils.get_subnet_mask_from_cidr_len(msa_network_info['netmask']))

        script_str = script_str.replace('%vnf_network_address%',
                            msa_network_info['network_address'] \
                                + '/' + msa_network_info['netmask'])

        if job_input['group_type'] in [
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
            ]:
            script_str = script_str.replace('%boot_level%', 'security')

        else:
            script_str = script_str.replace('%boot_level%', 'ipbase')

        personality = [{
            'path': servers.OscServers(self.job_config).\
                                        PERSONALITY_PATH_IOSXE_CONFIG,
            'contents': base64.b64encode(
                    script_str.encode(
                            self.job_config.CHAR_SET)).decode('ascii'),

        }]

        return personality
