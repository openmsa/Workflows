import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')
from job.auto import base
from job.conf import config
from job.auto import method
from job.auto.extension import routingpod
from job.lib.db import create
from job.lib.db import delete
from job.lib.db import list
from pprint import pprint

JOB_INPUT = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'IaaS_port_id': 'port_unit_test1',
    'IaaS_segmentation_id': '10',
    'tenant_id': 'tenant_unit_test1',
    'node_id': 'node_unit_test1',
    'pod_id': 'pod_unit_test1',
    'port_id': 'port11',
    'network_id': '61872574-5c66-418a-9e68-3d01f7e42824',
    'network_name': 'network_name123',
}


class TestRoutingPodAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestRoutingPodAPI, self).setUp()

    def tearDown(self):
        """Clear the test environment"""
        super(TestRoutingPodAPI, self).tearDown()

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
        delete_list = db_list.get_return_param()

        for delete_res in delete_list:
            key = delete_res['ID']
            db_delete.set_context(db_endpoint_apl, [key])
            db_delete.execute()

    def create_db_apl(self, nf_type, device_type=1):

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())
        db_list = list.ListClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_APL)

        # Create
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['node_id'] = JOB_INPUT['node_id']
        params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
        params['pod_id'] = JOB_INPUT['pod_id']
        params['tenant_id'] = JOB_INPUT['IaaS_tenant_id']
        params['apl_type'] = 1
        params['type'] = nf_type
        params['device_type'] = device_type
        params['task_status'] = 0

        params['actsby_flag_master'] = 'act'
        params['device_name_master'] = 'wn0fwxtf01'
        params['device_detail_master'] = '{}'
        params['master_ip_address'] = '100.99.0.5'
        params['redundant_configuration_flg'] = 0
        params['MSA_device_id'] = ''
        params['status'] = 0
        params['nic_MSA'] = 'mport'
        params['nic_public'] = 'pport'
        params['nic_external'] = 'eport'
        params['nic_tenant'] = 'tport'

        db_create.set_context(db_endpoint_apl, params)
        db_create.execute()

        # List NAL_APL_MNG
        params = {}
        params['node_id'] = JOB_INPUT['node_id']
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        return apl_list[0]['ID']

    def test_routing_pod_type1_device_type1(self):

        rec_id = self.create_db_apl(1, 1)
        self.exec_routing_pod(1, 1, rec_id)

    def test_routing_pod_type1_device_type2(self):

        rec_id = self.create_db_apl(1, 2)
        self.exec_routing_pod(1, 2, rec_id)

    def test_routing_pod_type1_device_type3(self):

        rec_id = self.create_db_apl(1, 3)
        self.exec_routing_pod(1, 3, rec_id)

    def test_routing_pod_type1_device_type4(self):

        rec_id = self.create_db_apl(1, 4)
        self.exec_routing_pod(1, 4, rec_id)

    def test_routing_pod_type1_device_type5(self):

        rec_id = self.create_db_apl(1, 5)
        self.exec_routing_pod(1, 5, rec_id)

    def test_routing_pod_type2_device_type1(self):

        rec_id = self.create_db_apl(2, 1)
        self.exec_routing_pod(2, 1, rec_id)

    def test_routing_pod_type2_device_type2(self):

        rec_id = self.create_db_apl(2, 2)
        self.exec_routing_pod(2, 2, rec_id)

    def test_routing_pod_type2_device_type3(self):

        rec_id = self.create_db_apl(2, 3)
        self.exec_routing_pod(2, 3, rec_id)

    def test_routing_pod_type3_device_type1(self):

        self.exec_routing_pod(3, 1)

    def test_routing_pod_type3_device_type2(self):

        self.exec_routing_pod(3, 2)

    def test_routing_pod_not_found(self):

        try:
            self.exec_routing_pod(4, 1)

        except SystemError as e:
            if e.args[0] != 'pods not exists.':
                raise

    def test_routing_vxlangw_pod(self):

        self.exec_routing_vxlangw_pod(JOB_INPUT['IaaS_region_id'])

    def test_routing_vxlangw_pod_not_found(self):

        try:
            self.exec_routing_vxlangw_pod('region_not_exists')

        except SystemError as e:
            if e.args[0] != 'vxlangw_pods not exists.':
                raise

    def exec_routing_pod(self, h_type, device_type, apl_rec_id=None):

        job_input = {
            'type': h_type,
            'device_type': device_type,
            'operation_id': JOB_INPUT['operation_id'],
        }

        if apl_rec_id is not None:
            job_input['apl_table_rec_id'] = apl_rec_id

        res = method.JobAutoMethod().routing_pod(job_input)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_routing_vxlangw_pod(self, iaas_tenant_id):

        job_input = {
            'IaaS_region_id': iaas_tenant_id,
        }

        res = routingpod.RoutingPod().routing_vxlangw_pod(job_input)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
