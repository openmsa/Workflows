import json
import mysql.connector
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
from rest.api import router
from rest.conf import config
from pprint import pprint


class TestSelectAPI(unittest.TestCase):
    # Do a test of Select.

    ID = 0

    def setUp(self):

        # Establish a clean test environment.
        super(TestSelectAPI, self).setUp()

        # Insert test data
        self.create_fixtures()

    def tearDown(self):
        """Clear the test environment"""
        super(TestSelectAPI, self).tearDown()
        self.destroy_fixtures()

    def create_fixtures(self):

        pass

    def destroy_fixtures(self):

        pass

    def connect_db(self):
            # Connect Database
            con = mysql.connector.connect(
                host=getattr(config, 'MYSQL_HOSTNAME', ''),
                db=getattr(config, 'MYSQL_DBNAME', ''),
                user=getattr(config, 'MYSQL_USERID', ''),
                passwd=getattr(config, 'MYSQL_PASSWORD', ''),
                buffered=True)

            # Set Autocommit Off
            con.autocommit = False

            # Open Cursor
            cur = con.cursor()

            return con, cur

    def cut_db(self, con, cur):
        # Commit Transaction
        con.commit()

        # Close Cursor
        cur.close()

        # Close Database
        con.close()

    def test_insert_nal_ep(self):

        con, cur = self.connect_db()
        param_vals = []
        cur.execute("DELETE FROM NAL_DEVICE_ENDPOINT_MNG", param_vals)
        self.cut_db(con, cur)

        # --------------------------------------------------
        # VIM(pod1)
        # --------------------------------------------------
        conf_type = 1
        dc_id = 'system'
        region_id = ''
        pod_id = 'dc01_pod01'
        config = {
            'endpoint': 'http://10.34.246.100:5000/v2.0',
            'user_id': 'admin',
            'user_password': 'admin',
            'user_key': '2953e1c876454fc3b59a1eaf09bd7a09',
            'role_id': 'cd034e1a0f774a1aa125edcc3f35598e',
            'admin_tenant_name': 'admin',
            'openstack_keystone_ip_address': '10.34.246.100',
            'openstack_controller_node_ip_address': '10.34.246.100',
            'openstack_controller_node_server_login_id': 'heat-admin',
            'openstack_controller_node_server_login_password': 'P@ssw0rd',
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # VIM(develop)
        # --------------------------------------------------
        conf_type = 1
        dc_id = 'system'
        region_id = ''
        pod_id = 'develop'
        config = {
            'endpoint': 'http://localhost:8080/api_nal/Stubs/OpenStackClient/index.php?/v2.0',
            'user_id': 'admin',
            'user_password': 'i-portal',
            'user_key': '4034dbce1e3946dbba822288baa330d3',
            'role_id': '37367b49c20d48459716b3a3227e902a',
            'admin_tenant_name': 'admin',
            'openstack_keystone_ip_address': 'localhost',
            'openstack_controller_node_ip_address': 'localhost',
            'openstack_controller_node_server_login_id': 'heat-admin',
            'openstack_controller_node_server_login_password': 'P@ssw0rd',
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # IaaS
        # --------------------------------------------------
        conf_type = 2
        dc_id = 'system'
        region_id = 'region001'
        pod_id = ''
        config = {
            'endpoint': 'http://10.34.2.21:5000/v2.0',
            'user_id': 'admin',
            'user_password': 'f4c6ad669c65c12e6701f2af04b6b2d598b21ed3',
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # MSA
        # --------------------------------------------------
        conf_type = 3
        dc_id = 'system'
        region_id = ''
        pod_id = 'dc01_pod01'
        config = {
            'endpoint': 'https://10.34.246.64/webapi/%MSA_CLASS_NAME%?',
            'user_id': 'ncroot',
            'user_password': 'ubiqube',
            'customer_create_endpoint': 'UserWS',
            'device_create_endpoint': 'DeviceWS',
            'init_provisioning_endpoint': 'DeviceWS',
            'object_attach_endpoint': 'DeviceConfigurationWS',
            'object_execute_endpoint': 'OrderCommandWS',
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # MSA(develop)
        # --------------------------------------------------
        conf_type = 3
        dc_id = 'system'
        region_id = ''
        pod_id = 'develop'
        config = {
            'endpoint': 'https://localhost/webapi/%MSA_CLASS_NAME%?',
            'user_id': 'msaadmin',
            'user_password': 'ms@pass1234',
            'customer_create_endpoint': 'UserWS',
            'device_create_endpoint': 'DeviceWS',
            'init_provisioning_endpoint': 'DeviceWS',
            'object_attach_endpoint': 'DeviceConfigurationWS',
            'object_execute_endpoint': 'OrderCommandWS',
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # VXLAN-GW
        # --------------------------------------------------
        conf_type = 4
        dc_id = 'system'
        region_id = 'region001'
        pod_id = ''
        config = {
            'endpoint': '10.34.2.21',
            'user_id': 'heat-admin',
            'user_password': 'P@ssw0rd',
            'timeout': 300,
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # VXLAN-GW
        # --------------------------------------------------
        conf_type = 5
        dc_id = 'system'
        region_id = ''
        pod_id = ''
        config = {
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # Assertion
        # --------------------------------------------------
        # Assertion(check select)
        request_params = {
            'query': {
            },
            'resource': 'nal-endpoints',
            'method': 'GET',
            'id': []
        }
        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')

        for rec in res_data:
            pprint(json.loads(rec['endpoint_info']))

        # --------------------------------------------------
        # VIM(pod_unit_test1)
        # --------------------------------------------------
        conf_type = 1
        dc_id = 'system'
        region_id = ''
        pod_id = 'pod_unit_test1'
        config = {
            'endpoint': 'http://10.58.79.178/icons/Stubs/NalOpenStackClient/index.php?/v2.0',
            'user_id': 'admin',
            'user_password': 'i-portal',
            'user_key': '4034dbce1e3946dbba822288baa330d3',
            'role_id': '37367b49c20d48459716b3a3227e902a',
            'admin_tenant_name': 'admin',
            'openstack_keystone_ip_address': 'localhost',
            'openstack_controller_node_ip_address': 'localhost',
            'openstack_controller_node_server_login_id': 'heat-admin',
            'openstack_controller_node_server_login_password': 'P@ssw0rd',
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # IaaS(region_unit_test1)
        # --------------------------------------------------
        conf_type = 2
        dc_id = 'system'
        region_id = 'region_unit_test1'
        pod_id = ''
        config = {
            'endpoint': 'http://10.58.79.178/icons/Stubs/IaaSOpenStackClient/index.php?/v2.0',
            'user_id': 'admin',
            'user_password': 'f4c6ad669c65c12e6701f2af04b6b2d598b21ed3',
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # MSA(pod_unit_test1)
        # --------------------------------------------------
        conf_type = 3
        dc_id = 'system'
        region_id = ''
        pod_id = 'pod_unit_test1'
        config = {
            'endpoint': 'https://localhost/webapi/%MSA_CLASS_NAME%?',
            'user_id': 'msaadmin',
            'user_password': 'ms@pass1234',
            'customer_create_endpoint': 'UserWS',
            'device_create_endpoint': 'DeviceWS',
            'init_provisioning_endpoint': 'DeviceWS',
            'object_attach_endpoint': 'DeviceConfigurationWS',
            'object_execute_endpoint': 'OrderCommandWS',
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'endpoint_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-endpoints',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

    def test_insert_nal_conf(self):

        con, cur = self.connect_db()
        param_vals = []
        cur.execute("DELETE FROM NAL_CONFIG_MNG", param_vals)
        self.cut_db(con, cur)

        # --------------------------------------------------
        # common
        # --------------------------------------------------
        conf_type = 5
        dc_id = 'system'
        region_id = ''
        pod_id = ''
        config = {
            'device_name_list': {
                '1': {
                    '1': {
                        '1': {'name': 'intersec_sg', },
                        '2': {'name': 'fortigate_vm', },
                        '3': {'name': 'paloalto_vm', },
                        '4': {'name': 'intersec_sg', },
                    },
                    '2': {
                        '1': {'name': 'intersec_lb', },
                        '2': {'name': 'bigip_ve', },
                        '3': {'name': 'vthunder', },
                    },
                    '3': {
                        '1': {'name': 'filefly', },
                    },
                },
                '2': {
                    '1': {
                        '1': {'name': 'fortigate', },
                    },
                    '2': {
                        '1': {'name': 'bigip', },
                    },
                },
            },
            'os_image_and_flavor_name_list': {
                '1': {
                    '1': {
                        'image_name': 'InterSecVM/SG',
                        'flavor_name': 'InterSecVM/SG',
                    },
                    '2': {
                        'image_name': 'FortiGate',
                        'flavor_name': 'FortiGate',
                    },
                    '3': {
                        'image_name': 'PaloAlto',
                        'flavor_name': 'PaloAlto',
                    },
                    '4': {
                        'image_name': 'InterSecVM/SG',
                        'flavor_name': 'InterSecVM/SG',
                    },
                },
                '2': {
                    '1': {
                        'image_name': 'InterSecVM/LB',
                        'flavor_name': 'InterSecVM/LB',
                    },
                    '2': {
                        'image_name': 'BIG-IP',
                        'flavor_name': 'BIG-IP',
                    },
                    '3': {
                        'image_name': 'vThunder',
                        'flavor_name': 'vThunder',
                    },
                },
                '3': {
                    '1': {
                        'image_name': 'vSRX',
                        'flavor_name': 'vSRX',
                    },
                },
            },
            'os_vlan_name_list': {
                'msa_lan': {'name': 'MSA', },
                'pub_lan': {'name': 'Pub', },
                'ext_lan': {'name': 'Ext', },
            },
            'inter_dc_netowrk_info': {
                'dc01': {
                    'ce01': {
                        'wan_ip': '100.80.251.1',
                        'wan_subnet_ip': '100.80.251.0',
                        'wan_netmask': '25',
                        'loopback_ip': '100.80.251.129',
                        'loopback_seg': '100.80.251.128',
                        'loopback_netmask': '30',
                    },
                    'ce02': {
                        'wan_ip': '100.80.251.2',
                        'wan_subnet_ip': '100.80.251.0',
                        'wan_netmask': '25',
                        'loopback_ip': '100.80.251.130',
                        'loopback_seg': '100.80.251.128',
                        'loopback_netmask': '30',
                    },
                },
                'dc03': {
                    'ce01': {
                        'wan_ip': '100.80.251.3',
                        'wan_subnet_ip': '100.80.251.0',
                        'wan_netmask': '25',
                        'loopback_ip': '100.80.251.133',
                        'loopback_seg': '100.80.251.132',
                        'loopback_netmask': '30',
                    },
                    'ce02': {
                        'wan_ip': '100.80.251.4',
                        'wan_subnet_ip': '100.80.251.0',
                        'wan_netmask': '25',
                        'loopback_ip': '100.80.251.134',
                        'loopback_seg': '100.80.251.132',
                        'loopback_netmask': '30',
                    }
                }
            },
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'config_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-configs',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # MSA
        # --------------------------------------------------
        conf_type = 3
        dc_id = 'system'
        region_id = ''
        pod_id = 'dc01_pod01'
        config = {
            'msa_config_for_common': {
                'msa_ip_address': '100.94.246.64',
                'msa_vlan_gateway': '100.94.254.254',
                'tftp_server_ip_address': '100.94.246.64',
                'pub_vlan_gateway': '100.65.255.254',
                'ext_vlan_gateway': '202.247.10.158',
                'svc_vlan_network_address': '100.64.0.0',
                'svc_vlan_network_mask': '16',
                'svc_vlan_dns_primary_ip_address': '100.64.10.16',
                'svc_vlan_dns_secondary_ip_address': '100.64.10.17',
                'svc_vlan_ntp_primary_ip_address': '100.64.10.16',
                'svc_vlan_ntp_secondary_ip_address': '100.64.10.17',
                'svc_vlan_proxy_ip_address': '100.64.10.9',
                'svc_vlan_proxy_port': '8080',
                'ext_vlan_gateway': '202.247.10.158',
                'msa_customer_name_prefix': 'c_tenant',
                'msa_server_device_id': '10',
            },
            'msa_config_for_device': {
                'fortigate_vm': {
                    'manufacturer_id': 17,
                    'model_id': 130,
                    'object_attach_file': [
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_System_Common.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_Interface.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_Admin_Account.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_DNS.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_NTP.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_Router_Static.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': '',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'admin_profile': 'super_admin',
                    'nic_prefix': 'port',
                    'default_language': 'japanese',
                    'default_timezone': '60',
                    'default_ntp_sync_interval': '60',
                    'default_ntp_action': 'enable',
                    'router_static_num': 1,
                    'device_name': 'fortigate_vm_fw',
                },
                'paloalto_vm': {
                    'manufacturer_id': 28,
                    'model_id': 134,
                    'object_attach_file': [
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_System_Common.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Vsys_Zone.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Vsys_Zone_mapping.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Network_vRouter_mapping.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Network_Interface.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_System_DNS.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Logsetting_SNMP.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Logsetting_SNMP_mapping.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Logsetting_Syslog.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Logsetting_Syslog_mapping.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_System_NTP.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Network_StaticRoute.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_System_Users.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': 'admin',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': 'ethernet1/',
                    'default_timezone': 'Asia/Tokyo',
                    'device_name': 'paloalto_vm',
                },
                'intersec_sg': {
                    'manufacturer_id': 70000,
                    'model_id': 70001,
                    'object_attach_file': [
                        '/CommandDefinition/NEC/InterSecVMSG/sg_nw.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_reboot.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_zabbix.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_ntp.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_default_gw.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_static_route.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': '',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': '',
                    'device_name': 'intersec_sg',
                },
                'bigip_ve': {
                    'manufacturer_id': 50000,
                    'model_id': 50001,
                    'object_attach_file': [
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_System_Common.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_Network_VLAN.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_Network_Self_IP.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_System_DNS.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_System_NTP.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_Network_Routes.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_System_Admin_Account.xml',
                    ],
                    'user_id': 'root',
                    'user_default_password': 'default',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': '',
                    'default_route_name': 'default',
                    'device_name': 'bigip_ve',
                },
                'vthunder': {
                    'manufacturer_id': 80000,
                    'model_id': 80001,
                    'object_attach_file': [
                        '/CommandDefinition/A10/Thunder/vThunder_System_Common.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_Network_VLAN_and_Virtualinterface.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_DNS.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_SNMP_trap.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_SNMP_Enable.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_SNMP.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_Syslog.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_NTP.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_Network_Routes.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_Admin_Account.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': 'a10',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': '',
                    'default_timezone': 'Asia/Tokyo',
                    'device_name': 'vthunder',
                },
                'intersec_lb': {
                    'manufacturer_id': 70000,
                    'model_id': 70001,
                    'object_attach_file': [
                        '/CommandDefinition/NEC/InterSecVMLB/lb_startup.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_nw.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_reboot.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_zabbix.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_ntp.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_default_gw.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_static_route.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': '',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': '',
                    'device_name': 'intersec_lb',
                },
                'fortigate': {
                    'manufacturer_id': 17,
                    'model_id': 130,
                    'object_attach_file': [
                        '/CommandDefinition/FORTINET/Generic/FortiVdomProvPNF.xml',
                        '/CommandDefinition/FORTINET/Generic/FortiVlanProvPNF.xml',
                    ],
                    'user_id': 'msaadmin',
                    'user_default_password': '',
                    'user_new_password': 'ms@pnf1234',
                    'admin_password': 'ms@pnf1234',
                    'nic_prefix': '',
                    'device_name': 'fortigate',
                },
                'bigip': {
                    'manufacturer_id': 50000,
                    'model_id': 50001,
                    'object_attach_file': [
                        '/CommandDefinition/F5/BIG-IP/BIGIP_partition.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_route_domain.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_default_route_domain.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_vlan.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_physical_IP.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VIP.xml',
                    ],
                    'user_id': 'msaadmin',
                    'user_default_password': '',
                    'user_new_password': 'ms@pnf1234',
                    'admin_password': 'ms@pnf1234',
                    'nic_prefix': '1.',
                    'default_selfip_name': 'management_ip',
                    'device_name': 'bigip',
                },
                'filefly': {
                    'manufacturer_id': 18,
                    'model_id': 121,
                    'object_attach_file': [
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_System_Common.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_LAN_Interface.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_WAN_Interface.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_Loopback_Interface.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Basic.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Peer.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP_Tracking.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_StaticRoute.xml',
                    ],
                    'user_id': 'msaadmin',
                    'user_default_password': '',
                    'user_new_password': 'ms@pnf1234',
                    'admin_password': 'ms@pnf1234',
                    'nic_prefix': 'ge-0/0/',
                    'default_device_name': 'Firefly',
                    'default_timezone': 'GMT-9',
                    'default_wan_interface_mtu': 1400,
                    'device_name': 'filefly',
                },
            },
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'config_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-configs',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # MSA(pod_unit_test1)
        # --------------------------------------------------
        conf_type = 3
        dc_id = 'system'
        region_id = ''
        pod_id = 'pod_unit_test1'
        config = {
            'msa_config_for_common': {
                'msa_ip_address': '100.94.246.64',
                'msa_vlan_gateway': '100.94.254.254',
                'tftp_server_ip_address': '100.94.246.64',
                'pub_vlan_gateway': '100.65.255.254',
                'ext_vlan_gateway': '202.247.10.158',
                'svc_vlan_network_address': '100.64.0.0',
                'svc_vlan_network_mask': '16',
                'svc_vlan_dns_primary_ip_address': '100.64.10.16',
                'svc_vlan_dns_secondary_ip_address': '100.64.10.17',
                'svc_vlan_ntp_primary_ip_address': '100.64.10.16',
                'svc_vlan_ntp_secondary_ip_address': '100.64.10.17',
                'svc_vlan_proxy_ip_address': '100.64.10.9',
                'svc_vlan_proxy_port': '8080',
                'ext_vlan_gateway': '202.247.10.158',
                'msa_customer_name_prefix': 'c_tenant',
                'msa_server_device_id': '10',
            },
            'msa_config_for_device': {
                'fortigate_vm': {
                    'manufacturer_id': 17,
                    'model_id': 130,
                    'object_attach_file': [
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_System_Common.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_Interface.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_Admin_Account.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_DNS.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_NTP.xml',
                        '/CommandDefinition/FORTINET/Generic/Fortigate_VM_Router_Static.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': '',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'admin_profile': 'super_admin',
                    'nic_prefix': 'port',
                    'default_language': 'japanese',
                    'default_timezone': '60',
                    'default_ntp_sync_interval': '60',
                    'default_ntp_action': 'enable',
                    'router_static_num': 1,
                    'device_name': 'fortigate_vm_fw',
                },
                'paloalto_vm': {
                    'manufacturer_id': 28,
                    'model_id': 134,
                    'object_attach_file': [
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_System_Common.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Vsys_Zone.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Vsys_Zone_mapping.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Network_vRouter_mapping.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Network_Interface.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_System_DNS.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Logsetting_SNMP.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Logsetting_SNMP_mapping.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Logsetting_Syslog.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Logsetting_Syslog_mapping.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_System_NTP.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_Network_StaticRoute.xml',
                        '/CommandDefinition/PALOALTO/VA/PaloAlto_VM_System_Users.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': 'admin',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': 'ethernet1/',
                    'default_timezone': 'Asia/Tokyo',
                    'device_name': 'paloalto_vm',
                },
                'intersec_sg': {
                    'manufacturer_id': 70000,
                    'model_id': 70001,
                    'object_attach_file': [
                        '/CommandDefinition/NEC/InterSecVMSG/sg_nw.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_reboot.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_zabbix.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_ntp.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_default_gw.xml',
                        '/CommandDefinition/NEC/InterSecVMSG/sg_static_route.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': '',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': '',
                    'device_name': 'intersec_sg',
                },
                'bigip_ve': {
                    'manufacturer_id': 50000,
                    'model_id': 50001,
                    'object_attach_file': [
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_System_Common.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_Network_VLAN.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_Network_Self_IP.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_System_DNS.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_System_NTP.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_Network_Routes.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VE_System_Admin_Account.xml',
                    ],
                    'user_id': 'root',
                    'user_default_password': 'default',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': '',
                    'default_route_name': 'default',
                    'device_name': 'bigip_ve',
                },
                'vthunder': {
                    'manufacturer_id': 80000,
                    'model_id': 80001,
                    'object_attach_file': [
                        '/CommandDefinition/A10/Thunder/vThunder_System_Common.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_Network_VLAN_and_Virtualinterface.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_DNS.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_SNMP_trap.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_SNMP_Enable.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_SNMP.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_Syslog.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_NTP.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_Network_Routes.xml',
                        '/CommandDefinition/A10/Thunder/vThunder_System_Admin_Account.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': 'a10',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': '',
                    'default_timezone': 'Asia/Tokyo',
                    'device_name': 'vthunder',
                },
                'intersec_lb': {
                    'manufacturer_id': 70000,
                    'model_id': 70001,
                    'object_attach_file': [
                        '/CommandDefinition/NEC/InterSecVMLB/lb_startup.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_nw.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_reboot.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_zabbix.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_ntp.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_default_gw.xml',
                        '/CommandDefinition/NEC/InterSecVMLB/lb_static_route.xml',
                    ],
                    'user_id': 'admin',
                    'user_default_password': '',
                    'user_new_password': 'Passw0rd',
                    'admin_password': 'Passw0rd',
                    'nic_prefix': '',
                    'device_name': 'intersec_lb',
                },
                'fortigate': {
                    'manufacturer_id': 17,
                    'model_id': 130,
                    'object_attach_file': [
                        '/CommandDefinition/FORTINET/Generic/FortiVdomProvPNF.xml',
                        '/CommandDefinition/FORTINET/Generic/FortiVlanProvPNF.xml',
                    ],
                    'user_id': 'msaadmin',
                    'user_default_password': '',
                    'user_new_password': 'ms@pnf1234',
                    'admin_password': 'ms@pnf1234',
                    'nic_prefix': '',
                    'device_name': 'fortigate',
                },
                'bigip': {
                    'manufacturer_id': 50000,
                    'model_id': 50001,
                    'object_attach_file': [
                        '/CommandDefinition/F5/BIG-IP/BIGIP_partition.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_route_domain.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_default_route_domain.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_vlan.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_physical_IP.xml',
                        '/CommandDefinition/F5/BIG-IP/BIGIP_VIP.xml',
                    ],
                    'user_id': 'msaadmin',
                    'user_default_password': '',
                    'user_new_password': 'ms@pnf1234',
                    'admin_password': 'ms@pnf1234',
                    'nic_prefix': '1.',
                    'default_selfip_name': 'management_ip',
                    'device_name': 'bigip',
                },
                'filefly': {
                    'manufacturer_id': 18,
                    'model_id': 121,
                    'object_attach_file': [
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_System_Common.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_LAN_Interface.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_WAN_Interface.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_Loopback_Interface.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Basic.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_BGP_Peer.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_VRRP_Tracking.xml',
                        '/CommandDefinition/JUNIPER/junOS_generic/Firefly_VM_StaticRoute.xml',
                    ],
                    'user_id': 'msaadmin',
                    'user_default_password': '',
                    'user_new_password': 'ms@pnf1234',
                    'admin_password': 'ms@pnf1234',
                    'nic_prefix': 'ge-0/0/',
                    'default_device_name': 'Firefly',
                    'default_timezone': 'GMT-9',
                    'default_wan_interface_mtu': 1400,
                    'device_name': 'filefly',
                },
            },
        }

        insert_params = {
            'create_id': 'system',
            'update_id': 'system',
            'delete_flg': 0,
            'type': conf_type,
            'dc_id': dc_id,
            'region_id': region_id,
            'pod_id': pod_id,
            'config_info': json.dumps(config),
        }
        request_params = {
            'body': insert_params,
            'query': {},
            'resource': 'nal-configs',
            'method': 'POST',
            'id': []
        }

        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        # --------------------------------------------------
        # Assertion
        # --------------------------------------------------
        # Assertion(check select)
        request_params = {
            'query': {
            },
            'resource': 'nal-configs',
            'method': 'GET',
            'id': []
        }
        res = router.Router().routing(request_params)
        status = res['status']
        res_data = res['message'].decode('utf-8')
        res_data = json.loads(res_data)

        self.assertEqual(status, '200 OK')

        for rec in res_data:
            pprint(json.loads(rec['config_info']))
