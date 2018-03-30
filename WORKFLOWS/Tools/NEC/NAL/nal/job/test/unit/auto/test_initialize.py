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


class TestInitializeAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestInitializeAPI, self).setUp()

    def tearDown(self):
        """Clear the test environment"""
        super(TestInitializeAPI, self).tearDown()

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

    def create_db_apl(self, apl_type,
        nf_type=1, device_type=1, redundant_configuration_flg=1):

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

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
        params['apl_type'] = apl_type
        params['type'] = nf_type
        params['device_type'] = device_type
        params['task_status'] = 0

        params['actsby_flag_master'] = 'act'
        params['device_name_master'] = 'wn0fwxtf01'
        params['device_detail_master'] = '{}'
        params['master_ip_address'] = '100.99.0.5'
        params['redundant_configuration_flg'] = redundant_configuration_flg
        params['MSA_device_id'] = ''
        params['status'] = 0
        params['nic_MSA'] = 'mport'
        params['nic_public'] = 'pport'
        params['nic_external'] = 'eport'
        params['nic_tenant'] = 'tport'

        db_create.set_context(db_endpoint_apl, params)
        db_create.execute()

        return node_id

    def test_initialize_create_vnf(self):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 1,
            'type': 1,
            'device_type': 1,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'host_name': JOB_INPUT['node_name'],
        }

        self.exec_initialize_create_vnf(job_input)

    def test_initialize_update_vnf(self):

        node_id = self.create_db_apl(1)

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'node_id': node_id,
        }

        self.exec_initialize_update_vnf(job_input)

    def test_initialize_update_vnf_not_found(self):

        node_id = self.create_db_apl(1)

        job_input = {
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'node_id': node_id + 'nf',
        }

        try:
            self.exec_initialize_update_vnf(job_input)

        except SystemError as e:
            if e.args[0] != 'server not exists.':
                raise

    def test_initialize_create_pnf_fw_fortigate(self):

        self.create_db_apl(2)

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'type': 1,
            'device_type': 1,
            'redundant_configuration_flg': 1,
            'vdom_name': 'vdom123',
        }

        self.exec_initialize_create_pnf(job_input)

    def test_initialize_create_pnf_fw_paloalto(self):

        self.create_db_apl(2, 1, 2)

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'type': 1,
            'device_type': 2,
            'redundant_configuration_flg': 1,
            'vsys_name': 'vsys123',
        }

        self.exec_initialize_create_pnf(job_input)

    def test_initialize_create_pnf_fw_fortigate_share(self):

        self.create_db_apl(2, 1, 3)

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'type': 1,
            'device_type': 3,
            'redundant_configuration_flg': 1,
            'vdom_name': 'vdom123',
        }

        self.exec_initialize_create_pnf(job_input)

    def test_initialize_create_pnf_lb_bigip(self):

        self.create_db_apl(2, 2, 1, 0)

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'type': 2,
            'device_type': 1,
            'redundant_configuration_flg': 0,
            'partition_id': 'partition_id123',
            'route_domain_id': 'route_domain_id123',
        }

        self.exec_initialize_create_pnf(job_input)

    def test_initialize_create_pnf_lb_thunder(self):

        self.create_db_apl(2, 2, 2)

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'type': 2,
            'device_type': 2,
            'redundant_configuration_flg': 1,
            'partition_name': 'partition_name123',
        }

        self.exec_initialize_create_pnf(job_input)

    def test_initialize_create_pnf_lb_bigip_share(self):

        self.create_db_apl(2, 2, 3, 0)

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'type': 2,
            'device_type': 3,
            'redundant_configuration_flg': 0,
            'partition_id': 'partition_id123',
            'route_domain_id': 'route_domain_id123',
        }

        self.exec_initialize_create_pnf(job_input)

    def test_initialize_create_pnf_lb_thunder_share(self):

        self.create_db_apl(2, 2, 4)

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'type': 2,
            'device_type': 4,
            'redundant_configuration_flg': 1,
            'partition_name': 'partition_name123',
        }

        self.exec_initialize_create_pnf(job_input)

    def test_initialize_create_pnf_not_found(self):

        self.create_db_apl(2)

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'type': 1,
            'device_type': 3,
            'redundant_configuration_flg': 1,
            'vdom_name': 'vdom123',
        }

        try:
            self.exec_initialize_create_pnf(job_input)

        except SystemError as e:
            if e.args[0] != 'physical server not exists.':
                raise

    def exec_initialize_create_vnf(self, job_input):

        res = method.JobAutoMethod().initialize_create_vnf(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_initialize_update_vnf(self, job_input):

        res = method.JobAutoMethod().initialize_update_vnf(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_initialize_create_pnf(self, job_input):

        res = method.JobAutoMethod().initialize_create_pnf(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
