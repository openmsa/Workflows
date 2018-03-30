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

from job.tool.stubs.soap.msa import base


class OrderCommandWS(base.MsaStubBase):

    def executeCommand(self, **params):

        object_params = json.loads(params['objectParameters'])
        object_params_key = object_params.keys()

        for key in object_params_key:
            object_file_name = key

        function_name = inspect.currentframe().f_code.co_name + \
                        object_file_name + params['commandName']

        # Parse XML(Stub)
        stub_xml = self.parse_stub_xml(__class__.__name__, function_name)

        # Set Parameters To Assertion File
        result = self.set_params_for_assertion(params, stub_xml)

        return result
