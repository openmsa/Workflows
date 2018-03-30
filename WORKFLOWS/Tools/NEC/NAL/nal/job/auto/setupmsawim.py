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
import traceback

from job.auto import base
from job.lib.soap.msa import deviceconfigws
from job.lib.soap.msa import devicews
from job.lib.soap.msa import sshws


class SetupMsaWim(base.JobAutoBase):

    def msa_setup_vm_wim(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # msa setup
        ret1 = self.__msa_setup_vm_wim(job_input,
                                   self.job_config.VM_ROUTER_NODE_NAME1)
        ret2 = self.__msa_setup_vm_wim(job_input,
                                   self.job_config.VM_ROUTER_NODE_NAME2)

        # Set JOB Output Parameters
        job_output = {}
        job_output['apl_wk'] = {}
        job_output['apl_wk'][self.job_config.VM_ROUTER_NODE_NAME1] = \
                                                        ret1['apl_wk']
        job_output['apl_wk'][self.job_config.VM_ROUTER_NODE_NAME2] = \
                                                        ret2['apl_wk']

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def msa_delete_device_setting_vm_wim(self, job_input):

        function_name = inspect.currentframe().f_code.co_name

        # Output Log(Job Input)
        self.output_log_job_params(self.LOG_TYPE_INPUT,
                                         __name__, function_name, job_input)

        # msa setup
        self.__msa_delete_device_setting_vm_wim(job_input,
                                   self.job_config.VM_ROUTER_NODE_NAME1)
        self.__msa_delete_device_setting_vm_wim(job_input,
                                   self.job_config.VM_ROUTER_NODE_NAME2)

        # Set JOB Output Parameters
        job_output = {}

        # Output Log(Job Output)
        self.output_log_job_params(self.LOG_TYPE_OUTPUT,
                                         __name__, function_name, job_output)

        return job_output

    def __msa_setup_vm_wim(self, job_input, router_name):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        apl_type = job_input['apl_type']
        nf_type = job_input['type']
        device_type = job_input['device_type']
        msa_customer_id = job_input['msa_customer_id']
        msa_ip_address = job_input['msa_wan_port_info'][
                                        router_name]['msa_ip_address']
        apl_wk = job_input['apl_wk'][router_name]

        # Get MSA Device Config
        device_name = self.device_type_to_name(apl_type,
                                               nf_type,
                                               device_type,
                                               dc_id)
        msa_config_for_device = \
            self.get_msa_config_for_device(pod_id, device_name, dc_id)

        # Create Instance(MSA Soap Client)
        msa_devicews = devicews.DeviceWs(self.job_config,
                                         self.nal_endpoint_config,
                                         pod_id,
                                         dc_id)
        msa_configws = \
            deviceconfigws.DeviceConfigurationWs(self.job_config,
                                                 self.nal_endpoint_config,
                                                 pod_id,
                                                 dc_id)

        # Create Instance(MSA Rest Client)
        msa_sshws = sshws.SshWs(self.job_config,
                                self.nal_endpoint_config,
                                pod_id,
                                dc_id)

        # Create Managed Device(MSA)
        msa_create_res = msa_devicews.create_managed_device(
                        msa_customer_id,
                        msa_config_for_device['device_name'],
                        msa_config_for_device['user_id'],
                        msa_config_for_device['user_new_password'],
                        msa_config_for_device['admin_password'],
                        msa_config_for_device['manufacturer_id'],
                        msa_config_for_device['model_id'],
                        msa_ip_address
                        )

        # Get Result Data(MSA)
        apl_wk['node_detail'] = {
            'create_managed_device': msa_create_res[msa_devicews.RES_KEY_IN]}
        msa_device_id = self.get_msa_client_result(
                                msa_create_res[msa_devicews.RES_KEY_OUT], 'id')
        apl_wk['MSA_device_id'] = msa_device_id

        # Wait Provisioning(MSA)
        ssh_port = msa_config_for_device.get('ssh_port', '')
        self.check_msa_provisioning_status(msa_devicews, msa_device_id,
                                self.job_config.MSA_PROVISIONING_CHECK_COUNT,
                                self.job_config.MSA_PROVISIONING_RETRY_COUNT,
                                self.job_config.MSA_PROVISIONING_WAIT_TIME,
                                apl_type, nf_type, device_type,
                                msa_sshws, msa_ip_address, ssh_port)

        # Attach Files To Device(MSA)
        msa_configws.attach_files_to_device(
            msa_device_id,
            msa_config_for_device['object_attach_file'])

        # Set JOB Output Parameters
        job_output = {
            'apl_wk': apl_wk,
        }

        return job_output

    def __msa_delete_device_setting_vm_wim(self, job_input, router_name):

        # Get JOB Input Parameters
        pod_id = job_input['pod_id']
        dc_id = job_input['dc_id']
        msa_device_id = job_input['apl_info'][router_name]['MSA_device_id']
        job_cleaning_mode = job_input.get('job_cleaning_mode', '0')

        # Create Instance(MSA Soap Client)
        msa_devicews = devicews.DeviceWs(self.job_config,
                                    self.nal_endpoint_config, pod_id, dc_id)

        try:
            # Delete Device(MSA)
            msa_devicews.delete_device_by_id(msa_device_id)
        except:
            if job_cleaning_mode == '1':
                self.output_log_fatal(__name__, traceback.format_exc())
            else:
                raise

        # Set JOB Output Parameters
        job_output = {}

        return job_output
