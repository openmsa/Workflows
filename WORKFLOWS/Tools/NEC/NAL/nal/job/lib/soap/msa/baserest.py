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
import re

from job.lib.common import utils
from job.lib.soap.msa.lib import rest


class MsaClientRestBase:

    def __init__(self,
                 api_config_instance,
                 nal_endpoint_config,
                 pod_id,
                 dc_id='system'):

        self.config = api_config_instance
        self.utils = utils.Utils()
        self.rest = rest.MsaRest(api_config_instance)

        user_name = \
            nal_endpoint_config[dc_id]['msa'][pod_id]['user_id']
        user_pass = \
            nal_endpoint_config[dc_id]['msa'][pod_id]['user_password']
        endpoint_url = \
            nal_endpoint_config[dc_id]['msa'][pod_id]['rest_endpoint']

        # Set Auth Info
        self.auth_info = {'id': user_name, 'pass': user_pass}

        # Set ENDPOINT
        self.endpoint = endpoint_url
