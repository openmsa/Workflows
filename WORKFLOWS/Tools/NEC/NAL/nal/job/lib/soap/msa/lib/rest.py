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
import base64
import json

from job.lib import logger
from urllib import parse
from urllib import request


class MsaRest:

    # HTTP METHOD
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'
    METHOD_PUT = 'PUT'
    METHOD_DELETE = 'DELETE'

    CONTENT_TYPE = 'application/json'

    def __init__(self, api_config_instance):
        self.logger = logger.LibLogger(api_config_instance)
        self.char_code = api_config_instance.CHAR_SET

    def rest_post(self, url, basic_auth={},
                  query_params={}, post_params=None):

        res = self.__execute(self.METHOD_POST,
                        url, basic_auth, query_params, post_params)
        return res

    def __execute(self, http_method, url, basic_auth,
                        query_params, post_params):

        passwords = []

        if len(url) == 0:
            raise SystemError('url required')

        if len(query_params) > 0:
            url += '?' + parse.urlencode(query_params)

        if post_params == None:
            request_body = ''
        else:
            request_body = json.dumps(post_params)

        request_body = request_body.encode(self.char_code)

        http_header = {
            'Content-Type': self.CONTENT_TYPE,
            'Content-Length': str(len(request_body))
        }

        if len(basic_auth) > 0:
            passwords.append(basic_auth['pass'])
            authorization = basic_auth['id'] + ':' + basic_auth['pass']
            http_header['Authorization'] = 'Basic ' + base64.b64encode(
                        authorization.encode(self.char_code)).decode('ascii')

        # Output Log(MSA Request)
        log_msg = '[MSA Request]'
        log_msg += '[METHOD]' + http_method
        log_msg += '[URL]' + url
        log_msg += '[HEADER]' + json.dumps(http_header)
        log_msg += '[PARAMS]' + json.dumps(post_params)
        self.logger.log_info(__name__, log_msg, passwords)

        req = request.Request(url, headers=http_header, data=request_body)
        req.method = http_method

        with request.urlopen(req) as res:
            response_params = res.read().decode(self.char_code)

        # Output Log(MSA Response)
        log_msg = '[NSA Response]'
        log_msg += '[STATUS]' + str(res.getcode())
        log_msg += '[HEADER]' + str(res.headers)
        log_msg += '[PARAMS]' + response_params
        self.logger.log_info(__name__, log_msg, passwords)

        if len(response_params) > 0:

            try:
                response_params = json.loads(response_params)

            except json.decoder.JSONDecodeError:
                raise SystemError(response_params)

            except:
                raise

        return response_params
