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


class Initialize(base.JobAutoBase):

    def get_apl_info(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        node_id = job_input['node_id']

        # Get VNF Info
        job_output = self.__get_vnf_info(tenant_name, node_id)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def get_apl_info_by_rec_id(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        apl_table_rec_id = job_input['apl_table_rec_id']

        # Get VNF Info
        job_output = self.__get_apl_info(tenant_name, apl_table_rec_id)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def initialize_create_vnf(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_type = job_input['apl_type']
        hard_type = job_input['type']
        device_type = job_input['device_type']
        tenant_name = job_input['tenant_name']
        host_name = job_input['host_name']
        description = job_input.get('description', '')

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create NAL_VNF_MNG(DB Client)
        params = {}
        params['create_id'] = operation_id
        params['update_id'] = operation_id
        params['delete_flg'] = 0
        params['node_id'] = ''
        params['apl_type'] = apl_type
        params['type'] = hard_type
        params['device_type'] = device_type
        params['tenant_name'] = tenant_name
        params['node_name'] = host_name
        params['description'] = description
        params['task_status'] = 0
        params['err_info'] = json.dumps([])

        db_create_instance.set_context(db_endpoint_apl, params)
        db_create_instance.execute()
        apl_table_data = db_create_instance.get_return_param()

        job_output = {'apl_table_rec_id': apl_table_data['ID']}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def initialize_create_pnf(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        apl_info = self.__update_pysical_apl_assign(job_input)

        job_output = {'apl_table_rec_id': apl_info['ID'],
                      'node_id':  apl_info['node_id'],
                      'pod_id':  apl_info['pod_id']}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __get_vnf_info(self, tenant_name, node_id):

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_VNF_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['node_id'] = node_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        vnf_list = db_list.get_return_param()

        if len(vnf_list) == 0:
            raise SystemError('server not exists.')

        # Update NAL_APL_MNG(DB Client)
        params = {}
        params['task_status'] = 0
        keys = [vnf_list[0]['ID']]
        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()

        vnf_output = {
            'apl_table_rec_id': vnf_list[0]['ID'],
            'msa_device_id': vnf_list[0]['MSA_device_id'],
            'pod_id': vnf_list[0]['pod_id'],
            'apl_type': vnf_list[0]['apl_type'],
            'type': vnf_list[0]['type'],
            'device_type': vnf_list[0]['device_type'],
            'nal_tenant_id': vnf_list[0]['tenant_id'],
            'node_id': vnf_list[0]['node_id'],
            'redundant_configuration_flg':
                    vnf_list[0]['redundant_configuration_flg']
        }

        return vnf_output

    def __get_apl_info(self, tenant_name, apl_table_rec_id):

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['ID'] = apl_table_rec_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        vnf_list = db_list.get_return_param()

        if len(vnf_list) == 0:
            raise SystemError('server not exists.')

        # Update NAL_APL_MNG(DB Client)
        params = {}
        params['task_status'] = 0
        keys = [vnf_list[0]['ID']]
        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()

        vnf_output = {
            'apl_table_rec_id': vnf_list[0]['ID'],
            'msa_device_id': vnf_list[0]['MSA_device_id'],
            'pod_id': vnf_list[0]['pod_id'],
            'apl_type': vnf_list[0]['apl_type'],
            'type': vnf_list[0]['type'],
            'device_type': vnf_list[0]['device_type'],
            'nal_tenant_id': vnf_list[0]['tenant_id'],
            'node_id': vnf_list[0]['node_id'],
            'redundant_configuration_flg':
                    vnf_list[0]['redundant_configuration_flg']
        }

        return vnf_output

    def __update_pysical_apl_assign(self, job_input):

        # Get Param
        tenant_name = job_input['tenant_name']
        operation_id = job_input['operation_id']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        redundant_configuration_flg = job_input['redundant_configuration_flg']
        vdom_name = job_input.get('vdom_name', '')
        partition_id = job_input.get('partition_id', '')
        partition_name = job_input.get('partition_name', '')
        vsys_name = job_input.get('vsys_name', '')
        description = job_input.get('description', '')

        # set devise name
        if len(vdom_name) != 0:
            device_user_name = vdom_name
        elif len(partition_name) != 0:
            device_user_name = partition_name
        elif len(vsys_name) != 0:
            device_user_name = vsys_name
        else:
            device_user_name = partition_id

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['apl_type'] = self.job_config.APL_TYPE_PH
        params['type'] = nf_type
        params['device_type'] = device_type
        params['status'] = 0
        params['delete_flg'] = 0
        params['redundant_configuration_flg'] \
                                    = redundant_configuration_flg

        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        if len(apl_list) == 0:
            raise SystemError('physical server not exists.')

        # Update NAL_APL_MNG(DB Client)
        params = {}
        params['update_id'] = operation_id
        params['tenant_name'] = tenant_name
        params['device_user_name'] = device_user_name
        params['description'] = description
        params['task_status'] = 0
        params['err_info'] = ''
        params['status'] = 1
        keys = [apl_list[0]['ID']]
        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['ID'] = apl_list[0]['ID']
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        return apl_list[0]
