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
from job.lib.soap.msa import baserest


class SshWs(baserest.MsaClientRestBase):

    def __init__(self,
        api_config_instance, nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance,
                         nal_endpoint_config, pod_id, dc_id)

    def confirm_ssh_status(self, ip_address, port):

        # Set InputParameters(Rest)
        query_params = {
            'params': ip_address + '\r\n' + port,
        }

        # Set Endpoint URL
        url = self.endpoint + '/ubi-api-rest/sms/cmd/SSHSTATUS/0'

        # Execute Rest
        resp = self.rest.rest_post(url, self.auth_info, query_params)

        return resp
