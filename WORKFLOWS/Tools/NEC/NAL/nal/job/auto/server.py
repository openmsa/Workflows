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
import socket
import struct
import traceback

from job.auto import base
from job.lib.db import list
from job.lib.db import update
from job.lib.openstack.nova import servers
from job.lib.soap.msa import sshws


class Server(base.JobAutoBase):

    IAAS_PORT_NAME = '#used-NFVI#'

    DEVICE_NAME_INTERSEC_SG = 'intersec_sg'
    DEVICE_NAME_INTERSEC_LB = 'intersec_lb'

    def virtual_server_create(self, job_input):

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

        # Create Server(OpenStack:VIM), Insert DB(NAL_VNF_MNG) For Firewall
        os_server_res = self.__create_server_vm(None, job_input,
                                                self.__set_networks(job_input))

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_device_config = \
            self.get_msa_config_for_device(pod_id, device_name)

        if 'port_id1' in job_input:
            # Update DB(NAL_PORT_MNG) For MSA Port
            self.__update_db_port_msa_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id2' in job_input:
            # Update DB(NAL_PORT_MNG) For Pub Port
            self.__update_db_port_pub_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id3' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Ext Port
            self.__update_db_port_ext_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id4' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Internal Port
            self.__update_db_port_internal_vm(job_input,
                                              os_server_res['server']['id'],
                                              msa_device_config['nic_prefix'])

        # Set JOB Output Parameters
        job_output['server_id'] = os_server_res['server']['id']
        job_output['node_id'] = os_server_res['server']['id']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                   __name__, function_name, job_output)

        return job_output

    def virtual_server_create_paloalto_vm(self, job_input):

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

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_device_config = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Set Personality(For Provisioning)
        personality = self.__set_personality_paloalto_vm(job_input,
                                    msa_device_config['user_new_password'])

        # Create Server(OpenStack:VIM), Insert DB(NAL_VNF_MNG) For Firewall
        os_server_res = self.__create_server_vm(None, job_input,
                                                self.__set_networks(job_input),
                                                True,
                                                personality)

        if 'port_id1' in job_input:
            # Update DB(NAL_PORT_MNG) For MSA Port
            self.__update_db_port_msa_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id2' in job_input:
            # Update DB(NAL_PORT_MNG) For Pub Port
            self.__update_db_port_pub_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id3' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Ext Port
            self.__update_db_port_ext_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id4' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Internal Port
            self.__update_db_port_internal_vm(job_input,
                                              os_server_res['server']['id'],
                                              msa_device_config['nic_prefix'])

        # Set JOB Output Parameters
        job_output['server_id'] = os_server_res['server']['id']
        job_output['node_id'] = os_server_res['server']['id']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                   __name__, function_name, job_output)

        return job_output

    def virtual_server_create_with_config_drive(self, job_input):

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

        # Create UserData(Script For Provisioning)
        user_data = self.__create_prov_script_server_vm_fw_fortigate(job_input)

        # Create Server(OpenStack:VIM), Insert DB(NAL_VNF_MNG) For Firewall
        os_server_res = self.__create_server_vm(user_data, job_input,
                                                self.__set_networks(job_input),
                                                True)

        # Update NAL_LICENSE_MNG(node_id)
        self.__update_license_fortigate_vm_541(
                                    job_input, os_server_res['server']['id'])

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_device_config = \
            self.get_msa_config_for_device(pod_id, device_name)

        if 'port_id1' in job_input:
            # Update DB(NAL_PORT_MNG) For MSA Port
            self.__update_db_port_msa_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id2' in job_input:
            # Update DB(NAL_PORT_MNG) For Pub Port
            self.__update_db_port_pub_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id3' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Ext Port
            self.__update_db_port_ext_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id4' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Internal Port
            self.__update_db_port_internal_vm(job_input,
                                              os_server_res['server']['id'],
                                              msa_device_config['nic_prefix'])

        # Set JOB Output Parameters
        job_output['server_id'] = os_server_res['server']['id']
        job_output['node_id'] = os_server_res['server']['id']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                   __name__, function_name, job_output)

        return job_output

    def virtual_server_create_intersec(self, job_input):

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

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_device_config = \
            self.get_msa_config_for_device(pod_id, device_name)

#         # Get RSA(Public Key)
#         intersecvm_instance = intersecvm.IntersecVmClient(self.job_config)
#         intersecvm_ret = intersecvm_instance.intersec_vm_get_rsa([
#             self.nal_endpoint_config['system']['msa'][pod_id]['login_id'],
#             self.nal_endpoint_config['system']['msa'][pod_id][
#                                                             'login_password'],
#             self.nal_endpoint_config['system']['msa'][pod_id]['ip_address'],
#             self.nal_endpoint_config['system']['msa'][pod_id][
#                                                         'nal_rsa_pub_dir'],
#             self.nal_endpoint_config['system']['msa'][pod_id][
#                                                 'generatekey_command_path'],
#             ],
#             [
#             self.nal_endpoint_config['system']['msa'][pod_id][
#                                                         'login_password'],
#             ])
#         rsa_prv_key_path = intersecvm_ret[0]
#         rsa_pub_key = intersecvm_ret[1]

        # Get RSA Pub Key
        rsa_pub_key_path = msa_device_config['rsa_pub_key_path']
        with open(rsa_pub_key_path, 'r') as f:
                rsa_pub_key = f.read()

        # Create UserData(Script For Provisioning)
        if device_name == self.DEVICE_NAME_INTERSEC_SG:
            user_data = self.__create_prov_script_server_vm_fw(job_input,
                                                               rsa_pub_key)
        else:
            user_data = self.__create_prov_script_server_vm_lb(job_input,
                                                               rsa_pub_key)

        # Create Server(OpenStack:VIM), Insert DB(NAL_VNF_MNG) For Firewall
        os_server_res = self.__create_server_vm(user_data, job_input,
                                                self.__set_networks(job_input),
                                                True)

        if 'port_id1' in job_input:
            # Update DB(NAL_PORT_MNG) For MSA Port
            self.__update_db_port_msa_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id2' in job_input:
            # Update DB(NAL_PORT_MNG) For Pub Port
            self.__update_db_port_pub_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id3' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Ext Port
            self.__update_db_port_ext_vm(job_input, os_server_res,
                                         msa_device_config['nic_prefix'])

        if 'port_id4' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Internal Port
            self.__update_db_port_internal_vm(job_input,
                                              os_server_res['server']['id'],
                                              msa_device_config['nic_prefix'])

        # Set JOB Output Parameters
        job_output['server_id'] = os_server_res['server']['id']
        job_output['node_id'] = os_server_res['server']['id']
#        job_output['rsa_prv_key_path'] = rsa_prv_key_path

        # Dump
        job_output['script_str'] = user_data

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_server_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Delete Server(OpenStack:VIM), Update DB(NAL_VNF_MNG) For Firewall
        self.__delete_server_vm_fw(job_input)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_server_port_attach(self, job_input):

        job_output = {}

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        port_id4 = job_input['port_id4']
        node_id = job_input['node_id']

        # Create Instance(MSA Rest Client)
        msa_sshws = sshws.SshWs(self.job_config,
                                self.nal_endpoint_config,
                                pod_id)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        params = {}
        params['node_id'] = node_id
        params['network_type_detail'] = '4'
        params['delete_flg'] = 0
        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()

        port_list = db_list.get_return_param()

        vnf_ip = ''
        for port in port_list:
            vnf_ip = port.get('ip_address')

        # Create Server(OpenStack:VIM), Insert DB(NAL_VNF_MNG) For Firewall
        self.__attach_port_internal_vm(job_input, port_id4)

        # Get MSA Device Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        ssh_port = msa_config_for_device.get('ssh_port', '')

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_device_config = \
            self.get_msa_config_for_device(pod_id, device_name)

        #check_ssh_connect_possible_confirm
        self.check_ssh_connect_possible_confirm(msa_sshws,
                                        vnf_ip,
                                        ssh_port)

        # Attach Interface, Update DB(NAL_PORT_MNG) For Internal Port
        self.__update_db_port_internal_vm(job_input,
                                          node_id,
                                          msa_device_config['nic_prefix'])

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                   __name__, function_name, job_output)

        return job_output

    def virtual_fw_interface_attach_ipv6(self, job_input):

        job_output = {}

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        port_id = job_input['port_id']
        node_id = job_input['node_id']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_device_config = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Attach Interface, Update DB(NAL_PORT_MNG) For Internal Port
        job_input['port_id4'] = port_id
        self.__update_db_port_internal_vm(job_input,
                                          node_id,
                                          msa_device_config['nic_prefix'])

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                   __name__, function_name, job_output)

        return job_output

    def virtual_lb_interface_attach_ipv6(self, job_input):

        job_output = {}

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        port_id = job_input['port_id']
        node_id = job_input['node_id']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_device_config = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Attach Interface, Update DB(NAL_PORT_MNG) For Internal Port
        job_input['port_id4'] = port_id
        self.__update_db_port_internal_vm(job_input,
                                          node_id,
                                          msa_device_config['nic_prefix'])

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                   __name__, function_name, job_output)

        return job_output

    def virtual_server_port_detach(self, job_input):

        job_output = {}

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        port_id4 = job_input['port_id']

        # Detach Server(OpenStack:VIM)
        self.__detach_port_internal_vm(job_input, port_id4)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                   __name__, function_name, job_output)

        return job_output

    def physical_server_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_table_rec_id = job_input['apl_table_rec_id']

        # Get/Update APL Info
        apl_info = self.__update_pysical_apl_assign(operation_id,
                                                    nal_tenant_id,
                                                    apl_table_rec_id)

        if 'port_id2' in job_input:
            # Update DB(NAL_PORT_MNG) For Pub Port
            self.__update_db_port_pub_ph(job_input,
                                         apl_info,
                                         apl_info['nic_public'])

        if 'port_id3' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Ext Port
            self.__update_db_port_ext_ph(job_input,
                                         apl_info,
                                         apl_info['nic_external'])

        if 'port_id4' in job_input:
            # Attach Interface, Update DB(NAL_PORT_MNG) For Internal Port
            self.__update_db_port_internal_ph(job_input,
                                         apl_info,
                                         apl_info['nic_tenant'])

        # Set JOB Output Parameters
        job_output['node_id'] = apl_info['node_id']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def physical_server_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        node_id = job_input['node_id']
        operation_id = job_input['operation_id']

        # Update APL Info
        self.__update_pysical_apl_withdraw(node_id, operation_id)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __update_pysical_apl_withdraw(self, node_id, operation_id):

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['node_id'] = node_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        # Update NAL_APL_MNG(DB Client)
        params = {}
        params['update_id'] = operation_id
        params['status'] = 2
        params['task_status'] = 1
        params['tenant_name'] = ''
        params['tenant_id'] = ''
        keys = [apl_list[0]['ID']]
        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()

    def __create_prov_script_server_vm_fw(self, job_input, rsa_pub_key):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        tenant_name = job_input['tenant_name']

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = \
            self.get_db_endpoint(self.job_config.REST_URI_MSA_VLAN)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # Get MSA VLAN Data
        params = {}
        params['delete_flg'] = 0
        params['tenant_name'] = tenant_name
        params['pod_id'] = pod_id
        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        msa_vlan_list = db_list.get_return_param()

        # Get Template
        with open(self.job_config.TEMPLATE_DIR \
                  + self.job_config.TEMPLATE_INIT_PROV_IS_VM_SG, 'r') as f:
                script_str = f.read()

        cidr = msa_vlan_list[0]['network_address'] + \
                            '/' + msa_vlan_list[0]['netmask']
        ret = self.utils.get_network_range_from_cidr(cidr)
        gatewy_ip = \
            socket.inet_ntoa(struct.pack('!L', ret['network'] + 1))

        # Replace Template
        script_str = script_str.replace('%gatewayIP%', gatewy_ip)
        script_str = script_str.replace('%remoteHostList%',\
                                    msa_vlan_list[0]['msa_ip_address'] + ' '  \
                                    + job_input['webclient_ip'])
        script_str = script_str.replace('%rsa_pub_key%', rsa_pub_key)

        return script_str

    def __create_prov_script_server_vm_lb(self, job_input, rsa_pub_key):

        # Get Template
        with open(self.job_config.TEMPLATE_DIR \
                  + self.job_config.TEMPLATE_INIT_PROV_IS_VM_LB, 'r') as f:
                script_str = f.read()

        # Replace Template
        script_str = script_str.replace('%rsa_pub_key%', rsa_pub_key)

        return script_str

    def __create_prov_script_server_vm_fw_fortigate(self, job_input):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        tenant_name = job_input['tenant_name']
        port_id1 = job_input['port_id1']
        port_id2 = job_input['port_id2']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        license_key = job_input['license_key']

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_endpoint_msa_vlan = \
            self.get_db_endpoint(self.job_config.REST_URI_MSA_VLAN)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_VNF_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id1
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list1 = db_list.get_return_param()

        # List NAL_VNF_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id2
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list2 = db_list.get_return_param()

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_common = self.get_msa_config_for_common(pod_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Get MSA VLAN Data
        params = {}
        params['delete_flg'] = 0
        params['tenant_name'] = tenant_name
        params['pod_id'] = pod_id
        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        msa_vlan_list = db_list.get_return_param()

        # Get Template
        with open(self.job_config.TEMPLATE_DIR \
            + self.job_config.TEMPLATE_INIT_PROV_IS_VM_FORTIGATE, 'r') as f:
                script_str = f.read()

        # Replace Template
        script_str = script_str.replace('%vnf_address_1%', \
                port_list1[0]['ip_address'] + '/' + port_list1[0]['netmask'])
        script_str = script_str.replace('%vnf_address_2%', \
                port_list2[0]['ip_address'] + '/' + port_list2[0]['netmask'])
        script_str = script_str.replace('%default_gateway%', \
                                    msa_config_for_common['pub_vlan_gateway'])
        script_str = script_str.replace('%default_gateway_device%', 'port2')
        script_str = script_str.replace('%proxy_server_address%', \
                        msa_config_for_common['svc_vlan_proxy_ip_address'])
        script_str = script_str.replace('%dns_address%', \
                    msa_config_for_common['svc_vlan_dns_primary_ip_address'])
        script_str = script_str.replace('%proxy_server_port%', \
                                msa_config_for_common['svc_vlan_proxy_port'])
        script_str = script_str.replace('%vnf_new_password%', \
                                msa_config_for_device['user_new_password'])
        script_str = script_str.replace('%tftp_server_address%', \
                                        msa_vlan_list[0]['msa_ip_address'])
        script_str = script_str.replace('%license_file_name%', \
                                                            license_key)

        return script_str

    def __create_server_vm(self,
                    user_data, job_input, networks, config_drive=False,
                    personality=None):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_table_rec_id = job_input['apl_table_rec_id']
        apl_type = job_input['apl_type']
        hard_type = job_input['type']
        device_type = job_input['device_type']
        nal_tenant_id = job_input['nal_tenant_id']
        pod_id = job_input['pod_id']
        host_name = job_input['host_name']

        # Create Instance(OpenStack Client)
        osc_servers_instance = servers.OscServers(self.job_config)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                           pod_id, '', nal_tenant_id)

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        global_ip = ''
        if 'port_id3' in job_input:
            # List NAL_PORT_MNG(DB Client) For Pub Port
            params = {}
            params['delete_flg'] = 0
            params['tenant_id'] = job_input['nal_tenant_id']
            params['port_id'] = job_input['port_id3']
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list3 = db_list_instance.get_return_param()
            global_ip = port_list3[0]['ip_address']

        # Set Parameter
        os_uuid = self.get_os_uuid_image_flavor(hard_type, device_type,
                                                pod_id, nal_tenant_id)

        # Create Server(OpenStack:VIM)
        os_server_res = osc_servers_instance.create_server(
                                            os_endpoint_vim,
                                            host_name,
                                            os_uuid['image_id'],
                                            os_uuid['flavor_id'],
                                            networks,
                                            [{'name': 'default'}],
                                            None,
                                            None,
                                            None,
                                            user_data,
                                            config_drive,
                                            personality)

        # Wait Server Activated(OpenStack:VIM)
        self.wait_os_server_active(osc_servers_instance, os_endpoint_vim,
                                os_server_res['server']['id'],
                                self.job_config.OS_SERVER_BOOT_COUNT,
                                self.job_config.OS_SERVER_BOOT_INTERVAL,
                                self.job_config.OS_SERVER_WAIT_TIME)

#         if config_drive == True:
#
#             # Reboot Server(OpenStack)
#             osc_servers_instance.action_server(
#                                     os_endpoint_vim,
#                                     os_server_res['server']['id'],
#                                     osc_servers_instance.SERVER_ACTION_REBOOT,
#                                     osc_servers_instance.SERVER_REBOOT_TYPE_SOFT)
#
#             # Wait Server Activated(OpenStack)
#             self.wait_os_server_active(
#                                     osc_servers_instance,
#                                     os_endpoint_vim,
#                                     os_server_res['server']['id'],
#                                     self.job_config.OS_SERVER_REBOOT_COUNT,
#                                     self.job_config.OS_SERVER_REBOOT_INTERVAL,
#                                     self.job_config.OS_SERVER_WAIT_TIME)

        # Create NAL_APL_MNG(DB Client)
        params = {}
        params['update_id'] = operation_id
        params['apl_type'] = apl_type
        params['type'] = hard_type
        params['device_type'] = device_type
        params['tenant_id'] = nal_tenant_id
        params['pod_id'] = pod_id
        params['node_id'] = os_server_res['server']['id']
        params['node_name'] = host_name
        params['node_detail'] = json.dumps([])
        params['server_id'] = os_server_res['server']['id']
        params['global_ip'] = global_ip
        params['server_info'] = json.dumps(os_server_res['server'])
        params['MSA_device_id'] = 0
        keys = [apl_table_rec_id]

        db_update_instance.set_context(db_endpoint_apl, keys, params)
        db_update_instance.execute()

        return os_server_res

    def __delete_server_vm_fw(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        apl_table_rec_id = job_input['apl_table_rec_id']
        pod_id = job_input['pod_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Create Instance(OpenStack Client)
        osc_servers_instance = servers.OscServers(self.job_config)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id, '', nal_tenant_id)

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        try:
            # Delete Server(OpenStack:VIM)
            osc_servers_instance.delete_server(os_endpoint_vim, node_id)
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Update NAL_VNF_MNG(DB Client):Set DeleteFlg On
        params = {}
        params['update_id'] = operation_id
        params['task_status'] = 1
        params['delete_flg'] = 1
        keys = [apl_table_rec_id]
        db_update_instance.set_context(db_endpoint_apl, keys, params)
        db_update_instance.execute()

    def __update_db_port_msa_vm(self, job_input, os_server_res, port_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id1 = job_input['port_id1']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get Create Server Result(id)
        server_id = os_server_res['server']['id']

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Assign Port For MSA Port
        port1 = self.assign_port(db_list_instance,
                                 db_endpoint_port,
                                 nal_tenant_id,
                                 apl_type,
                                 server_id,
                                 port_name,
                                 nf_type,
                                 device_type)

        # List NAL_PORT_MNG(DB Client) For MSA Port
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id1
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Update NAL_PORT_MNG(DB Client) For MSA Port
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['node_id'] = server_id
        params['nic'] = port1

        db_update_instance.set_context(db_endpoint_port, keys, params)
        db_update_instance.execute()

    def __update_db_port_msa_vm_lb(
                        self, job_input, os_server_res, port_name, port_nic):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id1 = job_input['port_id1']

        # Get Create Server Result(id)
        server_id = os_server_res['server']['id']

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # List NAL_PORT_MNG(DB Client) For MSA Port
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id1
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Update NAL_PORT_MNG(DB Client) For MSA Port
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['node_id'] = server_id
        params['nic'] = port_nic

        db_update_instance.set_context(db_endpoint_port, keys, params)
        db_update_instance.execute()

    def __update_db_port_pub_vm(self, job_input, os_server_res, port_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id2 = job_input['port_id2']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get Create Server Result(id)
        server_id = os_server_res['server']['id']

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Assign Port For Pub Port
        port2 = self.assign_port(db_list_instance,
                                 db_endpoint_port,
                                 nal_tenant_id,
                                 apl_type,
                                 server_id,
                                 port_name,
                                 nf_type, device_type)

        # List NAL_PORT_MNG(DB Client) For Pub Port
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id2
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Update NAL_PORT_MNG(DB Client) For Pub Port
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['node_id'] = server_id
        params['nic'] = port2
        db_update_instance.set_context(db_endpoint_port, keys, params)
        db_update_instance.execute()

    def __update_db_port_ext_vm(self, job_input, os_server_res, port_name):
        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id3 = job_input['port_id3']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get Create Server Result(id)
        server_id = os_server_res['server']['id']

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_endpoint_global_ip = self.get_db_endpoint(
                                    self.job_config.REST_URI_GLOBAL_IP)

        # Assign Port For Ext Port
        port3 = self.assign_port(db_list_instance,
                                 db_endpoint_port,
                                 nal_tenant_id,
                                 apl_type, server_id,
                                 port_name,
                                 nf_type,
                                 device_type)

        # List NAL_PORT_MNG(DB Client) For Ext Port
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id3
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Update NAL_PORT_MNG(DB Client) For Ext Port
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['node_id'] = server_id
        params['nic'] = port3
        db_update_instance.set_context(db_endpoint_port, keys, params)
        db_update_instance.execute()

        # List NAL_GLOBAL_IP_MNG(DB Client)
        params = {}
        params['global_ip'] = port_list[0]['ip_address']
        db_list_instance.set_context(db_endpoint_global_ip, params)
        db_list_instance.execute()
        global_ip_list = db_list_instance.get_return_param()

        # Update NAL_GLOBAL_IP_MNG(DB Client)
        keys = [global_ip_list[0]['ID']]
        params = {}
        params['node_id'] = server_id
        params['update_id'] = operation_id
        db_update_instance.set_context(db_endpoint_global_ip, keys, params)
        db_update_instance.execute()

    def __update_db_port_pub_ph(self, job_input, apl_info, port_name):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id2 = job_input['port_id2']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get Create Server Result(id)
        node_id = apl_info['node_id']

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Assign Port For Pub Port
        network_type_detail = self.job_config.NW_TYPE_PUBLIC
        if str(apl_type) == '2':
            if str(nf_type) == '1' and str(device_type) in ['2', '4']:
                network_type_detail = None
        port2 = self.assign_port(db_list_instance,
                                 db_endpoint_port,
                                 nal_tenant_id,
                                 apl_type,
                                 node_id,
                                 port_name,
                                 nf_type,
                                 device_type,
                                 network_type_detail)

        # List NAL_PORT_MNG(DB Client) For Pub Port
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id2
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Update NAL_PORT_MNG(DB Client) For Pub Port
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['node_id'] = node_id
        params['nic'] = port2
        db_update_instance.set_context(db_endpoint_port, keys, params)
        db_update_instance.execute()

    def __update_db_port_ext_ph(self, job_input, apl_info, port_name):
        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id3 = job_input['port_id3']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        apl_table_rec_id = job_input['apl_table_rec_id']

        # Get Create Server Result(id)
        node_id = apl_info['node_id']

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_global_ip = self.get_db_endpoint(
                                    self.job_config.REST_URI_GLOBAL_IP)

        # Assign Port For Ext Port
        network_type_detail = self.job_config.NW_TYPE_EXTRA
        if str(apl_type) == '2':
            if str(nf_type) == '1' and str(device_type) in ['2', '4']:
                network_type_detail = None
        port3 = self.assign_port(db_list_instance,
                                 db_endpoint_port,
                                 nal_tenant_id,
                                 apl_type,
                                 node_id,
                                 port_name,
                                 nf_type,
                                 device_type,
                                 network_type_detail)

        # List NAL_PORT_MNG(DB Client) For Ext Port
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id3
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Update NAL_PORT_MNG(DB Client) For Ext Port
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['node_id'] = node_id
        params['nic'] = port3
        db_update_instance.set_context(db_endpoint_port, keys, params)
        db_update_instance.execute()

        # Update NAL_APL_MNG(DB Client)
        params = {}
        params['update_id'] = operation_id
        params['global_ip'] = port_list[0]['ip_address']
        keys = [apl_table_rec_id]
        db_update_instance.set_context(db_endpoint_apl, keys, params)
        db_update_instance.execute()

        # List NAL_GLOBAL_IP_MNG(DB Client)
        params = {}
        params['global_ip'] = port_list[0]['ip_address']
        db_list_instance.set_context(db_endpoint_global_ip, params)
        db_list_instance.execute()
        global_ip_list = db_list_instance.get_return_param()

        # Update NAL_GLOBAL_IP_MNG(DB Client)
        keys = [global_ip_list[0]['ID']]
        params = {}
        params['node_id'] = node_id
        params['update_id'] = operation_id
        db_update_instance.set_context(db_endpoint_global_ip, keys, params)
        db_update_instance.execute()

    def __update_db_port_internal_vm(self, job_input, node_id, port_name):
        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input['port_id4']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Assign Port For Ext Port
        port4 = self.assign_port(db_list_instance,
                                 db_endpoint_port,
                                 nal_tenant_id,
                                 apl_type,
                                 node_id,
                                 port_name,
                                 nf_type,
                                 device_type)

        # List NAL_PORT_MNG(DB Client) For Internal Port
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id4

        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Update NAL_PORT_MNG(DB Client) For Internal Port
        if len(port_list[0]['nic']) == 0 and len(port_list[0]['node_id']) == 0:
            keys = [port_list[0]['ID']]
            params = {}
            params['update_id'] = operation_id
            params['node_id'] = node_id
            params['nic'] = port4

            db_update_instance.set_context(db_endpoint_port, keys, params)
            db_update_instance.execute()

    def __update_db_port_internal_ph(self, job_input, apl_info, port_name):
        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input['port_id4']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get Server Info(id)
        node_id = apl_info['node_id']

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Assign Port For Ext Port
        network_type_detail = self.job_config.NW_TYPE_TENANT
        if str(apl_type) == '2':
            if str(nf_type) == '1' and str(device_type) in ['2', '4']:
                network_type_detail = None
        port4 = self.assign_port(db_list_instance,
                                 db_endpoint_port,
                                 nal_tenant_id,
                                 apl_type,
                                 node_id,
                                 port_name,
                                 nf_type,
                                 device_type,
                                 network_type_detail)

        # List NAL_PORT_MNG(DB Client) For Internal Port
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id4

        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        # Update NAL_PORT_MNG(DB Client) For Internal Port
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        params['node_id'] = node_id
        params['nic'] = port4

        db_update_instance.set_context(db_endpoint_port, keys, params)
        db_update_instance.execute()

    def __attach_port_internal_vm(self,
                                  job_input,
                                  port_id):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']

        # Create Instance(OpenStack Client)
        osc_servers_instance = servers.OscServers(self.job_config)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                            pod_id,
                                            '',
                                            nal_tenant_id)

        # Attach Interface(OpenStack)
        osc_servers_instance.attach_interface(
                                    os_endpoint_vim, node_id, port_id)

        # Reboot Server(OpenStack)
        osc_servers_instance.action_server(
                                os_endpoint_vim,
                                node_id,
                                osc_servers_instance.SERVER_ACTION_REBOOT,
                                osc_servers_instance.SERVER_REBOOT_TYPE_SOFT)

        # Wait Server Activated(OpenStack)
        self.wait_os_server_active(
                                osc_servers_instance,
                                os_endpoint_vim,
                                node_id,
                                self.job_config.OS_SERVER_REBOOT_COUNT,
                                self.job_config.OS_SERVER_REBOOT_INTERVAL,
                                self.job_config.OS_SERVER_WAIT_TIME_FOR_ATTACH)

        return

    def __detach_port_internal_vm(self,
                                  job_input,
                                  port_id):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']

        # Create Instance(OpenStack Client)
        osc_servers_instance = servers.OscServers(self.job_config)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(
                                            pod_id,
                                            '',
                                            nal_tenant_id)

        # Detach Interface(OpenStack)
        osc_servers_instance.detach_interface(
                                    os_endpoint_vim, node_id, port_id)

        return

    def __set_networks(self, job_input):

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        networks = []
        if 'port_id1' in job_input:
            # List NAL_PORT_MNG(DB Client) For MSA Port
            params = {}
            params['delete_flg'] = 0
            params['tenant_id'] = job_input['nal_tenant_id']
            params['port_id'] = job_input['port_id1']
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list1 = db_list_instance.get_return_param()

            networks.append({
                'uuid': port_list1[0]['network_id'],
                'port': job_input['port_id1'],
            })

        if 'port_id2' in job_input:
            # List NAL_PORT_MNG(DB Client) For Pub Port
            params = {}
            params['delete_flg'] = 0
            params['tenant_id'] = job_input['nal_tenant_id']
            params['port_id'] = job_input['port_id2']
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list2 = db_list_instance.get_return_param()

            networks.append({
                'uuid': port_list2[0]['network_id'],
                'port': job_input['port_id2'],
            })

        if 'port_id3' in job_input:
            # List NAL_PORT_MNG(DB Client) For Ext Port
            params = {}
            params['delete_flg'] = 0
            params['tenant_id'] = job_input['nal_tenant_id']
            params['port_id'] = job_input['port_id3']
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list3 = db_list_instance.get_return_param()

            networks.append({
                'uuid': port_list3[0]['network_id'],
                'port': job_input['port_id3'],
            })

        if 'port_id4' in job_input:
            # List NAL_PORT_MNG(DB Client) For Internal Port
            params = {}
            params['delete_flg'] = 0
            params['tenant_id'] = job_input['nal_tenant_id']
            params['port_id'] = job_input['port_id4']
            db_list_instance.set_context(db_endpoint_port, params)
            db_list_instance.execute()
            port_list4 = db_list_instance.get_return_param()

            networks.append({
                'uuid': port_list4[0]['network_id'],
                'port': job_input['port_id4'],
            })

        return networks

    def __update_pysical_apl_assign(self,
                                    operation_id,
                                    nal_tenant_id,
                                    apl_table_rec_id):

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # Update NAL_APL_MNG(DB Client)
        params = {}
        params['update_id'] = operation_id
        params['tenant_id'] = nal_tenant_id
        keys = [apl_table_rec_id]
        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['ID'] = apl_table_rec_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        return apl_list[0]

    def __update_license_fortigate_vm_541(self, job_input, node_id):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        hard_type = job_input['type']
        device_type = job_input['device_type']

        # Get Endpoint(DB Client)
        db_endpoint_license = self.get_db_endpoint(
                                    self.job_config.REST_URI_LICENSE)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_LICENSE_MNG(DB Client)
        params = {}
        params['status'] = 2
        params['type'] = hard_type
        params['device_type'] = device_type
        params['delete_flg'] = 0
        params['node_id'] = ''
        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        license_list = db_list.get_return_param()

        if len(license_list) == 0:
            raise SystemError('assigned license not exists.')

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [license_list[0]['ID']]
        params = {}
        params['status'] = 2
        params['update_id'] = operation_id
        params['node_id'] = node_id
        db_update.set_context(db_endpoint_license, keys, params)
        db_update.execute()

    def __set_personality_paloalto_vm(self, job_input, user_new_password):

        personality = []

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        tenant_name = job_input['tenant_name']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id1 = job_input['port_id1']

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = self.get_db_endpoint(
                                    self.job_config.REST_URI_MSA_VLAN)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # List NAL_MSA_VLAN_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['pod_id'] = pod_id
        params['tenant_name'] = tenant_name
        db_list_instance.set_context(db_endpoint_msa_vlan, params)
        db_list_instance.execute()
        msa_vlan_list = db_list_instance.get_return_param()

        msa_subnet_info = json.loads(msa_vlan_list[0]['subnet_info'])

        # List NAL_PORT_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id1
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        msa_port_list = db_list_instance.get_return_param()

        msa_netmask = self.utils.get_subnet_mask_from_cidr_ipv6(
                msa_port_list[0]['ip_address'] + '/' + \
                                            msa_port_list[0]['netmask'])

        # Get Template(bootstrap)
        with open(self.job_config.TEMPLATE_DIR \
            + self.job_config.TEMPLATE_INIT_PROV_IS_VM_PALOALTO_BOOTSTRAP, 'r'
            ) as f:
                template_str = f.read()

        # Replace Template(bootstrap)
        template_str = template_str.replace('%admin_password%',
                                self.utils.get_hash_value('',
                                    self.job_config.CHAR_SET,
                                    self.job_config.SCRIPT_STDOUT_SEPARATER,
                                    user_new_password))

        template_str = template_str.replace('%mng_ip_address%',
                                            msa_port_list[0]['ip_address'])

        template_str = template_str.replace('%mng_net_mask%', msa_netmask)

        template_str = template_str.replace('%mng_dgw_ip_address%',
                                            msa_subnet_info['gateway_ip'])

        # Set Personality(bootstrap)
        personality.append({
                'path': servers.OscServers(self.job_config).\
                                                PERSONALITY_PATH_BOOTSTRAP,
                'contents': base64.b64encode(
                        template_str.encode(
                                self.job_config.CHAR_SET)).decode('ascii'),

            })

        # Get Template(init-cfg)
        with open(self.job_config.TEMPLATE_DIR \
            + self.job_config.TEMPLATE_INIT_PROV_IS_VM_PALOALTO_INIT_CFG, 'r'
            ) as f:
                template_str = f.read()

        # Replace Template(init-cfg)
        template_str = template_str.replace('%msa_port_ip_address%',
                                            msa_port_list[0]['ip_address'])

        template_str = template_str.replace('%msa_port_df_gw%',
                                            msa_subnet_info['gateway_ip'])

        template_str = template_str.replace('%msa_port_netmask%', msa_netmask)

        # Set Personality(init-cfg)
        personality.append({
                'path': servers.OscServers(self.job_config).\
                                                PERSONALITY_PATH_INIT_CFG,
                'contents': base64.b64encode(
                        template_str.encode(
                                self.job_config.CHAR_SET)).decode('ascii'),

            })

        return personality
