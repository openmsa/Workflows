import copy
import json
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
from job.conf import config
from job.lib.db import create
from job.lib.db import delete
from job.lib.db import list
from job.lib.db import update

from job.auto import base
from job.auto import method

JOB_INPUT_CREATE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': '1de3cf1741674a0dadd15affdb2ffae2',
    'IaaS_tenant_name': 'nal_tenant_test',
    'IaaS_region_id': 'region_unit_test1',
    'apl_type': '1',
    'type': '2',
    'network_name': 'network_name_AAA',
    'IaaS_network_type': 'VLAN',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'IaaS_segmentation_id': '10',
    'description': 'aaaaaa',
    'request-id': '123456789123'
}
JOB_INPUT_ADD_IPV6 = {
    'operation_id': 'test_nw_automation_user_001',
    'apl_type': '1',
    'type': '2',
    'IaaS_tenant_id': '1de3cf1741674a0dadd15affdb2ffae2',
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '7b71f9b8ca84e88f10b4375f74d153af',
    'network_name': 'network_name_AAA',
    'request-id': '123456789123'
}
JOB_INPUT_LICENSE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': '1de3cf1741674a0dadd15affdb2ffae2',
    'IaaS_tenant_name': 'nal_tenant_test',
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'network_name': 'network_name_AAA',
    'IaaS_network_type': 'vlan',
    'IaaS_segmentation_id': '10',
    'request-id': '123456789123'
}
JOB_INPUT_DELETE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': '1de3cf1741674a0dadd15affdb2ffae2',
    'IaaS_tenant_name': 'nal_tenant_test',
    'IaaS_region_id': 'region_unit_test1',
    'request-id': '123456789123'
}


class TestAutoVlbThrough(unittest.TestCase):
    # Do a test of Select.

    def setUp(self):
        # Establish a clean test environment.
        super(TestAutoVlbThrough, self).setUp()

        vim_iaas_with_flg = self.get_vim_iaas_with_flg_for_test()

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_pod = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_POD)
        db_endpoint_tenant = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_TENANT)
        db_endpoint_msa_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)
        db_endpoint_port = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PORT)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0
        params['pod_id'] = 'pod_unit_test2'
        params['use_type'] = 1
        params['ops_version'] = 1
        params['weight'] = '50'
        db_create.set_context(db_endpoint_pod, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0
        params['pod_id'] = 'pod_unit_test1'
        params['use_type'] = 1
        params['ops_version'] = 1
        params['weight'] = '60'
        db_create.set_context(db_endpoint_pod, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0
        params['status'] = 0
        params['network_address'] = '10.20.0.0'
        params['netmask'] = '24'
        params['vlan_id'] = 'vlan_id_0000_1111_2222'
        db_create.set_context(db_endpoint_msa_vlan, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0

        if vim_iaas_with_flg == 0:
            params['network_id'] = '094049539a7ba2548268d74cd5874ebc'
        else:
            params['network_id'] = 'd6680829-59a5-484b-98c2-36c8849ec8bc'

        params['tenant_name'] = '1de3cf1741674a0dadd15affdb2ffae2'
        params['pod_id'] = 'pod_unit_test1'
        params['tenant_id'] = ''
        params['IaaS_network_id'] = 'd6680829-59a5-484b-98c2-36c8849ec8bc'
        params['IaaS_network_type'] = 'VLAN'
        params['IaaS_region_id'] = 'region_unit_test1'
        params['vlan_id'] = '2016'
        db_create.set_context(db_endpoint_vlan, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0

        if vim_iaas_with_flg == 0:
            params['network_id'] = '094049539a7ba2548268d74cd5874ebc'
        else:
            params['network_id'] = 'd6680829-59a5-484b-98c2-36c8849ec8bc'

        params['tenant_name'] = '1de3cf1741674a0dadd15affdb2ffae2'
        params['pod_id'] = 'pod_unit_test1'
        params['tenant_id'] = ''
        params['IaaS_network_id'] = 'd6680829-59a5-484b-98c2-36c8849ec8bc'
        params['IaaS_network_type'] = 'VXLAN'
        params['IaaS_region_id'] = 'region_unit_test1'
        params['vlan_id'] = '2017'
        db_create.set_context(db_endpoint_vlan, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0
        params['port_id'] = 'port_id_00001'

        if vim_iaas_with_flg == 0:
            params['network_id'] = '094049539a7ba2548268d74cd5874ebc'
        else:
            params['network_id'] = 'd6680829-59a5-484b-98c2-36c8849ec8bc'

        params['tenant_name'] = '1de3cf1741674a0dadd15affdb2ffae2'
        params['pod_id'] = 'pod_unit_test1'
        params['tenant_id'] = ''
        params['network_type'] = '1'
        params['network_type_detail'] = '1'
        db_create.set_context(db_endpoint_port, params)
        db_create.execute()

        for device_type in ('1', '2', '3', '4'):
            params = {}
            params['create_id'] = 'test_nw_automation_user_001'
            params['update_id'] = 'test_nw_automation_user_001'
            params['delete_flg'] = 0
            params['license'] = 'test_license_001'
            params['type'] = 2
            params['device_type'] = device_type
            params['status'] = 0
            db_create.set_context(db_endpoint_license, params)
            db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0
        params['tenant_name'] = '1de3cf1741674a0dadd15affdb2ffae2'
        params['IaaS_region_id'] = 'region_unit_test1'
        params['IaaS_tenant_id'] = '1de3cf1741674a0dadd15affdb2ffae2'
        tenant_info = [
            {
                "description": "",
                "enabled": True,
                "id": "f81f98e26fd934a0544632420e43a8fa",
                "msa_customer_id": 0,
                "msa_customer_name": "",
                "name": "nal_tenant_test",
                "pod_id": "pod_unit_test1"
            }
        ]
        params['tenant_info'] = json.dumps(tenant_info)
        db_create.set_context(db_endpoint_tenant, params)
        db_create.execute()

    def get_vim_iaas_with_flg_for_test(self):
        pod_id = 'pod_unit_test1'
        dc_id = 'system'
        endpoint_config = \
            base.JobAutoBase().nal_endpoint_config[dc_id]['vim'][pod_id]
        vim_iaas_with_flg_str = endpoint_config.get('vim_iaas_with_flg', '0')

        vim_iaas_with_flg = int(vim_iaas_with_flg_str)

        return vim_iaas_with_flg

    def tearDown(self):
        """Clear the test environment"""
        super(TestAutoVlbThrough, self).tearDown()

        # Create Instance(DB Client)
        db_list = list.ListClient(config.JobConfig())
        db_delete = delete.DeleteClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_APL)
        db_endpoint_pod = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_POD)
        db_endpoint_tenant = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_TENANT)
        db_endpoint_valn = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)
        db_endpoint_port = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PORT)
        db_endpoint_msa_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)

        # Delete from NAL_APL_MNG
        params = {}
        params['create_id'] = JOB_INPUT_CREATE['operation_id']

        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        delete_apl_list = db_list.get_return_param()

        for delete_apl in delete_apl_list:
            key = delete_apl['ID']
            db_delete.set_context(db_endpoint_apl, [key])
            db_delete.execute()

        # Delete from NAL_POD_MNG
        params = {}
        params['create_id'] = JOB_INPUT_CREATE['operation_id']

        db_list.set_context(db_endpoint_pod, params)
        db_list.execute()
        delete_pod_list = db_list.get_return_param()

        for delete_pod in delete_pod_list:
            key = delete_pod['ID']
            db_delete.set_context(db_endpoint_pod, [key])
            db_delete.execute()

        # Delete from NAL_TENANT_MNG
        params = {}
        params['create_id'] = JOB_INPUT_CREATE['operation_id']

        db_list.set_context(db_endpoint_tenant, params)
        db_list.execute()
        delete_tenant_list = db_list.get_return_param()

        for delete_tenant in delete_tenant_list:
            key = delete_tenant['ID']
            db_delete.set_context(db_endpoint_tenant, [key])
            db_delete.execute()

        # Delete from NAL_MSA_VLAN_MNG
        params = {}
        params['create_id'] = JOB_INPUT_CREATE['operation_id']

        db_list.set_context(db_endpoint_valn, params)
        db_list.execute()
        delete_port_list = db_list.get_return_param()

        for delete_port in delete_port_list:
            key = delete_port['ID']
            db_delete.set_context(db_endpoint_valn, [key])
            db_delete.execute()

        # Delete from NAL_PORT_MNG
        params = {}
        params['create_id'] = JOB_INPUT_CREATE['operation_id']

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        delete_port_list = db_list.get_return_param()

        for delete_port in delete_port_list:
            key = delete_port['ID']
            db_delete.set_context(db_endpoint_port, [key])
            db_delete.execute()

        # Delete from NAL_MSA_VLAN_MNG
        params = {}
        params['create_id'] = JOB_INPUT_CREATE['operation_id']

        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        delete_msa_vlan_list = db_list.get_return_param()

        for delete_msa_vlan in delete_msa_vlan_list:
            key = delete_msa_vlan['ID']
            db_delete.set_context(db_endpoint_msa_vlan, [key])
            db_delete.execute()

        # Delete from NAL_VLAN_MNG
        params = {}
        params['create_id'] = JOB_INPUT_CREATE['operation_id']

        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        delete_vlan_list = db_list.get_return_param()

        for delete_vlan in delete_vlan_list:
            key = delete_vlan['ID']
            db_delete.set_context(db_endpoint_vlan, [key])
            db_delete.execute()

        # Delete from NAL_LICENSE_MNG
        params = {}
        params['create_id'] = JOB_INPUT_CREATE['operation_id']

        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        delete_license_list = db_list.get_return_param()

        for delete_license in delete_license_list:
            key = delete_license['ID']
            db_delete.set_context(db_endpoint_license, [key])
            db_delete.execute()

    def update_db_license_status(self, device_type, status):

        # Create Instance(DB Client)
        db_list = list.ListClient(config.JobConfig())
        db_update = update.UpdateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)

        # Update NAL_LICENSE_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['type'] = 2
        params['device_type'] = device_type

        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        update_license_list = db_list.get_return_param()

        for update_license in update_license_list:
            keys = [update_license['ID']]
            params = {}
            params['status'] = status
            db_update.set_context(db_endpoint_license, keys, params)
            db_update.execute()

    def test_through_intersec_lb(self):

        self.exec_through_intersec_lb()
        self.exec_through_intersec_lb()

    def test_through_bigip_ve(self):

        self.exec_through_bigip_ve()
        self.update_db_license_status(2, 0)
        self.exec_through_bigip_ve()

    def test_through_vthunder(self):

        self.exec_through_vthunder()
        self.update_db_license_status(3, 0)
        self.exec_through_vthunder()

    def test_through_vthunder411(self):

        self.exec_through_vthunder411()
        self.update_db_license_status(4, 0)
        self.exec_through_vthunder411()

    def test_through_intersec_lb_license_not_found(self):

        self.exec_through_intersec_lb()

        self.update_db_license_status(1, 2)

        try:
            self.exec_through_intersec_lb()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def test_through_bigip_ve_license_not_found(self):

        self.exec_through_bigip_ve()

        try:
            self.exec_through_bigip_ve()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def test_through_vthunder_license_not_found(self):

        self.exec_through_vthunder()

        try:
            self.exec_through_vthunder()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def test_through_vthunder411_license_not_found(self):

        self.exec_through_vthunder411()

        try:
            self.exec_through_vthunder411()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def exec_through_intersec_lb(self, iaas_network_type='VXLAN'):

        device_type = '1'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_intersec_lb'
        job_input['fw_ip_address'] = '10.58.10.1'
        job_input['zabbix_vip_ip'] = '10.58.10.3'
        job_input['zabbix_01_ip'] = '10.58.10.4'
        job_input['zabbix_02_ip'] = '10.58.10.5'

        create_output = self.main_create_vlb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vlb(job_input)

    def exec_through_bigip_ve(self, iaas_network_type='VXLAN'):

        device_type = '2'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_bigip_ve'
        job_input['fw_ip_address'] = '10.58.10.1'
        job_input['domain_name'] = 'domain_name_AAA'
        job_input['self_ip_name'] = 'self_ip_name_AAA'
        job_input['admin_id'] = 'admin_id'
        job_input['admin_pw'] = 'admin_pw'
        job_input['timezone'] = 'timezone'

        create_output = self.main_create_vlb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        port_id4 = create_output['port_id4']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4
        job_input['fw_ip_v6_address'] = '2001:db5::1'

        self.main_add_ipv6_vlb(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vlb(job_input)

    def exec_through_vthunder(self, iaas_network_type='VXLAN'):

        device_type = '3'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_vthunder'
        job_input['fw_ip_address'] = '10.58.10.1'
        job_input['admin_id'] = 'admin_id'
        job_input['admin_pw'] = 'admin_pw'

        create_output = self.main_create_vlb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        port_id4 = create_output['port_id4']

        # Create Instance(DB Client)
        db_list = list.ListClient(config.JobConfig())
        db_update = update.UpdateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)

        # List NAL_LICENSE_MNG(DB Client)
        params = {}
        params['status'] = 0
        params['type'] = 2
        params['device_type'] = device_type
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        license_list = db_list.get_return_param()

        # Update NAL_LICENSE_MNG(DB Client)
        if len(license_list) > 0:
            keys = [license_list[0]['ID']]
            params = {}
            params['tenant_name'] = JOB_INPUT_CREATE['IaaS_tenant_id']
            params['node_id'] = node_id
            db_update.set_context(db_endpoint_license, keys, params)
            db_update.execute()

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_LICENSE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        self.main_license_assign_vlb(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4
        job_input['fw_ip_v6_address'] = '2001:db5::1'

        self.main_add_ipv6_vlb(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vlb(job_input)

    def exec_through_vthunder411(self, iaas_network_type='VXLAN'):

        device_type = '4'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_vthunder'
        job_input['fw_ip_address'] = '10.58.10.1'
        job_input['admin_id'] = 'admin_id'
        job_input['admin_pw'] = 'admin_pw'

        create_output = self.main_create_vlb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        port_id4 = create_output['port_id4']

        # Create Instance(DB Client)
        db_list = list.ListClient(config.JobConfig())
        db_update = update.UpdateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)

        # List NAL_LICENSE_MNG(DB Client)
        params = {}
        params['status'] = 0
        params['type'] = 2
        params['device_type'] = device_type
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        license_list = db_list.get_return_param()

        # Update NAL_LICENSE_MNG(DB Client)
        if len(license_list) > 0:
            keys = [license_list[0]['ID']]
            params = {}
            params['tenant_name'] = JOB_INPUT_CREATE['IaaS_tenant_id']
            params['node_id'] = node_id
            db_update.set_context(db_endpoint_license, keys, params)
            db_update.execute()

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_LICENSE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        self.main_license_assign_vlb(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4
        job_input['fw_ip_v6_address'] = '2001:db5::1'

        self.main_add_ipv6_vlb(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vlb(job_input)

    def main_create_vlb(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'],
                            JOB_INPUT_CREATE['IaaS_tenant_id'])

        # initialize_create_vnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_create_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('apl_table_rec_id' in job_output)

        # routing_pod
        job_input.update(job_output)
        job_output = method.JobAutoMethod().routing_pod(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['pod_id'],
                         'pod_unit_test1')

        # get_or_create_pod_tenant
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_or_create_pod_tenant(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['nal_tenant_name'],
                         JOB_INPUT_CREATE['IaaS_tenant_name'])
        nal_tenant_id = job_output['nal_tenant_id']

        db_list = list.ListClient(config.JobConfig())
        db_update = update.UpdateClient(config.JobConfig())

        # List NAL_PORT_MNG(DB Client)
        db_endpoint_port = base.JobAutoBase().get_db_endpoint(
                                            config.JobConfig().REST_URI_PORT)
        params = {}
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        # Update NAL_PORT_MNG(DB Client)

        for port_res in port_list:
            keys = [port_res['ID']]
            params = {}
            params['tenant_id'] = nal_tenant_id
            db_update.set_context(db_endpoint_port, keys, params)
            db_update.execute()

        # List NAL_VLAN_MNG(DB Client)
        db_endpoint_vlan = base.JobAutoBase().get_db_endpoint(
                                            config.JobConfig().REST_URI_VLAN)
        params = {}
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        vlan_list = db_list.get_return_param()

        # Update NAL_VLAN_MNG(DB Client)
        for vlan_res in vlan_list:
            keys = [vlan_res['ID']]
            params = {}
            params['tenant_id'] = nal_tenant_id
            db_update.set_context(db_endpoint_vlan, keys, params)
            db_update.execute()

        # hostname_check
        job_input.update(job_output)
        job_output = method.JobAutoMethod().hostname_check(job_input)

        # Assertion
        self.assertEqual(job_output, {})

        # virtual_msa_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().virtual_msa_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('port_id1' in job_output)
        self.assertTrue('device_ip_address' in job_output)

        # virtual_lb_tenant_vlan_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            virtual_lb_tenant_vlan_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('port_id4' in job_output)

        # virtual_server_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
            .virtual_server_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('server_id' in job_output)
        self.assertTrue('node_id' in job_output)

        if job_input['device_type'] in ('1',):
            # license_assign
            job_input.update(job_output)
            job_output = method.JobAutoMethod().license_assign(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertEqual(job_output['license_key'], 'test_license_001')

        elif job_input['device_type'] in ('2',):
            # license_assign_bigip_ve
            job_input.update(job_output)
            job_output = \
                method.JobAutoMethod().license_assign_bigip_ve(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertEqual(job_output['license_key'], 'test_license_001')

        elif job_input['device_type'] in ('3',):
            # zerotouch_vthunder
            job_input.update(job_output)
            job_output = \
                method.JobAutoMethod().zerotouch_vthunder(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertEqual(job_output['license_key'], '')

        # msa_customer_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().msa_customer_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('msa_customer_id' in job_output)

        # msa_setup_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().msa_setup_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        if job_input['device_type'] in ('1',):
            # device_setup_create_for_intersec_lb
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_intersec_lb(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2',):
            # device_setup_create_for_bigip_ve
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_bigip_ve(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # device_setup_create_for_vthunder
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_vthunder(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # device_setup_create_for_vthunder411
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_vthunder411(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        # terminate_create_vnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().terminate_create_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')
        self.assertEqual(job_output['data'], {})

        job_input.update(job_output)
        return job_input

    def main_add_ipv6_vlb(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'],
                            JOB_INPUT_CREATE['IaaS_tenant_id'])

        # initialize
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], job_input['apl_type'])
        self.assertEqual(job_output['type'], job_input['type'])
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '')

        # virtual_lb_tenant_vlan_port_add_ipv6
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            virtual_lb_tenant_vlan_port_add_ipv6(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # virtual_lb_interface_attach_ipv6
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
                virtual_lb_interface_attach_ipv6(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        if job_input['device_type'] in ('2',):
            # device_setup_add_ipv6_for_bigip_ve
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                            .device_setup_add_ipv6_for_bigip_ve(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # device_setup_add_ipv6_for_vthunder
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                            .device_setup_add_ipv6_for_vthunder(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # device_setup_add_ipv6_for_vthunder411
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                            .device_setup_add_ipv6_for_vthunder411(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        # terminate
        job_input.update(job_output)
        job_output = method.JobAutoMethod().terminate(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')
        self.assertEqual(job_output['data'], {})

        job_input.update(job_output)
        return job_input

    def main_license_assign_vlb(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'],
                         JOB_INPUT_CREATE['IaaS_tenant_id'])

        # initialize_update_vnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_update_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '1')
        self.assertEqual(job_output['type'], '2')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '')

        # license_assign_vthunder
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
            .license_assign_vthunder(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # terminate_update_vnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().terminate_update_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')
        self.assertEqual(job_output['data'], {})

        job_input.update(job_output)
        return job_input

    def main_delete_vlb(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'],
                                JOB_INPUT_CREATE['IaaS_tenant_id'])

        # initialize_delete_vnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_delete_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '1')
        self.assertEqual(job_output['type'], '2')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '')

        # get_pod_tenant
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_pod_tenant(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['nal_tenant_name'], 'nal_tenant_test')

        # msa_setup_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().msa_setup_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # license_withdraw
        job_input.update(job_output)
        job_output = method.JobAutoMethod().license_withdraw(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # virtual_msa_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().virtual_msa_port_delete(job_input)

        # virtual_lb_tenant_vlan_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            virtual_lb_tenant_vlan_port_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # virtual_server_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().virtual_server_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # terminate_delete_vnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().terminate_delete_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')
        self.assertEqual(job_output['data'], {})

        job_input.update(job_output)
        return job_input
