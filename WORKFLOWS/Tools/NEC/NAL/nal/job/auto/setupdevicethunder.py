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
import traceback

from job.auto import base
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import thunderordercmdws


class SetupDeviceThunder(base.JobAutoBase):

    APL_DEVICE_DETAIL_COL = {
        'act': 'device_detail_master',
        'sby': 'device_detail_slave',
    }

    def device_setup_create_thunder(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        redundant_configuration_flg = job_input['redundant_configuration_flg']
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        # Get MSA Config
        msa_config_for_device = self.__get_msa_config_for_device(job_input)

        # Get Info(DB)
        db_info = self.__get_db_info(job_input)

        # Create Setup Thunder
        res_setup = self.__create_setup_thunder(job_input, 'act',
                                                msa_config_for_device, db_info)

        # Update(DB)
        self.__update_db_setup_result(job_input, 'act', db_info, res_setup)

        if redundant_configuration_flg == '0':

            # Create Setup Thunder
            res_setup = self.__create_setup_thunder(job_input, 'sby',
                                                msa_config_for_device, db_info)

            # Update(DB)
            self.__update_db_setup_result(job_input, 'sby', db_info, res_setup)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def device_setup_add_ipv6_for_thunder(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get Info(DB)
        db_info = self.__get_db_info(job_input)

        # Get JOB Input Parameters
        redundant_configuration_flg = job_input['redundant_configuration_flg']
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Setup IPv6 thunder
        self.__setup_add_ipv6_thunder(job_input,
                                       'act',
                                        pod_id,
                                        db_info['apl']['msa_device_id']['act'],
                                        msa_config_for_device)

        if redundant_configuration_flg == '0':

            # Setup IPv6 Setting thunder
            self.__setup_add_ipv6_thunder(job_input,
                                        'sby',
                                        pod_id,
                                        db_info['apl']['msa_device_id']['sby'],
                                        msa_config_for_device)

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, {})

        return {}

    def device_setup_delete_thunder(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        redundant_configuration_flg = job_input['redundant_configuration_flg']
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        # Get MSA Config
        msa_config_for_device = self.__get_msa_config_for_device(job_input)

        # Get Info(DB)
        db_info = self.__get_db_info(job_input)

        # Delete Setup Thunder
        self.__delete_setup_thunder(job_input, 'act',
                                            msa_config_for_device, db_info)

        if redundant_configuration_flg == '0':

            # Delete Setup Thunder
            self.__delete_setup_thunder(job_input, 'sby',
                                            msa_config_for_device, db_info)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __get_db_apl(self, job_input):

        node_id = job_input['node_id']

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_VNF_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['node_id'] = node_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        return apl_list[0]

    def __get_msa_config_for_device(self, job_input):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']

        # Get MSA Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        return msa_config_for_device

    def __setup_add_ipv6_thunder(self,
                                      job_input,
                                      act_sby,
                                      pod_id,
                                      msa_device_id,
                                      msa_config_for_device):

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        port_id = job_input['port_id']
        fw_ip_v6_address = self.utils.get_ipaddress_compressed(
                                            job_input['fw_ip_v6_address'])
        operation_id = job_input['operation_id']
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_PORT_MNG(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()

        port_list = db_list.get_return_param()
        port_info = port_list[0]['port_info']
        port_dict = json.loads(port_info)
        vip_address_v6 = port_dict['IaaS_port_info']['vip']['ip_address_v6']
        ip_address_v6 = port_dict['IaaS_port_info'][act_sby]['ip_address_v6']
        netmask_v6 = port_dict['IaaS_port_info'][act_sby]['netmask_v6']

        msa_info = json.loads(port_list[0]['msa_info'])

        # List NAL_VIRTUAL_LAN_MNG(DB Client)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)

        params = {}
        params['pod_id'] = pod_id
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = port_list[0]['network_id']
        params['delete_flg'] = 0
        node_id = job_input['node_id']

        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        vlan_list = db_list.get_return_param()
        iaas_network_type = vlan_list[0]['IaaS_network_type']

        # Get VLAN_ID
        if vim_iaas_with_flg == 1 and \
                iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:
            # List NAL_PNF_VLAN_MNG(DB Client)
            db_endpoint_pnf_vlan = self.get_db_endpoint(
                                            self.job_config.REST_URI_PNF_VLAN)
            params = {}
            params['delete_flg'] = 0
            params['status'] = 1
            params['network_id'] = port_list[0]['network_id']
            db_list.set_context(db_endpoint_pnf_vlan, params)
            db_list.execute()
            pnf_vlan_list = db_list.get_return_param()
            vlan_id = pnf_vlan_list[0]['vlan_id']
        else:
            vlan_id = vlan_list[0]['vlan_id']

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['node_id'] = node_id
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        # Create Instance(MSA Soap Client)
        msa = thunderordercmdws.ThunderOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    pod_id)

        # Setting thunder_login(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_thunder_login',
            msa_device_id,
            job_input['tenant_name']
        )

        # Get Session Id
        session_id = json.loads(msa_res[msa.RES_KEY_OUT]['message'])\
                                    ['response']['message']['session_id']

        msa_info['create_thunder_login'] = msa_res[msa.RES_KEY_IN]

        # Setting thunder_move_partition(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_thunder_move_partition',
            msa_device_id,
            apl_list[0]['device_user_name'],
            session_id
        )
        msa_info['create_thunder_move_partition'] = msa_res[msa.RES_KEY_IN]

        # Setting IPV6 address(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_thunder_api_set_ipv6',
            msa_device_id,
            vlan_id,
            ip_address_v6,
            netmask_v6,
            session_id
        )
        msa_info['create_thunder_api_set_ipv6'] = msa_res[msa.RES_KEY_IN]

        # Setting IPv6VRRP(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_thunder_api_vrrpv6',
            msa_device_id,
            vip_address_v6,
            msa_config_for_device['admin_password'],
            session_id,
            'disable',
            '1',
            '1'
        )
        msa_info['create_thunder_api_vrrpv6'] = msa_res[msa.RES_KEY_IN]

        # Setting IPv6StaticRoute(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_thunder_api_static_routev6',
            msa_device_id,
            '::',
            fw_ip_v6_address,
            session_id,
            vlan_id,
            '0'
        )
        msa_info['create_thunder_api_static_routev6'] = msa_res[msa.RES_KEY_IN]

        # Setting MovePartition(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'delete_thunder_move_partition',
            msa_device_id,
            apl_list[0]['device_user_name'],
            session_id
        )
        msa_info['create_thunder_move_partition'] = msa_res[msa.RES_KEY_IN]

        # Setting Save(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'create_thunder_save',
            msa_device_id,
            session_id
        )
        msa_info['create_thunder_save'] = msa_res[msa.RES_KEY_IN]

        # SettingLoginOut(MSA Soap Client)
        msa_res = self.execute_msa_command(
            msa_config_for_device,
            msa,
            'delete_thunder_login',
            msa_device_id,
            job_input['tenant_name'],
            session_id
        )
        msa_info['delete_thunder_login'] = msa_res[msa.RES_KEY_IN]

        # Update NAL_PORT_MNG(DB)
        self.__update_db_port(job_input, act_sby, port_id, msa_info)

    def __get_db_info(self, job_input):

        # Get JOB Input Parameters
        node_id = job_input['node_id']
        nal_tenant_id = job_input['nal_tenant_id']
        port_id4 = job_input.get('port_id4', '')
        vim_iaas_with_flg = self.get_vim_iaas_with_flg(job_input)

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)
        db_endpoint_vlan = self.get_db_endpoint(self.job_config.REST_URI_VLAN)
        db_endpoint_pnf_vlan = self.get_db_endpoint(
                                            self.job_config.REST_URI_PNF_VLAN)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['node_id'] = node_id
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        # List NAL_PORT_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id

        if len(port_id4) > 0:
            params['port_id'] = port_id4
        else:
            params['node_id'] = node_id

        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        # List NAL_VIRTUAL_LAN_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['network_id'] = port_list[0]['network_id']
        db_list.set_context(db_endpoint_vlan, params)
        db_list.execute()
        vlan_list = db_list.get_return_param()
        iaas_network_type = vlan_list[0]['IaaS_network_type']

        # Get VLAN_ID
        if vim_iaas_with_flg == 1 and \
                iaas_network_type.upper() == self.job_config.NW_TYPE_VXLAN:
            # List NAL_PNF_VLAN_MNG(DB Client)
            params = {}
            params['delete_flg'] = 0
            params['status'] = 1
            params['network_id'] = port_list[0]['network_id']
            db_list.set_context(db_endpoint_pnf_vlan, params)
            db_list.execute()
            pnf_vlan_list = db_list.get_return_param()
            vlan_id = pnf_vlan_list[0]['vlan_id']
        else:
            vlan_id = vlan_list[0]['vlan_id']

        return {
                'apl': {
                    'rec_id': apl_list[0]['ID'],
                    'nic_tenant': apl_list[0]['nic_tenant'],
                    'partition_id_seq': apl_list[0]['partition_id_seq'],
                    'device_name_master': apl_list[0]['device_name_master'],
                    'device_user_name': apl_list[0]['device_user_name'],
                    'msa_device_id': {
                        'act': apl_list[0]['master_MSA_device_id'],
                        'sby': apl_list[0]['slave_MSA_device_id'],
                    },
                    'node_detail': {
                        'act': apl_list[0]['device_detail_master'],
                        'sby': apl_list[0]['device_detail_slave'],
                    }
                },
                'port': {
                    'rec_id': port_list[0]['ID'],
                    'msa_info': port_list[0]['msa_info'],
                    'port_info': port_list[0]['port_info'],
                },
                'vlan': {
                    'vlan_id': vlan_id
                },
        }

    def __update_db_port(self, job_input, act_sby, port_id, msa_info):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']
        nal_tenant_id = job_input['nal_tenant_id']

        # Get Endpoint(DB Client)
        db_endpoint = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_update = update.UpdateClient(self.job_config)

        # List NAL_VNF_MNG(DB Client)
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['port_id'] = port_id
        db_list.set_context(db_endpoint, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [port_list[0]['ID']]
        params = {}
        params['update_id'] = operation_id
        msa_info_set = json.loads(port_list[0]['msa_info'])
        msa_info_set.update({act_sby: msa_info})
        params['msa_info'] = json.dumps(msa_info_set)
        db_update.set_context(db_endpoint, keys, params)
        db_update.execute()

    def __update_db_setup_result(self,
                                 job_input, act_sby, db_info, setup_result):

        device_detail_col = self.APL_DEVICE_DETAIL_COL[act_sby]

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Update NAL_APL_MNG(DB Client)
        keys = [db_info['apl']['rec_id']]
        params = {}
        params['update_id'] = operation_id
        params['default_gateway'] = setup_result['default_gateway']
        params[device_detail_col] = setup_result['node_detail']
        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()

        # Update NAL_PORT_MNG(DB Client)
        keys = [db_info['port']['rec_id']]
        params = {}
        params['update_id'] = operation_id
        params['msa_info'] = setup_result['msa_info']
        db_update.set_context(db_endpoint_port, keys, params)
        db_update.execute()

    def __create_setup_thunder(self, job_input,
                               act_sby, msa_config_for_device, db_info):

        msa_device_id = db_info['apl']['msa_device_id'][act_sby]
        nic_tenant = db_info['apl']['nic_tenant']
        vlan_id = db_info['vlan']['vlan_id']

        partition_id = db_info['apl']['partition_id_seq']
        if isinstance(partition_id, int):
            partition_id = str(partition_id)

        iaas_port_info = json.loads(
                        db_info['port']['port_info'])['IaaS_port_info']
        default_gateway = iaas_port_info['vip']['ip_address']

        node_detail = {}
        if len(db_info['apl']['node_detail'][act_sby]) > 0:
            node_detail = json.loads(db_info['apl']['node_detail'][act_sby])

        msa_info = {}
        if len(db_info['port']['msa_info']) > 0:
            msa_info = json.loads(db_info['port']['msa_info'])

        # Create Instance(MSA Soap Client)
        msa = thunderordercmdws.ThunderOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    job_input['pod_id'])

        # Create Thunder Login(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_login',
                                    msa_device_id,
                                    job_input['tenant_name'])
        node_detail[
            'create_thunder_login'] = msa_res[msa.RES_KEY_IN]

        # Get Session Id
        session_id = json.loads(msa_res[msa.RES_KEY_OUT]['message'])\
                                    ['response']['message']['session_id']

        # Create Thunder Partition(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_partition',
                                    msa_device_id,
                                    job_input['partition_name'],
                                    session_id,
                                    partition_id)
        node_detail[
            'create_thunder_partition'] = msa_res[msa.RES_KEY_IN]

        # Create Thunder User(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_user',
                                    msa_device_id,
                                    job_input['user_account_id'],
                                    session_id,
                                    job_input['partition_name'],
                                    job_input['account_password'],
                                    'TenantAdmin')
        node_detail[
            'create_thunder_user'] = msa_res[msa.RES_KEY_IN]

        # Create Thunder Move Partition(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_move_partition',
                                    msa_device_id,
                                    job_input['partition_name'],
                                    session_id)
        node_detail[
            'create_thunder_move_partition'] = msa_res[msa.RES_KEY_IN]

        # Create Thunder VLAN(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_vlan',
                                    msa_device_id,
                                    vlan_id,
                                    session_id,
                                    nic_tenant)
        msa_info['create_thunder_vlan'] = msa_res[msa.RES_KEY_IN]

        # Create Thunder Management Access(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_manage',
                                    msa_device_id,
                                    vlan_id,
                                    msa_config_for_device['admin_password'],
                                    session_id)
        msa_info['create_thunder_manage'] = msa_res[msa.RES_KEY_IN]

        # Create Thunder Set Ip(MSA)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_set_ip',
                                    msa_device_id,
                                    iaas_port_info[act_sby]['ip_address'],
                                    session_id,
                                    self.utils.get_subnet_mask_from_cidr_len(
                                        iaas_port_info[act_sby]['netmask']),
                                    vlan_id)
        msa_info['create_thunder_set_ip'] = msa_res[msa.RES_KEY_IN]

        # Create Thunder VRRP(MSA Soap Client)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_vrrp',
                                    msa_device_id,
                                    default_gateway,
                                    session_id,
                                    msa_config_for_device['admin_password'],
                                    'disable',
                                    '1',
                                    '1')
        msa_info['create_thunder_vrrp'] = msa_res[msa.RES_KEY_IN]

        # Create IPv4StaticRoute(MSA Soap Client)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_static_route',
                                    msa_device_id,
                                    '0.0.0.0',
                                    job_input['fw_ip_address'],
                                    session_id,
                                    '0.0.0.0')

        msa_info['create_thunder_static_route'] = msa_res[msa.RES_KEY_IN]

        # Create Thunder Save(MSA Soap Client)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_save',
                                    msa_device_id,
                                    session_id)
        node_detail['create_thunder_save'] = msa_res[msa.RES_KEY_IN]

        # Delete Thunder Login(MSA Soap Client)
        msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_login',
                                    msa_device_id,
                                    job_input['tenant_name'],
                                    session_id)
        node_detail['delete_thunder_login'] = msa_res[msa.RES_KEY_IN]

        return {
            'default_gateway': default_gateway,
            'node_detail': json.dumps(node_detail),
            'msa_info': json.dumps(msa_info),
        }

    def __delete_setup_thunder(self, job_input,
                          act_sby, msa_config_for_device, db_info):

        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        msa_device_id = db_info['apl']['msa_device_id'][act_sby]
        device_user_name = db_info['apl']['device_user_name']
        vlan_id = db_info['vlan']['vlan_id']
        port_info = db_info['port']['port_info']
        port_info_dict = json.loads(port_info)

        iaas_port_info = json.loads(
                        db_info['port']['port_info'])['IaaS_port_info']

        admin_user_name = self.get_apl_msa_input_params(
                                    db_info['apl']['node_detail'][act_sby],
                                    'create_thunder_user',
                                    'A10ThunderApiUser',
                                    'object_id',
                                    job_cleaning_mode)

        partition_id = self.get_apl_msa_input_params(
                                    db_info['apl']['node_detail'][act_sby],
                                    'create_thunder_partition',
                                    'A10ThunderApiPartition',
                                    'partition_id',
                                    job_cleaning_mode)

        partition_name = self.get_apl_msa_input_params(
                                    db_info['apl']['node_detail'][act_sby],
                                    'create_thunder_partition',
                                    'A10ThunderApiPartition',
                                    'object_id',
                                    job_cleaning_mode)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_PORT_MNG(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        # Get JOB Input Parameters
        nal_tenant_id = job_input['nal_tenant_id']
        node_id = job_input['node_id']
        params = {}
        params['delete_flg'] = 0
        params['tenant_id'] = nal_tenant_id
        params['node_id'] = node_id
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()
        port_list = db_list.get_return_param()

        ip_address_v6 = port_list[0].get('ip_address_v6', '')
        if ip_address_v6 != '':
            # get value of gateway for api static routev6
            gateway_routev6 = ''
            msa_info = port_list[0]['msa_info']
            msa_info_dict = json.loads(msa_info)
            if act_sby in msa_info_dict:
                if 'create_thunder_api_static_routev6' in msa_info_dict[
                                                                    act_sby]:
                    api_static_routev6 = msa_info_dict[act_sby][
                                        'create_thunder_api_static_routev6']
                    objectParameters = api_static_routev6['objectParameters']
                    objectParameters_dict = json.loads(objectParameters)
                    ApiStaticRoutev6 = objectParameters_dict[
                                                'A10ThunderApiStaticRoutev6']
                    gateway_routev6 = ApiStaticRoutev6['::']['gateway']

        # get value of gateway for api static route
        msa_info = port_list[0]['msa_info']
        msa_info_dict = json.loads(msa_info)
        if 'create_thunder_static_route' not in msa_info_dict \
                and job_cleaning_mode == '1':
            gateway_route = ''
        else:
            static_route = msa_info_dict['create_thunder_static_route']
            objectParameters = static_route['objectParameters']
            objectParameters_dict = json.loads(objectParameters)
            ApiStaticRoute = objectParameters_dict['A10ThunderApiStaticRoute']
            gateway_route = ApiStaticRoute['0_0_0_0']['gateway']

        # Create Instance(MSA Soap Client)
        msa = thunderordercmdws.ThunderOrderCommandWs(
                                                    self.job_config,
                                                    self.nal_endpoint_config,
                                                    job_input['pod_id'])

        # Create Thunder Login(MSA)/Get Session Id
        session_id = ''
        try:
            msa_res = self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_login',
                                    msa_device_id,
                                    job_input['tenant_name'])

            session_id = json.loads(msa_res[msa.RES_KEY_OUT]['message'])\
                                    ['response']['message']['session_id']

        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Delete Thunder User(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_user',
                                    msa_device_id,
                                    admin_user_name,
                                    session_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Create Thunder Move Partition(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'create_thunder_move_partition',
                                    msa_device_id,
                                    device_user_name,
                                    session_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        if ip_address_v6 != '':
            # Delete thunder api static routev6(MSA)
            try:
                self.execute_msa_command(
                                        msa_config_for_device,
                                        msa,
                                        'delete_thunder_api_static_routev6',
                                        msa_device_id,
                                        '::',
                                        gateway_routev6,
                                        session_id,
                                        '0'
                                        )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        else:
            pass

        # Delete thunder static route(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_static_route',
                                    msa_device_id,
                                    '0.0.0.0',
                                    gateway_route,
                                    session_id,
                                    '0.0.0.0'
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        if ip_address_v6 != '':
            vip_address = port_info_dict['IaaS_port_info']['vip'][
                                                            'ip_address_v6']
            # Delete thunder api vrrpv6(MSA)
            try:
                self.execute_msa_command(
                                        msa_config_for_device,
                                        msa,
                                        'delete_thunder_api_vrrpv6',
                                        msa_device_id,
                                        vip_address,
                                        session_id
                                        )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        else:
            pass

        # Delete Thunder VRRP(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_vrrp',
                                    msa_device_id,
                                    iaas_port_info['vip']['ip_address'],
                                    session_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        if ip_address_v6 != '':
            # Delete thunder api set ipv6(MSA)
            try:
                self.execute_msa_command(
                                        msa_config_for_device,
                                        msa,
                                        'delete_thunder_api_set_ipv6',
                                        msa_device_id,
                                        vlan_id,
                                        session_id
                                        )
            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise
        else:
            pass

        # Delete Thunder Set Ip(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_set_ip',
                                    msa_device_id,
                                    iaas_port_info[act_sby]['ip_address'],
                                    session_id,
                                    vlan_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Delete Thunder VLAN(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_vlan',
                                    msa_device_id,
                                    vlan_id,
                                    session_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Delete Thunder Move Partition(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_move_partition',
                                    msa_device_id,
                                    partition_id,
                                    session_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Delete Thunder Partition(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_partition',
                                    msa_device_id,
                                    partition_name,
                                    session_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Delete Thunder Save(MSA)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_save',
                                    msa_device_id,
                                    session_id
                                    )
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Delete Thunder Login(MSA Soap Client)
        try:
            self.execute_msa_command(
                                    msa_config_for_device,
                                    msa,
                                    'delete_thunder_login',
                                    msa_device_id,
                                    job_input['tenant_name'],
                                    session_id)
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise
