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
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'IaaS_port_id': 'port_unit_test1',
    'tenant_id': 'tenant_unit_test1',
    'node_id': 'node_unit_test1',
    'pod_id': 'pod_unit_test1',
    'port_id': 'port11',
    'network_id': '094049539a7ba2548268d74cd5874ebc',
    'partition_id': 'partition_id123',
    'route_domain_id': 'route_domain_id123',
    'mng_user_account_id': 'mng_user_account_id123',
    'mng_account_password': 'mng_account_password123',
    'certificate_user_account_id': 'certificate_user_account_id123',
    'certificate_account_password': 'certificate_account_password123',
    'fw_ip_address': '10.58.10.1',
}


class TestSetupDeviceBigIpApi(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestSetupDeviceBigIpApi, self).setUp()

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_vlan = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_VLAN)
        db_endpoint_port = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_PORT)

        # Create NAL_VLAN_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
        params['tenant_id'] = JOB_INPUT['tenant_id']
        params['pod_id'] = JOB_INPUT['pod_id']
        params['network_id'] = JOB_INPUT['network_id']
        params['IaaS_network_id'] = JOB_INPUT['IaaS_network_id']
        params['IaaS_network_type'] = 'VLAN'
        params['IaaS_region_id'] = JOB_INPUT['IaaS_region_id']
        params['vlan_id'] = '2016'
        db_create.set_context(db_endpoint_vlan, params)
        db_create.execute()

        # Create NAL_PORT_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
        params['tenant_id'] = JOB_INPUT['tenant_id']
        params['node_id'] = JOB_INPUT['node_id']
        params['pod_id'] = JOB_INPUT['pod_id']
        params['port_id'] = JOB_INPUT['port_id']
        params['network_id'] = JOB_INPUT['network_id']
        params['apl_type'] = 1
        params['network_type'] = 1
        params['network_type_detail'] = 1
        params['ip_address'] = '10.0.0.1'
        params['netmask'] = 16
        params['IaaS_region_id'] = JOB_INPUT['IaaS_region_id']
        params['IaaS_tenant_id'] = JOB_INPUT['IaaS_tenant_id']
        params['IaaS_network_id'] = JOB_INPUT['IaaS_network_id']
        params['IaaS_port_id'] = JOB_INPUT['IaaS_port_id']
        params['port_info'] = json.dumps({
                'IaaS_port_info': {
                    'vip': {'ip_address': '10.0.0.1', 'netmask': 16},
                    'act': {'ip_address': '10.0.0.2', 'netmask': 24},
                    'sby': {'ip_address': '10.0.0.3', 'netmask': 25},
                },
            })
        params['msa_info'] = '{}'
        db_create.set_context(db_endpoint_port, params)
        db_create.execute()

    def tearDown(self):
        """Clear the test environment"""
        super(TestSetupDeviceBigIpApi, self).tearDown()

        # Create Instance(DB Client)
        db_delete = delete.DeleteClient(config.JobConfig())
        db_list = list.ListClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_APL)
        db_endpoint_port = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_PORT)

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

    def create_db_apl(self, redundant_configuration_flg=0):

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

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
        params['tenant_id'] = JOB_INPUT['tenant_id']
        params['apl_type'] = 2
        params['type'] = 2
        params['device_type'] = 1
        params['task_status'] = 0
        params['actsby_flag_master'] = 'act'
        params['device_name_master'] = 'wn0fwxtf01'
        params['device_detail_master'] = '{}'
        params['device_detail_slave'] = '{}'
        params['master_ip_address'] = '100.99.0.5'
        params['redundant_configuration_flg'] = redundant_configuration_flg
        params['MSA_device_id'] = ''
        params['status'] = 0
        params['nic_MSA'] = 'mport'
        params['nic_public'] = 'pport'
        params['nic_external'] = 'eport'
        params['nic_tenant'] = 'tport'
        params['device_user_name'] = json.dumps({
                        'partition_id': JOB_INPUT['partition_id'],
                        'route_domain_id': JOB_INPUT['route_domain_id'],
                        })
        db_create.set_context(db_endpoint_apl, params)
        db_create.execute()

        params['actsby_flag_master'] = 'sby'
        db_create.set_context(db_endpoint_apl, params)
        db_create.execute()

    def test_device_setup_bigip_redundant_configuration_flg0(self):

        self.create_db_apl()
        self.exec_device_setup_create_for_bigip(0)
        self.exec_device_setup_delete_for_bigip(0)

    def test_device_setup_bigip_redundant_configuration_flg1(self):

        self.create_db_apl(1)
        self.exec_device_setup_create_for_bigip(1)
        self.exec_device_setup_delete_for_bigip(1)

    def exec_device_setup_create_for_bigip(self,
                                    redundant_configuration_flg):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 2,
            'type': 2,
            'device_type': 1,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id4': JOB_INPUT['port_id'],
            'partition_id': JOB_INPUT['partition_id'],
            'route_domain_id': JOB_INPUT['route_domain_id'],
            'mng_user_account_id': JOB_INPUT['mng_user_account_id'],
            'mng_account_password': JOB_INPUT['mng_account_password'],
            'certificate_user_account_id': \
                        JOB_INPUT['certificate_user_account_id'],
            'certificate_account_password': \
                        JOB_INPUT['certificate_account_password'],
            'redundant_configuration_flg': \
                        redundant_configuration_flg,
            'fw_ip_address': JOB_INPUT['fw_ip_address'],
        }

        res = method.JobAutoMethod().device_setup_create_for_bigip(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)

    def exec_device_setup_delete_for_bigip(self,
                                    redundant_configuration_flg,
                                    job_cleaning_mode='0'):

        job_input = {
            'job_cleaning_mode': job_cleaning_mode,
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 2,
            'type': 2,
            'device_type': 1,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id4': JOB_INPUT['port_id'],
            'redundant_configuration_flg': \
                        redundant_configuration_flg,
        }

        res = method.JobAutoMethod().device_setup_delete_for_bigip(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)
