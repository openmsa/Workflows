import datetime
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
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'IaaS_port_id': 'port_unit_test1',
    'tenant_id': 'tenant_unit_test1',
    'pod_id': 'pod_unit_test1',
    'node_id': 'node_unit_test1',
}


class TestLicenseAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestLicenseAPI, self).setUp()

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_port = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_PORT)

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

        # Create NAL_PORT_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
        params['tenant_id'] = JOB_INPUT['tenant_id']
        params['pod_id'] = JOB_INPUT['pod_id']
        params['port_id'] = 'port11'
        params['apl_type'] = 1
        params['network_type'] = 1
        params['network_type_detail'] = 1
        params['ip_address'] = '10.0.0.1'
        params['netmask'] = 16
        params['IaaS_region_id'] = JOB_INPUT['IaaS_region_id']
        params['IaaS_tenant_id'] = JOB_INPUT['IaaS_tenant_id']
        params['IaaS_network_id'] = JOB_INPUT['IaaS_network_id']
        params['IaaS_port_id'] = JOB_INPUT['IaaS_port_id']
        params['network_id'] = ''.join([random.choice(
            string.digits + string.ascii_letters) for i in range(10)])
        db_create.set_context(db_endpoint_port, params)
        db_create.execute()

        for network_type_detail in ('2', '3', '4', '5'):
            params = {}
            params['create_id'] = JOB_INPUT['operation_id']
            params['update_id'] = JOB_INPUT['operation_id']
            params['delete_flg'] = 0
            params['tenant_name'] = JOB_INPUT['IaaS_tenant_id']
            params['tenant_id'] = JOB_INPUT['tenant_id']
            params['pod_id'] = JOB_INPUT['pod_id']
            params['port_id'] = 'port2' + network_type_detail
            params['apl_type'] = 1
            params['network_type'] = 2
            params['network_type_detail'] = network_type_detail
            params['ip_address'] = '10.0.0.' + network_type_detail
            params['netmask'] = 16
            params['IaaS_region_id'] = JOB_INPUT['IaaS_region_id']
            params['IaaS_tenant_id'] = JOB_INPUT['IaaS_tenant_id']
            params['IaaS_network_id'] = JOB_INPUT['IaaS_network_id']
            params['IaaS_port_id'] = JOB_INPUT['IaaS_port_id']
            params['network_id'] = ''.join([random.choice(
                string.digits + string.ascii_letters) for i in range(10)])
            db_create.set_context(db_endpoint_port, params)
            db_create.execute()

    def tearDown(self):
        """Clear the test environment"""
        super(TestLicenseAPI, self).tearDown()

        # Create Instance(DB Client)
        db_delete = delete.DeleteClient(config.JobConfig())
        db_list = list.ListClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_license = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_LICENSE)
        db_endpoint_msa_vlan = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_port = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_PORT)

        # Delete from NAL_LICENSE_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']

        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        delete_list = db_list.get_return_param()

        for delete_res in delete_list:
            key = delete_res['ID']
            db_delete.set_context(db_endpoint_license, [key])
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

    def create_db_license(self, h_type, device_type, status=0,
                          tenant_name='', node_id='', update_date=''):

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_license = base.JobAutoBase().get_db_endpoint(
                                config.JobConfig().REST_URI_LICENSE)

        # Create NAL_LICENSE_MNG
        params = {}
        params['create_id'] = JOB_INPUT['operation_id']
        params['update_id'] = JOB_INPUT['operation_id']
        params['delete_flg'] = 0
        params['license'] = 'license' + str(h_type) + str(device_type)
        params['type'] = h_type
        params['device_type'] = device_type
        params['status'] = status
        if len(tenant_name) > 0:
            params['tenant_name'] = tenant_name
        if len(node_id) > 0:
            params['node_id'] = node_id
        if len(update_date) > 0:
            params['update_date'] = update_date

        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

    def test_license_assign(self):

        self.create_db_license(1, 1)
        self.exec_license_assign(1, 1)

        self.create_db_license(1, 4)
        self.exec_license_assign(1, 4)

        self.create_db_license(2, 1)
        self.exec_license_assign(2, 1)

    def test_license_assign_status3(self):

        update_date = (datetime.datetime.now()\
                                - datetime.timedelta(hours=5))\
                                .strftime('%Y-%m-%d %H:%M:%S')

        self.create_db_license(1, 1, 0, '', '', update_date)
        self.exec_license_assign(1, 1)

    def test_license_withdraw(self):

        self.create_db_license(1, 1, 2,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_withdraw(1, 1)

        self.create_db_license(1, 2, 2,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_withdraw(1, 2)

        self.create_db_license(1, 3, 2,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_withdraw(1, 3)

        self.create_db_license(1, 4, 2,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_withdraw(1, 4)

        self.create_db_license(1, 5, 2,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_withdraw(1, 5)

        self.create_db_license(2, 1, 2,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_withdraw(2, 1)

        self.create_db_license(2, 2, 2,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_withdraw(2, 2)

        self.create_db_license(2, 3, 2,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_withdraw(2, 3)

    def test_license_assign_fortigate_vm(self):

        self.create_db_license(1, 2)
        self.exec_license_assign_fortigate_vm()

    def test_license_assign_palpalto_vm(self):

        self.create_db_license(1, 3, 0,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_assign_palpalto_vm()

    def test_license_assign_fortigate_vm_541(self):

        self.create_db_license(1, 5)
        self.exec_license_assign_fortigate_vm_541()

    def test_license_assign_bigip_ve(self):

        self.create_db_license(2, 2)
        self.exec_license_assign_bigip_ve()

    def test_license_assign_vthunder(self):

        self.create_db_license(2, 3, 0,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])
        self.exec_license_assign_vthunder()

    def test_zerotouch_vthunder(self):

        self.exec_zerotouch_vthunder()

    def test_license_assign_not_found_device_type(self):

        self.create_db_license(1, 2)

        try:
            self.exec_license_assign(1, 1)

        except SystemError as e:
            if e.args[0] != 'license not found.':
                raise

    def test_license_assign_not_found_status2(self):

        self.create_db_license(1, 1, 2)

        try:
            self.exec_license_assign(1, 1)

        except SystemError as e:
            if e.args[0] != 'license not found.':
                raise

    def test_license_assign_not_found_status3(self):

        self.create_db_license(1, 1, 3)

        try:
            self.exec_license_assign(1, 1)

        except SystemError as e:
            if e.args[0] != 'license not found.':
                raise

    def test_license_withdraw_not_found(self):

        self.create_db_license(1, 1, 0)
        self.exec_license_withdraw(1, 1)

    def test_license_assign_palpalto_vm_not_found(self):

        self.create_db_license(1, 3, 1,
                JOB_INPUT['IaaS_tenant_id'], JOB_INPUT['node_id'])

        try:
            self.exec_license_assign_palpalto_vm()

        except SystemError as e:
            if e.args[0] != 'license not found.':
                raise

    def exec_license_assign(self, h_type, device_type):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 1,
            'type': h_type,
            'device_type': device_type,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id1': 'port24',
            'port_id2': 'port23',
        }

        res = method.JobAutoMethod().license_assign(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_license_withdraw(self, h_type, device_type):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'type': h_type,
            'device_type': device_type,
        }

        res = method.JobAutoMethod().license_withdraw(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)

    def exec_license_assign_fortigate_vm(self):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 1,
            'type': 1,
            'device_type': 2,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id1': 'port24',
            'port_id2': 'port23',
        }

        res = method.JobAutoMethod().license_assign_fortigate_vm(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_license_assign_palpalto_vm(self):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 1,
            'type': 1,
            'device_type': 3,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id1': 'port24',
        }

        res = method.JobAutoMethod().license_assign_palpalto_vm(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)

    def exec_license_assign_fortigate_vm_541(self):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 1,
            'type': 1,
            'device_type': 5,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id1': 'port24',
            'port_id2': 'port23',
        }

        res = method.JobAutoMethod().license_assign_fortigate_vm_541(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_license_assign_bigip_ve(self):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 1,
            'type': 2,
            'device_type': 2,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id1': 'port24',
            'port_id4': 'port11',
            'fw_ip_address': '10.0.1.1',
        }

        res = method.JobAutoMethod().license_assign_bigip_ve(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def exec_license_assign_vthunder(self):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 1,
            'type': 2,
            'device_type': 3,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id1': 'port24',
        }

        res = method.JobAutoMethod().license_assign_vthunder(job_input)
        print(res)

        # Assertion
        self.assertEqual(len(res), 0)

    def exec_zerotouch_vthunder(self):

        job_input = {
            'operation_id': JOB_INPUT['operation_id'],
            'apl_type': 1,
            'type': 2,
            'device_type': 3,
            'tenant_name': JOB_INPUT['IaaS_tenant_id'],
            'nal_tenant_id': JOB_INPUT['tenant_id'],
            'node_id': JOB_INPUT['node_id'],
            'pod_id': JOB_INPUT['pod_id'],
            'port_id1': 'port24',
        }

        res = method.JobAutoMethod().zerotouch_vthunder(job_input)
        print(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)
