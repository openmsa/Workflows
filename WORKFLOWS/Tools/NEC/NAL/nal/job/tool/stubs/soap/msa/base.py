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
import os

from job.tool.stubs import common
from xml.etree import ElementTree


class MsaStubBase:

    def __init__(self, api_config_instance):

        self.stub_common = common.StubCommon()
        self.config = api_config_instance

    def save_cilent_info(self, client_function_name, client_params):

        # Save Client Info(function, input)
        self.client_info = {
            'function': client_function_name,
            'input': client_params,
        }

    def parse_stub_xml(self, msa_class_name, msa_function_name):

        stub_reponse_dir = os.path.dirname(
                            os.path.abspath(__file__)) + '/response'
        api_name = msa_class_name + '_' + msa_function_name
        self.stub_xml_path = stub_reponse_dir + '/' + api_name + '.xml'

        if os.path.exists(self.stub_xml_path) == False:
            self.stub_xml_path = stub_reponse_dir + '/default_response.xml'

        # Parse XML(Stub)
        stub_xml = ElementTree.parse(self.stub_xml_path)

        return stub_xml

    def update_xml_value_increment(self, stub_xml, tag_name):

        root = stub_xml.getroot()
        tag = './/' + tag_name

        # Update XML Element Value(Increment)
        root.find(tag).text = str(int(root.find(tag).text) + 1)

        # Update XML(Stub)
        stub_xml.write(self.stub_xml_path, self.config.CHAR_SET, True)

        return stub_xml

    def set_params_for_assertion(self, msa_params, stub_xml):

        # Add MSA Client Input Params To Assertion File
        self.stub_common.add_msa_input_params_to_file(
                    self.client_info['function'], msa_params)

        # Convert XML(Stub) To Python Dictionary
        response_dict = self.__convert_xml_to_dict(stub_xml.getroot()[0], {})

        # Add MSA Client Output Params To Assertion File
        self.stub_common.add_msa_output_params_to_file(
                    self.client_info['function'], response_dict)

        soap_obj = self.__convert_dict_to_soap_obj(response_dict)

        return soap_obj['return']

    def __convert_xml_to_dict(self, response_xml, response_dict):

        tag = response_xml.tag
        response_dict_tmp = response_dict.get(tag, {})

        if len(response_xml) > 0:

            for idx in range(len(response_xml)):
                # Recursive Call
                response_dict_tmp = self.__convert_xml_to_dict(
                                        response_xml[idx], response_dict_tmp)

        else:
            response_dict_tmp = response_xml.text

        response_dict[tag] = response_dict_tmp

        return response_dict

    def __convert_dict_to_soap_obj(self, response_dict, soap_obj=None):

        return response_dict
