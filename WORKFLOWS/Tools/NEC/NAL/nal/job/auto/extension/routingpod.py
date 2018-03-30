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
from job.auto import base
from job.lib.db import list
from job.lib.db import update


class RoutingPod(base.JobAutoBase):

    def routing_pod(self, job_input):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        apl_table_rec_id = job_input.get('apl_table_rec_id', '')
        hard_type = job_input.get('type', '')
        device_type = job_input.get('device_type', '')

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(
                                    self.job_config.REST_URI_POD)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # List NAL_POD_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint, params)
        db_list_instance.execute()
        pod_list = db_list_instance.get_return_param()

        # Assing Pod
        if str(hard_type) == '1' and str(device_type) in ['1', '2', '3', '4']:
            usetype = ['1', '3']
            ops_version = ['1', ]
        elif str(hard_type) == '1' and str(device_type) in ['5', ]:
            usetype = ['1', '3']
            ops_version = ['1', ]
        elif str(hard_type) == '2' and str(device_type) in [
                                                        '1', '2', '3', '4']:
            usetype = ['1', '3']
            ops_version = ['1', ]
        elif str(hard_type) == '3':
            usetype = ['1', '2', '3', ]
            ops_version = ['1', ]
        else:
            usetype = []
            ops_version = []

        assing_podlist = []
        for pod_wk in pod_list:
            if str(pod_wk['use_type']) in usetype \
                     and str(pod_wk['ops_version']) in ops_version:
                assing_podlist.append(pod_wk)

        weight = 0
        assing_pod = {}
        for pod_wk in assing_podlist:
            if int(pod_wk['weight']) > weight:
                weight = int(pod_wk['weight'])
                assing_pod = pod_wk

        # Check
        if len(assing_pod.get('pod_id', '')) == 0:
            raise SystemError('pods not exists.')

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
            params['pod_id'] = assing_pod['pod_id']

            db_update_instance.set_context(db_endpoint_apl, keys, params)
            db_update_instance.execute()

        # Get JOB Output Parameters
        job_output = {
            'pod_id': assing_pod['pod_id'],
        }

        return job_output

    def routing_vxlangw_pod(self, job_input):

        # Get JOB Input Parameters
        iaas_region_id = job_input.get('IaaS_region_id', '')

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(
                                    self.job_config.REST_URI_VXLANGW_POD)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # List NAL_POD_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['IaaS_region_id'] = iaas_region_id
        db_list_instance.set_context(db_endpoint, params)
        db_list_instance.execute()
        pod_list = db_list_instance.get_return_param()

        # Assing Pod
        weight = 0
        assing_pod = {}
        for pod_wk in pod_list:
            if int(pod_wk['weight']) > weight:
                weight = int(pod_wk['weight'])
                assing_pod = pod_wk

        # Check
        if len(assing_pod.get('vxlangw_pod_id', '')) == 0:
            raise SystemError('vxlangw_pods not exists.')

        return assing_pod['vxlangw_pod_id']
