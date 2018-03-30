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
from job.lib.db import create
from job.lib.db import list
from job.lib.db import update
from job.lib.openstack.keystone import roles
from job.lib.openstack.keystone import tenants


class Tenant(base.JobAutoBase):

    def get_nal_tenant_name(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get Tenant(NAL)
        nal_tenant_list = self.__get_nal_tenant_name(job_input)

        if len(nal_tenant_list) == 0:
            raise SystemError('tenant not exists.')

        # Get JOB Output Parameters
        job_output = {
            'tenant_name': nal_tenant_list[0]['tenant_name'],
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def get_or_create_nal_tenant_name(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get Tenant(NAL)
        nal_tenant_list = self.__get_nal_tenant_name(job_input)

        if len(nal_tenant_list) == 0:
            # Set TenantInfo(NAL)/Create Tenant(NAL)
            tenant_name = self.__create_nal_tenant_name(job_input)
        else:
            tenant_name = nal_tenant_list[0]['tenant_name']

        # Get JOB Output Parameters
        job_output = {
            'tenant_name': tenant_name,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def get_pod_tenant(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get Tenant(NAL)
        os_tenant_info = self.__get_pod_tenant(job_input)

        if len(os_tenant_info['nal_tenant_id']) == 0:
            raise SystemError('tenant not exists in pod')

        # Get JOB Output Parameters
        job_output = os_tenant_info

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def get_or_create_pod_tenant(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_table_rec_id = job_input.get('apl_table_rec_id', '')
        hard_type = job_input.get('type', '')

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Tenant(NAL)
        os_tenant_info = self.__get_pod_tenant(job_input)

        if len(os_tenant_info['nal_tenant_id']) == 0:
            if vim_iaas_with_flg == 0:
                # Set TenantInfo(NAL)/Create Tenant(NAL)
                os_tenant_info = self.__create_pod_tenant(job_input)
            else:
                os_tenant_info = self.__get_device_endpoint_info(job_input)
        else:
            pass

        if hard_type in ['1', '2']:
            # Create Instance(DB Client)
            db_update_instance = update.UpdateClient(self.job_config)

            # Get Endpoint(DB Client)
            db_endpoint_apl = self.get_db_endpoint(
                                                self.job_config.REST_URI_APL)

            # Update NAL_APL_MNG(DB Client) For Set PodID
            keys = [apl_table_rec_id]
            params = {}
            params['update_id'] = operation_id
            params['tenant_id'] = os_tenant_info['nal_tenant_id']

            db_update_instance.set_context(db_endpoint_apl, keys, params)
            db_update_instance.execute()

        # Get JOB Output Parameters
        job_output = {
            'nal_tenant_id': os_tenant_info['nal_tenant_id'],
            'nal_tenant_name': os_tenant_info['nal_tenant_name'],
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __get_nal_tenant_name(self, job_input):

        # Get JOB Input Parameters
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_region_id = job_input['IaaS_region_id']

        # Get Endpoint(DB Client)
        db_endpoint_tenant = self.get_db_endpoint(
                                    self.job_config.REST_URI_TENANT)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # List NAL_TENANT_MNG(DB Client)
        params = {}
        params['IaaS_region_id'] = iaas_region_id
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_tenant, params)
        db_list_instance.execute()
        nal_tenant_list = db_list_instance.get_return_param()

        return nal_tenant_list

    def __create_nal_tenant_name(self, job_input):

        # Get JOB Input Parameters
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_region_id = job_input['IaaS_region_id']
        operation_id = job_input['operation_id']

        # Set UUID
        tenant_name = iaas_tenant_id

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_tenant = self.get_db_endpoint(
                                self.job_config.REST_URI_TENANT)

        # Create NAL_TENANT_MNG(DB Client)
        params = {}
        params['create_id'] = operation_id
        params['update_id'] = operation_id
        params['delete_flg'] = 0
        params['IaaS_region_id'] = iaas_region_id
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['tenant_name'] = tenant_name
        json_wk = []
        params['tenant_info'] = json.dumps(json_wk)
        db_create_instance.set_context(db_endpoint_tenant, params)
        db_create_instance.execute()

        return tenant_name

    def __get_pod_tenant(self, job_input):

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']

        # Get Endpoint(DB Client)
        db_endpoint_tenant = self.get_db_endpoint(
                                    self.job_config.REST_URI_TENANT)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # List NAL_TENANT_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_tenant, params)
        db_list_instance.execute()
        nal_tenant_list = db_list_instance.get_return_param()

        nal_tenant_name = ''
        tenant_id = ''
        if len(nal_tenant_list) != 0:
            tenant_info = json.loads(nal_tenant_list[0]['tenant_info'])

            for val in tenant_info:
                if val.get('pod_id', '') == pod_id:
                    tenant_id = val.get('id', '')
                    nal_tenant_name = val.get('name', '')
                    break

        job_output = {
            'nal_tenant_id': tenant_id,
            'nal_tenant_name': nal_tenant_name,
        }

        return job_output

    def __create_pod_tenant(self, job_input):

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        iaas_tenant_name = job_input['IaaS_tenant_name']
        operation_id = job_input['operation_id']
        dc_id = job_input.get('dc_id', 'system')

        # Get Endpoint(DB Client)
        db_endpoint_tenant = self.get_db_endpoint(
                                self.job_config.REST_URI_TENANT)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # Get Endpoint(OpenStack:VIM)
        endpoint_config = self.nal_endpoint_config[dc_id]['vim'][pod_id]
        os_endpoint = self.get_os_endpoint_vim(pod_id,
                                    '',
                                    endpoint_config['admin_tenant_id'],
                                    dc_id)

        # Create Instance(OpenStack Client)
        osc_tenants = tenants.OscTenants(self.job_config)
        osc_roles = roles.OscRoles(self.job_config)

        # Create Tenant(OpenStack Client)
        os_tenant_res = osc_tenants.create_tenant(
                                    os_endpoint, iaas_tenant_name)

        # Add Admin Role To Tenant Admin User(OpenStack Client)
        osc_roles.add_role_to_user(os_endpoint,
                                    endpoint_config['user_key'],
                                    os_tenant_res['project']['id'],
                                    endpoint_config['role_id'])

        # List NAL_TENANT_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_tenant, params)
        db_list_instance.execute()
        nal_tenant_list = db_list_instance.get_return_param()

        if len(nal_tenant_list) == 0:
            raise SystemError('tenant not exists.')

        rec_id = nal_tenant_list[0]['ID']
        tenant_info = json.loads(nal_tenant_list[0]['tenant_info'])

        tenant_info_wk = os_tenant_res['project']
        tenant_info_wk['pod_id'] = pod_id
        tenant_info_wk['msa_customer_name'] = ''
        tenant_info_wk['msa_customer_id'] = 0

        tenant_info.append(tenant_info_wk)

        # Update NAL_VNF_MNG(DB Client):Set DeleteFlg On
        params = {}
        params['update_id'] = operation_id
        params['tenant_info'] = json.dumps(tenant_info)
        keys = [rec_id]
        db_update_instance.set_context(db_endpoint_tenant, keys, params)
        db_update_instance.execute()

        job_output = {
            'nal_tenant_id': os_tenant_res['project']['id'],
            'nal_tenant_name': os_tenant_res['project']['name'],
        }

        return job_output

    def __get_device_endpoint_info(self, job_input):
        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        operation_id = job_input['operation_id']
        dc_id = job_input.get('dc_id', 'system')

        # Get Endpoint(DB Client)
        db_endpoint_tenant = self.get_db_endpoint(
                                self.job_config.REST_URI_TENANT)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # Get Endpoint(OpenStack:VIM)
        endpoint_config = self.nal_endpoint_config[dc_id]['vim'][pod_id]
        admin_tenant_id = endpoint_config['admin_tenant_id']
        admin_tenant_name = endpoint_config['admin_tenant_name']

        # List NAL_TENANT_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_tenant, params)
        db_list_instance.execute()
        nal_tenant_list = db_list_instance.get_return_param()

        if len(nal_tenant_list) == 0:
            raise SystemError('tenant not exists.')

        rec_id = nal_tenant_list[0]['ID']
        tenant_info = json.loads(nal_tenant_list[0]['tenant_info'])

        tenant_info_wk = {}
        tenant_info_wk['pod_id'] = pod_id
        tenant_info_wk['id'] = admin_tenant_id
        tenant_info_wk['name'] = admin_tenant_name
        tenant_info_wk['msa_customer_name'] = ''
        tenant_info_wk['msa_customer_id'] = 0
        tenant_info.append(tenant_info_wk)

        # Update NAL_VNF_MNG(DB Client):Set DeleteFlg On
        params = {}
        params['update_id'] = operation_id
        params['tenant_info'] = json.dumps(tenant_info)
        keys = [rec_id]
        db_update_instance.set_context(db_endpoint_tenant, keys, params)
        db_update_instance.execute()

        job_output = {
            'nal_tenant_id': admin_tenant_id,
            'nal_tenant_name': admin_tenant_name,
        }

        return job_output
