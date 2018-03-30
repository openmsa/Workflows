# -*- coding: utf-8 -*-

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
import ipaddress
import json
import re
import socket
import struct
import subprocess


class Utils:

    CIDR_REGEXP = '([\d\.]+)\/(\d+)'

    IP_VER_V4 = '4'
    IP_VER_V6 = '6'

    def get_hash_value(self, shebang, char_set, stdout_sep, src_str):

        cmd = shebang + 'openssl passwd -1 ' + src_str

        output = subprocess.check_output(cmd.split(" "))
        output = output.decode(char_set)
        output = output.split(stdout_sep)
        output.pop()

        return output[0]

    def json_encode_passwords(self, passwords):

        passwords_enc = []

        for val in passwords:

            if isinstance(val, str) and len(val) > 0:
                val_enc = json.dumps([val])
                val_enc = val_enc.replace('["', '')
                val_enc = val_enc.replace('"]', '')
                passwords_enc.append(val_enc)
            else:
                passwords_enc.append(val)

        return passwords_enc

    def get_subnet_mask_from_cidr_len(self, cidr_len):

        if isinstance(cidr_len, str):
            cidr_len = int(cidr_len)

        # Convert SubnetMask To IPv4 Style
        subnet_mask = socket.inet_ntoa(struct.pack(
                '!L', 0xffffffff ^ ((1 << 32 - cidr_len) - 1)))

        return subnet_mask

    def get_ipmask_from_cidr_ip(self, cidr):

        pattern = re.compile(self.CIDR_REGEXP)
        matchOB = pattern.match(cidr)
        if matchOB:
            ip_address = matchOB.group(1)
            length = int(matchOB.group(2))

            # Convert SubnetMask To IPv4 Style
            subnet_mask = socket.inet_ntoa(struct.pack(
                '!L', 0xffffffff ^ ((1 << 32 - length) - 1)))

        else:
            raise SystemError('Invalid Value(cidr):' + cidr)

        return {'ip_address': ip_address, 'subnet_mask': subnet_mask}

    def get_network_range_from_cidr(self, cidr):

        ipmask = self.get_ipmask_from_cidr_ip(cidr)
        ip_address = ipmask['ip_address']
        subnet_mask = ipmask['subnet_mask']

        ip_bin = struct.unpack('!i', socket.inet_aton(ip_address))[0]
        mask_bin = struct.unpack('!i', socket.inet_aton(subnet_mask))[0]

        network = ip_bin & mask_bin
        broadcast = ip_bin | ~mask_bin

        return {'network': network, 'broadcast': broadcast}

    def get_subnet_mask_from_cidr_ipv6(self, cidr):

        network = ipaddress.ip_network(
                    ipaddress.ip_interface(cidr).network)

        return str(network.netmask)

    def get_network_range_from_cidr_ipv6(self, cidr):

        network = ipaddress.ip_network(
                    ipaddress.ip_interface(cidr).network)

        return {
            'network': network.network_address,
            'broadcast': network.broadcast_address
        }

    def get_ipaddress_version(self, ip_address):

        return str(ipaddress.ip_address(ip_address).version)

    def get_ipaddress_compressed(self, ip_address):

        return str(ipaddress.ip_address(ip_address).compressed)

    def get_ipaddress_compressed_paloalto_vm(self, ip_address):

        ip_address = self.get_ipaddress_compressed(ip_address)

        ip_address_list = ip_address.split(':')

        ip_address_res = []

        for ip in ip_address_list:
            if ip == '0':
                ip = ''
            ip_address_res.append(ip)

        return ':'.join(ip_address_res)

    def get_cidr_compressed(self, cidr):

        subnet = cidr.split('/')
        subnet_ip = self.get_ipaddress_compressed(subnet[0])
        subnet_mask = subnet[1]

        return {
            'cidr': subnet_ip + '/' + subnet_mask,
            'ip': subnet_ip,
            'netmask': subnet_mask,
        }
