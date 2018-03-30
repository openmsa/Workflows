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

from job.lib.openstack.glance import base


class OscGlanceImages(base.OscGlanceBase):

    def list_images(self, endpoint_array):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/v2.0/images'

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'images' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp
