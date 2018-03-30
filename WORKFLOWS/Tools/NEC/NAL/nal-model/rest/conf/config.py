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

# Database Connecting Infomation
MYSQL_HOSTNAME = 'localhost'
MYSQL_USERID = 'root'
MYSQL_PASSWORD = 'i-portal'
MYSQL_DBNAME = 'nal'

# Column DataType Conversion Definition(for SELECT)
SELECT_COLUMN_TYPE_DEF = {
    'DECIMAL':
        'CAST(%field_name% AS CHAR) AS %field_name%',
    'DATETIME':
        "DATE_FORMAT(%field_name%, '%Y-%m-%d %T') AS %field_name%",
}

# HTTP Status Definition
HTTP_STATUS_DEF = {
    'GET': '200 OK',
    'PUT': '200 OK',
    'POST': '200 OK',
    'DELETE': '200 OK',
    'ERROR': '500 Internal Server Error',
}

# Log Output Pass Definition
LOG_OUTPUT_PASS = '/var/log/nal/nal_model_trace.log'
LOG_OUTPUT_LEVEL = 'DEBUG'
