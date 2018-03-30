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
import importlib
import json
import ssl

from job.lib import logger
from job.lib.common import utils


class MsaClientBase:

    RES_KEY_IN = 'in'
    RES_KEY_OUT = 'out'

    STUB_MSA_PACKAGE_PATH = 'job.tool.stubs.soap.msa.'
    SOAP_PACKAGE_PATH = 'suds.client'
    SOAP_CLASS_NAME = 'Client'

    def __init__(self,
                 api_config_instance,
                 endpoint_name,
                 nal_endpoint_config,
                 pod_id,
                 dc_id='system'):

        self.config = api_config_instance
        self.logger = logger.LibLogger(api_config_instance)
        self.utils = utils.Utils()

        user_name = \
            nal_endpoint_config[dc_id]['msa'][pod_id]['user_id']
        user_pass = \
            nal_endpoint_config[dc_id]['msa'][pod_id]['user_password']
        endpoint_url = \
            nal_endpoint_config[dc_id]['msa'][pod_id]['endpoint']
        msa_class_name = \
            nal_endpoint_config[dc_id]['msa'][pod_id][endpoint_name]

        # Set ENDPOINT
        endpoint = endpoint_url.replace(
                            '%MSA_CLASS_NAME%', msa_class_name)

        # Set WSDL
        wsdl = endpoint + 'WSDL=' + msa_class_name

        # Output Log(SoapClient Input Parameters)
        log_params = {
            'wsdl': wsdl,
            'username': user_name,
            'password': self.config.LOG_PASSWORD_MASK
        }
        self.output_log_soap_params('in', __name__, '__init__', log_params)

        if self.config.ENV == self.config.ENV_DEV:

            # Create Instance(Stub(MSA))
            module = importlib.import_module(
                        self.STUB_MSA_PACKAGE_PATH + msa_class_name)
            class_attr = getattr(module, msa_class_name)
            self.soap_client = class_attr(api_config_instance)

        else:

            # Create Instance(SoapClient(MSA))
            ssl._create_default_https_context = ssl._create_unverified_context
            module = importlib.import_module(self.SOAP_PACKAGE_PATH)
            class_attr = getattr(module, self.SOAP_CLASS_NAME)
            self.soap_client = class_attr(wsdl,
                                username=user_name,
                                password=user_pass).service

    def save_cilent_info(self, client_function_name, msa_params):

        if self.config.ENV == self.config.ENV_DEV:
            self.soap_client.save_cilent_info(
                                    client_function_name, msa_params)

    def set_msa_cmd_input_params(self, command_name, device_id, object_id,
                    object_file_name_list, client_function_name,
                    object_params_option={}):

        if client_function_name not in object_file_name_list:
            raise SystemError('ClientFunctionName '
                        + client_function_name
                        + ' is no match with MSA ObjectFileName')

        object_params = {'object_id': object_id}
        object_params.update(object_params_option)

        object_file_name = object_file_name_list[client_function_name]
        if type(object_id) is not int:
            object_key = object_id.replace('.', '_')
        else:
            object_key = object_id
        object_parameters = {object_file_name: {object_key: object_params}}

        msa_params = {
                'deviceId': device_id,
                'commandName': command_name,
                'objectParameters': json.dumps(object_parameters),
        }

        return msa_params

    def output_log_soap_params(self,
                log_type, module, function, params, passwords=[]):

        passwords = self.utils.json_encode_passwords(passwords)

        if isinstance(params, str) == False:
            params = str(params)

        if log_type == 'in':
            log_msg_type = '[INPUT]'
        else:
            log_msg_type = '[OUTPUT]'

        # Output Log(SoapClient Input Parameters)
        log_msg = '[SoapClient]' + function
        log_msg += log_msg_type + params
        self.logger.log_info(module, log_msg, passwords)
