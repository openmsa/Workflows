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
import datetime
import inspect

from job.auto import base
from job.lib.db import list
from job.lib.db import update
from job.lib.script import zerotouch
from job.lib.script import licenseauth


class License(base.JobAutoBase):

    DEVICE_NAME_FORTIGATE_VM = 'fortigate_vm'
    DEVICE_NAME_FORTIGATE_VM_541 = 'fortigate_vm_541'
    DEVICE_NAME_INTERSEC_SG = 'intersec_sg'
    DEVICE_NAME_INTERSEC_LB = 'intersec_lb'
    DEVICE_NAME_CSR1000V = 'csr1000v'

    def license_assign_fortigate_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Assign License(DB)
        license_key = self._assign_license(job_input)

        # Execute Initial Script(ZeroTouch)
        self.__initial_script_zerotouch_fortigate(job_input, license_key)

        # Set JOB Output Parameters
        job_output = {'license_key': license_key}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def license_assign_fortigate_vm_541(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Assign License(DB)
        license_key = self._assign_license(job_input)

        # Set JOB Output Parameters
        job_output = {'license_key': license_key}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def zerotouch_paloalto_vm(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Execute Initial Script(ZeroTouch)
        self.__initial_script_zerotouch_paloalto(job_input)

        # Set JOB Output Parameters
        job_output = {'license_key': ''}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def license_assign_palpalto_vm(self, job_input):

        job_output = {}

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Execute Initial Script(ZeroTouch)
        self.__activation(job_input)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def license_assign_bigip_ve(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Assign License(DB)
        license_key = self._assign_license(job_input)

        # Execute Initial Script(ZeroTouch)
        self.__initial_script_zerotouch_bigip_ve(job_input, license_key)

        # Set JOB Output Parameters
        job_output = {'license_key': license_key}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def zerotouch_vthunder(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Execute Initial Script(ZeroTouch)
        self.__initial_script_zerotouch_vthunder(job_input)

        # Set JOB Output Parameters
        job_output = {'license_key': ''}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def license_assign_vthunder(self, job_input):

        job_output = {}

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Execute Initial Script(ZeroTouch)
        self.__activation(job_input)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def license_assign(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Assign License(DB)
        license_key = self._assign_license(job_input)

        # Set JOB Output Parameters
        job_output = {'license_key': license_key}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def license_withdraw(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        node_id = job_input['node_id']

        # Withdraw License(DB)
        self._withdraw_license(job_input, node_id)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def _assign_license(self, job_input):

        license_key = ''

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        tenant_name = job_input['tenant_name']
        hard_type = job_input['type']
        device_type = job_input['device_type']
        node_id = job_input.get('node_id', '')
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        dc_id = job_input.get('dc_id', 'system')

        type_detail = job_input.get('license_type_detail', '')

        # Get Config(Device Name)
        device_name = self.device_type_to_name(
                                apl_type, nf_type, device_type, dc_id)

        # Get Endpoint(DB Client)
        db_endpoint_license = self.get_db_endpoint(
                                    self.job_config.REST_URI_LICENSE)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_LICENSE_MNG(DB Client)
        params = {}
        params['status'] = 0
        params['type'] = hard_type
        params['device_type'] = device_type
        params['delete_flg'] = 0

        if len(type_detail) > 0:
            params['type_detail'] = type_detail

        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        license_list1 = db_list.get_return_param()

        if len(license_list1) > 0:

            # Update NAL_LICENSE_MNG(DB Client)
            keys = [license_list1[0]['ID']]
            params = {}
            params['status'] = 2
            params['tenant_name'] = tenant_name
            params['update_id'] = operation_id
            params['node_id'] = node_id
            db_update.set_context(db_endpoint_license, keys, params)
            db_update.execute()

            license_key = license_list1[0]['license']
            license_id = license_list1[0]['ID']

        else:

            if device_name not in [
                    self.DEVICE_NAME_FORTIGATE_VM,
                    self.DEVICE_NAME_FORTIGATE_VM_541,
                    self.DEVICE_NAME_INTERSEC_SG,
                    self.DEVICE_NAME_INTERSEC_LB,
                    self.DEVICE_NAME_CSR1000V,
                ]:
                raise SystemError('license not found.')

            # List NAL_LICENSE_MNG(DB Client)
            params = {}
            params['status'] = 3
            params['type'] = hard_type
            params['device_type'] = device_type
            params['delete_flg'] = 0

            if len(type_detail) > 0:
                params['type_detail'] = type_detail

            db_list.set_context(db_endpoint_license, params)
            db_list.execute()
            license_list2 = db_list.get_return_param()

            if len(license_list2) == 0:
                raise SystemError('license not found.')

            check_date = (datetime.datetime.now()\
                                - datetime.timedelta(hours=4))\
                                .strftime('%Y-%m-%d %H:%M:%S')

            fortgate_vm_license_found = False

            for idx in range(len(license_list2)):

                if device_name in [
                        self.DEVICE_NAME_FORTIGATE_VM,
                        self.DEVICE_NAME_FORTIGATE_VM_541,
                    ]:

                    if check_date > license_list2[idx]['update_date']:
                        fortgate_vm_license_found = True
                    else:
                        continue

                # Update NAL_LICENSE_MNG(DB Client)
                params = {}
                params['status'] = 2
                params['tenant_name'] = tenant_name
                params['update_id'] = operation_id
                params['node_id'] = node_id
                keys = [license_list2[idx]['ID']]
                db_update.set_context(
                                db_endpoint_license, keys, params)
                db_update.execute()

                license_key = license_list2[idx]['license']
                license_id = license_list2[idx]['ID']
                break

            if device_name in [
                    self.DEVICE_NAME_FORTIGATE_VM,
                    self.DEVICE_NAME_FORTIGATE_VM_541,
                ] and fortgate_vm_license_found == False:

                raise SystemError('license not found.')

        if device_name == self.DEVICE_NAME_CSR1000V:
            return license_id
        else:
            return license_key

    def _withdraw_license(self, job_input, node_id):

        if len(node_id) > 0:

            # Get JOB Input Parameters
            operation_id = job_input['operation_id']
            tenant_name = job_input['tenant_name']
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
            params['node_id'] = node_id
            params['tenant_name'] = tenant_name
            params['delete_flg'] = 0
            params['type'] = hard_type
            params['device_type'] = device_type
            db_list.set_context(db_endpoint_license, params)
            db_list.execute()
            license_list = db_list.get_return_param()

            # Update NAL_LICENSE_MNG(DB Client)
            for rec in license_list:
                keys = [rec['ID']]
                params = {}
                params['status'] = 3
                params['tenant_name'] = ''
                params['node_id'] = ''
                params['type_detail'] = ''
                params['update_id'] = operation_id
                db_update.set_context(db_endpoint_license, keys, params)
                db_update.execute()

    def __initial_script_zerotouch_fortigate(self, job_input, license_key):

        # Create Instance(Script Client)
        zerotouch_instance = zerotouch.ZeroTouchClient(self.job_config)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        node_id = job_input['node_id']
        nal_tenant_id = job_input['nal_tenant_id']
        tenant_name = job_input['tenant_name']
        port_id1 = job_input['port_id1']
        port_id2 = job_input['port_id2']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

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

        # Get Vim Endpoint
        vim_endpoint_data = self.nal_endpoint_config['system']['vim'][pod_id]

        if vim_iaas_with_flg == 0:
            server_login_password = vim_endpoint_data[
                        'openstack_controller_node_server_login_password']
            nal_private_key_path = ''
        else:
            server_login_password = ''
            nal_private_key_path = self.get_nal_private_key_path()

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

        # Set Input Parameters(ZeroTouchClient)
        params = [
            vim_endpoint_data['openstack_controller_node_ip_address'],
            vim_endpoint_data['openstack_controller_node_server_login_id'],
            server_login_password,
            nal_private_key_path,
            vim_endpoint_data['openstack_keystone_ip_address'],
            vim_endpoint_data['user_id'],
            vim_endpoint_data['user_password'],
            node_id,
            msa_config_for_device['user_id'],
            msa_config_for_device['user_default_password'],
            port_list1[0]['ip_address'] + '/' + port_list1[0]['netmask'],
            port_list2[0]['ip_address'] + '/' + port_list2[0]['netmask'],
            msa_config_for_common['svc_vlan_dns_primary_ip_address'],
            msa_config_for_common['svc_vlan_proxy_ip_address'],
            msa_config_for_common['svc_vlan_proxy_port'],
            msa_vlan_list[0]['msa_ip_address'],
            license_key,
            msa_config_for_device['user_new_password'],
            msa_config_for_common['pub_vlan_gateway'],
            port_list2[0]['nic'],
            vim_endpoint_data['admin_tenant_name'],
            vim_endpoint_data['region_id']
        ]

        passwords = [
            vim_endpoint_data[
                        'openstack_controller_node_server_login_password'],
            vim_endpoint_data['user_password'],
            msa_config_for_device['user_new_password'],
        ]

        # Execute ZeroTouchClient
        zerotouch_instance.fortivm_provisioning(params, passwords)

    def __initial_script_zerotouch_paloalto(self, job_input):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        tenant_name = job_input['tenant_name']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        node_id = job_input['node_id']
        port_id1 = job_input['port_id1']

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

        # Get Vim Endpoint
        vim_endpoint_data = self.nal_endpoint_config['system']['vim'][pod_id]

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
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

        # Create Instance(Script Client)
        zerotouch_instance = zerotouch.ZeroTouchClient(self.job_config)

        # Set Input Parameters(ZeroTouchClient)
        params = [
            vim_endpoint_data['openstack_controller_node_ip_address'],
            vim_endpoint_data['openstack_controller_node_server_login_id'],
            vim_endpoint_data[
                        'openstack_controller_node_server_login_password'],
            vim_endpoint_data['openstack_keystone_ip_address'],
            vim_endpoint_data['user_id'],
            vim_endpoint_data['user_password'],
            node_id,
            msa_config_for_device['user_id'],
            msa_config_for_device['user_default_password'],
            port_list1[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(
                                            port_list1[0]['netmask']),
            msa_vlan_list[0]['msa_ip_address'],
            msa_config_for_device['user_new_password'],
            vim_endpoint_data['admin_tenant_name']
        ]

        passwords = [
            vim_endpoint_data[\
                        'openstack_controller_node_server_login_password'],
            vim_endpoint_data['user_password'],
            msa_config_for_device['user_default_password'],
            msa_config_for_device['user_new_password'],
        ]

        # Execute ZeroTouchClient
        zerotouch_instance.paloalto_provisioning(params, passwords)

    def __initial_script_zerotouch_bigip_ve(self, job_input, license_key):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        tenant_name = job_input['tenant_name']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        node_id = job_input['node_id']
        port_id1 = job_input['port_id1']
        port_id4 = job_input['port_id4']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

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
        params['port_id'] = port_id4
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list4 = db_list.get_return_param()

        # Get Vim Endpoint
        vim_endpoint_data = self.nal_endpoint_config['system']['vim'][pod_id]

        if vim_iaas_with_flg == 0:
            server_login_password = vim_endpoint_data[
                        'openstack_controller_node_server_login_password']
            nal_private_key_path = ''
        else:
            server_login_password = ''
            nal_private_key_path = self.get_nal_private_key_path()

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
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

        # Create Instance(Script Client)
        zerotouch_instance = zerotouch.ZeroTouchClient(self.job_config)

        # Set Input Parameters(ZeroTouchClient)
        params = [
            vim_endpoint_data['openstack_controller_node_ip_address'],
            vim_endpoint_data['openstack_controller_node_server_login_id'],
            server_login_password,
            nal_private_key_path,
            vim_endpoint_data['openstack_keystone_ip_address'],
            vim_endpoint_data['user_id'],
            vim_endpoint_data['user_password'],
            node_id,
            msa_config_for_device['user_id'],
            msa_config_for_device['user_default_password'],
            port_list1[0]['ip_address'],
            port_list1[0]['netmask'],
            msa_config_for_device['default_route_name'],
            msa_vlan_list[0]['msa_ip_address'],
            msa_config_for_device['admin_password'],
            license_key,
            port_list4[0]['ip_address'],
            self.utils.get_subnet_mask_from_cidr_len(
                                            port_list4[0]['netmask']),
            job_input['fw_ip_address'],
            vim_endpoint_data['admin_tenant_name'],
            vim_endpoint_data['region_id']
        ]

        passwords = [
            vim_endpoint_data[
                        'openstack_controller_node_server_login_password'],
            vim_endpoint_data['user_password'],
            msa_config_for_device['user_default_password'],
            msa_config_for_device['admin_password'],
        ]

        # Execute ZeroTouchClient
        zerotouch_instance.bigip_provisioning(params, passwords)

    def __initial_script_zerotouch_vthunder(self, job_input):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        tenant_name = job_input['tenant_name']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        node_id = job_input['node_id']
        port_id1 = job_input['port_id1']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

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

        # Get Vim Endpoint
        vim_endpoint_data = self.nal_endpoint_config['system']['vim'][pod_id]

        if vim_iaas_with_flg == 0:
            server_login_password = vim_endpoint_data[
                        'openstack_controller_node_server_login_password']
            nal_private_key_path = ''
        else:
            server_login_password = ''
            nal_private_key_path = self.get_nal_private_key_path()

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
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

        # Create Instance(Script Client)
        zerotouch_instance = zerotouch.ZeroTouchClient(self.job_config)

        # Set Input Parameters(ZeroTouchClient)
        params = [
            vim_endpoint_data['openstack_controller_node_ip_address'],
            vim_endpoint_data['openstack_controller_node_server_login_id'],
            server_login_password,
            nal_private_key_path,
            vim_endpoint_data['openstack_keystone_ip_address'],
            vim_endpoint_data['user_id'],
            vim_endpoint_data['user_password'],
            node_id,
            msa_config_for_device['user_id'],
            msa_config_for_device['user_default_password'],
            port_list1[0]['ip_address'] + ' /' + port_list1[0]['netmask'],
            msa_vlan_list[0]['msa_ip_address'],
            msa_config_for_device['admin_password'],
            vim_endpoint_data['admin_tenant_name'],
            vim_endpoint_data['region_id']
        ]

        passwords = [
            vim_endpoint_data[\
                        'openstack_controller_node_server_login_password'],
            vim_endpoint_data['user_password'],
            msa_config_for_device['user_default_password'],
            msa_config_for_device['admin_password'],
        ]

        # Execute ZeroTouchClient
        zerotouch_instance.a10_vthunder_provisioning(params, passwords)

    def __activation(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        node_id = job_input['node_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Endpoint(DB Client)
        db_endpoint_license = self.get_db_endpoint(
                                    self.job_config.REST_URI_LICENSE)
        db_endpoint_msa_vlan = \
            self.get_db_endpoint(self.job_config.REST_URI_MSA_VLAN)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # Create Instance(Script Client)
        license_instance = licenseauth.LicenseAuthClient(self.job_config)

        # Get Vim Endpoint
        vim_endpoint_data = self.nal_endpoint_config['system']['vim'][pod_id]

        if vim_iaas_with_flg == 0:
            server_login_password = vim_endpoint_data[
                        'openstack_controller_node_server_login_password']
            nal_private_key_path = ''
        else:
            server_login_password = ''
            nal_private_key_path = self.get_nal_private_key_path()

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
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

        # List NAL_LICENSE_MNG(DB Client)
        params = {}
        params['status'] = 0
        params['tenant_name'] = tenant_name
        params['node_id'] = node_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        license_list = db_list.get_return_param()

        if len(license_list) == 0:
            raise SystemError('license not found.')
        else:
            for rec in license_list:

                # activetion(LicenseClient)
                params = [
                    vim_endpoint_data['openstack_controller_node_ip_address'],
                    vim_endpoint_data[
                        'openstack_controller_node_server_login_id'],
                    server_login_password,
                    nal_private_key_path,
                    vim_endpoint_data['openstack_keystone_ip_address'],
                    vim_endpoint_data['user_id'],
                    vim_endpoint_data['user_password'],
                    node_id,
                    msa_config_for_device['user_id'],
                    msa_config_for_device['admin_password'],
                    msa_vlan_list[0]['msa_ip_address'],
                    rec['license'],
                    vim_endpoint_data['admin_tenant_name'],
                    vim_endpoint_data['region_id']
                ]

                passwords = [
                    vim_endpoint_data[
                        'openstack_controller_node_server_login_password'],
                    vim_endpoint_data['user_password'],
                    msa_config_for_device['admin_password'],
                ]

                # Execute LicenseClient
                if device_name == 'paloalto_vm':
                    license_instance.paloalto_authentication(params, passwords)
                else:
                    license_instance.a10_vthunder_authentication(params,
                                                                 passwords)

                # Update NAL_LICENSE_MNG(DB Client)
                keys = [rec['ID']]
                params = {}
                params['update_id'] = operation_id
                params['status'] = 2
                params['tenant_name'] = tenant_name
                params['node_id'] = node_id
                db_update.set_context(db_endpoint_license, keys, params)
                db_update.execute()
