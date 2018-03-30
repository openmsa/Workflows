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


import base64
import logging
import requests
import six
from six.moves.urllib import parse

from nalclient.common import utils
from nalclient import exc

try:
    from requests.packages.urllib3.exceptions import ProtocolError
except ImportError:
    ProtocolError = requests.exceptions.ConnectionError

try:
    import json
except ImportError:
    import simplejson as json

# Python 2.5 compat fix
if not hasattr(parse, 'parse_qsl'):
    import cgi
    parse.parse_qsl = cgi.parse_qsl

LOG = logging.getLogger(__name__)
USER_AGENT = 'nalclient'
CHUNKSIZE = 1024 * 64  # 64kB


class HTTPClient(object):

    def __init__(self, endpoint, **kwargs):
        self.endpoint = endpoint

        self._timeOut = float(kwargs.get('timeout', 600))
        self._idPass = kwargs.get('id_pass', '')
        self.session = requests.Session()

    @staticmethod
    def encode_headers(headers):
        """Encodes headers.

        Note: This should be used right before
        sending anything out.

        :param headers: Headers to encode
        :returns: Dictionary with encoded headers'
                  names and values
        """
        return dict((utils.safe_encode(h), utils.safe_encode(v))
                    for h, v in six.iteritems(headers) if v is not None)

    def _request(self, method, url, **kwargs):
        """Send an http request with the specified characteristics.
        Wrapper around httplib.HTTP(S)Connection.request to handle tasks such
        as setting headers and error handling.
        """
        # Copy the kwargs so we can reuse the original in case of redirects

        nalauth = base64.b64encode(self._idPass)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic ' + nalauth,
                   'Custom-Header': 'value'}

        data = kwargs.pop("data", None)
        if data is not None and not isinstance(data, six.string_types):
            try:
                data = json.dumps(data)
            except TypeError:
                raise exc.BaseException('Json format is incorrect')

        # Note(flaper87): Before letting headers / url fly,
        # they should be encoded otherwise httplib will
        # complain.
        headers = self.encode_headers(headers)

        try:
            if self.endpoint.endswith("/") or url.startswith("/"):
                conn_url = "%s%s" % (self.endpoint, url)
            else:
                conn_url = "%s/%s" % (self.endpoint, url)
            resp = self.session.request(method,
                                        conn_url,
                                        data=data,
                                        stream=False,
                                        headers=headers,
                                        **kwargs)
        except requests.exceptions.Timeout as e:
            message = ("Error communicating with %(endpoint)s %(e)s" %
                       dict(endpoint=self.endpoint, e=e))
            raise exc.InvalidEndpoint(message=message)
        except (requests.exceptions.ConnectionError, ProtocolError) as e:
            message = ("Error finding address for %(url)s: %(e)s" %
                       dict(url=conn_url, e=e))
            raise exc.CommunicationError(message=message)
        except Exception as e:
            message = ("Unexpected Error: %(e)s" %
                       dict(e=e))
            raise exc.BaseException(message=message)

        # Let's use requests json method,
        # it should take care of response
        # encoding
        body = resp.json()

        if not body['result']['status'] == 'success' \
                or not body['result']['error-code'] == 'NAL100000':
            raise exc.nal_response(body['result'])
        else:
            return body

    def get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)
