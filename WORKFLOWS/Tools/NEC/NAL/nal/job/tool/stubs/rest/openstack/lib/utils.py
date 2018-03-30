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
import json
import os
import random
import datetime
import ipaddress
import subprocess


class Utils:

    def create_uuid(self, char_set, stdout_sep):

        command = 'php ' + os.path.dirname(
                    os.path.abspath(__file__)) + '/../script/create_uuid.php'

        output = subprocess.check_output(
                            command,
                            shell=True,
                            stderr=subprocess.STDOUT,
                            )
        output = output.decode(char_set)
        output = output.split(stdout_sep)

        result = json.loads(output[0])
        return result['uuid']

    def create_instance_name(self):

        return 'instance-' \
            + '%04d' % random.choice(range(10000)) \
            + '%04d' % random.choice(range(10000))

    def create_mac_address(self):

        mac_address = []
        for i in range(6):
            mac_address.append('%02x' % random.choice(range(256)))

        return ':'.join(mac_address)

    def get_sysdate(self, suffix='Z'):

        return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + suffix

    def get_dict_value(self, dict_param, keys, notfound_val=None):

        for i, v in enumerate(keys):
            if v in dict_param:
                dict_param = dict_param[v]
            else:
                dict_param = notfound_val
                break

        return dict_param

    def get_ipaddress_not_inuse(self, allocation_pool):

        result = None
        start = ipaddress.ip_address(allocation_pool['start'])
        end = ipaddress.ip_address(allocation_pool['end'])
        inuse = allocation_pool['inuse']

        ip = start
        while ip >= start and ip < end:
            if str(ip) in inuse:
                ip = ip + 1
            else:
                result = str(ip)
                break

        return result

    def get_nw_from_cidr(self, cidr, gateway=None):

        interface = ipaddress.ip_interface(cidr)
        network = ipaddress.ip_network(interface.network)

        network_addr = network.network_address
        broadcast_addr = network.broadcast_address

        start_addr = network_addr + 1
        if gateway is not None:
            start_addr = ipaddress.ip_address(gateway) + 1

        return {'network': str(network_addr),
                'broadcast': str(broadcast_addr),
                'start': str(start_addr),
                'end': str(broadcast_addr - 1)}

    def is_ipaddress_usable(self, allocation_pool):

        result = False
        start = ipaddress.ip_address(allocation_pool['start'])
        end = ipaddress.ip_address(allocation_pool['end'])
        ip = ipaddress.ip_address(allocation_pool['ip'])
        inuse = allocation_pool['inuse']

        if ip not in inuse and ip.version == start.version:
            if ip >= start and ip <= end:
                result = True

        return result
