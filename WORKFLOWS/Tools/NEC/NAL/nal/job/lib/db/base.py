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
from urllib import parse, request

from job.lib import logger


class DbClientBase:

    def __init__(self, api_config_instance):
        self.logger = logger.LibLogger(api_config_instance)
        self.char_set = api_config_instance.CHAR_SET

    def execute(self, passwords=[]):

        request_body = parse.urlencode(self.params).encode(self.char_set)

        http_header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': str(len(request_body))
        }

        # Output Log(REST API Request)
        log_msg = '[REST API Request]'
        log_msg += '[METHOD]' + self.method
        log_msg += '[URL]' + self.end_point
        log_msg += '[HEADER]' + json.dumps(http_header)
        log_msg += '[PARAMS]' + json.dumps(self.params)
        self.logger.log_info(__name__, log_msg, passwords)

        req = request.Request(
                    self.end_point,
                    request_body,
                    http_header, None, False, self.method)

        res = request.urlopen(req)

        self.http_status = res.getcode()
        self.return_param = res.read()
        self.return_param = self.return_param.decode(self.char_set)

        # Output Log(REST API Response)
        log_msg = '[REST API Response]'
        log_msg += '[STATUS]' + str(self.http_status)
        log_msg += '[PARAMS]' + self.return_param
        self.logger.log_info(__name__, log_msg, passwords)

        if self.return_param != None and len(self.return_param) > 0:
            self.return_param = json.loads(self.return_param)

    def get_return_param(self):
        return {'status_code': self.http_status}
