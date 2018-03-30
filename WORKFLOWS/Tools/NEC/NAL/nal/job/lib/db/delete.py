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
from job.lib.db import base


class DeleteClient(base.DbClientBase):

    METHOD = 'DELETE'

    def set_context(self, end_point, keys):

        for key in keys:
            end_point += '/' + str(key)

        base.DbClientBase.end_point = end_point.rstrip('/')
        base.DbClientBase.method = self.METHOD
        base.DbClientBase.params = {}
