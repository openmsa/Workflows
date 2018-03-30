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
import inspect
import json
import re
import socket
import struct
import traceback
import uuid

from job.auto import base
from job.auto.extension import routingpod
from job.lib.db import create
from job.lib.db import list
from job.lib.db import update
from job.lib.openstack.quantum import networks
from job.lib.openstack.quantum import ports
from job.lib.openstack.quantum import subnets
from job.lib.script import vxlangw
from job.lib.soap.msa import msaordercmdws


class Port(base.JobAutoBase):

    def virtual_msa_port_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']
        apl_table_rec_id = job_input['apl_table_rec_id']

        # Get msa network info
        assign_network_info = self.__get_msa_network_info(tenant_name, pod_id)
        if len(assign_network_info) == 0:
            assign_network_info = self.__assign_msa_network(tenant_name,
                                                            pod_id,
                                                            nal_tenant_id,
                                                            operation_id,
                                                            job_input)

        msa_network_info = assign_network_info[0]

        # Create Port(OpenStack:VIM)
        os_port_res = self.__create_os_port_vim(
                                            pod_id,
                                            nal_tenant_id,
                                            msa_network_info['network_id'],
                                            msa_network_info['subnet_id'])

        # Get Port Info
        subnet_mask = msa_network_info['netmask']
        port_info = os_port_res['port']
        port_id = port_info['id']
        ip_address = port_info['fixed_ips'][0]['ip_address']
        device_ip_address = port_info['fixed_ips'][0]['ip_address']

        # Insert DB: NAL_PORT_MNG For MSA Port
        self.__insert_db_port(operation_id,
                                tenant_name,
                                pod_id,
                                nal_tenant_id,
                                apl_type,
                                msa_network_info['network_id'],
                                self.job_config.NW_TYPE_EX,
                                self.job_config.NW_TYPE_MSA,
                                port_id,
                                ip_address,
                                port_info,
                                subnet_mask,
                                apl_table_rec_id)

        # Set JOB Output Parameters
        job_output['port_id1'] = port_id
        job_output['device_ip_address'] = device_ip_address

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_msa_port_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_table_rec_id = job_input['apl_table_rec_id']
        node_id = job_input['node_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Get msa network info
        assign_network_info = self.__get_msa_network_info(tenant_name, pod_id)

        if len(assign_network_info) == 0:
            raise SystemError('vlan for MSA not Found.')

        msa_network_info = assign_network_info[0]

        # List NAL_PORT_MNG(DB)
        port_list = self.__list_db_port(apl_table_rec_id, node_id,
                                        msa_network_info['network_id'])

        if len(port_list) == 0:
            if job_cleaning_mode == '1':
                pass
            else:
                raise SystemError('port on MSA-lan not exists.')

        else:
            # Delete Port(OpenStack:VIM)
            self.__delete_os_port_vim(pod_id,
                                      nal_tenant_id,
                                      port_list[0]['port_id'],
                                      job_cleaning_mode)

            # Update NAL_PORT_MNG(DB): Set DeleteFlg On
            self.__delete_db_port_logical(operation_id, port_list[0]['ID'])

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def pub_port_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        tenant_name = job_input['tenant_name']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']
        apl_table_rec_id = job_input['apl_table_rec_id']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Network Info
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            '')

        # Create Port(OpenStack:VIM)
        os_port_res = self.__create_os_port_vim(pod_id,
                                                nal_tenant_id,
                                                pub_network_info['network_id'],
                                                pub_network_info['subnet_id'])

        # Get Port Info
        subnet_mask = pub_network_info['subnet_mask']
        port_info = os_port_res['port']
        port_id = port_info['id']
        ip_address = port_info['fixed_ips'][0]['ip_address']

        # Insert DB: NAL_PORT_MNG For Pub Port
        self.__insert_db_port(operation_id,
                              tenant_name,
                              pod_id,
                              nal_tenant_id,
                              apl_type,
                              pub_network_info['network_id'],
                              self.job_config.NW_TYPE_EX,
                              self.job_config.NW_TYPE_PUBLIC,
                              port_id,
                              ip_address,
                              port_info,
                              subnet_mask,
                              apl_table_rec_id)

        # Set JOB Output Parameters
        job_output['port_id2'] = port_id

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_pub_port_add_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        fixed_ip_v6_pub = job_input.get('fixed_ip_v6_pub', '')

        if len(fixed_ip_v6_pub) > 0:
            fixed_ip_v6_pub = self.utils.get_ipaddress_compressed(
                                                            fixed_ip_v6_pub)

        # Get Network Info
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            self.utils.IP_VER_V6)

        port_id_pub_ipv6 = ''

        if len(pub_network_info) > 0:

            subnet_id_ipv6 = pub_network_info['subnet_id']

            # List NAL_PORT_MNG(DB)
            port_list = self.__list_db_port('',
                                            node_id,
                                            pub_network_info['network_id'],
                                            nal_tenant_id,
                                            self.job_config.NW_TYPE_EX,
                                            self.job_config.NW_TYPE_PUBLIC)

            if len(port_list[0]['ip_address_v6']) == 0:

                port_rec_id = port_list[0]['ID']
                port_id_pub_ipv6 = port_list[0]['port_id']

                # Update Port(OpenStack:VIM)
                os_port_res = self.__add_os_port_fixed_ip_vim(
                                                    pod_id, nal_tenant_id,
                                                    port_id_pub_ipv6,
                                                    subnet_id_ipv6,
                                                    fixed_ip_v6_pub)

                for fixed_ip in os_port_res['fixed_ips']:
                    if fixed_ip['subnet_id'] == subnet_id_ipv6:
                        ip_ver = self.utils.get_ipaddress_version(
                                                    fixed_ip['ip_address'])
                        if ip_ver == self.utils.IP_VER_V6:
                            ip_address_v6 = fixed_ip['ip_address']
                            break

                db_port_update_params = {
                    'update_id': operation_id,
                    'IaaS_subnet_id_v6': subnet_id_ipv6,
                    'ip_address_v6': ip_address_v6,
                    'netmask_v6': pub_network_info['subnet_mask'],
                    'port_info': os_port_res,
                }

                # Update DB: NAL_PORT_MNG For Pub Port
                self._update_db_port(db_port_update_params, port_rec_id)

        job_output = {'port_id_pub_ipv6': port_id_pub_ipv6}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def pub_port_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_table_rec_id = job_input['apl_table_rec_id']
        node_id = job_input['node_id']
        apl_type = job_input['apl_type']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Network Info
        pub_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_PUB,
                                            '')

        # List NAL_PORT_MNG(DB)
        port_list = self.__list_db_port(apl_table_rec_id, node_id,
                                        pub_network_info['network_id'])

        if len(port_list) == 0:
            if job_cleaning_mode == '1':
                pass
            else:
                raise SystemError('port on Pub-lan not exists.')

        else:
            # Delete Port(OpenStack:VIM)
            self.__delete_os_port_vim(pod_id,
                                      nal_tenant_id,
                                      port_list[0]['port_id'],
                                      job_cleaning_mode)

            # Update NAL_PORT_MNG(DB): Set DeleteFlg On
            self.__delete_db_port_logical(operation_id, port_list[0]['ID'])

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def ext_port_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        job_output = {}

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        tenant_name = job_input['tenant_name']
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_type = job_input['apl_type']
        apl_table_rec_id = job_input['apl_table_rec_id']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Network Info
        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            '')

        # Assign Global IpAddress
        global_ip = self.__assign_global_ip(tenant_name, operation_id)

        # Create Port(OpenStack:VIM)
        if (str(apl_type) == str(self.job_config.APL_TYPE_VR)) \
            or (str(apl_type) == str(self.job_config.APL_TYPE_PH)):
            os_port_res = self.__create_os_port_vim(
                                                pod_id,
                                                nal_tenant_id,
                                                ext_network_info['network_id'],
                                                ext_network_info['subnet_id'],
                                                '',
                                                global_ip)
            # Get Port Info
            subnet_mask = ext_network_info['subnet_mask']
            port_info = os_port_res['port']
            port_id = port_info['id']
            ip_address = port_info['fixed_ips'][0]['ip_address']
        else:
            # Get Port Info
            subnet_mask = ext_network_info['subnet_mask']
            port_info = {}
            port_id = str(uuid.uuid4())
            ip_address = global_ip

        # Insert DB: NAL_PORT_MNG For MSA Port
        self.__insert_db_port(operation_id,
                                tenant_name,
                                pod_id,
                                nal_tenant_id,
                                apl_type,
                                ext_network_info['network_id'],
                                self.job_config.NW_TYPE_EX,
                                self.job_config.NW_TYPE_EXTRA,
                                port_id,
                                ip_address,
                                port_info,
                                subnet_mask,
                                apl_table_rec_id)

        # Set JOB Output Parameters
        job_output['global_ip'] = global_ip
        job_output['port_id3'] = port_id

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def virtual_ext_port_add_ipv6(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        fixed_ip_v6_ext = job_input.get('fixed_ip_v6_ext', '')

        if len(fixed_ip_v6_ext) > 0:
            fixed_ip_v6_ext = self.utils.get_ipaddress_compressed(
                                                            fixed_ip_v6_ext)

        # Get Network Info
        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            self.utils.IP_VER_V6)
        port_id_ext_ipv6 = ''

        if len(ext_network_info) > 0:

            subnet_id_ipv6 = ext_network_info['subnet_id']

            # List NAL_PORT_MNG(DB)
            port_list = self.__list_db_port('',
                                            node_id,
                                            ext_network_info['network_id'],
                                            nal_tenant_id,
                                            self.job_config.NW_TYPE_EX,
                                            self.job_config.NW_TYPE_EXTRA)

            if len(port_list[0]['ip_address_v6']) == 0:

                port_rec_id = port_list[0]['ID']
                port_id_ext_ipv6 = port_list[0]['port_id']

                # Update Port(OpenStack:VIM)
                os_port_res = self.__add_os_port_fixed_ip_vim(
                                                    pod_id, nal_tenant_id,
                                                    port_id_ext_ipv6,
                                                    subnet_id_ipv6,
                                                    fixed_ip_v6_ext)

                for fixed_ip in os_port_res['fixed_ips']:
                    if fixed_ip['subnet_id'] == subnet_id_ipv6:
                        ip_ver = self.utils.get_ipaddress_version(
                                                    fixed_ip['ip_address'])
                        if ip_ver == self.utils.IP_VER_V6:
                            ip_address_v6 = fixed_ip['ip_address']
                            break

                db_port_update_params = {
                    'update_id': operation_id,
                    'IaaS_subnet_id_v6': subnet_id_ipv6,
                    'ip_address_v6': ip_address_v6,
                    'netmask_v6': ext_network_info['subnet_mask'],
                    'port_info': os_port_res,
                }

                # Update DB: NAL_PORT_MNG For Ext Port
                self._update_db_port(db_port_update_params, port_rec_id)

        job_output = {'port_id_ext_ipv6': port_id_ext_ipv6}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def ext_port_delete(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        pod_id = job_input['pod_id']
        nal_tenant_id = job_input['nal_tenant_id']
        apl_table_rec_id = job_input['apl_table_rec_id']
        node_id = job_input['node_id']
        apl_type = job_input['apl_type']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Network Info
        ext_network_info = self.get_os_network_info(
                                            pod_id,
                                            nal_tenant_id,
                                            self.job_config.NW_NAME_EXT,
                                            '')

        # List NAL_PORT_MNG(DB)
        port_list = self.__list_db_port(apl_table_rec_id, node_id,
                                        ext_network_info['network_id'])

        if len(port_list) == 0:
            if job_cleaning_mode == '1':
                pass
            else:
                raise SystemError('port on Ext-lan not exists.')

        else:
            # Delete Port(OpenStack:VIM)
            self.__delete_os_port_vim(pod_id,
                                      nal_tenant_id,
                                      port_list[0]['port_id'],
                                      job_cleaning_mode)

            # Update NAL_PORT_MNG(DB): Set DeleteFlg On
            self.__delete_db_port_logical(operation_id, port_list[0]['ID'])

            # Withdraw Global Ip Address
            self.__withdraw_global_ip(operation_id, port_list[0]['ip_address'])

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __create_os_port_vim(self, pod_id, tenant_id, network_id, subnet_id,
                            port_name='', fixed_ips_ip_address=''):

        # Get Endpoint(OpenStack:VIM)
        os_endpoint = self.get_os_endpoint_vim(pod_id, '', tenant_id)

        # Create Port(OpenStack Client)
        osc_ports = ports.OscQuantumPorts(self.job_config)
        port_res = osc_ports.create_port(os_endpoint,
                                network_id,
                                port_name,
                                True,
                                subnet_id,
                                fixed_ips_ip_address
                                )

        return port_res

    def __add_os_port_fixed_ip_vim(self,
                        pod_id, tenant_id, port_id, subnet_id, ip_address):

        # Get Endpoint(OpenStack:VIM)
        os_endpoint = self.get_os_endpoint_vim(pod_id, '', tenant_id)

        # Create Port(OpenStack Client)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Get Port(OpenStack:VIM)
        os_port_res = os_ports_instance.get_port(os_endpoint, port_id)

        fixed_ip_append = {'subnet_id': subnet_id}
        if len(ip_address) > 0:
            fixed_ip_append['ip_address'] = ip_address

        fixed_ips_update = os_port_res['port']['fixed_ips']
        fixed_ips_update.append(fixed_ip_append)

        # Update Port(OpenStack:VIM)
        os_port_upd = os_ports_instance.update_port(os_endpoint,
                                                    port_id,
                                                    None,
                                                    None,
                                                    fixed_ips_update)

        return os_port_upd['port']

    def __delete_os_port_vim(self, pod_id, tenant_id, port_id,
                                                job_cleaning_mode=0):

        # Get Endpoint(OpenStack:VIM)
        os_endpoint = self.get_os_endpoint_vim(pod_id, '', tenant_id)

        osc_ports = ports.OscQuantumPorts(self.job_config)

        try:
            # Delete Port(OpenStack Client)
            osc_ports.delete_port(os_endpoint, port_id)

        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

    def __get_msa_network_info(self, tenant_name, pod_id):

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = self.get_db_endpoint(
                                    self.job_config.REST_URI_MSA_VLAN)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_MSA_VLAN_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['pod_id'] = pod_id
        params['tenant_name'] = tenant_name
        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        msa_network_info = db_list.get_return_param()

        return msa_network_info

    def __assign_msa_network(self, tenant_name, pod_id,
                             nal_tenant_id, operation_id, job_input):

        IaaS_tenant_id = job_input['IaaS_tenant_id']

        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Endpoint(DB Client)
        db_endpoint_msa_vlan = self.get_db_endpoint(
                                    self.job_config.REST_URI_MSA_VLAN)

        # Get Endpoint(OpenStack:VIM)
        os_endpoint_vim = self.get_os_endpoint_vim(pod_id, '', nal_tenant_id)

        # Create Instance(OpenStack Client)
        osc_networks = networks.OscQuantumNetworks(self.job_config)
        os_subnets_instance = subnets.OscQuantumSubnets(self.job_config)
        os_ports_instance = ports.OscQuantumPorts(self.job_config)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_MSA_VLAN_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['status'] = 0
        db_list.set_context(db_endpoint_msa_vlan, params)
        db_list.execute()
        msa_vlan_list = db_list.get_return_param()

        msa_network_info = {}
        if len(msa_vlan_list) != 0:

            rec = msa_vlan_list[0]

            # Update NAL_MSA_VLAN_MNG(DB Client)
            keys = [rec['ID']]
            params = {}
            params['update_id'] = operation_id
            params['pod_id'] = pod_id
            params['tenant_name'] = tenant_name
            params['status'] = 1
            params['tenant_id'] = nal_tenant_id
            db_update.set_context(db_endpoint_msa_vlan, keys, params)
            db_update.execute()

            cidr = rec['network_address'] + '/' + rec['netmask']

            if vim_iaas_with_flg == 0:
                # Create Network(OpenStack:VIM)
                network_name = 'MSA_for_' + nal_tenant_id
                physical_network_name = None
            else:
                # Create Network(OpenStack:VIM)
                network_name = 'MSA_for_' + IaaS_tenant_id
                physical_network_name = self.get_os_physical_network_name()

            os_cre_network_vim = osc_networks.create_network(
                                                    os_endpoint_vim,
                                                    network_name,
                                                    True,
                                                    False,
                                                    rec['vlan_id'],
                                                    physical_network_name)
            network_info = os_cre_network_vim['network']
            network_id = network_info['id']

            # Get Network Data(id)
            ret = self.utils.get_network_range_from_cidr(cidr)
            gatewy_ip = \
                socket.inet_ntoa(struct.pack('!L', ret['network'] + 1))

            os_cre_subnet_vim = os_subnets_instance.create_subnet(
                                                    os_endpoint_vim,
                                                    network_id,
                                                    cidr,
                                                    '',
                                                    nal_tenant_id,
                                                    '4',
                                                    gatewy_ip)
            subnet_info = os_cre_subnet_vim['subnet']
            subnet_id = subnet_info['id']

            # Create Port(OpenStack:VIM)
            os_cre_port_vim = os_ports_instance.create_port(os_endpoint_vim,
                                                            network_id)

            # Get Port Info
            port_info = os_cre_port_vim['port']
            port_id = port_info['id']
            ip_address = port_info['fixed_ips'][0]['ip_address']

            # MSA setup
            self.__setup_msa_network_vlan(pod_id,
                                                    rec['vlan_id'],
                                                    ip_address,
                                                    rec['netmask'])

            # Update NAL_MSA_VLAN_MNG(DB Client)
            keys = [rec['ID']]
            params = {}
            params['update_id'] = operation_id
            params['msa_ip_address'] = ip_address
            params['network_id'] = network_id
            params['subnet_id'] = subnet_id
            params['port_id'] = port_id
            params['network_info'] = json.dumps(network_info)
            params['subnet_info'] = json.dumps(subnet_info)
            params['port_info'] = json.dumps(port_info)
            db_update.set_context(db_endpoint_msa_vlan, keys, params)
            db_update.execute()

            # List NAL_MSA_VLAN_MNG(DB Client)
            params = {}
            params['delete_flg'] = 0
            params['pod_id'] = pod_id
            params['tenant_name'] = tenant_name
            db_list.set_context(db_endpoint_msa_vlan, params)
            db_list.execute()
            msa_network_info = db_list.get_return_param()

        else:
            raise SystemError('vlan for MSA not Found.')

        return msa_network_info

    def __assign_global_ip(self, tenant_name, operation_id):

        # Get Endpoint(DB Client)
        db_endpoint_global_ip = self.get_db_endpoint(
                                    self.job_config.REST_URI_GLOBAL_IP)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_GLOBAL_IP_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_global_ip, params)
        db_list.execute()
        global_ip_list = db_list.get_return_param()

        global_ip = ''
        for rec in global_ip_list:
            if str(rec['status']) == '0':
                key_id = rec['ID']
                global_ip = rec['global_ip']

        if len(global_ip) == 0:
            for rec in global_ip_list:
                if str(rec['status']) == '103' or \
                        str(rec['status']) == '203':
                    key_id = rec['ID']
                    global_ip = rec['global_ip']

        if len(global_ip) == 0:
            raise SystemError('global ip not found.')

        # Update NAL_GLOBAL_IP_MNG(DB Client)
        keys = [key_id]
        params = {}
        params['status'] = 101
        params['tenant_name'] = tenant_name
        params['update_id'] = operation_id
        db_update.set_context(db_endpoint_global_ip, keys, params)
        db_update.execute()

        return global_ip

    def __withdraw_global_ip(self, operation_id, global_ip):

        # Get Endpoint(DB Client)
        db_endpoint_global_ip = self.get_db_endpoint(
                                    self.job_config.REST_URI_GLOBAL_IP)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_GLOBAL_IP_MNG(DB Client)
        params = {}
        params['status'] = 101
        params['delete_flg'] = 0
        params['global_ip'] = global_ip
        db_list.set_context(db_endpoint_global_ip, params)
        db_list.execute()
        global_ip_list = db_list.get_return_param()

        if len(global_ip_list) == 0:
            raise SystemError('global_ip is already deleted.')

        # Update NAL_GLOBAL_IP_MNG(DB Client)
        keys = [global_ip_list[0]['ID']]
        params = {}
        params['status'] = 103
        params['tenant_name'] = ''
        params['node_id'] = ''
        params['update_id'] = operation_id
        db_update.set_context(db_endpoint_global_ip, keys, params)
        db_update.execute()

    def __insert_db_port(self, operation_id,
                               tenant_name,
                               pod_id,
                               tenant_id,
                               apl_type,
                               network_id,
                               network_type,
                               network_type_detail,
                               port_id,
                               ip_address,
                               port_info,
                               subnet_mask,
                               apl_table_rec_id):

        # Create Instance(DB Client)
        db_create_instance = create.CreateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        params = {}
        params['create_id'] = operation_id
        params['update_id'] = operation_id
        params['delete_flg'] = 0
        params['port_id'] = port_id
        params['tenant_name'] = tenant_name
        params['pod_id'] = pod_id
        params['tenant_id'] = tenant_id
        params['network_id'] = network_id
        params['network_type'] = network_type
        params['network_type_detail'] = network_type_detail
        params['apl_type'] = apl_type
        params['node_id'] = ''
        params['apl_table_rec_id'] = apl_table_rec_id
        params['IaaS_region_id'] = ' '
        params['IaaS_tenant_id'] = ' '
        params['IaaS_network_id'] = ' '
        params['IaaS_port_id'] = ' '
        params['nic'] = ''
        params['ip_address'] = ip_address
        params['netmask'] = subnet_mask
        params['port_info'] = json.dumps(port_info)
        params['msa_info'] = json.dumps({})

        db_create_instance.set_context(db_endpoint_port, params)
        db_create_instance.execute()

    def __list_db_port(self, apl_table_rec_id, node_id, network_id,
                       nal_tenant_id=None,
                       network_type=None,
                       network_type_detail=None):

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        params = {}
        params['network_id'] = network_id
        params['delete_flg'] = 0

        if node_id == '':
            params['apl_table_rec_id'] = apl_table_rec_id
        else:
            params['node_id'] = node_id

        if nal_tenant_id is not None:
            params['nal_tenant_id'] = nal_tenant_id

        if network_type is not None:
            params['network_type'] = network_type

        if network_type_detail is not None:
            params['network_type_detail'] = network_type_detail

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()

        return db_list.get_return_param()

    def __delete_db_port_logical(self, operation_id, port_key_id):

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        params = {}
        params['delete_flg'] = 1
        params['update_id'] = operation_id
        keys = [port_key_id]
        db_update.set_context(db_endpoint_port, keys, params)
        db_update.execute()

    def __setup_msa_network_vlan(self, pod_id, vlan_id, ip_address, netmask):

        # Create Instance(MSA Soap Client)
        msa = msaordercmdws.MsaOrderCommandWs(self.job_config,
                                              self.nal_endpoint_config,
                                              pod_id)

        # get config
        msa_config_for_common = self.get_msa_config_for_common(pod_id)

        msa_mask = self.utils.get_subnet_mask_from_cidr_len(netmask)

        # Create System Common(MSA)
        msa_res = msa.create_msa_network_vlan(
                          msa_config_for_common['msa_server_device_id'],
                          vlan_id,
                          ip_address,
                          msa_mask)

        return msa_res
