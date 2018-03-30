import copy
import datetime
import ipaddress
import json
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
from job.auto import base
from job.auto import method
from job.conf import config
from job.lib.db import create
from job.lib.db import delete
from job.lib.db import list
from job.lib.db import update
from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import subnets

JOB_INPUT_CREATE = {
    'operation_id': 'test_nw_automation_user_001',
    'IaaS_tenant_id': 'IaaS_tenant_id_001',
    'IaaS_tenant_name': 'IaaS_tenant_name_AAA',
    'IaaS_region_id': 'region_unit_test1',
    'apl_type': '1',
    'type': '1',
    'network_name': 'network_name_AAA',
    'IaaS_network_type': 'VLAN',
    'IaaS_network_id': 'd6680829-59a5-484b-98c2-36c8849ec8bc',
    'IaaS_subnet_id': '6c1857dc07435b30bdeaa4c350337f0a',
    'IaaS_segmentation_id': '10',
    'description': 'aaaaaa',
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
    'IaaS_segmentation_id': '10',
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
    'IaaS_network_type': 'vlan',
    'IaaS_segmentation_id': '10',
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


class TestAutoVfwThrough(unittest.TestCase):
    # Do a test of Select.

    def setUp(self):
        # Establish a clean test environment.
        super(TestAutoVfwThrough, self).setUp()

        # Create Instance(DB Client)
        db_create = create.CreateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_pod = \
            base.JobAutoBase().get_db_endpoint(config.JobConfig().REST_URI_POD)
        db_endpoint_msa_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_MSA_VLAN)
        db_endpoint_global_ip = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_GLOBAL_IP)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)
        db_endpoint_tenant = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_TENANT)

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
        params['global_ip'] = '192.168.80.245'
        params['status'] = 0
        db_create.set_context(db_endpoint_global_ip, params)
        db_create.execute()

        for device_type in ('1', '2', '3', '4', '5'):
            params = {}
            params['create_id'] = 'test_nw_automation_user_001'
            params['update_id'] = 'test_nw_automation_user_001'
            params['delete_flg'] = 0
            params['license'] = 'test_license_001'
            params['type'] = 1
            params['device_type'] = device_type
            params['status'] = 0
            db_create.set_context(db_endpoint_license, params)
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

    def tearDown(self):
        """Clear the test environment"""
        super(TestAutoVfwThrough, self).tearDown()

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
        db_endpoint_global_ip = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_GLOBAL_IP)
        db_endpoint_vlan = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_VLAN)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)

        # Delete from NAL_APL_MNG
        params = {}
        params['create_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0

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
        params['delete_flg'] = 0

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
        params['delete_flg'] = 0

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
        params['delete_flg'] = 0

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
        params['create_id'] = 'test_nw_automation_user_001'
        params['delete_flg'] = 0

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
        params['delete_flg'] = 0

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
        params['delete_flg'] = 0

        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        delete_license_list = db_list.get_return_param()

        for delete_license in delete_license_list:
            key = delete_license['ID']
            db_delete.set_context(db_endpoint_license, [key])
            db_delete.execute()

    def update_db_license_update_date(self, device_type, hours):

        update_date = (datetime.datetime.now()\
                        - datetime.timedelta(hours=5))\
                        .strftime('%Y-%m-%d %H:%M:%S')

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
        params['type'] = 1
        params['device_type'] = device_type

        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        update_license_list = db_list.get_return_param()

        for update_license in update_license_list:
            keys = [update_license['ID']]
            params = {}
            params['update_date'] = update_date
            db_update.set_context(db_endpoint_license, keys, params)
            db_update.execute()

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
        params['type'] = 1
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

    def create_os_subnet_ipv6(self, vlan_type, pod_id, nal_tenant_id):

        # Get Network Info
        os_network_info = base.JobAutoBase().get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            vlan_type,
                                            base.JobAutoBase().utils.IP_VER_V6)

        network_name = base.JobAutoBase().get_os_vlan_name(vlan_type, 'system')

        if len(os_network_info) == 0:

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

    def test_through_intersec_ext(self):

        # Ext Port(IPv6) Not Exists
        self.exec_through_intersec_ext()
        self.exec_through_intersec_ext('VXLAN',
                                       '2001:DB6::1', '2001:DB7::1')

        # Ext Port(IPv6) Exists
        self.exec_through_intersec_ext('VXLAN', '', '', True)
        self.exec_through_intersec_ext('VXLAN',
                                       '2001:DB8::1', '2001:DB9::1', True)

    def test_through_fortigate_vm(self):

        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_fortigate_vm()
        self.update_db_license_update_date(2, 5)
        self.exec_through_fortigate_vm('VXLAN',
                                       '2001:DB6::1', '2001:DB7::1')
        self.update_db_license_update_date(2, 5)

        # Pub/Ext Port(IPv6) Exists
        self.exec_through_fortigate_vm('VXLAN', '', '', True)
        self.update_db_license_update_date(2, 5)
        self.exec_through_fortigate_vm('VXLAN',
                                       '2001:DB8::1', '2001:DB9::1', True)

    def test_through_paloalto_vm(self):

        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_paloalto_vm()
        self.update_db_license_status(3, 0)
        self.exec_through_paloalto_vm('VXLAN',
                                       '2001:DB6::1', '2001:DB7::1')
        self.update_db_license_status(3, 0)

        # Pub/Ext Port(IPv6) Exists
        self.exec_through_paloalto_vm('VXLAN', '', '', True)
        self.update_db_license_status(3, 0)
        self.exec_through_paloalto_vm('VXLAN',
                                       '2001:DB8::1', '2001:DB9::1', True)

    def test_through_intersec_pub(self):

        # Pub Port(IPv6) Not Exists
        self.exec_through_intersec_pub()
        self.exec_through_intersec_pub('VXLAN', '2001:DB6::1')

        # Pub Port(IPv6) Exists
        self.exec_through_intersec_pub('VXLAN', '', True)
        self.exec_through_intersec_pub('VXLAN', '2001:DB8::1', True)

    def test_through_fortigate_vm_541(self):

        # Pub/Ext Port(IPv6) Not Exists
        self.exec_through_fortigate_vm_541()
        self.update_db_license_update_date(5, 5)
        self.exec_through_fortigate_vm_541('VXLAN',
                                       '2001:DB6::1', '2001:DB7::1')
        self.update_db_license_update_date(5, 5)

        # Pub/Ext Port(IPv6) Exists
        self.exec_through_fortigate_vm_541('VXLAN', '', '', True)
        self.update_db_license_update_date(5, 5)
        self.exec_through_fortigate_vm_541('VXLAN',
                                       '2001:DB8::1', '2001:DB9::1', True)

    def test_through_intersec_ext_license_not_found(self):

        self.exec_through_intersec_ext()

        self.update_db_license_status(1, 2)

        try:
            self.exec_through_intersec_ext()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def test_through_fortigate_vm_license_not_found(self):

        self.exec_through_fortigate_vm()

        try:
            self.exec_through_fortigate_vm()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def test_through_paloalto_vm_license_not_found(self):

        self.exec_through_paloalto_vm()

        try:
            self.exec_through_paloalto_vm()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def test_through_intersec_pub_license_not_found(self):

        self.exec_through_intersec_pub()

        self.update_db_license_status(4, 2)

        try:
            self.exec_through_intersec_pub()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def test_through_fortigate_vm_541_license_not_found(self):

        self.exec_through_fortigate_vm_541()

        try:
            self.exec_through_fortigate_vm_541()

        except SystemError as e:
            if e.args[0] == 'license not found.':
                return
            else:
                raise

        self.assertTrue(False, 'Exception(license not found.) not raised')

    def exec_through_intersec_ext(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_ext='',
                                          static_route_ip_ipv6='',
                                          is_subnet_ipv6=False
                                          ):

        device_type = '1'
        port_id4 = []

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_intersec_ext'
        job_input['webclient_ip'] = '10.58.10.1'
        job_input['ntp_ip'] = '10.58.10.2'
        job_input['zabbix_vip_ip'] = '10.58.10.3'
        job_input['zabbix_01_ip'] = '10.58.10.4'
        job_input['zabbix_02_ip'] = '10.58.10.5'
        job_input['static_route_ip'] = '10.58.10.6'

        create_output = self.main_create_vfw(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        pod_id = create_output['pod_id']
        nal_tenant_id = create_output['nal_tenant_id']

        if is_subnet_ipv6:
            subnet_id_ipv6_ext = self.create_os_subnet_ipv6(
                            'ext_lan', pod_id, nal_tenant_id)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        create_output = self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[0]

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = fixed_ip_v6_ext

        if len(static_route_ip_ipv6) > 0:
            job_input['static_route_ip_ipv6'] = static_route_ip_ipv6

        self.main_ipv6_add_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        create_output = self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[1]

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = str(
                        ipaddress.ip_address(fixed_ip_v6_ext) + 1)

        if len(static_route_ip_ipv6) > 0:
            job_input['static_route_ip_ipv6'] = str(
                    ipaddress.ip_address(static_route_ip_ipv6) + 1)

        self.main_ipv6_add_vfw(job_input)

        for port_id in port_id4:

            # Create input data
            job_input = copy.deepcopy(JOB_INPUT_PORT_DELETE)
            job_input['device_type'] = device_type
            job_input['node_id'] = node_id
            job_input['port_id'] = port_id
            job_input['apl_table_rec_id'] = apl_table_rec_id

            self.main_port_delete_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_ext)

    def exec_through_fortigate_vm(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_pub='',
                                          fixed_ip_v6_ext='',
                                          is_subnet_ipv6=False
                                          ):

        device_type = '2'
        port_id4 = []

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_fortigate_vm'
        job_input['admin_id'] = 'admin_id_001'
        job_input['admin_pw'] = 'admin_pw_123456789'

        create_output = self.main_create_vfw(job_input)

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

        create_output = self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[0]

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = fixed_ip_v6_pub

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = fixed_ip_v6_ext

        self.main_ipv6_add_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        create_output = self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[1]

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = str(
                        ipaddress.ip_address(fixed_ip_v6_pub) + 1)

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = str(
                        ipaddress.ip_address(fixed_ip_v6_ext) + 1)

        self.main_ipv6_add_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_pub)
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_ext)

    def exec_through_paloalto_vm(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_pub='',
                                          fixed_ip_v6_ext='',
                                          is_subnet_ipv6=False
                                          ):

        device_type = '3'
        port_id4 = []

        # Create Instance(DB Client)
        db_list = list.ListClient(config.JobConfig())
        db_update = update.UpdateClient(config.JobConfig())

        # Get Endpoint(DB Client)
        db_endpoint_license = \
            base.JobAutoBase().get_db_endpoint(
                config.JobConfig().REST_URI_LICENSE)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_paloalto_vm'
        job_input['admin_id'] = 'admin_id_001'
        job_input['admin_pw'] = 'admin_pw_123456789'
        job_input['pavm_zone_name'] = 'zone_name_AAA'

        create_output = self.main_create_vfw(job_input)

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

        # List NAL_LICENSE_MNG(DB Client)
        params = {}
        params['status'] = 0
        params['type'] = 1
        params['device_type'] = 3
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_license, params)
        db_list.execute()
        license_list = db_list.get_return_param()

        # Update NAL_LICENSE_MNG(DB Client)
        if len(license_list) > 0:
            keys = [license_list[0]['ID']]
            params = {}
            params['tenant_name'] = 'IaaS_tenant_id_001'
            params['node_id'] = node_id
            db_update.set_context(db_endpoint_license, keys, params)
            db_update.execute()

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_LICENSE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        self.main_license_assign_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = '3'
        job_input['node_id'] = node_id
        job_input['pavm_zone_name'] = 'pavm_zone_name_BBB'

        self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[0]

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = fixed_ip_v6_pub

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = fixed_ip_v6_ext

        self.main_ipv6_add_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = '3'
        job_input['node_id'] = node_id
        job_input['pavm_zone_name'] = 'pavm_zone_name_CCC'

        self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[1]

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = str(
                        ipaddress.ip_address(fixed_ip_v6_pub) + 1)

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = str(
                        ipaddress.ip_address(fixed_ip_v6_ext) + 1)

        self.main_ipv6_add_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_pub)
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_ext)

    def exec_through_intersec_pub(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_pub='',
                                          is_subnet_ipv6=False
                                          ):

        device_type = '4'
        port_id4 = []

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_intersec_pub'
        job_input['webclient_ip'] = '10.58.10.1'
        job_input['ntp_ip'] = '10.58.10.2'
        job_input['zabbix_vip_ip'] = '10.58.10.3'
        job_input['zabbix_01_ip'] = '10.58.10.4'
        job_input['zabbix_02_ip'] = '10.58.10.5'

        create_output = self.main_create_vfw(job_input)

        # Get node_id from create process
        node_id = create_output['node_id']
        apl_table_rec_id = create_output['apl_table_rec_id']
        pod_id = create_output['pod_id']
        nal_tenant_id = create_output['nal_tenant_id']

        if is_subnet_ipv6:
            subnet_id_ipv6_pub = self.create_os_subnet_ipv6(
                            'pub_lan', pod_id, nal_tenant_id)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        create_output = self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[0]

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = fixed_ip_v6_pub

        self.main_ipv6_add_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        create_output = self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[1]

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = str(
                        ipaddress.ip_address(fixed_ip_v6_pub) + 1)

        self.main_ipv6_add_vfw(job_input)

        for port_id in port_id4:

            # Create input data
            job_input = copy.deepcopy(JOB_INPUT_PORT_DELETE)
            job_input['device_type'] = device_type
            job_input['node_id'] = node_id
            job_input['port_id'] = port_id
            job_input['apl_table_rec_id'] = apl_table_rec_id

            self.main_port_delete_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_pub)

    def exec_through_fortigate_vm_541(self, iaas_network_type='VXLAN',
                                          fixed_ip_v6_pub='',
                                          fixed_ip_v6_ext='',
                                          is_subnet_ipv6=False
                                          ):

        device_type = '5'
        port_id4 = []

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_CREATE)
        job_input['IaaS_network_type'] = iaas_network_type
        job_input['device_type'] = device_type
        job_input['host_name'] = 'host_name_fortigate_vm'
        job_input['admin_id'] = 'admin_id_001'
        job_input['admin_pw'] = 'admin_pw_123456789'

        create_output = self.main_create_vfw(job_input)

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

        create_output = self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[0]

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = fixed_ip_v6_pub

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = fixed_ip_v6_ext

        self.main_ipv6_add_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_PORT_CREATE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id

        create_output = self.main_port_create_vfw(job_input)

        # Get port_id from create process
        port_id4.append(create_output['port_id4'])

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_ADD_IPV6)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['port_id'] = port_id4[1]

        if len(fixed_ip_v6_pub) > 0:
            job_input['fixed_ip_v6_pub'] = str(
                        ipaddress.ip_address(fixed_ip_v6_pub) + 1)

        if len(fixed_ip_v6_ext) > 0:
            job_input['fixed_ip_v6_ext'] = str(
                        ipaddress.ip_address(fixed_ip_v6_ext) + 1)

        self.main_ipv6_add_vfw(job_input)

        for port_id in port_id4:

            # Create input data
            job_input = copy.deepcopy(JOB_INPUT_PORT_DELETE)
            job_input['device_type'] = device_type
            job_input['node_id'] = node_id
            job_input['port_id'] = port_id
            job_input['apl_table_rec_id'] = apl_table_rec_id

            self.main_port_delete_vfw(job_input)

        # Create input data
        job_input = copy.deepcopy(JOB_INPUT_DELETE)
        job_input['device_type'] = device_type
        job_input['node_id'] = node_id
        job_input['apl_table_rec_id'] = apl_table_rec_id

        self.main_delete_vfw(job_input)

        if is_subnet_ipv6:
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_pub)
            self.delete_os_subnet_ipv6(
                        pod_id, nal_tenant_id, subnet_id_ipv6_ext)

    def main_create_vfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

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
                         'IaaS_tenant_name_AAA')

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

        if job_input['device_type'] in ('2', '3', '4', '5'):
            # virtual_pub_port_create
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_pub_port_create(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertTrue('port_id2' in job_output)

        if job_input['device_type'] in ('1', '2', '3', '5'):
            # virtual_ext_port_create
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_ext_port_create(job_input)

            # Assertion
            self.assertEqual(len(job_output), 2)
            self.assertTrue('port_id3' in job_output)
            self.assertEqual(job_output['global_ip'], '192.168.80.245')

        # virtual_fw_tenant_vlan_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            virtual_fw_tenant_vlan_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('port_id4' in job_output)

        if job_input['device_type'] in ('1', '4'):
            # virtual_server_create_intersec
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_server_create_intersec(job_input)

            # Assertion
            self.assertEqual(len(job_output), 3)
            self.assertTrue('server_id' in job_output)
            self.assertTrue('node_id' in job_output)
            self.assertTrue('script_str' in job_output)

        elif job_input['device_type'] in ('3',):
            # virtual_server_create_paloalto_vm
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_server_create_paloalto_vm(job_input)

            # Assertion
            self.assertEqual(len(job_output), 2)
            self.assertTrue('server_id' in job_output)
            self.assertTrue('node_id' in job_output)

        elif job_input['device_type'] in ('5',):
            # license_assign_fortigate_vm_541
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .license_assign_fortigate_vm_541(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertEqual(job_output['license_key'], 'test_license_001')

            # virtual_server_create_with_config_drive
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_server_create_with_config_drive(job_input)

            # Assertion
            self.assertEqual(len(job_output), 2)
            self.assertTrue('server_id' in job_output)
            self.assertTrue('node_id' in job_output)

        else:
            # virtual_server_create
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_server_create(job_input)

            # Assertion
            self.assertEqual(len(job_output), 2)
            self.assertTrue('server_id' in job_output)
            self.assertTrue('node_id' in job_output)

        if job_input['device_type'] in ('1', '4'):
            # license_assign
            job_input.update(job_output)
            job_output = method.JobAutoMethod().license_assign(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertEqual(job_output['license_key'], 'test_license_001')

        elif job_input['device_type'] in ('2',):
            # license_assign_fortigate_vm
            job_input.update(job_output)
            job_output = \
                method.JobAutoMethod().license_assign_fortigate_vm(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertEqual(job_output['license_key'], 'test_license_001')

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
            # device_setup_create_for_intersec_sg_internet
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_intersec_sg_internet(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2',):
            # device_setup_create_for_fortigate_vm
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_fortigate_vm(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # device_setup_create_for_paloalto_vm
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_paloalto_vm(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # device_setup_create_for_intersec_sg_pub
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_intersec_sg_pub(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('5',):
            # device_setup_create_for_fortigate_vm_541
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .device_setup_create_for_fortigate_vm_541(job_input)

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

    def main_license_assign_vfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

        # initialize_update_vnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_update_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '1')
        self.assertEqual(job_output['type'], '1')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '')

        # license_assign_palpalto_vm
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
            .license_assign_palpalto_vm(job_input)

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

    def main_port_create_vfw(self, job_input):

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
        self.assertEqual(job_output['apl_type'], '1')
        self.assertEqual(job_output['type'], '1')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '')

        # virtual_fw_tenant_vlan_port_create
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
            .virtual_fw_tenant_vlan_port_create(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertTrue('port_id4' in job_output)

        # virtual_fw_interface_attach
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            virtual_fw_interface_attach(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        if job_input['device_type'] in ('1',):
            # msa_configuration_create_for_intersec_sg_internet
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_create_for_intersec_sg_internet(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2',):
            # msa_configuration_create_for_fortigate_vm
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_create_for_fortigate_vm(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3',):
            # msa_configuration_createfor_paloalto_vm
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_createfor_paloalto_vm(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # msa_configuration_create_for_intersec_sg_pub
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_create_for_intersec_sg_pub(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('5',):
            # msa_configuration_create_for_fortigate_vm_541
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_create_for_fortigate_vm_541(job_input)

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

    def main_ipv6_add_vfw(self, job_input):

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
        self.assertEqual(job_output['apl_type'], '1')
        self.assertEqual(job_output['type'], '1')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '')

        if job_input['device_type'] in ('2', '3', '4', '5'):

            # virtual_pub_port_add_ipv6
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_pub_port_add_ipv6(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertTrue('port_id_pub_ipv6' in job_output)

        if job_input['device_type'] in ('1', '2', '3', '5'):
            # virtual_ext_port_add_ipv6
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_ext_port_add_ipv6(job_input)

            # Assertion
            self.assertEqual(len(job_output), 1)
            self.assertTrue('port_id_ext_ipv6' in job_output)

        # virtual_fw_tenant_vlan_port_add_ipv6
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                .virtual_fw_tenant_vlan_port_add_ipv6(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # virtual_fw_interface_attach_ipv6
        job_input.update(job_output)
        job_output = method.JobAutoMethod()\
                .virtual_fw_interface_attach_ipv6(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        if job_input['device_type'] in ('1'):
            # msa_configuration_add_ipv6_for_intersec_sg_internet
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
            .msa_configuration_add_ipv6_for_intersec_sg_internet(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('2'):
            # device_setup_add_ipv6_for_fortigate_vm
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
            .device_setup_add_ipv6_for_fortigate_vm(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('3'):
            # device_setup_add_ipv6_for_paloalto_vm
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
            .device_setup_add_ipv6_for_paloalto_vm(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4'):
            # msa_configuration_add_ipv6_for_intersec_sg_pub
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
            .msa_configuration_add_ipv6_for_intersec_sg_pub(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('5'):
            # device_setup_add_ipv6_for_fortigate_vm_541
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
            .device_setup_add_ipv6_for_fortigate_vm_541(job_input)

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

    def main_port_delete_vfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

        # initialize
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_delete_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '1')
        self.assertEqual(job_output['type'], '1')
        self.assertEqual(job_output['device_type'], job_input['device_type'])
        self.assertTrue('nal_tenant_id' in job_output)
        self.assertEqual(job_output['node_id'], job_input['node_id'])
        self.assertEqual(job_output['redundant_configuration_flg'], '')

        if job_input['device_type'] in ('1',):
            # msa_configuration_delete_for_intersec_sg_internet
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_delete_for_intersec_sg_internet(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        elif job_input['device_type'] in ('4',):
            # msa_configuration_delete_for_intersec_sg_pub
            job_input.update(job_output)
            job_output = method.JobAutoMethod().\
                msa_configuration_delete_for_intersec_sg_pub(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        # virtual_fw_interface_detach
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            virtual_fw_interface_detach(job_input)

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        # virtual_fw_tenant_vlan_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            virtual_fw_tenant_vlan_port_delete(job_input)

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

    def main_delete_vfw(self, job_input):

        # tenant_id_convert
        job_output = method.JobAutoMethod().tenant_id_convert(job_input)

        # Assertion
        self.assertEqual(len(job_output), 1)
        self.assertEqual(job_output['tenant_name'], 'IaaS_tenant_id_001')

        # initialize_delete_vnf
        job_input.update(job_output)
        job_output = method.JobAutoMethod().initialize_delete_vnf(job_input)

        # Assertion
        self.assertEqual(len(job_output), 9)
        self.assertTrue('apl_table_rec_id' in job_output)
        self.assertTrue('msa_device_id' in job_output)
        self.assertEqual(job_output['pod_id'], 'pod_unit_test1')
        self.assertEqual(job_output['apl_type'], '1')
        self.assertEqual(job_output['type'], '1')
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
        self.assertEqual(job_output['nal_tenant_name'], 'IaaS_tenant_name_AAA')

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

        # Assertion
        self.assertEqual(len(job_output), 0)
        self.assertEqual(job_output, {})

        if job_input['device_type'] in ('2', '3', '4', '5'):
            # virtual_pub_port_delete
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_pub_port_delete(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        if job_input['device_type'] in ('1', '2', '3', '5'):
            # virtual_ext_port_delete
            job_input.update(job_output)
            job_output = method.JobAutoMethod()\
                .virtual_ext_port_delete(job_input)

            # Assertion
            self.assertEqual(len(job_output), 0)
            self.assertEqual(job_output, {})

        # virtual_fw_tenant_vlan_port_delete
        job_input.update(job_output)
        job_output = method.JobAutoMethod().\
            virtual_fw_tenant_vlan_port_delete(job_input)

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
