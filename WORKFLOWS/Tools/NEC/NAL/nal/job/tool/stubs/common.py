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
import hashlib
import json
import os


class StubCommon:

    # Flag(execute __add_params_to_assertion_file)
    EXEC_ASSERT = False

    # Assertion File Path
    OS_RESPONSE_PARAMS_ASSERT_FILEPATH = '/assert/os_response_params.tmp'
    SCRIPT_OUTPARAMS_ASSERT_FILEPATH = '/assert/script_output_params.tmp'
#     SOAP_CLIENT_INPUT_ASSERT_FILEPATH = '/assert/soap_client_input_values.tmp'
    MSA_INPUT_PARAMS_ASSERT_FILEPATH = '/assert/msa_input_params.tmp'
    MSA_OUTPUT_PARAMS_ASSERT_FILEPATH = '/assert/msa_output_params.tmp'

    def gen_rand_str_hex(self, length):

        buf = ''
        while len(buf) < length:
            buf += hashlib.md5(os.urandom(100)).hexdigest()
        return buf[0:length]

    def get_script_name(self, argv0):

        script_file_name = argv0.split('/')
        script_file_name = script_file_name[-1].split('.')

        return script_file_name[0]

    def add_script_output_params_to_file(self, api_name, params):

        file_path = os.path.dirname(os.path.abspath(__file__)
                                ) + self.SCRIPT_OUTPARAMS_ASSERT_FILEPATH

        self.__add_params_to_assertion_file(file_path, api_name, params)

    def add_msa_input_params_to_file(self, function_name, params):

        file_path = os.path.dirname(os.path.abspath(__file__)
                                ) + self.MSA_INPUT_PARAMS_ASSERT_FILEPATH

        self.__add_params_to_assertion_file(file_path, function_name, params)

    def add_msa_output_params_to_file(self, function_name, params):

        file_path = os.path.dirname(os.path.abspath(__file__)
                                ) + self.MSA_OUTPUT_PARAMS_ASSERT_FILEPATH

        self.__add_params_to_assertion_file(file_path, function_name, params)

#     def add_soap_client_input_params_to_file(self, function_name, params):
#
#         file_path = os.path.dirname(os.path.abspath(__file__)
#                                 ) + self.SOAP_CLIENT_INPUT_ASSERT_FILEPATH
#
#         self.__add_params_to_assertion_file(file_path, function_name, params)

    def __add_params_to_assertion_file(self, file_path, api_name, params):

        if self.EXEC_ASSERT:

            assert_params = {}
            api_params = []

            if os.path.exists(file_path):

                f = open(file_path, 'r')
                assert_json = f.read()
                f.close()

                assert_json.rstrip()
                if len(assert_json) == 0:
                    assert_params = {}
                else:
                    assert_params = json.loads(assert_json)

                if api_name in assert_params:
                    api_params = assert_params[api_name]

            api_params.append(params)
            assert_params[api_name] = api_params

            f = open(file_path, 'w')
            f.write(json.dumps(assert_params))
            f.close()
