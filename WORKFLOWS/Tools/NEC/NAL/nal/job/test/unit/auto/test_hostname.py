import random
import os
import string
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')
from job.auto import base
from job.auto import method
from job.conf import config
from job.lib.db import create
from job.lib.db import delete
from job.lib.db import list

JOB_INPUT = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'pod_id': 'pod_unit_test1',
    'node_name': 'node_name_unit_test',
}


class TestHostnameAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestHostnameAPI, self).setUp()

    def tearDown(self):
        """Clear the test environment"""
        super(TestHostnameAPI, self).tearDown()

        # Create Instance(DB Client)
        db_delete = delete.DeleteClient(config.JobConfig())
        db_list = list.ListClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_APL)

        # Delete from NAL_APL_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']

        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        delete_apl_list = db_list.get_return_param()

        for delete_apl in delete_apl_list:
            key = delete_apl['ID']
            db_delete.set_context(db_endpoint_apl, [key])
            db_delete.execute()

    def create_db_apl(self, node_name):

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())
        db_list = list.ListClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_APL)

        node_id = ''.join([random.choice(
            string.digits + string.ascii_letters) for i in range(10)])

        # Create
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['node_id'] = node_id
        params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
        params['pod_id'] = JOB_INPUT['pod_id']
        params['tenant_id'] = JOB_INPUT['IaaS_tenant_id']
        params['apl_type'] = 1
        params['device_type'] = 1
        params['task_status'] = 0
        params['node_name'] = node_name
        db_create.set_context(db_endpoint_apl, params)
        db_create.execute()

        # List
        params = {}
        params['node_id'] = node_id
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        return apl_list[0]['ID']

    def test_hostname_check(self):

        apl_rec_id = self.create_db_apl(JOB_INPUT['node_name'])

        job_input = {
            'host_name': JOB_INPUT['node_name'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'apl_table_rec_id': apl_rec_id,
        }

        self.exec_hostname_check(job_input)

    def test_hostname_check_not_found(self):

        apl_rec_id = self.create_db_apl(JOB_INPUT['node_name'])

        job_input = {
            'host_name': JOB_INPUT['node_name'] + 'nf',
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'apl_table_rec_id': apl_rec_id,
        }

        self.exec_hostname_check(job_input)

    def test_hostname_check_duplicated(self):

        self.create_db_apl(JOB_INPUT['node_name'])
        apl_rec_id = self.create_db_apl(JOB_INPUT['node_name'])

        job_input = {
            'host_name': JOB_INPUT['node_name'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'apl_table_rec_id': apl_rec_id,
        }

        try:
            self.exec_hostname_check(job_input)

        except SystemError as e:
            if e.args[0] != 'host_name duplicated:' + JOB_INPUT['node_name']:
                raise

    def exec_hostname_check(self, job_input):

        res = method.JobAutoMethod().hostname_check(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)
