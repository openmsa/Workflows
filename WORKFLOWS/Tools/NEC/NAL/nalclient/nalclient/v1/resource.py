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


"""Interface of called ServiceComponent."""
from nalclient.common import base
from nalclient.common import utils


class ResourceManager(base.BaseManager):
    """Manager class for manipulating Nal."""

    def create(self, fields):
        """Create a Resource.
        :param fields: Resource data.
        """
        url = '/Nal/resource/'

        body = self.client.post(url, data=fields)

        return body['result']

    def update(self, fields):
        """Update a Resource.
        :param fields: Resource data.
        """
        url = '/Nal/resource/'

        body = self.client.put(url, data=fields)

        return body['result']

    def delete(self, fields):
        """Delete a Resource.
        :param fields: Resource data.
        """
        url = '/Nal/resource/'

        body = self.client.delete(url, data=fields)

        return body['result']

    def get(self, kwargs):
        """Get a Resource.
        :param fields: Resource data.
        """
        url = '/Nal/resource/'
        if kwargs:
            url = url + "?" + utils.urlencode(kwargs)

        body = self.client.get(url)

        return body['data']
