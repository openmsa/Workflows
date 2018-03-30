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


import testtools

from nalclient import client
from nalclient.v1 import client as v1


class ClientTest(testtools.TestCase):

    def test_no_endpoint_error(self):
        self.assertRaises(ValueError, client.Client, None)

    def test_endpoint(self):
        gc = client.Client(1, "http://example.com")
        self.assertEqual("http://example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.Client)

    def test_versioned_endpoint(self):
        gc = client.Client(1, "http://example.com/v2")
        self.assertEqual("http://example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.Client)
