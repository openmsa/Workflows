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
import os
import sys
import traceback

sys.path.append(
os.path.dirname(os.path.abspath(__file__)) + '/../../../../../')

from job.tool.stubs.rest.msa.conf import config


def application(environ, start_response):

    status = config.HTTP_STATUS_DEF['OK']
    response_headers = [('Content-type', 'application/json'),
                        ('charset', 'utf-8')]
    response_body = ''

    error_path = os.path.dirname(os.path.abspath(__file__)) \
                                                + '/log/error.log'

    try:
        # Get HTTP Method
        http_method = environ.get('REQUEST_METHOD')

        # Get URI
        uri = environ.get('REQUEST_URI')
        resource_info = uri.split('index.py/')
        resource_info = resource_info[-1].split('?')
        uri_params = resource_info[0].split('/')

        # Set ResponseFile Path
        response_dir = os.path.dirname(os.path.abspath(__file__)) \
                                                        + '/response/'
        response_filename = http_method + '@' + '@'.join(uri_params)

        response_path = response_dir + response_filename
        if os.path.exists(response_path):

            # Get Response Body
            with open(response_path, 'r') as f:
                response_body = f.read()

        else:
            status = config.HTTP_STATUS_DEF['NOTFOUND']
            response_body = '{"error":"stub response file not found(' \
                + response_path.replace(
                                '\\', '\\\\').replace('"', '\\"') + ')"}'

            with open(error_path, 'w') as f:
                f.write(response_body)

    except:
        status = config.HTTP_STATUS_DEF['ERROR']
        response_body = '{"error":"' \
            + traceback.format_exc().replace(
                                '\\', '\\\\').replace('"', '\\"') + ')"}'

        with open(error_path, 'w') as f:
            f.write(response_body)

    # ------------------------------------------------------
    # Return Response
    # ------------------------------------------------------
    response_headers.append(('Content-Length', str(len(response_body))))

    start_response(status, response_headers)

    return [response_body.encode()]
