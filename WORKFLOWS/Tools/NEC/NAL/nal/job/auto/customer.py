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
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import userws


class Customer(base.JobAutoBase):

    def msa_customer_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']

        # Get Endpoint(DB Client)
        db_endpoint_tenant = self.get_db_endpoint(
                                            self.job_config.REST_URI_TENANT)

        # Get MSA Common Config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)

        # List NAL_TENANT_MNG(DB Client)
        db_list = list.ListClient(self.job_config)
        params = {}
        params['tenant_name'] = tenant_name
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_tenant, params)
        db_list.execute()
        tenant_list = db_list.get_return_param()

        if len(tenant_list) == 0:
            raise SystemError('tenant not exists.')

        tenant_info_list = json.loads(tenant_list[0]['tenant_info'])

        msa_customer_id = ''
        msa_customer_name = ''

        tenant_info_idx = -1
        for idx in range(len(tenant_info_list)):

            pod_id_wk = tenant_info_list[idx]['pod_id']
            tenant_id_wk = tenant_info_list[idx]['id']

            if pod_id_wk == pod_id and tenant_id_wk == nal_tenant_id:
                msa_customer_id = tenant_info_list[idx]['msa_customer_id']
                msa_customer_name = tenant_info_list[idx]['msa_customer_name']
                tenant_info_idx = idx
                break

        if tenant_info_idx == -1:
            raise SystemError('tenant_info not exists.')

        if msa_customer_id == 0:

            msa_customer_name = \
                msa_config_for_common['msa_customer_name_prefix']\
                + str(tenant_list[0]['ID'])
            # Create Customer(MSA Client)
            user_ws = userws.UserWs(self.job_config,
                                    self.nal_endpoint_config,
                                    pod_id)
            ret_user_ws = user_ws.create_customer(msa_customer_name)

            msa_customer_id = self.get_msa_client_result(
                                    ret_user_ws[user_ws.RES_KEY_OUT], 'id')

            # Update NAL_TENANT_MNG(DB Client)
            tenant_info_list[tenant_info_idx]['msa_customer_id'] \
                                                    = msa_customer_id
            tenant_info_list[tenant_info_idx]['msa_customer_name'] \
                                                    = msa_customer_name

            db_update = update.UpdateClient(self.job_config)
            params = {}
            params['tenant_info'] = json.dumps(tenant_info_list)
            params['update_id'] = operation_id
            keys = [tenant_list[0]['ID']]
            db_update.set_context(db_endpoint_tenant, keys, params)
            db_update.execute()

        job_output = {
            'msa_customer_id': msa_customer_id
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output
