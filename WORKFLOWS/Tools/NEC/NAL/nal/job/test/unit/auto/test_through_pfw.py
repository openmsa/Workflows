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

from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import subnets


JOB_INPUT_CREATE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'apl_type': '2',
    'type': '1',
    'network_name': 'network_name_AAA',
    'IaaS_network_type': 'VLAN',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'IaaS_segmentation_id': 'IaaS_segmentation_id_001',
    'description': 'aaaaaa',
    'redundant_configuration_flg': '1',
    'request-id': '123456789123'
}
JOB_INPUT_LICENSE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'network_name': 'network_name_AAA',
    'IaaS_network_type': 'vlan',
    'IaaS_segmentation_id': '15',
    'request-id': '123456789123'
}
JOB_INPUT_PORT_CREATE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'network_name': 'network_name_AAA',
    'IaaS_network_type': 'vxlan',
    'IaaS_segmentation_id': '15',
    'request-id': '123456789123'
}
JOB_INPUT_ADD_IPV6 = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '7b71f9b8ca84e88f10b4375f74d153af',
    'request-id': '123456789123'
}
JOB_INPUT_PORT_DELETE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'request-id': '123456789123'
}
JOB_INPUT_DELETE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'request-id': '123456789123'
}


class TestAutoPfwThrough(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):
        # Establish a clean test environment.
        super(TestAutoPfwThrough, self).setUp()

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_APL)
        db_endpoint_pod = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_POD)
        db_endpoint_msa_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_pnf_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PNF_VLAN)
        db_endpoint_global_ip = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_GLOBAL_IP)
        db_endpoint_tenant = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_TENANT)

        for device_type in ('1', '2', '3', '4'):
            # Create test data to NAL_APL_MNG
            params = {}
            params['create_id'] = 'test_nw_automation_user_001'
            params['update_id'] = 'test_nw_automation_user_001'
            params['delete_flg'] = 0
            params['apl_type'] = 2
            params['type'] = 1
            params['device_type'] = device_type
            params['node_id'] = 'node_id_001' + device_type
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
            params['nic_public'] = 'ethernet1/3.'
            params['nic_external'] = 'ethernet1/3.'
            params['nic_tenant'] = 'ethernet1/3.'
            params['vsys_id_seq'] = '1'
            db_create.set_context(db_endpoint_apl, params)
            db_create.execute()

        for device_type in ('3', '4'):
            # Create test data to NAL_APL_MNG
            params = {}
            params['create_id'] = 'test_nw_automation_user_001'
            params['update_id'] = 'test_nw_automation_user_001'
            params['delete_flg'] = 0
            params['apl_type'] = 2
            params['type'] = 1
            params['device_type'] = device_type
            params['node_id'] = 'node_id_001' + device_type + '_2'
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
            params['nic_public'] = 'ethernet1/4.'
            params['nic_external'] = 'ethernet1/4.'
            params['nic_tenant'] = 'ethernet1/4.'
            params['vsys_id_seq'] = '2'
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

        for vlan_num in range(1, 9):
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
        params['global_ip'] = '192.168.80.245'
        params['status'] = 0
        db_create.set_context(db_endpoint_global_ip, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0
        params['global_ip'] = '192.168.80.246'
        params['status'] = 0
        db_create.set_context(db_endpoint_global_ip, params)
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

        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['update_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0
        params['tenant_name'] = 'IaaS_tenant_id_002'
        params['IaaS_region_id'] = 'region_unit_test1'
        params['IaaS_tenant_id'] = 'IaaS_tenant_id_002'
        tenant_info = [
            {
                "description": "",
                "enabled": True,
                "id": "ef5d2e187b9636f9a4811318069137a7",
                "msa_customer_id": 0,
                "msa_customer_name": "",
                "name": "IaaS_tenant_name_BBB",
                "pod_id": "pod_unit_test1"
            }
        ]
        params['tenant_info'] = json.dumps(tenant_info)
        db_create.set_context(db_endpoint_tenant, params)
        db_create.execute()

    def tearDown(self):
        """Clear the test environment"""
        super(TestAutoPfwThrough, self).tearDown()

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
        db_endpoint_port = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PORT)
        db_endpoint_msa_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_pnf_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PNF_VLAN)
        db_endpoint_global_ip = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_GLOBAL_IP)
        db_endpoint_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)

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
        delete_pod_list = db_list.get_return_param()

        for delete_pod in delete_pod_list:
            key = delete_pod['ID']
            db_delete.set_context(db_endpoint_tenant, [key])
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

        # Delete from NAL_GLOBAL_IP_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'

        db_list.set_context(db_endpoint_global_ip, params)
        db_list.execute()
        delete_global_ip_list = db_list.get_return_param()

        for delete_global_ip in delete_global_ip_list:
            key = delete_global_ip['ID']
            db_delete.set_context(db_endpoint_global_ip, [key])
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

    def test_through_fortigate1(self):
        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_fortigate()

    def test_through_fortigate2(self):
        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_fortigate('VXLAN',
                                       '2001:DB6::1', '2001:DB7::1')

    def test_through_fortigate3(self):
        # Pub/Ext Port(IPv6) Exists
        self.exec_through_fortigate('VXLAN',
                                       '', '', True)

    def test_through_fortigate4(self):
        # Pub/Ext Port(IPv6) Exists
        self.exec_through_fortigate('VXLAN',
                                       '2001:DB6::1', '2001:DB7::1', True)

    def test_through_paloalto1(self):
        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_paloalto()

    def test_through_paloalto2(self):
        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_paloalto('VXLAN', '2001:DB6::1', '2001:DB7::1')

    def test_through_paloalto3(self):
        # Pub/Ext Port(IPv6) Exists
        self.exec_through_paloalto('VXLAN', '', '', True)

    def test_through_paloalto4(self):
        # Pub/Ext Port(IPv6) Exists
        self.exec_through_paloalto('VXLAN',
                                '2001:DB8::1', '2001:DB9::1', True)

    def test_through_paloalto_share1(self):
        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_paloalto_share()

    def test_through_paloalto_share2(self):
        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_paloalto_share('VXLAN', '2001:DB6::1', '2001:DB7::1')

    def test_through_paloalto_share3(self):
        # Pub/Ext Port(IPv6) Exists
        self.exec_through_paloalto_share('VXLAN', '', '', True)

    def test_through_paloalto_share4(self):
        # Pub/Ext Port(IPv6) Exists
        self.exec_through_paloalto_share('VXLAN',
                                '2001:DB8::1', '2001:DB9::1', True)

    def test_through_fortigate_share1(self):
        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_fortigate_share()

    def test_through_fortigate_share2(self):
        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_fortigate_share('VXLAN',
                                       '2001:DB6::1', '2001:DB7::1')

    def test_through_fortigate_share3(self):
        # Pub/Ext Port(IPv6) Exists
        self.exec_through_fortigate_share('VXLAN',
                                       '', '', True)

    def test_through_fortigate_share4(self):
        # Pub/Ext Port(IPv6) Exists
        self.exec_through_fortigate_share('VXLAN',
                                       '2001:DB6::1', '2001:DB7::1', True)

    def create_os_subnet_ipv6(self, vlan_type, pod_id, nal_tenant_id):

        network_name = base.JobAutoBase().get_os_vlan_name(vlan_type, 'system')

        # Create Instance(OpenStack Client)
        osc_networks = networks.OscQuantumNetworks(config.JobConfig())
        os_subnets_instance = subnets.OscQuantumSubnets(config.JobConfig())

        # Get Endpoint(OpenStack:VIM)
        os_endpoint = base.JobAutoBase().get_os_endpoint_vim(
                                                pod_id,
                                                '',
                                                nal_tenant_id)

        # List Networks
        os_network_list = osc_networks.list_networks(os_endpoint)

        for os_network in os_network_list['networks']:
            if os_network['name'] == network_name:
                network_id = os_network['id']
                break

        # Create Subnet
        os_subnet_cre = os_subnets_instance.create_subnet(
                                            os_endpoint,
                                            network_id,
                                            '2001:DB1::/48',
                                            '',
                                            nal_tenant_id,
                                            base.JobAutoBase().utils.IP_VER_V6,
                                            )
        subnet_id_ipv6 = os_subnet_cre['subnet']['id']

        return subnet_id_ipv6

    def delete_os_subnet_ipv6(self, pod_id, nal_tenant_id, subnet_id):

        # Create Instance(OpenStack Client)
        os_subnets_instance = subnets.OscQuantumSubnets(config.JobConfig())

        # Get Endpoint(OpenStack:VIM)
        os_endpoint = base.JobAutoBase().get_os_endpoint_vim(
                                                pod_id,
                                                '',
                                                nal_tenant_id)

        # Delete Subnet
        os_subnets_instance.delete_subnet(os_endpoint, subnet_id)

    def exec_through_fortigate(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_pub='',
                                          fixed_ip_v6_ext='',
                                          is_subnet_ipv6=False):

        device_type = '1'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['vdom_name'] = 'vdom_name'
        job_input['admin_prof_name'] = 'admin_prof_name123'
        job_input['user_account_id'] = 'user_account_id123'
        job_input['account_password'] = 'account_password123'

        create_output = self.main_create_pfw(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        pod_id = create_output['pod_id']
        nal_tenant_id = create_output['nal_tenant_id']

        if is_subnet_ipv6:
            subnet_id_ipv6_pub = self.create_os_subnet_ipv6(
                            'pub_lan', pod_id, nal_tenant_id)
            subnet_id_ipv6_ext = self.create_os_subnet_ipv6(
                            'ext_lan', pod_id, nal_tenant_id)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        create_output = self.main_port_create_pfw(job_input)

        # Get port_id from create process
        port_id = create_output['port_id4']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = fixed_ip_v6_pub

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = fixed_ip_v6_ext

        self.main_ipv6_add_pfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_port_delete_pfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_pfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_pub)
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_ext)

    def exec_through_paloalto(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_pub='',
                                          fixed_ip_v6_ext='',
                                          is_subnet_ipv6=False):

        device_type = '2'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['vsys_name'] = 'vsys_name'
        job_input['zone_name'] = 'zone_name'
        job_input['admin_id'] = 'admin_id'
        job_input['admin_pw'] = 'admin_pw'

        create_output = self.main_create_pfw(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        pod_id = create_output['pod_id']
        nal_tenant_id = create_output['nal_tenant_id']

        if is_subnet_ipv6:
            subnet_id_ipv6_pub = self.create_os_subnet_ipv6(
                            'pub_lan', pod_id, nal_tenant_id)
            subnet_id_ipv6_ext = self.create_os_subnet_ipv6(
                            'ext_lan', pod_id, nal_tenant_id)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['zone_name'] = 'zone_name_puls'

        create_output = self.main_port_create_pfw(job_input)

        # Get port_id from create process
        port_id = create_output['port_id4']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = fixed_ip_v6_pub

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = fixed_ip_v6_ext

        self.main_ipv6_add_pfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_port_delete_pfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_pfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_pub)
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_ext)

    def exec_through_fortigate_share(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_pub='',
                                          fixed_ip_v6_ext='',
                                          is_subnet_ipv6=False):

        device_type = '3'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['vdom_name'] = 'vdom_name'
        job_input['admin_prof_name'] = 'admin_prof_name123'
        job_input['user_account_id'] = 'user_account_id123'
        job_input['account_password'] = 'account_password123'

        create_output = self.main_create_pfw(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        pod_id = create_output['pod_id']
        nal_tenant_id = create_output['nal_tenant_id']

        if is_subnet_ipv6:
            subnet_id_ipv6_pub = self.create_os_subnet_ipv6(
                            'pub_lan', pod_id, nal_tenant_id)
            subnet_id_ipv6_ext = self.create_os_subnet_ipv6(
                            'ext_lan', pod_id, nal_tenant_id)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        create_output = self.main_port_create_pfw(job_input)

        # Get port_id from create process
        port_id = create_output['port_id4']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = fixed_ip_v6_pub

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = fixed_ip_v6_ext

        self.main_ipv6_add_pfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_port_delete_pfw(job_input)

        # Create a second machine
        # Create input data
        job_input_2 = copy.deepcopy(JOB_INPUT_CREATE)
        job_input_2['IaaS_network_type'] = iaas_network_type
        job_input_2['IaaS_tenant_id'] = 'IaaS_tenant_id_002'
        job_input_2['IaaS_tenant_name'] = 'IaaS_tenant_name_BBB'
        job_input_2['device_type'] = device_type
        job_input_2['vdom_name'] = 'vdom_name'
        job_input_2['admin_prof_name'] = 'admin_prof_name123'
        job_input_2['user_account_id'] = 'user_account_id123'
        job_input_2['account_password'] = 'account_password123'

        create_output = self.main_create_pfw(job_input_2)

        # Get node_id from create process
        node_id2 = create_output['node_id']
        apl_table_rec_id2 = create_output['apl_table_rec_id']

        # Delete a second machine
        # Create input data
        job_input_2 = copy.deepcopy(JOB_INPUT_DELETE)
        job_input_2['IaaS_tenant_id'] = 'IaaS_tenant_id_002'
        job_input_2['IaaS_tenant_name'] = 'IaaS_tenant_name_BBB'
        job_input_2['device_type'] = device_type
        job_input_2['node_id'] = node_id2
        job_input_2['apl_table_rec_id'] = apl_table_rec_id2

        self.main_delete_pfw(job_input_2)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_pfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_pub)
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_ext)

    def exec_through_paloalto_share(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_pub='',
                                          fixed_ip_v6_ext='',
                                          is_subnet_ipv6=False):

        device_type = '4'

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['vsys_name'] = 'vsys_name'
        job_input['zone_name'] = 'zone_name'
        job_input['admin_id'] = 'admin_id'
        job_input['admin_pw'] = 'admin_pw'

        create_output = self.main_create_pfw(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        pod_id = create_output['pod_id']
        nal_tenant_id = create_output['nal_tenant_id']

        if is_subnet_ipv6:
            subnet_id_ipv6_pub = self.create_os_subnet_ipv6(
                            'pub_lan', pod_id, nal_tenant_id)
            subnet_id_ipv6_ext = self.create_os_subnet_ipv6(
                            'ext_lan', pod_id, nal_tenant_id)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['zone_name'] = 'zone_name_puls'

        create_output = self.main_port_create_pfw(job_input)

        # Get port_id from create process
        port_id = create_output['port_id4']

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = fixed_ip_v6_pub

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = fixed_ip_v6_ext

        self.main_ipv6_add_pfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_port_delete_pfw(job_input)

        # Create a second machine
        # Create input data
        job_input_2 = copy.deepcopy(JOB_INPUT_CREATE)
        job_input_2['IaaS_network_type'] = iaas_network_type
        job_input_2['IaaS_tenant_id'] = 'IaaS_tenant_id_002'
        job_input_2['IaaS_tenant_name'] = 'IaaS_tenant_name_BBB'
        job_input_2['device_type'] = device_type
        job_input_2['vsys_name'] = 'vsys_name'
        job_input_2['zone_name'] = 'zone_name'
        job_input_2['admin_id'] = 'admin_id'
        job_input_2['admin_pw'] = 'admin_pw'

        create_output = self.main_create_pfw(job_input_2)

        # Get node_id from create process
        node_id2 = create_output['node_id']
        apl_table_rec_id2 = create_output['apl_table_rec_id']

        # Delete a second machine
        # Create input data
        job_input_2 = copy.deepcopy(JOB_INPUT_DELETE)
        job_input_2['IaaS_tenant_id'] = 'IaaS_tenant_id_002'
        job_input_2['IaaS_tenant_name'] = 'IaaS_tenant_name_BBB'
        job_input_2['device_type'] = device_type
        job_input_2['node_id'] = node_id2
        job_input_2['apl_table_rec_id'] = apl_table_rec_id2

        self.main_delete_pfw(job_input_2)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_pfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_pub)
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_ext)

    def main_create_pfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], job_input['IaaS_tenant_id'])

        # initialize_create_pnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_create_pnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 3)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('node_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')

        # get_or_create_pod_tenant
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_or_create_pod_tenant(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['nal_tenant_name'],
                         job_input['IaaS_tenant_name'])

        # physical_pub_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().physical_pub_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('port_id2' in job_output)

        # physical_ext_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().physical_ext_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('port_id3' in job_output)
        self.assertTrue('global_ip' in job_output)

        # physical_fw_tenant_vlan_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            physical_fw_tenant_vlan_port_create(job_input)

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
            # device_setup_create_for_fortigate
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_create_for_fortigate(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2',):
            # device_setup_create_for_paloalto
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_create_for_paloalto(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # device_setup_create_for_fortigate_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_create_for_fortigate_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # device_setup_create_for_paloalto_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                device_setup_create_for_paloalto_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        else:
            pass

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

    def main_port_create_pfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

        # initialize
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '2')
        self.assertEqual(job_output['type'], '1')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '1')

        # physical_fw_tenant_vlan_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
            .physical_fw_tenant_vlan_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('port_id4' in job_output)

        if job_input['device_type'] in ('1',):
            # msa_configuration_create_for_fortigate
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_create_for_fortigate(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2',):
            # msa_configuration_create_for_paloalto
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_create_for_paloalto(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # msa_configuration_create_for_fortigate_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_create_for_fortigate_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # msa_configuration_create_for_paloalto_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_create_for_paloalto_share(job_input)

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

    def main_ipv6_add_pfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

        # initialize
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '2')
        self.assertEqual(job_output['type'], '1')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '1')

        # physical_pub_port_add_ipv6
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
            .physical_pub_port_add_ipv6(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('port_id_pub_ipv6' in job_output)

        # physical_ext_port_add_ipv6
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
            .physical_ext_port_add_ipv6(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('port_id_ext_ipv6' in job_output)

        # physical_fw_tenant_vlan_port_add_ipv6
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                       .physical_fw_tenant_vlan_port_add_ipv6(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('network_address_ipv6' in job_output)

        if job_input['device_type'] in ('1'):
            # device_setup_add_ipv6_for_fortigate
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_add_ipv6_for_fortigate(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2'):
            # device_setup_add_ipv6_for_paloalto
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_add_ipv6_for_paloalto(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3'):
            # device_setup_add_ipv6_for_fortigate_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_add_ipv6_for_fortigate_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4'):
            # device_setup_add_ipv6_for_paloalto_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_add_ipv6_for_paloalto_share(job_input)

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

    def main_port_delete_pfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

        # initialize
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '2')
        self.assertEqual(job_output['type'], '1')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '1')

        if job_input['device_type'] in ('1',):
            # msa_configuration_delete_for_fortigate
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_delete_for_fortigate(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2',):
            # msa_configuration_delete_for_paloalto
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_delete_for_paloalto(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # msa_configuration_delete_for_fortigate_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_delete_for_fortigate_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # msa_configuration_delete_for_paloalto_share
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_delete_for_paloalto_share(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        else:
            pass

        # physical_fw_tenant_vlan_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            physical_fw_tenant_vlan_port_delete(job_input)

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

    def main_delete_pfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], job_input['IaaS_tenant_id'])

        # initialize_delete_pnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_delete_pnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '2')
        self.assertEqual(job_output['type'], '1')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '1')

        # get_pod_tenant
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_pod_tenant(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['nal_tenant_name'], job_input['IaaS_tenant_name'])

        job_input.update(job_output)
        if job_input['device_type'] == '1':

            # device_setup_delete_for_fortigate
            job_output = method.JobAutoMethod()\
                            .device_setup_delete_for_fortigate(job_input)

        elif job_input['device_type'] in ('2',):

            # device_setup_delete_for_paloalto
            job_output = method.JobAutoMethod()\
                        .device_setup_delete_for_paloalto(job_input)

        elif job_input['device_type'] == '3':

            # device_setup_delete_for_fortigate_share
            job_output = method.JobAutoMethod()\
                        .device_setup_delete_for_fortigate_share(job_input)

        elif job_input['device_type'] in ('4',):

            # device_setup_delete_for_paloalto_share
            job_output = method.JobAutoMethod()\
                        .device_setup_delete_for_paloalto_share(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # msa_setup_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().msa_setup_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # physical_pub_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().physical_pub_port_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # physical_ext_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().physical_ext_port_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # physical_fw_tenant_vlan_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            physical_fw_tenant_vlan_port_delete(job_input)

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
