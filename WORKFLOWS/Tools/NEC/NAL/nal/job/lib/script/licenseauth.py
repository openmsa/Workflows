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

from job.lib.script import base


class LicenseAuthClient(base.ScriptClientBase):

    def __init__(self, api_config_instance):

        super().__init__(api_config_instance)
        base.ScriptClientBase.shebang = self.config.SCRIPT_SHEBANG_PYTHON

    def a10_vthunder_authentication(self, params, passwords=[]):

        output = super().execute(
                inspect.currentframe().f_code.co_name, params, passwords)
        return output

    def paloalto_authentication(self, params, passwords=[]):

        output = super().execute(
                inspect.currentframe().f_code.co_name, params, passwords)
        return output
