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

from job.lib.soap.msa import base


class DeviceFieldsWs(base.MsaClientBase):

    def __init__(self,
        api_config_instance, nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'hostname_setting_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def set_hostname(self, device_id, host_name):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = {'deviceId': device_id,
                      'hostname': host_name}

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.setHostname(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}
