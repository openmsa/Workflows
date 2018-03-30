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


class TestVlanApi(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestVlanApi, self).setUp()

    def tearDown(self):
        """Clear the test environment"""
        super(TestVlanApi, self).tearDown()

        # Create Instance(DB Client)
        db_delete = delete.DeleteClient(config.JobConfig())
        db_list = list.ListClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_APL)
        db_endpoint_msa_vlan = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_port = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_PORT)
        db_endpoint_vlan = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_VLAN)

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

        # Delete from NAL_VIRTUAL_LAN_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']

        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        delete_list = db_list.get_return_param()

        for delete_res in delete_list:
            key = delete_res['ID']
            db_delete.set_context(db_endpoint_vlan, [key])
            db_delete.execute()

        # Delete from NAL_PORT_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        delete_list = db_list.get_return_param()

        for delete_res in delete_list:
            key = delete_res['ID']
            db_delete.set_context(db_endpoint_port, [key])
            db_delete.execute()

        # Delete from NAL_MSA_VLAN_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']

        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        delete_list = db_list.get_return_param()

        for delete_res in delete_list:
            key = delete_res['ID']
            db_delete.set_context(db_endpoint_msa_vlan, [key])
            db_delete.execute()

    def create_db_vlan(self, iaas_network_type):

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_vlan = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_VLAN)

        # Create NAL_VIRTUAL_LAN_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
        params['tenant_id'] = JOB_INPUT['tenant_id']
        params['node_id'] = JOB_INPUT['node_id']
        params['pod_id'] = JOB_INPUT['pod_id']
        params['network_id'] = JOB_INPUT['network_id']
        params['IaaS_network_id'] = JOB_INPUT['IaaS_network_id']
        params['IaaS_network_type'] = iaas_network_type
        params['IaaS_region_id'] = JOB_INPUT['IaaS_region_id']
        params['vlan_id'] = '2016'
        db_create.set_context(db_endpoint_vlan, params)
        db_create.execute()

    def create_db_msa_vlan(self):

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_MSA_VLAN)

        # Create NAL_MSA_VLAN_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['status'] = 0
        params['network_address'] = '10.20.0.0'
        params['netmask'] = '24'
        params['vlan_id'] = 'vlan_id_0000_1111_2222'
        params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
        params['pod_id'] = JOB_INPUT['pod_id']
        db_create.set_context(db_endpoint_msa_vlan, params)
        db_create.execute()

    def create_db_apl(self, apl_type, nf_type, device_type=1,
                                    redundant_configuration_flg=0):

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

        # List NAL_APL_MNG
        params = {}
        params['node_id'] = JOB_INPUT['node_id']
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        return apl_list[0]['ID']

    def test_virtual_fw_tenant_vlan_port_vxlan(self):

        self.create_db_msa_vlan()
        apl_rec_id = self.create_db_apl(1, 1)
        port_id = self.exec_virtual_fw_tenant_vlan_port_create(
                                                'VXLAN', apl_rec_id)
        self.exec_virtual_fw_tenant_vlan_port_delete(apl_rec_id,
                        port_id, JOB_INPUT['IaaS_network_id'])

    def test_virtual_fw_tenant_vlan_port_vlan(self):

        self.create_db_msa_vlan()
        apl_rec_id = self.create_db_apl(1, 1)
        self.exec_virtual_fw_tenant_vlan_port_create('VLAN', apl_rec_id)
        self.exec_virtual_fw_tenant_vlan_port_delete(apl_rec_id)

    def test_virtual_lb_tenant_vlan_port(self):

        self.create_db_vlan('VXLAN')
        self.create_db_msa_vlan()
        apl_rec_id = self.create_db_apl(1, 2)
        self.exec_virtual_lb_tenant_vlan_port_create('VXLAN', apl_rec_id)
        self.exec_virtual_lb_tenant_vlan_port_delete(apl_rec_id)

    def test_physical_fw_tenant_vlan_port(self):

        self.create_db_vlan('VXLAN')
        apl_rec_id = self.create_db_apl(2, 1)
        self.exec_physical_fw_tenant_vlan_port_create('VXLAN', apl_rec_id)
#         self.exec_physical_fw_tenant_vlan_port_delete()

    def test_physical_lb_tenant_vlan_port(self):

        self.create_db_vlan('VXLAN')
        apl_rec_id = self.create_db_apl(2, 2)
        self.exec_physical_lb_tenant_vlan_port_create('VXLAN', apl_rec_id)

    def test_physical_lb_tenant_vlan_port_redundant_configuration_flg1(self):

        self.create_db_vlan('VXLAN')
        apl_rec_id = self.create_db_apl(2, 2, 1, 1)
        self.exec_physical_lb_tenant_vlan_port_create('VXLAN', apl_rec_id, 1)

    def exec_virtual_fw_tenant_vlan_port_create(self,
                                            iaas_network_type, apl_rec_id):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
            'IaaS_network_id': JOB_INPUT['IaaS_network_id'],
            'IaaS_network_type': iaas_network_type,
            'IaaS_subnet_id': JOB_INPUT['IaaS_subnet_id'],
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'IaaS_segmentation_id': JOB_INPUT['IaaS_segmentation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'network_name': JOB_INPUT['network_name'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'apl_table_rec_id': apl_rec_id,
        }

        res = method.JobAutoMethod()\
                        .virtual_fw_tenant_vlan_port_create(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        return res['port_id4']

    def exec_virtual_fw_tenant_vlan_port_delete(self, apl_rec_id,
                            port_id='', iaas_network_id=''):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
            'IaaS_network_id': iaas_network_id,
            'IaaS_subnet_id': JOB_INPUT['IaaS_subnet_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': '',
            'pod_id': JOB_INPUT['pod_id'],
            'port_id': port_id,
            'apl_type': 1,
            'apl_table_rec_id': apl_rec_id,
        }

        res = method.JobAutoMethod()\
                        .virtual_fw_tenant_vlan_port_delete(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)

    def exec_virtual_lb_tenant_vlan_port_create(self,
                                        iaas_network_type, apl_rec_id):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
            'IaaS_network_id': JOB_INPUT['IaaS_network_id'],
            'IaaS_network_type': iaas_network_type,
            'IaaS_subnet_id': JOB_INPUT['IaaS_subnet_id'],
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'IaaS_segmentation_id': JOB_INPUT['IaaS_segmentation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'network_name': JOB_INPUT['network_name'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'apl_table_rec_id': apl_rec_id,
        }

        res = method.JobAutoMethod()\
                        .virtual_lb_tenant_vlan_port_create(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_virtual_lb_tenant_vlan_port_delete(self, apl_rec_id,
                                    port_id='', iaas_network_id=''):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
            'IaaS_network_id': iaas_network_id,
            'IaaS_subnet_id': JOB_INPUT['IaaS_subnet_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': '',
            'pod_id': JOB_INPUT['pod_id'],
            'port_id': port_id,
            'apl_type': 1,
            'apl_table_rec_id': apl_rec_id,
        }

        res = method.JobAutoMethod()\
                        .virtual_lb_tenant_vlan_port_delete(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)

    def exec_physical_fw_tenant_vlan_port_create(self,
                                        iaas_network_type, apl_rec_id):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
            'IaaS_network_id': JOB_INPUT['IaaS_network_id'],
            'IaaS_network_type': iaas_network_type,
            'IaaS_subnet_id': JOB_INPUT['IaaS_subnet_id'],
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'IaaS_segmentation_id': JOB_INPUT['IaaS_segmentation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'network_name': JOB_INPUT['network_name'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'apl_type': 2,
            'type': 1,
            'device_type': 1,
            'apl_table_rec_id': apl_rec_id,
        }

        res = method.JobAutoMethod()\
                        .physical_fw_tenant_vlan_port_create(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_physical_fw_tenant_vlan_port_delete(self,
                                    port_id='', iaas_network_id=''):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
            'IaaS_network_id': iaas_network_id,
            'IaaS_subnet_id': JOB_INPUT['IaaS_subnet_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': '',
            'pod_id': JOB_INPUT['pod_id'],
            'port_id': port_id,
            'apl_type': 1,
        }

        res = method.JobAutoMethod()\
                        .physical_fw_tenant_vlan_port_delete(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)

    def exec_physical_lb_tenant_vlan_port_create(self,
                                        iaas_network_type, apl_rec_id,
                                        redundant_configuration_flg=0):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'IaaS_tenant_id': JOB_INPUT['IaaS_tenant_id'],
            'IaaS_network_id': JOB_INPUT['IaaS_network_id'],
            'IaaS_network_type': iaas_network_type,
            'IaaS_subnet_id': JOB_INPUT['IaaS_subnet_id'],
            'IaaS_region_id': JOB_INPUT['IaaS_region_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'network_name': JOB_INPUT['network_name'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'apl_type': 2,
            'type': 2,
            'device_type': 1,
            'apl_table_rec_id': apl_rec_id,
            'redundant_configuration_flg': redundant_configuration_flg,
        }

        res = method.JobAutoMethod()\
                        .physical_lb_tenant_vlan_port_create(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
