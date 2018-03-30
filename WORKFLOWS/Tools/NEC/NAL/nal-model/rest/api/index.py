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

import cgi
import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from rest.api import router


def application(environ, start_response):

    request_params = {}

    # ------------------------------------------------------
    # Get Param
    # ------------------------------------------------------
    request_params['environ'] = environ

    # Get HTTP Method
    request_params['method'] = environ.get('REQUEST_METHOD')

    # Get resource,id
    uri = environ.get('REQUEST_URI')
    resource_info = uri.split('index.py/')
    resource_info = resource_info[-1].split('?')
    parse_res = resource_info[0].split('/')

    request_params['resource'] = ''
    ids = []

    for i in range(len(parse_res)):

        if i == 0:
            request_params['resource'] = parse_res[0]
        else:
            if len(parse_res[i]):
                ids.append(parse_res[i])

    request_params['id'] = ids

    # Get Query String
    form = cgi.FieldStorage(environ=environ, keep_blank_values=True)
    request_params['query'] = {k: form[k].value for k in form}

    # Get Body Parameters
    wsgi_input = environ.get('wsgi.input')
    form = cgi.FieldStorage(
        fp=wsgi_input, environ=environ, keep_blank_values=True)
    request_params['body'] = {k: form[k].value for k in form}

    # Get request_id
    if request_params['method'] == 'GET' \
            or request_params['method'] == 'DELETE':
        request_id = request_params['query'].get('request-id', '')
    else:
        request_id = request_params['body'].get('request-id', '')

    request_params['request_id'] = request_id

    # ------------------------------------------------------
    # Execute Routing
    # ------------------------------------------------------
    router_obj = router.Router()
    output = router_obj.routing(request_params)
    status = output['status']
    message = output['message']

    # ------------------------------------------------------
    # Return Result
    # ------------------------------------------------------
    response_headers = [('Content-type', 'text/plain'),
                         ('Content-Length', str(len(message)))]
    start_response(status, response_headers)
    return [message]
