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
import time
import traceback

from job.auto import base
from job.lib.db import list
from job.lib.db import update
from job.lib.soap.msa import deviceconfigws
from job.lib.soap.msa import devicefieldsws
from job.lib.soap.msa import devicews
from job.lib.soap.msa import sshws


class SetupMsa(base.JobAutoBase):

    DEVICE_NAME_INTERSEC_SG = 'intersec_sg'
    DEVICE_NAME_INTERSEC_LB = 'intersec_lb'

    def msa_setup_create(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        apl_table_rec_id = job_input['apl_table_rec_id']
        pod_id = job_input['pod_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        node_id = job_input['node_id']

        # Get Endpoint(DB Client)
        db_endpoint_port = self.get_db_endpoint(self.job_config.REST_URI_PORT)

        params = {}
        params['node_id'] = node_id
        params['network_type_detail'] = '4'
        params['delete_flg'] = 0
        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)
        db_list.set_context(db_endpoint_port, params)
        db_list.execute()

        port_list = db_list.get_return_param()

        vnf_ip = ''
        for port in port_list:
            vnf_ip = port.get('ip_address')

        # Get Endpoint(DB Client)
        db_endpoint_apl = \
            self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['node_id'] = node_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        if str(apl_type) == str(self.job_config.APL_TYPE_PH):
            device_ip_address = apl_list[0]['master_ip_address']
            device_ip_address_sby = apl_list[0]['slave_ip_address']
            act_flg = 'act'
            sby_flg = 'sby'
        else:
            device_ip_address = job_input['device_ip_address']
            act_flg = ''
            sby_flg = ''

        # Get MSA Device Config
        device_name = self.device_type_to_name(apl_type, nf_type, device_type)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name)

        # Create Instance(MSA Soap Client)
        msa_devicews = devicews.DeviceWs(self.job_config,
                                         self.nal_endpoint_config,
                                         pod_id)
        msa_devicefieldsws = devicefieldsws.DeviceFieldsWs(self.job_config,
                                         self.nal_endpoint_config,
                                         pod_id)
        # Create Instance(MSA Rest Client)
        msa_sshws = sshws.SshWs(self.job_config,
                                self.nal_endpoint_config,
                                pod_id)
        msa_configws = \
            deviceconfigws.DeviceConfigurationWs(self.job_config,
                                                 self.nal_endpoint_config,
                                                 pod_id)

        host_name = None
        if device_name == self.DEVICE_NAME_INTERSEC_SG or \
            device_name == self.DEVICE_NAME_INTERSEC_LB:
            host_name = job_input['host_name']

        # Create Managed Device(MSA)
        msa_create_res = msa_devicews.create_managed_device(
                        job_input['msa_customer_id'],
                        msa_config_for_device['device_name'],
                        msa_config_for_device['user_id'],
                        msa_config_for_device['user_new_password'],
                        msa_config_for_device['admin_password'],
                        msa_config_for_device['manufacturer_id'],
                        msa_config_for_device['model_id'],
                        device_ip_address,
                        host_name
                        )

        # Get Result Data(MSA)
        node_detail = {
            'create_managed_device': msa_create_res[msa_devicews.RES_KEY_IN]}
        msa_device_id = self.get_msa_client_result(
                                msa_create_res[msa_devicews.RES_KEY_OUT], 'id')

        if str(apl_type) == str(self.job_config.APL_TYPE_PH) and \
                str(nf_type) == str(self.job_config.TYPE_LB):
            if str(device_type) in (str(self.job_config.DEV_TYPE_PHY_THUNDER),
                            str(self.job_config.DEV_TYPE_PHY_THUNDER_SHARE)):
                msa_devicews.update_device_management_port(msa_device_id,
                                                           '443')
            else:
                pass
        else:
            pass

        # Wait Provisioning(MSA)
        ssh_port = msa_config_for_device.get('ssh_port', '')
        self.check_msa_provisioning_status(msa_devicews, msa_device_id,
                                self.job_config.MSA_PROVISIONING_CHECK_COUNT,
                                self.job_config.MSA_PROVISIONING_RETRY_COUNT,
                                self.job_config.MSA_PROVISIONING_WAIT_TIME,
                                apl_type, nf_type, device_type,
                                msa_sshws, vnf_ip, ssh_port,
                                msa_devicefieldsws)

        # Attach Files To Device(MSA)
        msa_configws.attach_files_to_device(
            msa_device_id,
            msa_config_for_device['object_attach_file'])

        # Update NAL_VNF_MNG(DB)
        self.__update_db_apl(job_input, apl_table_rec_id,
                             msa_device_id, node_detail, act_flg)

        redundant_configuration_flg = apl_list[0][
                                    'redundant_configuration_flg']
        if isinstance(redundant_configuration_flg, int):
            redundant_configuration_flg = str(redundant_configuration_flg)

        if redundant_configuration_flg == '0':
            # Create Managed Device(MSA)
            msa_create_res = msa_devicews.create_managed_device(
                            job_input['msa_customer_id'],
                            msa_config_for_device['device_name'],
                            msa_config_for_device['user_id'],
                            msa_config_for_device['user_new_password'],
                            msa_config_for_device['admin_password'],
                            msa_config_for_device['manufacturer_id'],
                            msa_config_for_device['model_id'],
                            device_ip_address_sby,
                            host_name
                            )

            # Get Result Data(MSA)
            node_detail = {
             'create_managed_device': msa_create_res[msa_devicews.RES_KEY_IN]}
            msa_device_id = self.get_msa_client_result(
                msa_create_res[msa_devicews.RES_KEY_OUT], 'id')

            if str(apl_type) == str(self.job_config.APL_TYPE_PH) and \
                    str(nf_type) == str(self.job_config.TYPE_LB):
                if str(device_type) in (str(self.job_config.DEV_TYPE_PHY_THUNDER),
                            str(self.job_config.DEV_TYPE_PHY_THUNDER_SHARE)):
                    msa_devicews.update_device_management_port(msa_device_id,
                                                               '443')
                else:
                    pass
            else:
                pass

            # Wait Provisioning(MSA)
            self.check_msa_provisioning_status(msa_devicews, msa_device_id,
                                self.job_config.MSA_PROVISIONING_CHECK_COUNT,
                                self.job_config.MSA_PROVISIONING_RETRY_COUNT,
                                self.job_config.MSA_PROVISIONING_WAIT_TIME,
                                apl_type, nf_type, device_type, '', '', '',
                                msa_devicefieldsws)

            # Attach Files To Device(MSA)
            msa_configws.attach_files_to_device(
                msa_device_id,
                msa_config_for_device['object_attach_file'])

            # Update NAL_VNF_MNG(DB)
            self.__update_db_apl(job_input, apl_table_rec_id,
                                 msa_device_id, node_detail, sby_flg)

        # Wait
        time.sleep(self.job_config.OS_SERVER_WAIT_TIME)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def msa_delete_device_setting(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        apl_table_rec_id = job_input['apl_table_rec_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Create Instance(MSA Soap Client)
        msa_devicews = devicews.DeviceWs(self.job_config,
                                         self.nal_endpoint_config,
                                         pod_id)

        # Get Endpoint(DB Client)
        db_endpoint_apl = \
            self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_list = list.ListClient(self.job_config)

        # List NAL_APL_MNG(DB Client)
        params = {}
        params['ID'] = apl_table_rec_id
        params['delete_flg'] = 0
        db_list.set_context(db_endpoint_apl, params)
        db_list.execute()
        apl_list = db_list.get_return_param()

        if str(apl_list[0]['apl_type']) == str(self.job_config.APL_TYPE_PH):
            msa_device_id = apl_list[0]['master_MSA_device_id']
            msa_device_id_sby = apl_list[0]['slave_MSA_device_id']
        else:
            msa_device_id = apl_list[0]['MSA_device_id']

        try:
            # Delete Device(MSA)
            msa_devicews.delete_device_by_id(msa_device_id)

        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Update NAL_APL_MNG for PNF(Share)
        if str(apl_list[0]['apl_type']) == str(self.job_config.APL_TYPE_PH):

            # Update NAL_APL_MNG(DB)
            self.__update_db_apl(job_input, apl_table_rec_id,
                                 '', {}, 'act')

        if apl_list[0]['redundant_configuration_flg'] == 0:

            try:
                # Delete Device(MSA)
                msa_devicews.delete_device_by_id(msa_device_id_sby)

            except:
                if job_cleaning_mode == '1':
                    self.output_log_fatal(__name__, traceback.format_exc())
                else:
                    raise

            # Update NAL_APL_MNG for PNF(Share)
            if str(apl_list[0]['apl_type']) == \
                    str(self.job_config.APL_TYPE_PH):

                # Update NAL_APL_MNG(DB)
                self.__update_db_apl(job_input, apl_table_rec_id,
                                     '', {}, 'sby')

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __update_db_apl(self, job_input, apl_table_rec_id,
                        msa_device_id='', node_detail={}, act_or_sby=''):

        # Get JOB Input Parameters
        operation_id = job_input['operation_id']

        # Get Endpoint(DB Client)
        db_endpoint_apl = self.get_db_endpoint(self.job_config.REST_URI_APL)

        # Create Instance(DB Client)
        db_update = update.UpdateClient(self.job_config)

        # Update NAL_LICENSE_MNG(DB Client)
        keys = [apl_table_rec_id]
        params = {}
        params['update_id'] = operation_id
        if act_or_sby == 'act':
            params['master_MSA_device_id'] = msa_device_id
            params['device_detail_master'] = json.dumps(node_detail)
        elif act_or_sby == 'sby':
            params['slave_MSA_device_id'] = msa_device_id
            params['device_detail_slave'] = json.dumps(node_detail)
        else:
            params['MSA_device_id'] = msa_device_id
            params['node_detail'] = json.dumps(node_detail)

        db_update.set_context(db_endpoint_apl, keys, params)
        db_update.execute()
