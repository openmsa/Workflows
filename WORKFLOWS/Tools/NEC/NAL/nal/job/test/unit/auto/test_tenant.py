import json
import os
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
    'IaaS_region_id': 'region_unit_test1',
    'pod_id': 'pod_unit_test1'
}


class TestTenatAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestTenatAPI, self).setUp()

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_tenant = base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_TENANT)

        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
        params['IaaS_region_id'] = JOB_INPUT['IaaS_region_id']
        params['IaaS_tenant_id'] = JOB_INPUT['IaaS_tenant_id']
        tenant_info = [
            {
                "description": "",
                "enabled": True,
                "id": "ef5d2e187b9636f9a4811318069137a6",
                "msa_customer_id": 0,
                "msa_customer_name": "",
                "name": JOB_INPUT['IaaS_tenant_name'],
                "pod_id": JOB_INPUT['pod_id']
            }
        ]
        params['tenant_info'] = json.dumps(tenant_info)
        db_create.set_context(db_endpoint_tenant, params)
        db_create.execute()

    def tearDown(self):
        """Clear the test environment"""
        super(TestTenatAPI, self).tearDown()

        # Create Instance(DB Client)
        db_delete = delete.DeleteClient(config.JobConfig())
        db_list = list.ListClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_tenant = base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_TENANT)

        # Delete from NAL_TENANT_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']

        db_list.set_context(db_endpoint_tenant, params)
        db_list.execute()
        delete_pod_list = db_list.get_return_param()

        for delete_pod in delete_pod_list:
            key = delete_pod['ID']
            db_delete.set_context(db_endpoint_tenant, [key])
            db_delete.execute()

    def test_get_nal_tenant_name(self):

        job_input = {
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
        }

        self.exec_get_nal_tenant_name(job_input)

    def test_get_nal_tenant_name_not_found(self):

        job_input = {
            'IaaS_region_id': 'IaaS_region_id_002',
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
        }

        try:
            self.exec_get_nal_tenant_name(job_input)

        except SystemError as e:
            if e.args[0] != 'tenant not exists.':
                raise

    def test_tenant_id_convert_get(self):

        job_input = {
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
        }

        self.exec_tenant_id_convert(job_input)

    def test_tenant_id_convert_create(self):

        job_input = {
            'IaaS_region_id': 'IaaS_region_id_002',
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
            'operation_id': JOB_INPUT['operation_id'],
        }

        self.exec_tenant_id_convert(job_input)

    def test_get_pod_tenant(self):

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'pod_id': JOB_INPUT['pod_id'],
        }

        self.exec_get_pod_tenant(job_input)

    def test_get_pod_tenant_not_found_tenant(self):

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'] + 'nf',
            'pod_id': JOB_INPUT['pod_id'],
        }

        try:
            self.exec_get_pod_tenant(job_input)

        except SystemError as e:
            if e.args[0] != 'tenant not exists in pod':
                raise

    def test_get_pod_tenant_not_found_pod(self):

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'pod_id': 'pod_unit_test3',
        }

        try:
            self.exec_get_pod_tenant(job_input)

        except SystemError as e:
            if e.args[0] != 'tenant not exists in pod':
                raise

    def test_get_or_create_pod_tenant_get(self):

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'operation_id': JOB_INPUT['operation_id'],
        }

        self.exec_get_or_create_pod_tenant(job_input)

    def test_get_or_create_pod_tenant_create(self):

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'pod_id': 'pod_unit_test3',
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_tenant_name': JOB_INPUT['IaaS_tenant_name'],
        }

        self.exec_get_or_create_pod_tenant(job_input)

    def test_get_or_create_pod_tenant_create_not_found_tenant(self):

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'] + 'nf',
            'pod_id': JOB_INPUT['pod_id'],
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_tenant_name': JOB_INPUT['IaaS_tenant_name'],
        }

        try:
            self.exec_get_or_create_pod_tenant(job_input)

        except SystemError as e:
            if e.args[0] != 'tenant not exists.':
                raise

    def exec_get_nal_tenant_name(self, job_input):

        res = method.JobAutoMethod().get_nal_tenant_name(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_tenant_id_convert(self, job_input):

        res = method.JobAutoMethod().tenant_id_convert(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_get_pod_tenant(self, job_input):

        res = method.JobAutoMethod().get_pod_tenant(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_get_or_create_pod_tenant(self, job_input):

        res = method.JobAutoMethod().get_or_create_pod_tenant(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
