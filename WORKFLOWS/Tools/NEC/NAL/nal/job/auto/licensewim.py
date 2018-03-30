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

from job.auto import license
from job.lib.db import list
from job.lib.db import update


class LicenseWim(license.License):

    def license_assign_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Assign License(DB)
        job_input['license_type_detail'] = job_input['bandwidth']
        license_id_list = []
        license_id_list.append(self._assign_license(job_input))
        license_id_list.append(self._assign_license(job_input))

        # Set JOB Output Parameters
        job_output = {"license_list": license_id_list}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def license_withdraw_csr1000v(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        logical_delete_apl_list = job_input['data']['logical_delete_apl_list']

        for apl_data in logical_delete_apl_list:

            # Withdraw License(DB)
            self.__withdraw_license(job_input, apl_data['search']['node_id'])

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __withdraw_license(self, job_input, node_id):

        # Get JOB Input Parameters
        operation_id = job_input['data']['operation_id']

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
        params['delete_flg'] = 0
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
            params['update_id'] = operation_id
            db_update.set_context(db_endpoint_license, keys, params)
            db_update.execute()
