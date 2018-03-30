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


from nalclient.common import http
from nalclient.common import utils
from nalclient.v1.node import NodeManager
from nalclient.v1.resource import ResourceManager
from nalclient.v1.service import ServiceManager


class Client(object):
    """Client for the Nal API.

    :param string endpoint: A user-supplied endpoint URL for the aflo
                            service.
    :param string token: Token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, endpoint, *args, **kwargs):
        """Initialize a new client for the Nal API."""
        endpoint, version = utils.strip_version(endpoint)
        self.version = version or 1.0
        self.http_client = http.HTTPClient(endpoint, *args, **kwargs)
        self.node = NodeManager(self.http_client)
        self.resource = ResourceManager(self.http_client)
        self.service = ServiceManager(self.http_client)
