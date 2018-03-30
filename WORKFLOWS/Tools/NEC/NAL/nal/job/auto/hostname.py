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


class Hostname(base.JobAutoBase):

    def hostname_check(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        host_name = job_input['host_name']
        nal_tenant_name = job_input['tenant_name']
        apl_table_rec_id = job_input['apl_table_rec_id']

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(
                                            self.job_config.REST_URI_APL)

        # List NAL_VNF_MNG(DB Client)
        db_list = list.ListClient(self.job_config)
        params = {}
        params['tenant_name'] = nal_tenant_name
        params['node_name'] = host_name
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        tenant_list = db_list.get_return_param()

        host_check_flg = 0
        for tenant_data in tenant_list:
            if tenant_data['ID'] != apl_table_rec_id:
                host_check_flg = 1
                break

        if host_check_flg == 1:
            raise SystemError('host_name duplicated:' + host_name)

        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output
