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
import uuid

from job.auto import base
from job.lib.db import create
from job.lib.db import list
from job.lib.db import update


class MemberWim(base.JobAutoBase):

    def dc_member_create_info_get(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        iaas_tenant_id = job_input['IaaS_tenant_id']
        operation_id = job_input['operation_id']
        dc_id = job_input['dc_id']
        group_type = job_input['group_type']
        group_name = job_input['group_name']
        tenant_name = job_input['tenant_name']

        # Get Endpoint(DB Client)
        db_endpoint_dc = self.get_db_endpoint(self.job_config.REST_URI_WIM_DC)
        db_endpoint_dc_group = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_GROUP)
        db_endpoint_dc_member = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_MEMBER)
        db_endpoint_dc_vlan = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_VLAN)
        db_endpoint_dc_segment = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_SEGMENT_MNG)

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # List WIM_DC_MNG(DB Client)
        params = {}
        params['dc_id'] = dc_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc, params)
        db_list_instance.execute()
        dc_mng_list = db_list_instance.get_return_param()

        if len(dc_mng_list) == 0:
            raise SystemError('dc info not exists.')

        # List WIM_DC_CONNECT_GROUP_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['group_type'] = group_type
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc_group, params)
        db_list_instance.execute()
        dc_group_list = db_list_instance.get_return_param()

        group_id = ''
        group_rec_id = ''

        if len(dc_group_list) == 0:

            # Generate Group Id
            group_id = str(uuid.uuid4())

            # Create WIM_DC_CONNECT_GROUP_MNG(DB Client)
            params = {}
            params['create_id'] = operation_id
            params['update_id'] = operation_id
            params['delete_flg'] = 0
            params['IaaS_tenant_id'] = iaas_tenant_id
            params['group_id'] = group_id
            params['group_type'] = group_type
            params['group_name'] = group_name
            params['tenant_name'] = tenant_name
            params['task_status'] = 0
            db_create_instance.set_context(db_endpoint_dc_group, params)
            db_create_instance.execute()

            # List WIM_DC_CONNECT_GROUP_MNG(DB Client)
            params = {}
            params['tenant_name'] = tenant_name
            params['group_type'] = group_type
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_dc_group, params)
            db_list_instance.execute()
            dc_group_list = db_list_instance.get_return_param()

            group_rec_id = dc_group_list[0]['ID']

        else:

            group_id = dc_group_list[0]['group_id']
            group_rec_id = dc_group_list[0]['ID']

            # Update WIM_DC_VLAN_MNG(DB Client)
            keys = [group_rec_id]
            params = {}
            params['task_status'] = 0
            params['update_id'] = operation_id
            db_update_instance.set_context(
                                db_endpoint_dc_group, keys, params)
            db_update_instance.execute()

        # List WIM_DC_CONNECT_MEMBER_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['group_id'] = group_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc_member, params)
        db_list_instance.execute()
        dc_member_list = db_list_instance.get_return_param()

        dc_vlan_id = None

        if job_input['group_type'] in [
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
            ]:

            # List WIM_DC_SEGMENT_MNG(DB Client)
            params = {}
            params['dc_id'] = dc_id
            params['group_id'] = group_id
            params['status'] = 1
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_dc_segment, params)
            db_list_instance.execute()
            dc_segment_list = db_list_instance.get_return_param()

            if len(dc_segment_list) == 0:

                # List WIM_DC_SEGMENT_MNG(DB Client)
                params = {}
                params['dc_id'] = dc_id
                params['status'] = 0
                params['delete_flg'] = 0
                db_list_instance.set_context(db_endpoint_dc_segment, params)
                db_list_instance.execute()
                dc_segment_list1 = db_list_instance.get_return_param()

                if len(dc_segment_list1) > 0:

                    # Update WIM_DC_SEGMENT_MNG(DB Client)
                    keys = [dc_segment_list1[0]['ID']]
                    params = {}
                    params['status'] = 1
                    params['group_id'] = group_id
                    params['update_id'] = operation_id
                    db_update_instance.set_context(
                                        db_endpoint_dc_segment, keys, params)
                    db_update_instance.execute()

                else:
                    # List WIM_DC_SEGMENT_MNG(DB Client)
                    params = {}
                    params['dc_id'] = dc_id
                    params['status'] = 2
                    params['delete_flg'] = 0
                    db_list_instance.set_context(
                                            db_endpoint_dc_segment, params)
                    db_list_instance.execute()
                    dc_segment_list2 = db_list_instance.get_return_param()

                    if len(dc_segment_list2) > 0:

                        # Update WIM_DC_SEGMENT_MNG(DB Client)
                        keys = [dc_segment_list2[0]['ID']]
                        params = {}
                        params['status'] = 1
                        params['group_id'] = group_id
                        params['update_id'] = operation_id
                        db_update_instance.set_context(
                                        db_endpoint_dc_segment, keys, params)
                        db_update_instance.execute()

                    else:
                        raise SystemError('dc segment not found.')

        else:
            # List WIM_DC_VLAN_MNG(DB Client)
            params = {}
            params['group_id'] = group_id
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_dc_vlan, params)
            db_list_instance.execute()
            dc_vlan_list = db_list_instance.get_return_param()

            if len(dc_vlan_list) > 0:
                dc_vlan_id = dc_vlan_list[0]['vlan_id']

            else:

                # List WIM_DC_VLAN_MNG(DB Client)
                params = {}
                params['status'] = 0
                params['delete_flg'] = 0
                db_list_instance.set_context(db_endpoint_dc_vlan, params)
                db_list_instance.execute()
                dc_vlan_list1 = db_list_instance.get_return_param()

                if len(dc_vlan_list1) > 0:

                    # Update WIM_DC_VLAN_MNG(DB Client)
                    keys = [dc_vlan_list1[0]['ID']]
                    params = {}
                    params['status'] = 1
                    params['group_id'] = group_id
                    params['update_id'] = operation_id
                    db_update_instance.set_context(
                                        db_endpoint_dc_vlan, keys, params)
                    db_update_instance.execute()

                    dc_vlan_id = dc_vlan_list1[0]['vlan_id']

                else:
                    # List WIM_DC_VLAN_MNG(DB Client)
                    params = {}
                    params['status'] = 2
                    params['delete_flg'] = 0
                    db_list_instance.set_context(db_endpoint_dc_vlan, params)
                    db_list_instance.execute()
                    dc_vlan_list2 = db_list_instance.get_return_param()

                    if len(dc_vlan_list2) > 0:

                        # Update WIM_DC_VLAN_MNG(DB Client)
                        keys = [dc_vlan_list2[0]['ID']]
                        params = {}
                        params['status'] = 1
                        params['group_id'] = group_id
                        params['update_id'] = operation_id
                        db_update_instance.set_context(
                                            db_endpoint_dc_vlan, keys, params)
                        db_update_instance.execute()

                        dc_vlan_id = dc_vlan_list2[0]['vlan_id']

                    else:
                        raise SystemError('vlanid not found.')

        # Get Config(wan_allocation_info)
        wan_allocation_info = self.get_wan_allocation_info(
                                    job_input['group_type'], dc_id)

        # Set JOB Output Parameters
        job_output = {
            'dc_name': dc_mng_list[0]['dc_name'],
            'group_id': group_id,
            'group_rec_id': group_rec_id,
            'dc_member_list': dc_member_list,
            'dc_vlan_id': dc_vlan_id,
            'wan_allocation_info': wan_allocation_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def dc_member_update_info_get(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        iaas_tenant_id = job_input['IaaS_tenant_id']
        group_type = job_input['group_type']
        tenant_name = job_input['tenant_name']
        dc_id = job_input['dc_id']
        operation_id = job_input['operation_id']

        # Get Endpoint(DB Client)
        db_endpoint_dc = self.get_db_endpoint(self.job_config.REST_URI_WIM_DC)
        db_endpoint_dc_group = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_GROUP)
        db_endpoint_dc_member = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_MEMBER)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # List WIM_DC_MNG(DB Client)
        params = {}
        params['dc_id'] = dc_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc, params)
        db_list_instance.execute()
        dc_mng_list = db_list_instance.get_return_param()

        if len(dc_mng_list) == 0:
            raise SystemError('dc info not exists.')

        # List WIM_DC_CONNECT_GROUP_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['group_type'] = group_type
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc_group, params)
        db_list_instance.execute()
        dc_group_list = db_list_instance.get_return_param()

        if len(dc_group_list) == 0:
            raise SystemError('dc groupe info not exists.')

        group_id = dc_group_list[0]['group_id']
        group_rec_id = dc_group_list[0]['ID']

        # Update WIM_DC_CONNECT_GROUP_MNG(DB Client)
        keys = [group_rec_id]
        params = {}
        params['task_status'] = 0
        params['update_id'] = operation_id
        db_update_instance.set_context(
                                    db_endpoint_dc_group, keys, params)
        db_update_instance.execute()

        # List WIM_DC_CONNECT_MEMBER_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['group_id'] = group_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc_member, params)
        db_list_instance.execute()
        dc_member_list = db_list_instance.get_return_param()

        if len(dc_member_list) == 0:
            raise SystemError('dc groupe info not exists.')

        # Get Config(wan_allocation_info)
        wan_allocation_info = self.get_wan_allocation_info(
                                    job_input['group_type'], dc_id)

        # Set JOB Output Parameters
        job_output = {
            'group_id': group_id,
            'group_rec_id': group_rec_id,
            'dc_member_list': dc_member_list,
            'wan_allocation_info': wan_allocation_info,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def dc_member_delete_info_get(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        dc_id = job_input['dc_id']
        group_type = job_input['group_type']

        iaas_tenant_id = job_input['IaaS_tenant_id']
        tenant_name = job_input['tenant_name']

        # Get Endpoint(DB Client)
        db_endpoint_dc_group = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_GROUP)
        db_endpoint_dc_member = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_MEMBER)
        db_endpoint_dc_vlan = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_VLAN)
        db_endpoint_dc_segment = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_SEGMENT_MNG)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)
        db_update_instance = update.UpdateClient(self.job_config)

        # List WIM_DC_CONNECT_GROUP_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['IaaS_tenant_id'] = iaas_tenant_id
        params['group_type'] = group_type
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc_group, params)
        db_list_instance.execute()
        dc_group_list = db_list_instance.get_return_param()

        if len(dc_group_list) == 0:
            raise SystemError('group not exists.')

        group_rec_id = dc_group_list[0]['ID']
        group_id = dc_group_list[0]['group_id']

        # Update WIM_DC_CONNECT_GROUP_MNG(DB Client)
        keys = [group_rec_id]
        params = {}
        params['task_status'] = 0
        params['update_id'] = job_input['operation_id']
        db_update_instance.set_context(
                                    db_endpoint_dc_group, keys, params)
        db_update_instance.execute()

        dc_segment_rec_id = ''
        dc_vlan_rec_id = ''

        if job_input['group_type'] in [
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
            ]:

            # List WIM_DC_SEGMENT_MNG(DB Client)
            params = {}
            params['dc_id'] = dc_id
            params['group_id'] = group_id
            params['status'] = 1
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_dc_segment, params)
            db_list_instance.execute()
            dc_segment_list = db_list_instance.get_return_param()

            if len(dc_segment_list) == 0:
                raise SystemError('dc segment not exists.')

            dc_segment_rec_id = dc_segment_list[0]['ID']

        else:

            # List WIM_DC_VLAN_MNG(DB Client)
            params = {}
            params['group_id'] = group_id
            params['status'] = 1
            params['delete_flg'] = 0
            db_list_instance.set_context(db_endpoint_dc_vlan, params)
            db_list_instance.execute()
            dc_vlan_list = db_list_instance.get_return_param()

            if len(dc_vlan_list) == 0:
                raise SystemError('dc vlan not exists.')

            dc_vlan_rec_id = dc_vlan_list[0]['ID']

        dc_member_myself_list = []
        dc_member_other_list = []

        # List WIM_DC_CONNECT_MEMBER_MNG(DB Client)
        params = {}
        params['tenant_name'] = tenant_name
        params['group_id'] = group_id
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint_dc_member, params)
        db_list_instance.execute()
        dc_member_list = db_list_instance.get_return_param()

        if len(dc_member_list) == 0:
            raise SystemError('dc member not exists.')

        else:
            if len(dc_member_list) == 1:
                if dc_member_list[0]['dc_id'] != dc_id:
                    raise SystemError('dc member not exists.')

            for dc_member in dc_member_list:

                dc_info = {}
                dc_info['rec_id'] = dc_member['ID']
                dc_info['dc_id'] = dc_member['dc_id']
                dc_info['pod_id'] = dc_member['pod_id']
                dc_info['ce1_info'] = json.loads(dc_member['ce1_info'])
                dc_info['ce2_info'] = json.loads(dc_member['ce2_info'])
                dc_info['ce1_address_v6'] = dc_member['ce1_address_v6']

                if dc_info['dc_id'] == dc_id:

                    dc_member_myself_list.append(dc_info)

                else:
                    dc_member_other_list.append(dc_info)

        if len(dc_member_myself_list) == 0:
            raise SystemError('dc member not exists.')

        # Set JOB Output Parameters
        job_output = {
            'group_rec_id': group_rec_id,
            'group_id': group_id,
            'dc_vlan_rec_id': dc_vlan_rec_id,
            'dc_member_count': len(dc_member_list),
            'dc_member_myself_list': dc_member_myself_list,
            'dc_member_other_list': dc_member_other_list,
            'dc_segment_rec_id': dc_segment_rec_id,
        }

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def dc_member_vlan_group_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name
        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        group_rec_id = job_input['group_rec_id']
        dc_vlan_rec_id = job_input['dc_vlan_rec_id']
        dc_segment_rec_id = job_input['dc_segment_rec_id']
        dc_member_other_count = len(job_input['dc_member_other_list'])
        dc_member_myself_list = job_input['dc_member_myself_list']

        # Get Endpoint(DB Client)
        db_endpoint_dc_group = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_GROUP)
        db_endpoint_dc_member = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_MEMBER)
        db_endpoint_dc_vlan = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_VLAN)
        db_endpoint_dc_segment = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_SEGMENT_MNG)

        # Create Instance(DB Client)
        db_update_instance = update.UpdateClient(self.job_config)

        for dc_member_myself in dc_member_myself_list:

            # Update WIM_DC_CONNECT_MEMBER_MNG(DB Client)
            keys = [dc_member_myself['rec_id']]
            params = {}
            params['update_id'] = operation_id
            params['delete_flg'] = 1
            db_update_instance.set_context(
                                        db_endpoint_dc_member, keys, params)
            db_update_instance.execute()

        if job_input['group_type'] in [
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
            ]:

            # Update WIM_DC_SEGMENT_MNG(DB Client)
            keys = [dc_segment_rec_id]
            params = {}
            params['update_id'] = operation_id
            params['status'] = 2
            params['group_id'] = ''
            db_update_instance.set_context(
                                    db_endpoint_dc_segment, keys, params)
            db_update_instance.execute()

        if dc_member_other_count == 0:

            if job_input['group_type'] in [
                    str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                    str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
                ]:

                pass

            else:

                # Update WIM_DC_VLAN_MNG(DB Client)
                keys = [dc_vlan_rec_id]
                params = {}
                params['update_id'] = operation_id
                params['status'] = 2
                params['group_id'] = ''
                db_update_instance.set_context(
                                        db_endpoint_dc_vlan, keys, params)
                db_update_instance.execute()

            # Update WIM_DC_CONNECT_GROUP_MNG(DB Client)
            keys = [group_rec_id]
            params = {}
            params['update_id'] = operation_id
            params['delete_flg'] = 1
            db_update_instance.set_context(
                                        db_endpoint_dc_group, keys, params)
            db_update_instance.execute()

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output
