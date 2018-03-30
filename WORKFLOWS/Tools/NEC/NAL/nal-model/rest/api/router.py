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
import importlib
import json
import traceback
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from pprint import pprint
from rest.common import exception
from rest.conf import config
from rest.conf import router as router_conf
from rest.lib import logger

MODEL_PACKAGE_PATH = 'rest.model.'
LOG_FILE = getattr(config, 'LOG_OUTPUT_PASS', {})
DECORAT = "\n" + \
          "**********************************************************\n" + \
          "%s\n" + \
          "**********************************************************"


class Router:

    def routing(self, request_params):

        # Set Logger
        LOG = logger.LibLogger(request_params.get('request_id'))
        LOG.log_debug(__name__, DECORAT % request_params.get('environ', {}))

        result = {}

        try:
            resource = request_params.get('resource', '')
            method = request_params.get('method', '')

            if len(resource) == 0 or len(method) == 0:
                raise exception.InvalidRequestParam

            # Get Status Code
            status = getattr(config, 'HTTP_STATUS_DEF', {})\
                                .get(request_params['method'], '')

            # Get Router Definition
            cl_nt_tbl = getattr(router_conf, 'CLASS_METHOD_TABLE', {})
            router_config = cl_nt_tbl.get(resource, {}).get(method, {})

            # Get Classname & Methodname & Tablename
            execute_module_name = router_config.get('moduleName', '')
            execute_class_name = router_config.get('className', '')
            execute_method_name = router_config.get('methodName', '')
            table_name = router_config.get('tableName', '')

            if len(execute_module_name) == 0\
                     or len(execute_class_name) == 0\
                     or len(execute_method_name) == 0\
                     or len(table_name) == 0\
                     or len(status) == 0:
                raise exception.NotFound

            # Import Module
            module = importlib.import_module(
                MODEL_PACKAGE_PATH + execute_module_name)

            # Get Class Object
            class_obj = getattr(module, execute_class_name)

            # Get Method Object
            method = getattr(class_obj(), execute_method_name)

            # Execute Method
            result = method(request_params, table_name)

        except exception.ApiAppException as api_e:
            tb = traceback.format_exc()
            LOG.log_error(__name__, tb)
            status = api_e.code
            result = api_e.message

        except Exception:
            tb = traceback.format_exc()
            LOG.log_fatal(__name__, tb)
            status = getattr(config, 'HTTP_STATUS_DEF', {}).get('ERROR')
            result = 'Internal Server Error.'

        output = {}
        output['status'] = status
        output['message'] = json.dumps(result).encode('utf-8')

        LOG.log_debug(__name__, DECORAT % output)

        return output
