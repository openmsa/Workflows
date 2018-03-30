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
from urllib import parse

from job.lib.db import base


class ListClient(base.DbClientBase):

    METHOD = 'GET'

    def set_context(self, end_point, params):

        if len(params) > 0:
            end_point += '?' + parse.urlencode(params)

        base.DbClientBase.end_point = end_point.rstrip('/')
        base.DbClientBase.method = self.METHOD
        base.DbClientBase.params = {}

    def get_return_param(self):
        return self.return_param
