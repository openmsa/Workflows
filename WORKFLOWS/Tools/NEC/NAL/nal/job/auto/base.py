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
import socket
import struct
import time
import traceback

from job.conf import config
from job.lib import logger
from job.lib.common import utils
from job.lib.db import list
from job.lib.db import update
from job.lib.openstack.glance import images
from job.lib.openstack.keystone import tokens
from job.lib.openstack.nova import flavors
from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import ports
from job.lib.openstack.quantum import subnets


class JobAutoBase:

    LOG_TYPE_INPUT = 'in'
    LOG_TYPE_OUTPUT = 'out'
    JOB_SOAP_MODULE_PATH = 'job.lib.soap.msa'

    def __init__(self, request_id='-'):
        self.job_config = config.JobConfig()
        self.logger = logger.LibLogger(self.job_config, request_id)
        self.utils = utils.Utils()
        self.log_deco_line = self.job_config.LOG_DECORATE_LINE

        self.nal_endpoint_config = self.get_config('nal_ep')
        self.nal_config = self.get_config('nal_conf')
        self.nal_endpoint_config.update(self.get_config('wim_ep'))
        self.nal_config.update(self.get_config('wim_conf'))

    def get_config(self, config_type):

        if config_type == 'nal_ep':
            ep_uri = self.job_config.REST_URI_NAL_ENDPOINT
            column_name = 'endpoint_info'
        elif config_type == 'nal_conf':
            ep_uri = self.job_config.REST_URI_NAL_CONFIG
            column_name = 'config_info'
        elif config_type == 'wim_ep':
            ep_uri = self.job_config.REST_URI_WIM_ENDPOINT
            column_name = 'endpoint_info'
        elif config_type == 'wim_conf':
            ep_uri = self.job_config.REST_URI_WIM_CONFIG
            column_name = 'config_info'
        else:
            raise SystemError('configration type is invalid.')

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(ep_uri)

        # Create Instance(DB Client)
        db_list_instance = list.ListClient(self.job_config)

        # List NAL_POD_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        db_list_instance.set_context(db_endpoint, params)
        db_list_instance.execute()
        pod_list = db_list_instance.get_return_param()

        ep_config = {}
        for row in pod_list:

            dc_id = row['dc_id']

            if str(row['type']) == '1':
                ep_type = 'vim'
                ep_id = row['pod_id']
            elif str(row['type']) == '2':
                ep_type = 'iaas'
                ep_id = row['region_id']
            elif str(row['type']) == '3':
                ep_type = 'msa'
                ep_id = row['pod_id']
            elif str(row['type']) == '4':
                ep_type = 'vxlangw'
                ep_id = row['region_id']
            elif str(row['type']) == '5':
                ep_type = 'common'
                ep_id = ''
            else:
                continue

            if dc_id in ep_config:
                if ep_type in ep_config[dc_id]:
                    wk_conf = {}
                    if str(row['type']) == '5':
                        wk_conf = json.loads(row[column_name])
                    else:
                        wk_conf[ep_id] = json.loads(row[column_name])
                    ep_config[dc_id][ep_type].update(wk_conf)
                else:
                    wk_conf = {}
                    wk_conf[ep_type] = {}
                    if str(row['type']) == '5':
                        wk_conf[ep_type] = json.loads(row[column_name])
                    else:
                        wk_conf[ep_type][ep_id] = json.loads(row[column_name])
                    ep_config[dc_id].update(wk_conf)
            else:
                wk_conf = {}
                wk_conf[dc_id] = {}
                wk_conf[dc_id][ep_type] = {}
                if str(row['type']) == '5':
                    wk_conf[dc_id][ep_type] = json.loads(row[column_name])
                else:
                    wk_conf[dc_id][ep_type][ep_id] = json.loads(row[column_name])
                ep_config.update(wk_conf)

        return ep_config

    def device_type_to_name(self,
                            apl_type,
                            nf_type,
                            device_type,
                            dc_id='system'):

        device_type_name = \
            self.nal_config[dc_id]['common']['device_name_list'].\
                                                    get(str(apl_type), {}).\
                                                    get(str(nf_type), {}).\
                                                    get(str(device_type), {}).\
                                                    get('name', '')

        return device_type_name

    def get_os_vlan_name(self, vlan_type, dc_id='system'):

        os_vlan_name = \
            self.nal_config[dc_id]['common']['os_vlan_name_list'].\
                                                    get(vlan_type, {}).\
                                                    get('name', '')

        return os_vlan_name

    def get_os_physical_network_name(self, dc_id='system'):

        os_physical_network_name = \
            self.nal_config[dc_id]['common']['os_physical_network'].\
                                                    get('name', '')

        return os_physical_network_name

    def get_nal_private_key_path(self, dc_id='system'):

        nal_private_key_path = \
            self.nal_config[dc_id]['common']['nal_private_key'].\
                                                    get('path', '')

        return nal_private_key_path

    def get_msa_config_for_common(self, pod_id, dc_id='system'):

        msa_config_for_common = \
            self.nal_config[dc_id]['msa'][pod_id]['msa_config_for_common']

        return msa_config_for_common

    def get_msa_config_for_device(self,
                                pod_id, device_type_name, dc_id='system'):

        msa_config_for_device = \
            self.nal_config[dc_id]['msa'][pod_id]['msa_config_for_device'].\
                get(device_type_name, {})

        return msa_config_for_device

    def get_os_endpoint_vim(self,
                        pod_id, tenant_name='', tenant_id='', dc_id='system'):

        osc_tokens = tokens.OscTokens(self.job_config)

        user_name = \
            self.nal_endpoint_config[dc_id]['vim'][pod_id]['user_id']
        user_pass = \
            self.nal_endpoint_config[dc_id]['vim'][pod_id]['user_password']
        endpoint_url = \
            self.nal_endpoint_config[dc_id]['vim'][pod_id]['endpoint']
        region_id = \
            self.nal_endpoint_config[dc_id]['vim'][pod_id]['region_id']

        token = osc_tokens.create_token(user_name, user_pass, endpoint_url)
        endpoint_array = osc_tokens.get_endpoints(
            endpoint_url, token, user_name, user_pass, tenant_id)

        if dc_id != 'system':
            endpoint_array['wim_fig'] = True

        endpoint_array['region_id'] = region_id

        return endpoint_array

    def get_os_endpoint_iaas(self,
                    region_id, tenant_name='', tenant_id='', dc_id='system'):

        osc_tokens = tokens.OscTokens(self.job_config)

        user_name = \
         self.nal_endpoint_config[dc_id]['iaas'][region_id]['user_id']
        user_pass = \
         self.nal_endpoint_config[dc_id]['iaas'][region_id]['user_password']
        endpoint_url = \
         self.nal_endpoint_config[dc_id]['iaas'][region_id]['endpoint']

        token = osc_tokens.create_token(user_name, user_pass, endpoint_url)
        endpoint_array = osc_tokens.get_endpoints(
            endpoint_url, token, user_name, user_pass, tenant_id)

        endpoint_array['region_id'] = region_id

        return endpoint_array

    def get_os_endpoint_vxlangw(self, region_id, dc_id='system'):

        vxlangw_endpoint = \
            self.nal_endpoint_config[dc_id]['vxlangw'][region_id]
        return vxlangw_endpoint

    def wait_os_server_active(self, osc_servers_instance, os_endpoint,
                    server_id, boot_count, boot_interval, after_wait_time):

        for wait_count in range(boot_count):

            get_server_res = osc_servers_instance.get_server(
                                                    os_endpoint, server_id)

            if get_server_res['server']['status']\
                                == osc_servers_instance.SERVER_STATUS_ACTIVE:
                break

            elif get_server_res['server']['status']\
                                == osc_servers_instance.SERVER_STATUS_ERROR:
                raise SystemError('OpenStack Server can not be created.')

            time.sleep(boot_interval)
            wait_count += 1

            if wait_count == boot_count:
                raise SystemError(
                'Exceeded Limit Count: OpenStack Server Waiting(Active).')

        time.sleep(after_wait_time)

    def check_msa_provisioning_status(self, msa_instance, device_id,
                                    check_count, retry_count, wait_time,
                                    apl_type='', nf_type='', device_type='',
                                    msa_sshws='', vnf_ip='', ssh_port='',
                                    msa_devicefieldsws=''):

        if str(apl_type) == str(self.job_config.APL_TYPE_VR) and (
            (str(nf_type) == str(self.job_config.TYPE_FW) and \
                str(device_type) in [
                        str(self.job_config.DEV_TYPE_IS_VM_SG),
                        str(self.job_config.DEV_TYPE_IS_VM_SG_PUB)]) or \
            (str(nf_type) == str(self.job_config.TYPE_LB) and \
                str(device_type) in [
                        str(self.job_config.DEV_TYPE_IS_VM_LB)])):

            #check_ssh_connect_possible_confirm
            self.check_ssh_connect_possible_confirm(msa_sshws,
                                        vnf_ip,
                                        ssh_port)
            # Provisioning(MSA)
            msa_instance.do_provisioning_by_device_id(device_id)
            return

        retry_limit_count = retry_count - 1

        for ng_cnt in range(retry_count):

            if str(apl_type) == str(self.job_config.APL_TYPE_VR):
                #check_ssh_connect_possible_confirm
                self.check_ssh_connect_possible_confirm(msa_sshws,
                                        vnf_ip,
                                        ssh_port)

            if str(apl_type) == str(self.job_config.APL_TYPE_PH) and \
                    str(nf_type) == str(self.job_config.TYPE_FW) and \
                    str(device_type) in [
                        str(self.job_config.DEV_TYPE_PHY_PALOALTO),
                        str(self.job_config.DEV_TYPE_PHY_PALOALTO_SHARE)]:
                # Change host name for Paloalto
                msa_devicefieldsws.set_hostname(device_id, 'vsys1')

            # Provisioning(MSA)
            msa_instance.do_provisioning_by_device_id(device_id)

            limit_count = check_count - 1

            for c_cnt in range(check_count):

                msa_res = msa_instance.get_provisioning_status_by_id(device_id)

                status = msa_res[msa_instance.RES_KEY_OUT]['status']
                result = json.loads(
                            msa_res[msa_instance.RES_KEY_OUT]['rawJSONResult'])

                if status not in ['OK', 'RUNNING']:
                    break

                if status == 'OK' and len(result['sms_result']) > 0:
                    return

                if c_cnt == limit_count:
                    raise SystemError(
                            'Exceeded Limit Count: MSA Provisioning Waiting.')

                time.sleep(wait_time)

            if ng_cnt == retry_limit_count:
                raise SystemError(
                    'MSA Object Response(getProvisioningStatusById) ' \
                    + 'is not Normal:' \
                    + str(msa_res[msa_instance.RES_KEY_OUT]))

            time.sleep(wait_time)

    def check_ssh_connect_possible_confirm(self, msa_instance,
                                           vnf_ip, ssh_port):

        for count in range(self.job_config.SSH_CONNECTION_COUNT):
            msa_res = msa_instance.confirm_ssh_status(vnf_ip, ssh_port)
            status = msa_res['status']

            if status == 'OK':
                break
            else:
                time.sleep(self.job_config.SSH_CONNECTION_INTERVAL)
                count += 1

            if count == self.job_config.SSH_CONNECTION_COUNT:
                raise SystemError(
                    'Exceeded Limit Count: MSA Provisioning Waiting.')

    def get_os_uuid_image_flavor(self, hardware_type, device_type,
                                 pod_id, tenant_id, dc_id='system'):

        os_image_and_flavor = \
            self.nal_config[dc_id]['common']['os_image_and_flavor_name_list']

        image_and_flavor_name = \
            os_image_and_flavor[str(hardware_type)][str(device_type)]

        # Get Endpoint(OpenStack:VIM)
        os_endpoint = self.get_os_endpoint_vim(pod_id, '', tenant_id, dc_id)

        # Create Instance (OpenStack Client)
        osc_flavors = flavors.OscNovaFlavors(self.job_config)
        osc_images = images.OscGlanceImages(self.job_config)

        # refer flavor (OpenStack Client)
        result = osc_flavors.list_flavors(os_endpoint)
        for rec in result['flavors']:
            if rec['name'] == image_and_flavor_name['flavor_name']:
                flavor_id = rec['id']
                break

        # refer image (OpenStack Client)
        result = osc_images.list_images(os_endpoint)
        for rec in result['images']:
            if rec['name'] == image_and_flavor_name['image_name']:
                image_id = rec['id']
                break

        uuid_image_flavor = {'flavor_id': flavor_id,
                             'image_id': image_id}

        return uuid_image_flavor

    def output_log_job_params(self,
                log_type, module, function, params, passwords=[]):

        passwords = self.utils.json_encode_passwords(passwords)

        if isinstance(params, str) == False:
            params = json.dumps(params)

        if log_type == self.LOG_TYPE_INPUT:
            log_msg_type = '[INPUT]'
        else:
            log_msg_type = '[OUTPUT]'

        # Output Log(SoapClient Input Parameters)
        log_msg = '[Job Automation]' + function + log_msg_type
        log_msg += "\n" + self.log_deco_line
        log_msg += "\n" + params
        log_msg += "\n" + self.log_deco_line
        self.logger.log_debug(module, log_msg, passwords)

    def output_log_fatal(self, module, msg):

        self.logger.log_fatal(module, msg)

    def get_db_endpoint(self, uri):

        return self.job_config.REST_ENDPOINT + uri

    def get_msa_client_result(self, msa_res_out, key):

        return msa_res_out[key]

    def get_os_network_info(self, pod_id, tenant_id,
                                    vlan_type, ip_version='', dc_id='system'):

        network_name = self.get_os_vlan_name(vlan_type, dc_id)

        if len(ip_version) == 0:
            ip_version = self.utils.IP_VER_V4

        # Get Endpoint(OpenStack:VIM)
        os_endpoint = self.get_os_endpoint_vim(pod_id, '', tenant_id, dc_id)

        # Create Instance (OpenStack Client)
        osc_networks = networks.OscQuantumNetworks(self.job_config)
        osc_subnets = subnets.OscQuantumSubnets(self.job_config)

        # List Networks (OpenStack Client)
        result = osc_networks.list_networks(os_endpoint)

        for rec in result['networks']:

            if rec['name'] == network_name:
                network_id = rec['id']
                subnet_list = rec['subnets']
                vlan_id = rec['provider:segmentation_id']
                network_type = rec['provider:network_type']
                break

        network_info = {}
        subnet_info = {}
        for subnet_id in subnet_list:

            # Get Subnet (OpenStack Client)
            subnets_res = osc_subnets.get_subnet(os_endpoint, subnet_id)

            if str(subnets_res['subnet']['ip_version']) == ip_version:

                # get first record
                subnet_info = subnets_res['subnet']
                break

        if len(subnet_info) > 0:

            array = subnet_info['cidr'].split('/')
            network_info = {
                'network_name': network_name,
                'network_id': network_id,
                'subnet_id': subnet_info['id'],
                'cidr': subnet_info['cidr'],
                'network_address': array[0],
                'subnet_mask': array[1],
                'vlan_id': vlan_id,
                'network_type': network_type
            }

        return network_info

    def get_wan_allocation_info(self, group_type, dc_id):

        if group_type in [
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_ESP),
                str(self.job_config.GROUP_TYPE_CSRV_TUNNEL_AH),
            ]:
            wan_allocation_info = self.get_wan_allocation_info_for_tunnel(
                                                                    dc_id)
        else:
            wan_allocation_info = self.nal_config[
                            dc_id]['common']['inter_dc_netowrk_info'][dc_id]

            # Compress IPv6 Address
            for rt, rt_array in wan_allocation_info.items():
                wan_v6 = rt_array['wan'].get(self.utils.IP_VER_V6, {})
                if len(wan_v6) == 0:
                    continue
                if 'ip' in wan_v6:
                    wan_v6['ip'] = self.utils.get_ipaddress_compressed(
                                                                wan_v6['ip'])
                if 'subnet_ip' in wan_v6:
                    wan_v6['subnet_ip'] = \
                            self.utils.get_ipaddress_compressed(
                                                        wan_v6['subnet_ip'])
                wan_allocation_info[rt]['wan'][
                                                self.utils.IP_VER_V6] = wan_v6

        return wan_allocation_info

    def get_wan_allocation_info_for_tunnel(self, dc_id):

        inter_dc = self.nal_config[dc_id]['common'][
                                'inter_dc_netowrk_info_for_tunnel'][dc_id]

        # Compress IPv6 Address
        for rt_self, rt_self_array in inter_dc.items():

            for dc_other, dc_other_array in rt_self_array['tenant'].items():

                for rt_other, rt_other_array in dc_other_array.items():

                    tenant_v6 = rt_other_array[self.utils.IP_VER_V6]

                    tenant_v6['ip'] = \
                    self.utils.get_ipaddress_compressed(tenant_v6['ip'])

                    tenant_v6['network'] = \
                    self.utils.get_ipaddress_compressed(tenant_v6['network'])

                    inter_dc[rt_self]['tenant'][dc_other][rt_other][
                                            self.utils.IP_VER_V6] = tenant_v6

        return inter_dc

    def execute_msa_command(self,
                            msa_config_for_device,
                            instance,
                            job_method_name,
                            *args):

        # Create Instance(Job Automation)
        method_attr = getattr(instance, job_method_name)

        for count in range(int(self.job_config.MSA_SSH_RETRY_COUNT)):

            # Execute Method(Job Automation)
            msa_res = method_attr(*args)

            if msa_res['out']['status'] == 'ERROR':
                if self.job_config.SOAP_SSH_ERR_STR \
                                in msa_res['out']['message']:
                    pass
                else:
                    raise SystemError('Request to MSA failed.')
            else:
                break

            time.sleep(int(self.job_config.MSA_SSH_RETRY_INTERVAL))
            count += 1

        if count == int(self.job_config.MSA_SSH_RETRY_COUNT):
            raise SystemError(
            'Request to MSA failed. By Connection closed by peer.')

        return msa_res

    def get_os_endpoint_info_vim(self, pod_id, dc_id='system'):

        return self.nal_endpoint_config[dc_id]['vim'][pod_id]

    def get_os_endpoint_info_iaas(self, region_id, dc_id='system'):

        return self.nal_endpoint_config[dc_id]['iaas'][region_id]

    def get_free_ip_max(self, job_input, subnet_id=''):

        free_ip = {}
        free_ip1 = {}
        free_ip2 = {}
        free_ip3 = {}

        # Get JOB Input Parameters
        iaas_region_id = job_input['IaaS_region_id']
        iaas_tenant_id = job_input['IaaS_tenant_id']
        iaas_network_id = job_input['IaaS_network_id']
        nal_tenant_id = job_input['nal_tenant_id']
        dc_id = job_input.get('dc_id', 'system')

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Create Instance(OpenStack Client)
        os_subnets = subnets.OscQuantumSubnets(self.job_config)
        os_ports = ports.OscQuantumPorts(self.job_config)

        if vim_iaas_with_flg == 0:
            iaas_token_tenant = iaas_tenant_id
        else:
            iaas_token_tenant = nal_tenant_id

        # Get Endpoint(OpenStack:IaaS)
        os_endpoint_iaas = self.get_os_endpoint_iaas(iaas_region_id,
                                                     '',
                                                     iaas_token_tenant,
                                                     dc_id)

        # List Subnets(OpenStack)
        os_subnet_list = os_subnets.list_subnets(os_endpoint_iaas)

        # List Ports(OpenStack)
        os_port_list = os_ports.list_ports(os_endpoint_iaas)

        port_list = []
        for port_array in os_port_list['ports']:

            if port_array['network_id'] == iaas_network_id:
                port_list.append(port_array)

        for subnet_array in os_subnet_list['subnets']:

            if str(subnet_array['ip_version']) != self.utils.IP_VER_V4:
                continue

            if subnet_id != '' and subnet_id != subnet_array['id']:
                continue

            if subnet_array['network_id'] == iaas_network_id:

                cidr = subnet_array['cidr']
                netmask = cidr.split('/')
                network_range = self.utils.get_network_range_from_cidr(cidr)
                network_bin = network_range['network']
                broadcast_bin = network_range['broadcast']

                ip_tmp = broadcast_bin - 1
                end = network_bin + 1

                while ip_tmp > end:

                    ip_inuse = False

                    for port in port_list:

                        for fixed_ip in port['fixed_ips']:

                            if self.utils.get_ipaddress_version(fixed_ip[
                                    'ip_address']) != self.utils.IP_VER_V4:
                                continue

                            fixed_ip_address = fixed_ip['ip_address']
                            fixed_ip_address = struct.unpack(
                                '!i', socket.inet_aton(fixed_ip_address))[0]

                            if fixed_ip_address == ip_tmp:
                                ip_inuse = True
                                break

                        if ip_inuse == True:
                            break

                    if ip_inuse == False:

                        free_ip_tmp = {}
                        free_ip_tmp['ip'] \
                            = socket.inet_ntoa(struct.pack(r'!i', (ip_tmp)))
                        free_ip_tmp['cidr'] = cidr
                        free_ip_tmp['netmask'] = netmask[1]
                        free_ip_tmp['subnet_ip'] = netmask[0]
                        free_ip_tmp['id'] = subnet_array['id']

                        if free_ip_tmp['ip'] \
                                            == subnet_array['gateway_ip']:

                            if self.job_config.USE_GATEWAY_ADDR_VLAN_IP \
                                            == True  and len(free_ip3) == 0:
                                free_ip3 = free_ip_tmp

                        else:

                            ip_indhcp = False

                            for dhcp in subnet_array['allocation_pools']:

                                dhcp_start_bin = struct.unpack(
                                    '!i', socket.inet_aton(dhcp['start']))[0]

                                dhcp_end_bin = struct.unpack(
                                    '!i', socket.inet_aton(dhcp['end']))[0]

                                if ip_tmp >= dhcp_start_bin \
                                                and ip_tmp <= dhcp_end_bin:

                                    ip_indhcp = True
                                    break

                            if ip_indhcp == True:

                                if len(free_ip2) == 0:
                                    free_ip2 = free_ip_tmp

                            else:
                                free_ip1 = free_ip_tmp
                                break

                    ip_tmp = ip_tmp - 1

            if len(free_ip1) > 0:
                break

        if len(free_ip1) > 0:
            free_ip = free_ip1

        elif len(free_ip2) > 0:
            free_ip = free_ip2

        elif len(free_ip3) > 0:
            free_ip = free_ip3

        if len(free_ip) == 0:
            raise SystemError('free_ip not found')

        return free_ip

    def assign_port(self,
                    db_list_instance,
                    db_endpoint_port,
                    tenant_id,
                    apl_type,
                    node_id,
                    port_name,
                    nf_type,
                    device_type,
                    network_type_detail=None):

        # List NAL_PORT_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = tenant_id
        params['apl_type'] = apl_type
        params['node_id'] = node_id
        if network_type_detail is not None:
            params['network_type_detail'] = network_type_detail
        db_list_instance.set_context(db_endpoint_port, params)
        db_list_instance.execute()
        port_list = db_list_instance.get_return_param()

        array_prot_number = []
        for port in port_list:
            nic = port.get('nic')
            if isinstance(nic, str) and len(nic) > 0:
                nic = nic.replace(port_name, '')
                array_prot_number.append(int(nic))

        if len(array_prot_number) == 0:
            if str(apl_type) == '1':
                if str(nf_type) == '1' and str(device_type) in ['2', '5']:
                    number = 1
                else:
                    number = 0
            else:
                number = 1
        else:
            number = max(array_prot_number) + 1

        return port_name + str(number)

    def set_status_error(self, job_input, error_info):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        if 'apl_table_rec_id' in job_input:
            apl_table_rec_id = job_input['apl_table_rec_id']

            # Get Error Information
            try:
                if hasattr(error_info, 'args'):
                    err_info = json.dumps(error_info.args)
                else:
                    err_info = error_info.__str__()
            except:
                err_info = 'An unexpected error has occurred'

            # Create Instance(DB Client)
            db_update = update.UpdateClient(self.job_config)

            # Get Endpoint(DB Client)
            db_endpoint_apl = self.get_db_endpoint(
                                        self.job_config.REST_URI_APL)

            params = {}
            params['task_status'] = 9
            params['update_id'] = operation_id
            params['err_info'] = err_info
            keys = [apl_table_rec_id]
            db_update.set_context(db_endpoint_apl, keys, params)
            db_update.execute()

        elif 'group_rec_id' in job_input:
            group_rec_id = job_input['group_rec_id']

            # Get Error Information
            try:
                if hasattr(error_info, 'args'):
                    err_info = json.dumps(error_info.args)
                else:
                    err_info = error_info.__str__()
            except:
                err_info = 'An unexpected error has occurred'

            # Create Instance(DB Client)
            db_update = update.UpdateClient(self.job_config)

            # Get Endpoint(DB Client)
            db_endpoint_dc_group = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_CON_GROUP)

            params = {}
            params['task_status'] = 9
            params['update_id'] = operation_id
            params['err_info'] = err_info
            keys = [group_rec_id]
            db_update.set_context(db_endpoint_dc_group, keys, params)
            db_update.execute()

    def set_msa_dns_address(self, job_input, msa_config_for_common):

        # Set MSA Parameters(DNS IP Address)
        dns_server_primary = job_input.get('dns_server_primary', '')
        dns_server_secondary = job_input.get('dns_server_secondary', '')

        if len(dns_server_primary) == 0:
            dns_server_primary = msa_config_for_common.get(
                                    'svc_vlan_dns_primary_ip_address', '')
            dns_server_secondary = msa_config_for_common.get(
                                    'svc_vlan_dns_secondary_ip_address', '')

        return {
            'dns_server_primary': dns_server_primary,
            'dns_server_secondary': dns_server_secondary,
        }

    def set_msa_ntp_address(self, job_input, msa_config_for_common):

        # Set MSA Parameters(NTP IP Address)
        ntp_server_primary = job_input.get('ntp_server_primary', '')
        ntp_server_secondary = job_input.get('ntp_server_secondary', '')

        if len(ntp_server_primary) == 0:
            ntp_server_primary = msa_config_for_common.get(
                                'svc_vlan_ntp_primary_ip_address', '')
            ntp_server_secondary = msa_config_for_common.get(
                                'svc_vlan_ntp_secondary_ip_address', '')

        return {
            'ntp_server_primary': ntp_server_primary,
            'ntp_server_secondary': ntp_server_secondary,
        }

    def get_apl_msa_input_params(self,
                                 apl_device_detail,
                                 msa_method_name,
                                 msa_obj_name,
                                 msa_param_name='',
                                 job_cleaning_mode='0'):

        try:
            device_detail = json.loads(apl_device_detail)
            object_parameters = json.loads(device_detail[
                                        msa_method_name]['objectParameters'])

            msa_input_params = {}
            for key in object_parameters[msa_obj_name].keys():
                msa_input_params = object_parameters[msa_obj_name][key]

            if msa_param_name == '':
                return msa_input_params
            else:
                return msa_input_params[msa_param_name]
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
                if msa_param_name == '':
                    return {}
                else:
                    return ''
            else:
                raise

    def _get_dc_segment(self, dc_id, group_id):

        # Get Endpoint(DB Client)
        db_endpoint_dc_segment = self.get_db_endpoint(
                                self.job_config.REST_URI_WIM_DC_SEGMENT_MNG)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['dc_id'] = dc_id
        params['group_id'] = group_id
        params['status'] = '1'
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_dc_segment, params)
        db_list.execute()
        dc_segment_list = db_list.get_return_param()

        return dc_segment_list[0]

    def _update_db_port(self, update_params, port_rec_id):

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        keys = [port_rec_id]
        db_update.set_context(db_endpoint_port, keys, update_params)
        db_update.execute()

    def get_vim_iaas_with_flg(self, job_input):
        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        dc_id = job_input.get('dc_id', 'system')

        # Get Endpoint(OpenStack:VIM)
        endpoint_config = self.nal_endpoint_config[dc_id]['vim'][pod_id]

        vim_iaas_with_flg_str = endpoint_config.get('vim_iaas_with_flg', '0')

        vim_iaas_with_flg = int(vim_iaas_with_flg_str)

        return vim_iaas_with_flg
