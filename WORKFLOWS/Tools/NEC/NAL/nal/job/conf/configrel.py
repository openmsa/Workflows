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


class JobConfigRel:

    """JOB Config For Integrated Environment(External)."""

    # Definition For Log
    LOG_OUTPUT_PASS = '/var/log/nal/nal_automation_trace.log'
    LOG_LEVEL = 'INFO'

    # Definition For ScriptClient
    SCRIPT_DIR = '/home/nsumsmgr/NAL/nwa/job/lib/script'
    SCRIPT_DIR += '/script'
    SCRIPT_SHEBANG = 'sh'
    SCRIPT_SHEBANG_PYTHON = '/usr/bin/python2'
    SCRIPT_EXTENSION = '.sh'
    SCRIPT_PARAM_ENCLOSURE = "'"
    SCRIPT_STDOUT_SEPARATER = '\n'

    # Definition For DB Client(RestAPI)
    REST_ENDPOINT = 'http://10.169.11.3/rest/api/index.py/'

    # Difinition For Template Directory
    TEMPLATE_DIR = '/home/nsumsmgr/NAL/nwa/job/template'
