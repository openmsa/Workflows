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


class TestAutoDcCreateAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):

        # Establish a clean test environment.
        super(TestAutoDcCreateAPI, self).setUp()

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_pod = \
            base.JobAutoBase()\
            .get_db_endpoint(config.JobConfig().REST_URI_POD)
        db_endpoint_msa_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_global_ip = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_GLOBAL_IP)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)
        db_endpoint_dc_segment = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_WIM_DC_SEGMENT_MNG)

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['pod_id'] = 'pod0002'
        params['use_type'] = 2
        params['ops_version'] = 1
        params['weight'] = '50'
        db_create.set_context(db_endpoint_pod, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['pod_id'] = 'pod_unit_test1'
        params['use_type'] = 3
        params['ops_version'] = 1
        params['weight'] = '60'
        db_create.set_context(db_endpoint_pod, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['status'] = 0
        params['network_address'] = '10.20.0.0'
        params['netmask'] = '24'
        params['vlan_id'] = 'vlan_id_0000_1111_2222'
        db_create.set_context(db_endpoint_msa_vlan, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['global_ip'] = '192.168.80.245'
        params['status'] = 0
        db_create.set_context(db_endpoint_global_ip, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_firefly_001'
        params['type'] = 3
        params['device_type'] = 1
        params['type_detail'] = ""
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_cisco_001'
        params['type'] = 3
        params['device_type'] = 2
        params['type_detail'] = 1
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_cisco_002'
        params['type'] = 3
        params['device_type'] = 2
        params['type_detail'] = 1
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_cisco_003'
        params['type'] = 3
        params['device_type'] = 2
        params['type_detail'] = 1
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_cisco_004'
        params['type'] = 3
        params['device_type'] = 2
        params['type_detail'] = 1
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_cisco_tunnel_esp_001'
        params['type'] = 3
        params['device_type'] = 2
        params['type_detail'] = 1
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_cisco_tunnel_esp_002'
        params['type'] = 3
        params['device_type'] = 2
        params['type_detail'] = 1
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_cisco_tunnel_ah_001'
        params['type'] = 3
        params['device_type'] = 2
        params['type_detail'] = 1
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['license'] = 'test_license_cisco_tunnel_ah_002'
        params['type'] = 3
        params['device_type'] = 2
        params['type_detail'] = 1
        params['status'] = 0
        db_create.set_context(db_endpoint_license, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['dc_id'] = 'dc01'
        params['group_id'] = ''
        params['ce01_ip_address'] = '100.112.0.1'
        params['ce02_ip_address'] = '100.112.0.2'
        params['network_address'] = '100.112.0.0'
        params['netmask'] = 16
        params['next_hop'] = '100.107.1.254'
        params['status'] = 0
        db_create.set_context(db_endpoint_dc_segment, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['dc_id'] = 'dc02'
        params['group_id'] = ''
        params['ce01_ip_address'] = '100.113.0.1'
        params['ce02_ip_address'] = '100.113.0.2'
        params['network_address'] = '100.113.0.0'
        params['netmask'] = 16
        params['next_hop'] = '100.107.2.254'
        params['status'] = 0
        db_create.set_context(db_endpoint_dc_segment, params)
        db_create.execute()

        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['update_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0
        params['dc_id'] = 'dc03'
        params['group_id'] = ''
        params['ce01_ip_address'] = '100.114.0.1'
        params['ce02_ip_address'] = '100.114.0.2'
        params['network_address'] = '100.114.0.0'
        params['netmask'] = 16
        params['next_hop'] = '100.107.3.254'
        params['status'] = 0
        db_create.set_context(db_endpoint_dc_segment, params)
        db_create.execute()

    def tearDown(self):

        """Clear the test environment"""
        super(TestAutoDcCreateAPI, self).tearDown()

        # Create Instance(DB Client)
        db_list = list.ListClient(config.JobConfig())
        db_delete = delete.DeleteClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_APL)
        db_endpoint_pod = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_POD)
        db_endpoint_port = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PORT)
        db_endpoint_msa_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_global_ip = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_GLOBAL_IP)
        db_endpoint_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)
        db_endpoint_dc_segment = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_WIM_DC_SEGMENT_MNG)
        db_endpoint_dc_member = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_WIM_DC_CON_MEMBER)
        db_endpoint_dc_group = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_WIM_DC_CON_GROUP)

        # Delete from NAL_APL_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        delete_apl_list = db_list.get_return_param()

        for delete_apl in delete_apl_list:
            key = delete_apl['ID']
            db_delete.set_context(db_endpoint_apl, [key])
            db_delete.execute()

        # Delete from NAL_POD_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_pod, params)
        db_list.execute()
        delete_pod_list = db_list.get_return_param()

        for delete_pod in delete_pod_list:
            key = delete_pod['ID']
            db_delete.set_context(db_endpoint_pod, [key])
            db_delete.execute()

        # Delete from NAL_PORT_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        delete_port_list = db_list.get_return_param()

        for delete_port in delete_port_list:
            key = delete_port['ID']
            db_delete.set_context(db_endpoint_port, [key])
            db_delete.execute()

        # Delete from NAL_MSA_VLAN_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'
        params['delete_flg'] = 0

        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        delete_msa_vlan_list = db_list.get_return_param()

        for delete_msa_vlan in delete_msa_vlan_list:
            key = delete_msa_vlan['ID']
            db_delete.set_context(db_endpoint_msa_vlan, [key])
            db_delete.execute()

        # Delete from NAL_GLOBAL_IP_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_global_ip, params)
        db_list.execute()
        delete_global_ip_list = db_list.get_return_param()

        for delete_global_ip in delete_global_ip_list:
            key = delete_global_ip['ID']
            db_delete.set_context(db_endpoint_global_ip, [key])
            db_delete.execute()

        # Delete from NAL_VIRTUAL_LAN_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        delete_vlan_list = db_list.get_return_param()

        for delete_vlan in delete_vlan_list:
            key = delete_vlan['ID']
            db_delete.set_context(db_endpoint_vlan, [key])
            db_delete.execute()

        # Delete from NAL_LICENSE_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        delete_license_list = db_list.get_return_param()

        for delete_license in delete_license_list:
            key = delete_license['ID']
            db_delete.set_context(db_endpoint_license, [key])
            db_delete.execute()

        # Delete from WIM_DC_SEGMENT_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_dc_segment, params)
        db_list.execute()
        delete_segment_list = db_list.get_return_param()

        for delete_segment in delete_segment_list:
            key = delete_segment['ID']
            db_delete.set_context(db_endpoint_dc_segment, [key])
            db_delete.execute()

        # Delete from WIM_DC_CONNECT_MEMBER_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_dc_member, params)
        db_list.execute()
        delete_dc_member_list = db_list.get_return_param()

        for delete_dc_member in delete_dc_member_list:
            key = delete_dc_member['ID']
            db_delete.set_context(db_endpoint_dc_member, [key])
            db_delete.execute()

        # Delete from WIM_DC_CONNECT_GROUP_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_dc_group, params)
        db_list.execute()
        delete_dc_group_list = db_list.get_return_param()

        for delete_dc_group in delete_dc_group_list:
            key = delete_dc_group['ID']
            db_delete.set_context(db_endpoint_dc_group, [key])
            db_delete.execute()

    def delete_nal_db(self):

        # Create Instance(DB Client)
        db_list = list.ListClient(config.JobConfig())
        db_delete = delete.DeleteClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_apl = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_APL)
        db_endpoint_port = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_PORT)
        db_endpoint_global_ip = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_GLOBAL_IP)
        db_endpoint_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)

        # Delete from NAL_APL_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        delete_apl_list = db_list.get_return_param()

        for delete_apl in delete_apl_list:
            key = delete_apl['ID']
            db_delete.set_context(db_endpoint_apl, [key])
            db_delete.execute()

        # Delete from NAL_PORT_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        delete_port_list = db_list.get_return_param()

        for delete_port in delete_port_list:
            key = delete_port['ID']
            db_delete.set_context(db_endpoint_port, [key])
            db_delete.execute()

        # Delete from NAL_GLOBAL_IP_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_global_ip, params)
        db_list.execute()
        delete_global_ip_list = db_list.get_return_param()

        for delete_global_ip in delete_global_ip_list:
            key = delete_global_ip['ID']
            db_delete.set_context(db_endpoint_global_ip, [key])
            db_delete.execute()

        # Delete from NAL_VIRTUAL_LAN_MNG
        params = {}
        params['create_id'] = 'TestAutoDcUser'

        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        delete_vlan_list = db_list.get_return_param()

        for delete_vlan in delete_vlan_list:
            key = delete_vlan['ID']
            db_delete.set_context(db_endpoint_vlan, [key])
            db_delete.execute()

    def test_dc_create_firefly(self):
        self.execute_create_dc_connect('dc01', '1', '1')
        self.delete_nal_db()
        self.execute_create_dc_connect('dc02', '1', '1')
        self.execute_delete_dc_connect('dc02', '1', '1')

    def test_dc_create_csr1000v(self):
        self.execute_create_dc_connect('dc01', '2', '2', 'VXLAN', '1')
        self.delete_nal_db()
        self.execute_create_dc_connect('dc02', '2', '2', 'VXLAN', '1')
        self.execute_delete_dc_connect('dc02', '2', '2')

    def test_dc_create_csr1000v_tunnel_esp(self):
        self.execute_create_dc_connect('dc01', '2', '3', 'VXLAN', '1')
        self.delete_nal_db()
        self.execute_create_dc_connect('dc02', '2', '3', 'VXLAN', '1')
        self.execute_delete_dc_connect('dc02', '2', '3')

    def test_dc_create_csr1000v_tunnel_ah(self):
        self.execute_create_dc_connect('dc01', '2', '4', 'VXLAN', '1')
        self.delete_nal_db()
        self.execute_create_dc_connect('dc02', '2', '4', 'VXLAN', '1')
        self.execute_delete_dc_connect('dc02', '2', '4')

    def execute_create_dc_connect(self, dc_id, device_type,
                                  group_type,
                                  network_type='VXLAN', bandwidth=''):

        # Input Params
        job_input = {}
        job_input['dc_id'] = dc_id
        job_input['apl_type'] = 1
        job_input['type'] = 3
        job_input['device_type'] = device_type
        job_input['service_type'] = group_type
        job_input['IaaS_network_type'] = network_type
        job_input['IaaS_network_id'] = 'd6680829-59a5-484b-98c2-36c8849ec8bc'
        job_input['IaaS_region_id'] = 'region_unit_test1'
        job_input['IaaS_segmentation_id'] = '10'
        job_input['IaaS_subnet_id'] = '6c1857dc07435b30bdeaa4c350337f0a'
        job_input['IaaS_tenant_id'] = '1de3cf1741674a0dadd15affdb2ffae2'
        job_input['IaaS_tenant_name'] = 'nal_tenant_test'
        job_input['IaaS_network_name'] = 'nal_nw_test'
        job_input['network_name'] = 'nal_test_net'
        job_input['operation_id'] = 'TestAutoDcUser'
        job_input['fw_ip_address'] = '10.0.0.1'
        job_input['service_name'] = 'dc_group_unit_test'

        job_input['dns_server_ip_address'] = '10.59.70.151'
        job_input['ntp_server_ip_address'] = '10.59.70.152'

        if len(bandwidth) > 0:
            job_input['bandwidth'] = bandwidth

        # Prepare
        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'],
                                            job_input['IaaS_tenant_id'])

        # routing_pod
        job_input.update(job_output)
        job_output = method.JobAutoMethod().routing_pod(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')

        # get_or_create_pod_tenant
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                                    .get_or_create_pod_tenant(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertTrue('nal_tenant_name' in job_output)
        self.assertGreaterEqual(len(job_output['nal_tenant_id']), 1)

        # virtual_rt_msa_lan_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                                        .virtual_rt_msa_lan_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('msa_network_info' in job_output)

        # msa_customer_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().msa_customer_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('msa_customer_id' in job_output)

        if group_type in ['2', '3', '4']:
            # license_assign_csr1000v
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                                .license_assign_csr1000v(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)

        # virtual_rt_tenant_vlan_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                                .virtual_rt_tenant_vlan_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 3)
        self.assertTrue('vrrp' in job_output)
        self.assertTrue('ce01' in job_output)
        self.assertTrue('ce02' in job_output)

        # set_job_return_data_virtual_rt_connect_prepare
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                    .set_job_return_data_virtual_rt_connect_prepare(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('job_ret_data' in job_output)

        # get_job_return_value
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_job_return_value(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('data' in job_output)
        self.assertTrue('result' in job_output)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')

        # Connect
        # virtual_rt_dc_member_create_info
        job_input = job_output['data']
        job_output = method.JobAutoMethod()\
                                .virtual_rt_dc_member_create_info(job_input)

        # Assertion
        self.assertEqual(len(job_output), 6)
        self.assertTrue('dc_name' in job_output)
        self.assertTrue('group_id' in job_output)
        self.assertTrue('group_rec_id' in job_output)
        self.assertTrue('dc_member_list' in job_output)
        self.assertTrue('dc_vlan_id' in job_output)
        self.assertTrue('wan_allocation_info' in job_output)

        # virtual_rt_wan_vlan_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
                                virtual_rt_wan_vlan_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('wan_network_id' in job_output)
        self.assertTrue('virtual_lan_list' in job_output)

        job_input.update(job_output)
        if group_type == '1':
            # virtual_rt_port_create
            job_output = method.JobAutoMethod()\
                                .virtual_rt_port_create(job_input)

        elif group_type == '2':
            # virtual_rt_port_create_csr1000v
            job_output = method.JobAutoMethod()\
                            .virtual_rt_port_create_csr1000v(job_input)

        else:
            # virtual_rt_port_create_csr1000v_for_tunnel
            job_output = method.JobAutoMethod()\
                    .virtual_rt_port_create_csr1000v_for_tunnel(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('msa_wan_port_info' in job_output)

        job_input.update(job_output)
        if group_type == '1':
            # virtual_rt_server_create_firefly
            job_output = method.JobAutoMethod()\
                                .virtual_rt_server_create_firefly(job_input)

            # Assertion
            self.assertEqual(len(job_output), 5)
            self.assertTrue('server_id' in job_output)
            self.assertTrue('apl_wk' in job_output)
            self.assertTrue('msa_port_wk' in job_output)
            self.assertTrue('wan_port_wk' in job_output)
            self.assertTrue('tenant_lan_port_wk' in job_output)

        elif group_type in ['2', '3', '4']:
            # virtual_rt_server_create_csr1000v
            job_output = method.JobAutoMethod()\
                                .virtual_rt_server_create_csr1000v(job_input)

            # Assertion
            self.assertEqual(len(job_output), 5)
            self.assertTrue('server_id' in job_output)
            self.assertTrue('apl_wk' in job_output)
            self.assertTrue('msa_port_wk' in job_output)
            self.assertTrue('wan_port_wk' in job_output)
            self.assertTrue('tenant_lan_port_wk' in job_output)

        # virtual_rt_msa_setup
        job_input.update(job_output)
        job_output = method.JobAutoMethod().virtual_rt_msa_setup(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('apl_wk' in job_output)

        job_input.update(job_output)
        if group_type == '1':
            # virtual_rt_device_setup_create_firefly
            job_output = method.JobAutoMethod()\
                            .virtual_rt_device_setup_create_firefly(job_input)

            # Assertion
            self.assertEqual(len(job_output), 4)
            self.assertTrue('virtual_apl_list' in job_output)
            self.assertTrue('apl_port_list' in job_output)
            self.assertTrue('update_apl_port_list' in job_output)
            self.assertTrue('ce_info' in job_output)

        elif group_type in ['2']:
            # virtual_rt_device_setup_create_csr1000v
            job_output = method.JobAutoMethod()\
                        .virtual_rt_device_setup_create_csr1000v(job_input)

            # Assertion
            self.assertEqual(len(job_output), 5)
            self.assertTrue('apl_wk' in job_output)
            self.assertTrue('msa_port_wk' in job_output)
            self.assertTrue('wan_port_wk' in job_output)
            self.assertTrue('tenant_lan_port_wk' in job_output)
            self.assertTrue('ce_info' in job_output)

        elif group_type in ['3', '4']:
            # virtual_rt_device_setup_create_csr1000v_for_tunnel
            job_output = method.JobAutoMethod()\
                .virtual_rt_device_setup_create_csr1000v_for_tunnel(job_input)

            # Assertion
            self.assertEqual(len(job_output), 5)
            self.assertTrue('apl_wk' in job_output)
            self.assertTrue('msa_port_wk' in job_output)
            self.assertTrue('wan_port_wk' in job_output)
            self.assertTrue('tenant_lan_port_wk' in job_output)
            self.assertTrue('ce_info' in job_output)

        if group_type in ['2', '3', '4']:
            # virtual_rt_device_setup_create_csr1000v_extra
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                    .virtual_rt_device_setup_create_csr1000v_extra(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertTrue('apl_wk' in job_output)

            # virtual_rt_msa_license_create_csr1000v
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                    .virtual_rt_msa_license_create_csr1000v(job_input)

            # Assertion
            self.assertEqual(len(job_output), 4)
            self.assertTrue('virtual_apl_list' in job_output)
            self.assertTrue('apl_port_list' in job_output)
            self.assertTrue('update_apl_port_list' in job_output)
            self.assertTrue('ce_info' in job_output)

        job_input.update(job_output)
        if group_type == '1':
            # virtual_rt_dc_connect_firefly
            job_output = method.JobAutoMethod()\
                            .virtual_rt_dc_connect_firefly(job_input)
        elif group_type in ['2']:
            # virtual_rt_dc_connect_csr1000v
            job_output = method.JobAutoMethod()\
                        .virtual_rt_dc_connect_csr1000v(job_input)

        elif group_type in ['3', '4']:
            # virtual_rt_dc_connect_csr1000v_for_tunnel
            job_output = method.JobAutoMethod()\
                        .virtual_rt_dc_connect_csr1000v_for_tunnel(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # set_job_return_data_virtual_rt_connect_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                    .set_job_return_data_virtual_rt_connect_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('job_ret_data' in job_output)

        # get_job_return_value
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_job_return_value_wim(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('data' in job_output)
        self.assertTrue('result' in job_output)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')

        # Finalize
        # virtual_rt_dc_finalize_connect
        job_input = {}
        job_input['data'] = job_output['data']
        job_output = method.JobAutoMethod()\
                                .virtual_rt_dc_finalize_connect(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # get_job_return_value
        job_output = method.JobAutoMethod()\
                                .get_job_return_value({})

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('data' in job_output)
        self.assertTrue('result' in job_output)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')
        self.assertEqual(job_output['data'], {})

    def execute_delete_dc_connect(self, dc_id, device_type, group_type):

        # Input Params
        job_input = {}
        job_input['dc_id'] = dc_id
        job_input['device_type'] = device_type
        job_input['service_type'] = group_type
        job_input['IaaS_region_id'] = 'region_unit_test1'
        job_input['IaaS_subnet_id'] = '6c1857dc07435b30bdeaa4c350337f0a'
        job_input['IaaS_tenant_id'] = '1de3cf1741674a0dadd15affdb2ffae2'
        job_input['operation_id'] = 'TestAutoDcUser'

        # Prepare
        # get_nal_tenant_name
        job_output = method.JobAutoMethod().get_nal_tenant_name(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'],
                                            job_input['IaaS_tenant_id'])

        # virtual_rt_dc_connected_info_get
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                            .virtual_rt_dc_connected_info_get(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertTrue('pod_id' in job_output)
        self.assertTrue('apl_type' in job_output)
        self.assertTrue('type' in job_output)
        self.assertTrue('apl_info' in job_output)
        self.assertTrue('tenant_lan_list' in job_output)
        self.assertTrue('wan_lan_list' in job_output)
        self.assertTrue('pub_port_list' in job_output)
        self.assertTrue('msa_network_id' in job_output)

        # set_job_return_data_virtual_rt_disconnect_prepare
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                .set_job_return_data_virtual_rt_disconnect_prepare(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('job_ret_data' in job_output)

        # get_job_return_value
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_job_return_value(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('data' in job_output)
        self.assertTrue('result' in job_output)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')

        # DisConnect
        # virtual_rt_dc_member_delete_info
        job_input.update(job_output['data'])
        job_output = method.JobAutoMethod()\
                                .virtual_rt_dc_member_delete_info(job_input)

        # Assertion
        self.assertEqual(len(job_output), 7)
        self.assertTrue('group_rec_id' in job_output)
        self.assertTrue('group_id' in job_output)
        self.assertTrue('dc_vlan_rec_id' in job_output)
        self.assertTrue('dc_segment_rec_id' in job_output)
        self.assertTrue('dc_member_count' in job_output)
        self.assertTrue('dc_member_myself_list' in job_output)
        self.assertTrue('dc_member_other_list' in job_output)

        job_input.update(job_output)
        if group_type == '1':
            # virtual_rt_dc_disconnect_firefly
            job_output = method.JobAutoMethod()\
                                .virtual_rt_dc_disconnect_firefly(job_input)
        elif group_type in ['2']:
            # virtual_rt_dc_disconnect_csr1000v
            job_output = method.JobAutoMethod()\
                                .virtual_rt_dc_disconnect_csr1000v(job_input)

        elif group_type in ['3', '4']:
            # virtual_rt_dc_disconnect_csr1000v_for_tunnel
            job_output = method.JobAutoMethod()\
                    .virtual_rt_dc_disconnect_csr1000v_for_tunnel(job_input)

        # Assertion
        self.assertEqual(job_output, {})

        if group_type in ['2', '3', '4']:
            # virtual_rt_msa_license_delete_csr1000v
            job_output = method.JobAutoMethod()\
                    .virtual_rt_msa_license_delete_csr1000v(job_input)

            # Assertion
            self.assertEqual(job_output, {})

        # virtual_rt_msa_setup_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                                    .virtual_rt_msa_setup_delete(job_input)

        # Assertion
        self.assertEqual(job_output, {})

        # virtual_rt_tenant_vlan_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                                .virtual_rt_tenant_vlan_port_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('logical_delete_apl_port_list' in job_output)

        # virtual_rt_wan_vlan_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                                .virtual_rt_wan_vlan_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('logical_delete_apl_port_list' in job_output)
        self.assertTrue('logical_delete_vlan_list' in job_output)

        # virtual_rt_msa_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                                .virtual_rt_msa_port_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('logical_delete_apl_port_list' in job_output)

        # virtual_rt_server_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                                .virtual_rt_server_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('logical_delete_apl_list' in job_output)

        # virtual_rt_dc_member_vlan_group_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                    .virtual_rt_dc_member_vlan_group_delete(job_input)

        # Assertion
        self.assertEqual(job_output, {})

        # set_job_return_data_virtual_rt_disconnect_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                .set_job_return_data_virtual_rt_disconnect_delete(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('job_ret_data' in job_output)

        # get_job_return_value
        job_input.update(job_output)
        job_output = method.JobAutoMethod().get_job_return_value_wim(job_input)

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('data' in job_output)
        self.assertTrue('result' in job_output)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')

        # Finalize
        # virtual_rt_tenant_vlan_port_iaas_delete
        job_input = {}
        job_input['data'] = job_output['data']
        job_output = method.JobAutoMethod()\
                        .virtual_rt_tenant_vlan_port_iaas_delete(job_input)

        # Assertion
        self.assertEqual(job_output, {})

        if group_type in ['2', '3', '4']:
            # license_withdraw_csr1000v
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                                    .license_withdraw_csr1000v(job_input)

            # Assertion
            self.assertEqual(job_output, {})

        # virtual_rt_dc_finalize_disconnect
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                    .virtual_rt_dc_finalize_disconnect(job_input)

        # Assertion
        self.assertEqual(job_output, {})

        # get_job_return_value
        job_output = method.JobAutoMethod()\
                                .get_job_return_value({})

        # Assertion
        self.assertEqual(len(job_output), 2)
        self.assertTrue('data' in job_output)
        self.assertTrue('result' in job_output)
        self.assertEqual(job_output['result']['status'], 0)
        self.assertEqual(job_output['result']['error-code'], '')
        self.assertEqual(job_output['result']['message'], '')
        self.assertEqual(job_output['data'], {})
