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

from job.tool.stubs.soap.msa import base


class UserWS(base.MsaStubBase):

    def createCustomer(self, **params):

        # Parse XML(Stub)
        stub_xml = self.parse_stub_xml(__class__.__name__,
                                    inspect.currentframe().f_code.co_name)

        # Update XML(Stub): id(Increment)
        stub_xml = self.update_xml_value_increment(stub_xml, 'id')

        # Set Parameters To Assertion File
        result = self.set_params_for_assertion(params, stub_xml)

        return result

    def deleteCustomerById(self, **params):

        # Parse XML(Stub)
        stub_xml = self.parse_stub_xml(__class__.__name__,
                                    inspect.currentframe().f_code.co_name)

        # Set Parameters To Assertion File
        result = self.set_params_for_assertion(params, stub_xml)

        return result
