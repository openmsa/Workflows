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


import json

import mox
import requests
import testtools

from nalclient.common import http
from nalclient import exc
from nalclient.tests.unit import utils


class TestClient(testtools.TestCase):

    def setUp(self):
        super(TestClient, self).setUp()
        self.mock = mox.Mox()
        self.mock.StubOutWithMock(requests.Session, 'request')

        self.endpoint = 'http://example.com:9292'
        self.client = http.HTTPClient(self.endpoint, timeout=200,
                                      id_pass='id_pass')

    def tearDown(self):
        super(TestClient, self).tearDown()
        self.mock.UnsetStubs()

    def test_http_get_method(self):
        data = {"test": "json_request"}
        return_data = {
            "data": [{'ID': '11',
                      'node_id': 'node_11'}],
            "request-id": "20160927110557057580971",
            "result": {
                "error-code": "NAL100000",
                "message": "",
                "status": "success"
            }
        }
        fake = utils.FakeResponse({}, json.dumps(return_data))

        requests.Session.request(
            mox.IgnoreArg(),
            mox.IgnoreArg(),
            stream=mox.IgnoreArg(),
            data=json.dumps(data),
            headers=mox.IgnoreArg()).AndReturn(fake)
        self.mock.ReplayAll()
        body = self.client.get('/v1/node/', data=data)
        self.assertEqual(return_data, body)

    def test_http_post_method(self):
        data = {"test": "json_request"}
        return_data = {
            "request-id": "20160927110557057580971",
            "result": {
                "error-code": "NAL100000",
                "message": "",
                "status": "success"
            }
        }
        fake = utils.FakeResponse({}, json.dumps(return_data))

        requests.Session.request(
            mox.IgnoreArg(),
            mox.IgnoreArg(),
            stream=mox.IgnoreArg(),
            data=json.dumps(data),
            headers=mox.IgnoreArg()).AndReturn(fake)
        self.mock.ReplayAll()
        body = self.client.post('/v1/node/', data=data)
        self.assertEqual(return_data, body)

    def test_http_put_method(self):
        data = {"test": "json_request"}
        return_data = {
            "request-id": "20160927110557057580971",
            "result": {
                "error-code": "NAL100000",
                "message": "",
                "status": "success"
            }
        }
        fake = utils.FakeResponse({}, json.dumps(return_data))

        requests.Session.request(
            mox.IgnoreArg(),
            mox.IgnoreArg(),
            stream=mox.IgnoreArg(),
            data=json.dumps(data),
            headers=mox.IgnoreArg()).AndReturn(fake)
        self.mock.ReplayAll()
        body = self.client.put('v1/node/', data=data)
        self.assertEqual(return_data, body)

    def test_http_delete_method(self):
        data = {"test": "json_request"}
        return_data = {
            "request-id": "20160927110557057580971",
            "result": {
                "error-code": "NAL100000",
                "message": "",
                "status": "success"
            }
        }
        fake = utils.FakeResponse({}, json.dumps(return_data))

        requests.Session.request(
            mox.IgnoreArg(),
            mox.IgnoreArg(),
            stream=mox.IgnoreArg(),
            data=json.dumps(data),
            headers=mox.IgnoreArg()).AndReturn(fake)
        self.mock.ReplayAll()
        body = self.client.delete('v1/node/', data=data)
        self.assertEqual(return_data, body)

    def test_http_timeout_error(self):
        data = {"test": "json_request"}

        requests.Session.request(
            mox.IgnoreArg(),
            mox.IgnoreArg(),
            stream=mox.IgnoreArg(),
            data=json.dumps(data),
            headers=mox.IgnoreArg()).AndRaise(requests.exceptions.Timeout)

        self.mock.ReplayAll()
        self.assertRaises(exc.InvalidEndpoint,
                          self.client.post,
                          '/v1/node/',
                          data=data)

    def test_http_connection_error(self):
        data = {"test": "json_request"}

        requests.Session.request(
            mox.IgnoreArg(),
            mox.IgnoreArg(),
            stream=mox.IgnoreArg(),
            data=json.dumps(data),
            headers=mox.IgnoreArg()
        ).AndRaise(requests.exceptions.ConnectionError)

        self.mock.ReplayAll()
        self.assertRaises(exc.CommunicationError,
                          self.client.post,
                          '/v1/node/',
                          data=data)

    def test_http_other_error(self):
        data = {"test": "json_request"}

        requests.Session.request(
            mox.IgnoreArg(),
            mox.IgnoreArg(),
            stream=mox.IgnoreArg(),
            data=json.dumps(data),
            headers=mox.IgnoreArg()).AndRaise(OSError)

        self.mock.ReplayAll()
        self.assertRaises(exc.BaseException,
                          self.client.post,
                          '/v1/node/',
                          data=data)

    def test_http_nal_api_error(self):
        data = {"test": "json_request"}
        return_data = {
            "request-id": "20160927110557057580971",
            "result": {
                "error-code": "NAL110001",
                "message": "",
                "status": "success"
            }
        }
        fake = utils.FakeResponse({}, json.dumps(return_data))

        requests.Session.request(
            mox.IgnoreArg(),
            mox.IgnoreArg(),
            stream=mox.IgnoreArg(),
            data=json.dumps(data),
            headers=mox.IgnoreArg()).AndReturn(fake)

        self.mock.ReplayAll()
        self.assertRaises(exc.NalBadRequest,
                          self.client.post,
                          '/v1/node/',
                          data=data)

    def test_http_json_format_error(self):
        data = "no_json_data"

        self.mock.ReplayAll()
        self.assertRaises(exc.BaseException,
                          self.client.post,
                          '/v1/node/',
                          data=data)
