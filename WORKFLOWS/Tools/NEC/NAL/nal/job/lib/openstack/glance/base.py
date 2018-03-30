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
from job.lib.openstack import base


class OscGlanceBase(base.OpenstackClientBase):

    def get_endpoint(self, endpoint_array):

        wim_fig = endpoint_array.get('wim_fig', False)

        if wim_fig == True:
            catalog_names = ['glance_dcmng']
        else:
            catalog_names = ['glance']

        admin_roles = ['admin', 'KeystoneAdmin']

        url = super().get_endpoint(endpoint_array,
                            admin_roles, catalog_names)
        if len(url) == 0:
            raise SystemError(self.EXCEPT_MSG08)

        return url
