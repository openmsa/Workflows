import inspect
import socket
import struct
import unittest

from job.lib.common import utils
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

    def test_get_ipmask_from_cidr_ip(self):

        cidr = '192.168.79.0/24'

        res = utils.Utils().get_ipmask_from_cidr_ip(cidr)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_get_network_range_from_cidr(self):

        cidr = '192.168.79.0/24'

        res = utils.Utils().get_network_range_from_cidr(cidr)
        print(inspect.currentframe().f_code.co_name)
        pprint(res)
        print(socket.inet_ntoa(struct.pack(r'!i', (res['network']))))
        print(socket.inet_ntoa(struct.pack(r'!i', (res['broadcast']))))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_get_subnet_mask_from_cidr_ipv6(self):

        print(inspect.currentframe().f_code.co_name + '[IPv4]')
        cidr = '192.168.79.0/24'
        res = utils.Utils().get_subnet_mask_from_cidr_ipv6(cidr)
        print(type(res))
        print(res)

        print(inspect.currentframe().f_code.co_name + '[IPv6]')
        cidr = 'dead:beef::3/48'
        res = utils.Utils().get_subnet_mask_from_cidr_ipv6(cidr)
        print(type(res))
        print(res)

    def test_get_network_range_from_cidr_ipv6(self):

        print(inspect.currentframe().f_code.co_name + '[IPv4]')

        cidr = '192.168.79.0/24'
        res = utils.Utils().get_network_range_from_cidr_ipv6(cidr)
        print(res)
        print(str(res['network']))
        print(str(res['broadcast']))

        network_bin = struct.unpack(
                '!i', socket.inet_aton(str(res['network'])))[0]
        broadcast_bin = struct.unpack(
                '!i', socket.inet_aton(str(res['broadcast'])))[0]

        print(network_bin)
        print(broadcast_bin)

        print(socket.inet_ntoa(struct.pack(r'!i', (network_bin))))
        print(socket.inet_ntoa(struct.pack(r'!i', (broadcast_bin))))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        print(inspect.currentframe().f_code.co_name + '[IPv6]')

        cidr = 'dead:beef::3/48'
        res = utils.Utils().get_network_range_from_cidr_ipv6(cidr)
        print(res)
        print(str(res['network']))
        print(str(res['broadcast']))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_get_ipaddress_version(self):

        print(inspect.currentframe().f_code.co_name + '[IPv4]')
        res = utils.Utils().get_ipaddress_version('192.168.0.1')
        print(type(res))
        print(res)

        # Assertion
        self.assertEqual(res, utils.Utils().IP_VER_V4)

        print(inspect.currentframe().f_code.co_name + '[IPv6]')
        res = utils.Utils().get_ipaddress_version('dead:beef::2')
        print(type(res))
        print(res)

        # Assertion
        self.assertEqual(res, utils.Utils().IP_VER_V6)

    def test_get_ipaddress_compressed(self):

        print(inspect.currentframe().f_code.co_name + '[IPv4]')
        res = utils.Utils().get_ipaddress_compressed('192.168.0.1')
        print(res)
        self.assertEqual(res, '192.168.0.1')

        print(inspect.currentframe().f_code.co_name + '[IPv6]')
        res = utils.Utils().get_ipaddress_compressed('DEAD:BEEF::2')
        print(res)
        self.assertEqual(res, 'dead:beef::2')

        res = utils.Utils().get_ipaddress_compressed('DEAD:BEEF::0')
        print(res)
        self.assertEqual(res, 'dead:beef::')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:260:88:0:80:3eff:fe5a:8ac9')
        print(res)
        self.assertEqual(res, '2001:260:88:0:80:3eff:fe5a:8ac9')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:260:88:0:0:3eff:fe5a:8ac9')
        print(res)
        self.assertEqual(res, '2001:260:88::3eff:fe5a:8ac9')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:260:88:0:0000:3eff:fe5a:8ac9')
        print(res)
        self.assertEqual(res, '2001:260:88::3eff:fe5a:8ac9')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:260:88:0:0:0:fe5a:8ac9')
        print(res)
        self.assertEqual(res, '2001:260:88::fe5a:8ac9')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:260:88:0:1:0:0:0')
        print(res)
        self.assertEqual(res, '2001:260:88:0:1::')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:260:88:0:0:1:0:0')
        print(res)
        self.assertEqual(res, '2001:260:88::1:0:0')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:0:0:1:0:0:0:1')
        print(res)
        self.assertEqual(res, '2001:0:0:1::1')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:0:0:1:0:0:0:0')
        print(res)
        self.assertEqual(res, '2001:0:0:1::')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:0:0:0:1:0:0:8ac9')
        print(res)
        self.assertEqual(res, '2001::1:0:0:8ac9')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:0:0:0:1:0:0:0')
        print(res)
        self.assertEqual(res, '2001::1:0:0:0')

    def test_get_ipaddress_compressed_paloalto_vm(self):

        print(inspect.currentframe().f_code.co_name + '[IPv4]')
        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                                    '192.168.0.1')
        print(res)
        self.assertEqual(res, '192.168.0.1')

        print(inspect.currentframe().f_code.co_name + '[IPv6]')
        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                                    'DEAD:BEEF::2')
        print(res)
        self.assertEqual(res, 'dead:beef::2')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                                    'DEAD:BEEF::0')
        print(res)
        self.assertEqual(res, 'dead:beef::')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:260:88:0:80:3eff:fe5a:8ac9')
        print(res)
        self.assertEqual(res, '2001:260:88::80:3eff:fe5a:8ac9')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:260:88:0:0:3eff:fe5a:8ac9')
        print(res)
        self.assertEqual(res, '2001:260:88::3eff:fe5a:8ac9')

        res = utils.Utils().get_ipaddress_compressed(
                                    '2001:260:88:0:0000:3eff:fe5a:8ac9')
        print(res)
        self.assertEqual(res, '2001:260:88::3eff:fe5a:8ac9')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:260:88:0:0:0:fe5a:8ac9')
        print(res)
        self.assertEqual(res, '2001:260:88::fe5a:8ac9')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:260:88:0:1:0:0:0')
        print(res)
        self.assertEqual(res, '2001:260:88::1::')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:260:88:0:0:1:0:0')
        print(res)
        self.assertEqual(res, '2001:260:88::1::')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:0:0:1:0:0:0:1')
        print(res)
        self.assertEqual(res, '2001:::1::1')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:0:0:1:0:0:0:0')
        print(res)
        self.assertEqual(res, '2001:::1::')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:0:0:0:1:0:0:8ac9')
        print(res)
        self.assertEqual(res, '2001::1:::8ac9')

        res = utils.Utils().get_ipaddress_compressed_paloalto_vm(
                                    '2001:0:0:0:1:0:0:0')
        print(res)
        self.assertEqual(res, '2001::1:::')

#
#         print('fe80::f' + format(int(1000), 'x'))
#         print('fe80::f' + format(int('4000'), 'x'))
#         print(format(int('4000'), 'x'))
#         print('{0:02d}'.format(int('101'))[-1:])
#         print('{0:02d}'.format(int('1'))[-1:])
#         print('{0:02d}'.format(int('10'))[-1:])
#         print('{0:02d}'.format(int('11'))[-1:])
#         print('{0:d}'.format(int('0')).replace('0', ''))
#         print('{0:d}'.format(int('1')))
#         print('{0:d}'.format(int('10')))
#
#         print(int(1))
#         print(str('1'))
