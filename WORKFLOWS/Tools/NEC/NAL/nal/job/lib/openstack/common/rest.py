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
import json

from job.lib import logger
from urllib import parse
from urllib import request


class OscRest:

    # HTTP METHOD
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'
    METHOD_PUT = 'PUT'
    METHOD_DELETE = 'DELETE'
    METHOD_PATCH = 'PATCH'

    CONTENT_TYPE = 'application/json'

    def __init__(self, api_config_instance):
        self.logger = logger.LibLogger(api_config_instance)
        self.char_code = api_config_instance.CHAR_SET

    def rest_get(self, url, token,
                 post_params={}, query_params={}, passwords=[]):

        res = self.__execute(self.METHOD_GET,
                        url, token, post_params, query_params, passwords)
        return res['params']

    def rest_post(self, url, token,
                 post_params={}, query_params={}, passwords=[]):

        res = self.__execute(self.METHOD_POST,
                        url, token, post_params, query_params, passwords)
        return res['params']

    def rest_post_token_v3(self, url, token,
                 post_params={}, query_params={}, passwords=[]):

        res = self.__execute(self.METHOD_POST,
                        url, token, post_params, query_params, passwords)
        return res

    def rest_put(self, url, token,
                 post_params={}, query_params={}, passwords=[]):

        res = self.__execute(self.METHOD_PUT,
                        url, token, post_params, query_params, passwords)
        return res['params']

    def rest_delete(self, url, token,
                 post_params={}, query_params={}, passwords=[]):

        res = self.__execute(self.METHOD_DELETE,
                        url, token, post_params, query_params, passwords)
        return res['params']

    def rest_patch(self, url, token,
                 post_params={}, query_params={}, passwords=[]):

        res = self.__execute(self.METHOD_PATCH,
                        url, token, post_params, query_params, passwords)
        return res['params']

    def __execute(self, http_method, url, token,
                        post_params, query_params, passwords):

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

        if len(token) > 0:
            http_header['X-Auth-Token'] = token

        # Output Log(OpenStack Request)
        log_msg = '[OpenStack Request]'
        log_msg += '[METHOD]' + http_method
        log_msg += '[URL]' + url
        log_msg += '[HEADER]' + json.dumps(http_header)
        log_msg += '[PARAMS]' + json.dumps(post_params)
        self.logger.log_info(__name__, log_msg, passwords)

        req = request.Request(url, headers=http_header, data=request_body)
        req.method = http_method

        with request.urlopen(req) as res:
            response_params = res.read().decode(self.char_code)

        # Output Log(OpenStack Response)
        log_msg = '[OpenStack Response]'
        log_msg += '[STATUS]' + str(res.getcode())
        log_msg += '[HEADER]' + str(res.headers)
        log_msg += '[PARAMS]' + response_params
        self.logger.log_info(__name__, log_msg, passwords)

        res_token = res.headers.get('X-Subject-Token', '')

        if len(response_params) > 0:

            try:
                response_params = json.loads(response_params)

            except json.decoder.JSONDecodeError:
                raise SystemError(response_params)

            except:
                raise

        return {'token': res_token, 'params': response_params}
