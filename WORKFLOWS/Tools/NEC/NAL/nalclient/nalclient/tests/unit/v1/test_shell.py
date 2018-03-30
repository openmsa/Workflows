#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  


"""Test nalclient/v1/shell.py."""
import exceptions
import json
import mock
import os
import sys
import testtools

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')

from nalclient.common import utils
from nalclient.v1 import shell as v1shell

return_node_data = [
    {
        "ID": "1",
        "MSA_device_id": "",
        "actsby_flag_master": "act",
        "actsby_flag_slave": "",
        "apl_type": "2",
        "create_date": "2016-10-03 13:11:44",
        "create_id": "system",
        "default_gateway": "",
        "delete_flg": "0",
        "description": "",
        "device_detail_master": "",
        "device_detail_slave": "",
        "device_name_master": "wn0fwxtf01",
        "device_name_slave": "",
        "device_type": "1",
        "device_user_name": "",
        "err_info": "",
        "global_ip": "",
        "master_MSA_device_id": "",
        "master_ip_address": "100.99.0.5",
        "node_detail": "{}",
        "node_id": "31yb5633-692h-u67t-199e-j5i703ng8f4d",
        "node_name": "",
        "pod_id": "pod0001",
        "redundant_configuration_flg": "1",
        "server_id": "",
        "server_info": "{}",
        "slave_MSA_device_id": "",
        "slave_ip_address": "",
        "status": "0",
        "task_status": "1",
        "tenant_id": "",
        "tenant_name": "",
        "type": "1",
        "update_date": "2016-10-03 13:11:44",
        "update_id": "system"
    },
    {
        "ID": "2",
        "MSA_device_id": "1",
        "actsby_flag_master": "",
        "actsby_flag_slave": "",
        "apl_type": "1",
        "create_date": "2016-10-07 18:48:15",
        "create_id": "a0905826fd484046a5590f03d57897e7",
        "default_gateway": "202.247.10.158",
        "delete_flg": "0",
        "description": "",
        "device_detail_master": "",
        "device_detail_slave": "",
        "device_name_master": "",
        "device_name_slave": "",
        "device_type": "3",
        "device_user_name": "",
        "err_info": "[]",
        "global_ip": "172.17.3.60",
        "master_MSA_device_id": "",
        "master_ip_address": "",
        "node_detail": "{}",
        "node_id": "0bd0bca3-44df-4164-8bc3-8b9518e0fbc9",
        "node_name": "test_unit",
        "pod_id": "pod0001",
        "redundant_configuration_flg": "",
        "server_id": "0bd0bca3-44df-4164-8bc3-8b9518e0fbc9",
        "server_info": "{}",
        "slave_MSA_device_id": "",
        "slave_ip_address": "",
        "status": "",
        "task_status": "2",
        "tenant_id": "709795e2be784f9ba99cc508dec11458",
        "tenant_name": "a97c1a4aa4aa4ebea4da5e212cf3c1ff",
        "type": "1",
        "update_date": "2016-10-07 18:52:56",
        "update_id": "a0905826fd484046a5590f03d57897e7"
    }
]

return_service_data = [
    {
        "create_id": "system",
        "create_date": "2016-10-07 18:52:56",
        "update_id": "system",
        "update_date": "2016-10-07 18:52:56",
        "delete_flg": "0",
        "ID": "23",
        "group_id": "1",
        "group_name": "dc_gru_1",
        "group_type": "1",
        "tenant_name": "admin",
        "IaaS_tenant_id": "1234",
        "my_group_flg": "1"
    },
    {
        "create_id": "system",
        "create_date": "2016-10-07 18:52:56",
        "update_id": "system",
        "update_date": "2016-10-07 18:52:56",
        "delete_flg": "0",
        "ID": "24",
        "group_id": "2",
        "group_name": "dc_gru_2",
        "group_type": "2",
        "tenant_name": "tenant_name2",
        "IaaS_tenant_id": "9876"
    }
]

return_resource_data = {
    "cpu": {
        "num": 4.1666666666667e-8,
        "quota": 3
    },
    "memory": {
        "num": 0.000021333333333333,
        "quota": 3
    },
    "strage": {
        "num": 4.1666666666667e-8,
        "quota": 3
    },
    "globalip": {
        "num": 2,
        "quota": 5
    },
    "license": {
        "num": 2,
        "quota": 5
    },
    "pnf": {
        "num": 2,
        "quota": 3
    }
}


return_status = {'status': 'success',
                 'error-code': 'NAL100000',
                 'message': ''}


class ShellTest(testtools.TestCase):
    """Test Shell."""

    def setUp(self):
        """Setup test mock."""
        super(ShellTest, self).setUp()
        self._mock_utils()
        self.gc = self._mock_client()

    def _make_args(self, args):
        """Create arguments object.
        :param args: source arguments.
        """

        class Args():

            def __init__(self, entries):
                self.__dict__.update(entries)

        return Args(args)

    def _mock_client(self):
        """Create client of mock."""
        my_mocked_gc = mock.Mock()
        my_mocked_gc.schemas.retun_value = 'test'
        my_mocked_gc.get.return_value = {}

        return my_mocked_gc

    def _mock_utils(self):
        """Set utility function of mock."""
        utils.print_list = mock.Mock()
        utils.print_dict = mock.Mock()

    def assert_exits_with_msg(self, func, func_args, err_msg):
        """Test function and add message to result.
        :param func: run test function.
        :param func_args: run test function arguments.
        :param err_msg: error message.
        """
        with mock.patch.object(utils, 'exit') as mocked_utils_exit:
            mocked_utils_exit.return_value = '%s' % err_msg

            func(self.gc, func_args)
            mocked_utils_exit.assert_called_once_with(err_msg)

    def test_do_node_create(self):
        """Test create node command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'test_tenant',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'host_name': 'test_host',
                     'device_name': 'test_device',
                     'type': '1',
                     'device_type': '1',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
                     'network_name': 'test_network',
                     'webclient_ip': '10.20.30.10',
                     'ntp_ip': '10.20.30.11'}
        input = {'type': 'vfw',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.node,
                               'create') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_node_create(self.gc, args)

            fields = json_data
            fields['function_type'] = 'vfw'

            mocked_func.assert_called_once_with(fields)

    def test_do_node_create_no_type_error(self):
        """Test create node command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'test_tenant',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'host_name': 'test_host',
                     'device_name': 'test_device',
                     'type': '1',
                     'device_type': '1',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
                     'network_name': 'test_network',
                     'webclient_ip': '10.20.30.10',
                     'ntp_ip': '10.20.30.11'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_create,
                          self.gc,
                          args)

    def test_do_node_create_no_json_data_error(self):
        """Test create node command without json_data."""
        input = {'type': 'vfw'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_create,
                          self.gc,
                          args)

    def test_do_node_create_json_format_error(self):
        """Test create node command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'vfw'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_create,
                          self.gc,
                          args)

    def test_do_node_update(self):
        """Test update vfw for create port command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'test_tenant',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
                     'network_name': 'test_network',
                     'node_id': 'nodeid-414b-aa5e-dedbeef00101'}
        input = {'type': 'vfw-port-p',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.node,
                               'update') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_node_update(self.gc, args)

            fields = json_data
            fields['function_type'] = 'vfw-port-p'

            mocked_func.assert_called_once_with(fields)

    def test_do_node_update_no_type_error(self):
        """Test update node command without type."""
        """Test update vfw for create port command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'test_tenant',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
                     'network_name': 'test_network',
                     'node_id': 'nodeid-414b-aa5e-dedbeef00101'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_update,
                          self.gc,
                          args)

    def test_do_node_update_no_json_data_error(self):
        """Test update node command without json_data."""
        input = {'type': 'vfw_port_p'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_update,
                          self.gc,
                          args)

    def test_do_node_update_json_format_error(self):
        """Test update node command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'vfw_port_p'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_update,
                          self.gc,
                          args)

    def test_do_node_delete(self):
        """Test delete node command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'node_id': 'nodeid-414b-aa5e-dedbeef00101'}
        input = {'type': 'delete',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.node,
                               'delete') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_node_delete(self.gc, args)

            fields = json_data
            fields['function_type'] = 'delete'

            mocked_func.assert_called_once_with(fields)

    def test_do_node_delete_no_type_error(self):
        """Test delete node command without type."""
        """Test delete node command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'node_id': 'nodeid-414b-aa5e-dedbeef00101'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_delete,
                          self.gc,
                          args)

    def test_do_node_delete_no_json_data_error(self):
        """Test delete node command without json_data."""
        input = {'type': 'vfw'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_delete,
                          self.gc,
                          args)

    def test_do_node_delete_json_format_error(self):
        """Test delete node command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'vfw'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_delete,
                          self.gc,
                          args)

    def test_do_node_get(self):
        """Test get node command."""
        json_data = {'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'apl_type': '1',
                     'type': '1',
                     'device_type': '1'}
        input = {'type': 'all_node',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.node,
                               'get') as mocked_func:
            mocked_func.return_value = return_node_data
            v1shell.do_node_get(self.gc, args)

            fields = json_data
            fields['function_type'] = 'all_node'

            mocked_func.assert_called_once_with(fields)

    def test_do_node_get_no_type_error(self):
        """Test get node command without type."""
        json_data = {'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'apl_type': '1',
                     'type': '1',
                     'device_type': '1'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_get,
                          self.gc,
                          args)

    def test_do_node_get_no_json_data_error(self):
        """Test get node command without json_data."""
        input = {'type': 'vfw'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_get,
                          self.gc,
                          args)

    def test_do_node_get_json_format_error(self):
        """Test get node command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'vfw'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_node_get,
                          self.gc,
                          args)

    def test_do_service_create(self):
        """Test create dcconnect command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'test_tenant',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
                     'network_name': 'test_network',
                     'dc_id': 'dcid-414b-aa5e-dedbeef00101',
                     'fw_ip_address': '10.20.30.11'}
        input = {'type': 'dcconnect',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.service,
                               'create') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_service_create(self.gc, args)

            fields = json_data
            fields['function_type'] = 'dcconnect'

            mocked_func.assert_called_once_with(fields)

    def test_do_service_create_no_type_error(self):
        """Test create service command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'test_tenant',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
                     'network_name': 'test_network',
                     'dc_id': 'dcid-414b-aa5e-dedbeef00101',
                     'fw_ip_address': '10.20.30.11'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_create,
                          self.gc,
                          args)

    def test_do_service_create_no_json_data_error(self):
        """Test create service command without json_data."""
        input = {'type': 'dcconnect'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_create,
                          self.gc,
                          args)

    def test_do_service_create_json_format_error(self):
        """Test create service command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'dcconnect'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_create,
                          self.gc,
                          args)

    def test_do_service_update(self):
        """Test update dcconnect command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'tanant_name',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'IaaS_subnet_id': 'subnet_id-00001',
                     'IaaS_network_id': 'network_id-00001',
                     'network_name': 'network_nameA',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_segmentation_id': '20',
                     'device_type': '1',
                     'group_id': 'group_id-00001'}
        input = {'type': 'dcconnect',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.service,
                               'update') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_service_update(self.gc, args)

            fields = json_data
            fields['function_type'] = 'dcconnect'

            mocked_func.assert_called_once_with(fields)

    def test_do_service_update_no_type_error(self):
        """Test update service command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'tanant_name',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'IaaS_subnet_id': 'subnet_id-00001',
                     'IaaS_network_id': 'network_id-00001',
                     'network_name': 'network_nameA',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_segmentation_id': '20',
                     'device_type': '1',
                     'group_id': 'group_id-00001'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_update,
                          self.gc,
                          args)

    def test_do_service_update_no_json_data_error(self):
        """Test update service command without json_data."""
        input = {'type': 'dcconnect'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_update,
                          self.gc,
                          args)

    def test_do_service_update_json_format_error(self):
        """Test update service command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'dcconnect'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_update,
                          self.gc,
                          args)

    def test_do_service_delete(self):
        """Test delete dcconnect command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'dc_id': 'dcid-414b-aa5e-dedbeef00101'}
        input = {'type': 'dcconnect',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.service,
                               'delete') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_service_delete(self.gc, args)

            fields = json_data
            fields['function_type'] = 'dcconnect'

            mocked_func.assert_called_once_with(fields)

    def test_do_service_delete_no_type_error(self):
        """Test delete service command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'dc_id': 'dcid-414b-aa5e-dedbeef00101'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_delete,
                          self.gc,
                          args)

    def test_do_service_delete_no_json_data_error(self):
        """Test delete service command without json_data."""
        input = {'type': 'dcconnect'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_delete,
                          self.gc,
                          args)

    def test_do_service_delete_json_format_error(self):
        """Test delete service command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'dcconnect'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_delete,
                          self.gc,
                          args)

    def test_do_service_get(self):
        """Test get dcconnect command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101'}
        input = {'type': 'all_dcconnect',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.service,
                               'get') as mocked_func:
            mocked_func.return_value = return_service_data
            v1shell.do_service_get(self.gc, args)

            fields = json_data
            fields['function_type'] = 'all_dcconnect'

            mocked_func.assert_called_once_with(fields)

    def test_do_service_get_no_type_error(self):
        """Test get service command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_get,
                          self.gc,
                          args)

    def test_do_service_get_no_json_data_error(self):
        """Test get service command without json_data."""
        input = {'type': 'dcconnect'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_get,
                          self.gc,
                          args)

    def test_do_service_get_json_format_error(self):
        """Test get service command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'dcconnect'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_service_get,
                          self.gc,
                          args)

    def test_do_resource_create(self):
        """Test create resource command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'test_tenant',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101'}
        input = {'type': 'globalip',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.resource,
                               'create') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_resource_create(self.gc, args)

            fields = json_data
            fields['function_type'] = 'globalip'

            mocked_func.assert_called_once_with(fields)

    def test_do_resource_create_no_type_error(self):
        """Test create resource command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'test_tenant',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101',
                     'IaaS_network_type': 'vxlan',
                     'IaaS_network_id': 'netid-414b-aa5e-dedbeef00101',
                     'network_name': 'test_network',
                     'dc_id': 'dcid-414b-aa5e-dedbeef00101',
                     'fw_ip_address': '10.20.30.11'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_create,
                          self.gc,
                          args)

    def test_do_resource_create_no_json_data_error(self):
        """Test create resource command without json_data."""
        input = {'type': 'globalip'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_create,
                          self.gc,
                          args)

    def test_do_resource_create_json_format_error(self):
        """Test create resource command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'globalip'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_create,
                          self.gc,
                          args)

    def test_do_resource_update(self):
        """Test update resource command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'tanant_name',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101'}
        input = {'type': 'globalip',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.resource,
                               'update') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_resource_update(self.gc, args)

            fields = json_data
            fields['function_type'] = 'globalip'

            mocked_func.assert_called_once_with(fields)

    def test_do_resource_update_no_type_error(self):
        """Test update resource command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_name': 'tanant_name',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_update,
                          self.gc,
                          args)

    def test_do_resource_update_no_json_data_error(self):
        """Test update resource command without json_data."""
        input = {'type': 'globalip'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_update,
                          self.gc,
                          args)

    def test_do_resource_update_json_format_error(self):
        """Test update resource command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'globalip'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_update,
                          self.gc,
                          args)

    def test_do_resource_delete(self):
        """Test delete resource command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101'}
        input = {'type': 'globalip',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.resource,
                               'delete') as mocked_func:
            mocked_func.return_value = return_status
            v1shell.do_resource_delete(self.gc, args)

            fields = json_data
            fields['function_type'] = 'globalip'

            mocked_func.assert_called_once_with(fields)

    def test_do_resource_delete_no_type_error(self):
        """Test delete resource command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101',
                     'IaaS_region_id': 'regionid-414b-aa5e-dedbeef00101'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_delete,
                          self.gc,
                          args)

    def test_do_resource_delete_no_json_data_error(self):
        """Test delete resource command without json_data."""
        input = {'type': 'globalip'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_delete,
                          self.gc,
                          args)

    def test_do_resource_delete_json_format_error(self):
        """Test delete resource command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'globalip'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_delete,
                          self.gc,
                          args)

    def test_do_resource_get(self):
        """Test get resource command."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101'}
        input = {'type': 'all_resource',
                 'json_data': json.dumps(json_data)}
        args = self._make_args(input)
        with mock.patch.object(self.gc.resource,
                               'get') as mocked_func:
            mocked_func.return_value = return_resource_data
            v1shell.do_resource_get(self.gc, args)

            fields = json_data
            fields['function_type'] = 'all_resource'

            mocked_func.assert_called_once_with(fields)

    def test_do_resource_get_no_type_error(self):
        """Test get resource command without type."""
        json_data = {'operation_id': 'test_user-414b-aa5e-dedbeef00101',
                     'IaaS_tenant_id': 'tenantid-414b-aa5e-dedbeef00101'}
        input = {'json_data': json.dumps(json_data)}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_get,
                          self.gc,
                          args)

    def test_do_resource_get_no_json_data_error(self):
        """Test get resource command without json_data."""
        input = {'type': 'globalip'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_get,
                          self.gc,
                          args)

    def test_do_resource_get_json_format_error(self):
        """Test get resource command json format error."""
        input = {'json_data': 'no_json_data',
                 'type': 'globalip'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_resource_get,
                          self.gc,
                          args)
