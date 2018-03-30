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
    'pod_id': 'pod_unit_test1',
    'nal_tenant_id': 'ef5d2e187b9636f9a4811318069137a6'
}


class TestCustomerAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestCustomerAPI, self).setUp()

    def tearDown(self):
        """Clear the test environment"""
        super(TestCustomerAPI, self).tearDown()

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
        tenant_list = db_list.get_return_param()

        for tenant_res in tenant_list:
            key = tenant_res['ID']
            db_delete.set_context(db_endpoint_tenant, [key])
            db_delete.execute()

    def create_db_tenant(self, msa_customer_id=0):

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_tenant = base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_TENANT)

        # Create
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
                "id": JOB_INPUT['nal_tenant_id'],
                "msa_customer_id": msa_customer_id,
                "msa_customer_name": "",
                "name": JOB_INPUT['IaaS_tenant_name'],
                "pod_id": JOB_INPUT['pod_id']
            }
        ]
        params['tenant_info'] = json.dumps(tenant_info)
        db_create.set_context(db_endpoint_tenant, params)
        db_create.execute()

    def test_msa_customer_create(self):

        self.create_db_tenant()

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'operation_id': JOB_INPUT['operation_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'nal_tenant_id': JOB_INPUT['nal_tenant_id'],
        }

        self.exec_msa_customer_create(job_input)

    def test_msa_customer_create_msa_exists(self):

        self.create_db_tenant('10')

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'operation_id': JOB_INPUT['operation_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'nal_tenant_id': JOB_INPUT['nal_tenant_id'],
        }

        self.exec_msa_customer_create(job_input)

    def test_msa_customer_create_not_found_tenant(self):

        self.create_db_tenant()

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'] + 'nf',
            'operation_id': JOB_INPUT['operation_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'nal_tenant_id': JOB_INPUT['nal_tenant_id'],
        }

        try:
            self.exec_msa_customer_create(job_input)

        except SystemError as e:
            if e.args[0] != 'tenant not exists.':
                raise

    def test_msa_customer_create_not_found_tenant_info(self):

        self.create_db_tenant()

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'operation_id': JOB_INPUT['operation_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'nal_tenant_id': JOB_INPUT['nal_tenant_id'] + 'nf',
        }

        try:
            self.exec_msa_customer_create(job_input)

        except SystemError as e:
            if e.args[0] != 'tenant_info not exists.':
                raise

    def exec_msa_customer_create(self, job_input):

        res = method.JobAutoMethod().msa_customer_create(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
