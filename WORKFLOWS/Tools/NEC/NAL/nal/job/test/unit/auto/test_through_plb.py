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

from job.auto import base
from job.auto import method

JOB_INPUT_CREATE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'apl_type': '2',
    'type': '2',
    'network_name': 'network_name_AAA',
    'IaaS_network_type': 'VLAN',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'IaaS_segmentation_id': 'IaaS_segmentation_id_001',
    'description': 'aaaaaa',
    'redundant_configuration_flg': '0',
    'fw_ip_address': '10.58.10.1',
    'request-id': '123456789123'
}
JOB_INPUT_ADD_IPV6 = {
    'operation_id': 'test_nw_automation_user_001',
    'apl_type': '2',
    'type': '2',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '7b71f9b8ca84e88f10b4375f74d153af',
    'network_name': 'network_name_AAA',
    'fw_ip_v6_address': '2001:db5::1',
    'request-id': '123456789123',
    'redundant_configuration_flg': '0'
}
JOB_INPUT_DELETE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'request-id': '123456789123'
}


class TestAutoPlbThrough(unittest.TestCase):
    # Do a test of Select.

    def setUp(self):
        # Establish a clean test environment.
        super(TestAutoPlbThrough, self).setUp()

        vim_iaas_with_flg = self.get_vim_iaas_with_flg_for_test()
        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_APL)
        db_endpoint_pod = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_POD)
        db_endpoint_tenant = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_TENANT)
        db_endpoint_msa_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_pnf_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PNF_VLAN)
        db_endpoint_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)
        db_endpoint_port = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PORT)

        partition_id_seq = 0
        for device_type in ('1', '2', '3', '4'):
            # Create test data to NAL_APL_MNG
            params = {}
            params['create_id'] = 'test_nw_automation_user_001'
            params['update_id'] = 'test_nw_automation_user_001'
            params['delete_flg'] = 0
            params['apl_type'] = 2
            params['type'] = 2
            params['device_type'] = device_type
            params['node_id'] = 'node_id_001' + device_type
            params['actsby_flag_master'] = 'act'
            params['device_name_master'] = 'wn0fwxtf01' + device_type
            params['device_detail_master'] = '{}'
            params['master_ip_address'] = '100.99.0.5'
            params['pod_id'] = 'pod_unit_test1'
            params['redundant_configuration_flg'] = '0'
            params['tenant_name'] = ''
            params['MSA_device_id'] = ''
            params['status'] = 0
            params['task_status'] = 1
            params['nic_MSA'] = 'mport'
            params['nic_public'] = 'pport'
            params['nic_external'] = 'eport'
            params['nic_tenant'] = 'tport'

            if device_type in ('2', '4'):
                partition_id_seq += 1
                params['partition_id_seq'] = str(partition_id_seq)

            db_create.set_context(db_endpoint_apl, params)
            db_create.execute()

            params = {}
            params['create_id'] = 'test_nw_automation_user_001'
            params['update_id'] = 'test_nw_automation_user_001'
            params['delete_flg'] = 0
            params['apl_type'] = 2
            params['type'] = 2
            params['device_type'] = device_type
            params['node_id'] = 'node_id_002' + device_type
            params['actsby_flag_master'] = 'act'
            params['device_name_master'] = 'wn0fwxtf01'
            params['device_detail_master'] = '{}'
            params['master_ip_address'] = '100.99.0.5'
            params['pod_id'] = 'pod_unit_test1'
            params['redundant_configuration_flg'] = '1'
            params['tenant_name'] = ''
            params['MSA_device_id'] = ''
            params['status'] = 0
            params['task_status'] = 1
            params['nic_MSA'] = 'mport'
            params['nic_public'] = 'pubport'
            params['nic_external'] = 'extport'
            params['nic_tenant'] = 'tport'

            if device_type in ('2', '4'):
                partition_id_seq += 1
                params['partition_id_seq'] = str(partition_id_seq)

            db_create.set_context(db_endpoint_apl, params)
            db_create.execute()

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

        for vlan_num in range(1, 4):
            params = {}
            params['create_id'] = 'test_nw_automation_user_001'
            params['update_id'] = 'test_nw_automation_user_001'
            params['delete_flg'] = 0
            params['status'] = 0
            params['network_address'] = '10.21.' + str(vlan_num) + '.0'
            params['netmask'] = '24'
            params['vlan_id'] = '200' + str(vlan_num)
            db_create.set_context(db_endpoint_pnf_vlan, params)
            db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0

        if vim_iaas_with_flg == 0:
            params['network_id'] = '094049539a7ba2548268d74cd5874ebc'
        else:
            params['network_id'] = 'd6680829-59a5-484b-98c2-36c8849ec8bc'

        params['tenant_name'] = 'IaaS_tenant_id_001'
        params['pod_id'] = 'pod_unit_test1'
        params['tenant_id'] = 'ef5d2e187b9636f9a4811318069137a6'
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

        params['tenant_name'] = 'IaaS_tenant_id_001'
        params['pod_id'] = 'pod_unit_test1'
        params['tenant_id'] = 'ef5d2e187b9636f9a4811318069137a6'
        params['IaaS_network_id'] = 'd6680829-59a5-484b-98c2-36c8849ec8bc'
        params['IaaS_network_type'] = 'VXLAN'
        params['IaaS_region_id'] = 'region_unit_test1'
        params['vlan_id'] = '2016'
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

        params['tenant_name'] = 'IaaS_tenant_id_001'
        params['pod_id'] = 'pod_unit_test1'
        params['tenant_id'] = 'ef5d2e187b9636f9a4811318069137a6'
        params['network_type'] = '1'
        params['network_type_detail'] = '1'
        db_create.set_context(db_endpoint_port, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0
        params['tenant_name'] = 'IaaS_tenant_id_001'
        params['IaaS_region_id'] = 'region_unit_test1'
        params['IaaS_tenant_id'] = 'IaaS_tenant_id_001'
        tenant_info = [
            {
                "description": "",
                "enabled": True,
                "id": "ef5d2e187b9636f9a4811318069137a6",
                "msa_customer_id": 0,
                "msa_customer_name": "",
                "name": "IaaS_tenant_name_AAA",
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
        super(TestAutoPlbThrough, self).tearDown()

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
        db_endpoint_pnf_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PNF_VLAN)
        db_endpoint_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)

        # Delete from NAL_APL_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        delete_apl_list = db_list.get_return_param()

        for delete_apl in delete_apl_list:
            key = delete_apl['ID']
            db_delete.set_context(db_endpoint_apl, [key])
            db_delete.execute()

        # Delete from NAL_POD_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_pod, params)
        db_list.execute()
        delete_pod_list = db_list.get_return_param()

        for delete_pod in delete_pod_list:
            key = delete_pod['ID']
            db_delete.set_context(db_endpoint_pod, [key])
            db_delete.execute()

        # Delete from NAL_TENANT_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_tenant, params)
        db_list.execute()
        delete_tenant_list = db_list.get_return_param()

        for delete_tenant in delete_tenant_list:
            key = delete_tenant['ID']
            db_delete.set_context(db_endpoint_tenant, [key])
            db_delete.execute()

        # Delete from NAL_MSA_VLAN_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_valn, params)
        db_list.execute()
        delete_port_list = db_list.get_return_param()

        for delete_port in delete_port_list:
            key = delete_port['ID']
            db_delete.set_context(db_endpoint_valn, [key])
            db_delete.execute()

        # Delete from NAL_PORT_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        delete_port_list = db_list.get_return_param()

        for delete_port in delete_port_list:
            key = delete_port['ID']
            db_delete.set_context(db_endpoint_port, [key])
            db_delete.execute()

        # Delete from NAL_MSA_VLAN_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        delete_msa_vlan_list = db_list.get_return_param()

        for delete_msa_vlan in delete_msa_vlan_list:
            key = delete_msa_vlan['ID']
            db_delete.set_context(db_endpoint_msa_vlan, [key])
            db_delete.execute()

        # Delete from NAL_PNF_VLAN_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_pnf_vlan, params)
        db_list.execute()
        delete_pnf_vlan_list = db_list.get_return_param()

        for delete_pnf_vlan in delete_pnf_vlan_list:
            key = delete_pnf_vlan['ID']
            db_delete.set_context(db_endpoint_pnf_vlan, [key])
            db_delete.execute()

        # Delete from NAL_VLAN_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        delete_vlan_list = db_list.get_return_param()

        for delete_vlan in delete_vlan_list:
            key = delete_vlan['ID']
            db_delete.set_context(db_endpoint_vlan, [key])
            db_delete.execute()

        # Delete from NAL_LICENSE_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        delete_license_list = db_list.get_return_param()

        for delete_license in delete_license_list:
            key = delete_license['ID']
            db_delete.set_context(db_endpoint_license, [key])
            db_delete.execute()

    def test_through_bigip(self):

        self.exec_through_bigip()

    def test_through_bigip_redundant(self):

        self.exec_through_bigip(0)

    def test_through_thunder(self):

        self.exec_through_thunder()

    def test_through_thunder_redundant(self):

        self.exec_through_thunder(0)

    def test_through_bigip_share(self):

        self.exec_through_bigip_share()

    def test_through_thunder_share(self):

        self.exec_through_thunder_share()

    def exec_through_bigip(self,
            redundant_configuration_flg=1, iaas_network_type='VXLAN'):

        device_type = '1'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['partition_id'] = 'partition_id123'
        job_input['route_domain_id'] = 'route_domain_id123'
        job_input['mng_user_account_id'] = 'mng_user_account_id123'
        job_input['mng_account_password'] = 'mng_account_password123'
        job_input['certificate_user_account_id'] = 'certificate_user123'
        job_input['certificate_account_password'] = 'certificate_pass123'
        job_input['redundant_configuration_flg'] = redundant_configuration_flg

        create_output = self.main_create_plb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        port_id4 = create_output['port_id4']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4

        self.main_add_ipv6_plb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id
        job_input['redundant_configuration_flg'] = redundant_configuration_flg

        self.main_delete_plb(job_input)

    def exec_through_bigip_share(self,
            redundant_configuration_flg=1, iaas_network_type='VXLAN'):

        device_type = '3'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['partition_id'] = 'partition_id123'
        job_input['route_domain_id'] = 'route_domain_id123'
        job_input['mng_user_account_id'] = 'mng_user_account_id123'
        job_input['mng_account_password'] = 'mng_account_password123'
        job_input['certificate_user_account_id'] = 'certificate_user123'
        job_input['certificate_account_password'] = 'certificate_pass123'
        job_input['redundant_configuration_flg'] = redundant_configuration_flg

        create_output = self.main_create_plb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        port_id4 = create_output['port_id4']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4

        self.main_add_ipv6_plb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id
        job_input['redundant_configuration_flg'] = redundant_configuration_flg

        self.main_delete_plb(job_input)

    def exec_through_thunder(self,
            redundant_configuration_flg=1, iaas_network_type='VXLAN'):

        device_type = '2'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['partition_name'] = 'partition_name123'
        job_input['user_account_id'] = 'user_account_id123'
        job_input['account_password'] = 'account_password123'
        job_input['redundant_configuration_flg'] = redundant_configuration_flg

        create_output = self.main_create_plb(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        port_id4 = create_output['port_id4']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4

        self.main_add_ipv6_plb(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id
        job_input['redundant_configuration_flg'] = redundant_configuration_flg

        self.main_delete_plb(job_input)

    def exec_through_thunder_share(self,
            redundant_configuration_flg=1, iaas_network_type='VXLAN'):

        device_type = '4'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['partition_name'] = 'partition_name123'
        job_input['user_account_id'] = 'user_account_id123'
        job_input['account_password'] = 'account_password123'
        job_input['redundant_configuration_flg'] = redundant_configuration_flg

        create_output = self.main_create_plb(job_input)

        # Get node_id from create process
        port_id4 = create_output['port_id4']
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        job_input['port_id'] = port_id4

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4

        self.main_add_ipv6_plb(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id
        job_input['redundant_configuration_flg'] = redundant_configuration_flg

        self.main_delete_plb(job_input)

    def main_create_plb(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

        # initialize_create_pnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_create_pnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 3)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('node_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')

        # get_pod_tenant
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_pod_tenant(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['nal_tenant_name'],
                         'IaaS_tenant_name_AAA')

        # physical_lb_tenant_vlan_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            physical_lb_tenant_vlan_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('port_id4' in job_output)

        # physical_server_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().physical_server_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('node_id' in job_output)

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
            # device_setup_create_for_bigip
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_create_for_bigip(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # device_setup_create_for_bigip_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_create_for_bigip_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2',):
            # device_setup_create_for_thunder
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_create_for_thunder(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # device_setup_create_for_thunder_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_create_for_thunder_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        # terminate_create_pnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().terminate_create_pnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')
        self.assertEqual(job_output['data'], {})

        job_input.update(job_output)
        return job_input

    def main_add_ipv6_plb(self, job_input):

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

        self.assertTrue('redundant_configuration_flg' in job_output)

        # physical_lb_tenant_vlan_port_add_ipv6
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            physical_lb_tenant_vlan_port_add_ipv6(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        if job_input['device_type'] in ('1',):
            # Device setup add ipv6 for bigip
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                            .device_setup_add_ipv6_for_bigip(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})
        elif job_input['device_type'] in ('2',):
            # Device setup add ipv6 for thunder
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                            .device_setup_add_ipv6_for_thunder(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # Device setup add ipv6 for bigip share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_add_ipv6_for_bigip_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})
        elif job_input['device_type'] in ('4',):
            # Device setup add ipv6 for thunder share
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                            .device_setup_add_ipv6_for_thunder_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})
        else:
            pass

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

    def main_delete_plb(self, job_input):
        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

        # initialize_delete_pnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_delete_pnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '2')
        self.assertEqual(job_output['type'], '2')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])

        redundant_configuration_flg = job_input['redundant_configuration_flg']
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        self.assertEqual(job_output['redundant_configuration_flg'],
                         redundant_configuration_flg)

        if job_input['device_type'] in ('1',):
            # device_setup_delete_for_bigip
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_delete_for_bigip(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2',):
            # device_setup_delete_for_thunder
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_delete_for_thunder(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # device_setup_delete_for_bigip_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_delete_for_bigip_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # device_setup_delete_for_thunder_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_delete_for_thunder_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})
        else:
            pass

        # msa_setup_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().msa_setup_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # physical_lb_tenant_vlan_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            physical_lb_tenant_vlan_port_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # physical_server_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().physical_server_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # terminate_delete_pnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().terminate_delete_pnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')
        self.assertEqual(job_output['data'], {})

        job_input.update(job_output)
        return job_input
