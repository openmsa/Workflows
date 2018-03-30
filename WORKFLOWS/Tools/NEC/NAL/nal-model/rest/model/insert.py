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

import datetime
import json

from rest.conf import tables as tables_conf
from rest.lib import database


class Insert:

    def execute(self, request_params, table_name):

        # ------------------------------------------------------
        # Initialaize
        # ------------------------------------------------------
        table_conf = getattr(tables_conf, table_name, {})
        table_columns = table_conf.get('columns')
        table_extension_columns = table_conf.get('extension_columns')
        request_params_body = request_params.get('body')
        now_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        # Create Instance(LibDatabase)
        db = database.LibDatabase()

        # ------------------------------------------------------
        # Insert Record
        # ------------------------------------------------------
        sql_columns = ''
        sql_values = ''
        param_vals = []

        for column in table_columns:

            if column != 'extension_info' \
                    and column in request_params_body:
                val = request_params_body.get(column)
            else:
                if column == 'create_date' or column == 'update_date':
                    val = now_date
                else:
                    continue

            if len(sql_columns) > 0:
                sql_columns += ','
                sql_values += ','

            sql_columns += column
            sql_values += '%s'
            param_vals.append(val)

        extension_info = {}
        for extension_column in table_extension_columns:

            if extension_column in request_params_body:
                extension_val = request_params_body.get(extension_column)
            else:
                extension_val = ''

            extension_info[extension_column] = extension_val

        sql_columns += ',extension_info'
        sql_values += ',%s'
        param_vals.append(json.dumps(extension_info))

        sql = 'INSERT INTO ' + table_name
        sql += '(' + sql_columns + ') VALUES (' + sql_values + ')'

        # Execute SQL
        res = db.execute_sql(sql, param_vals)

        # Return Create Primary Key
        return {'ID': res[0]['last_insert_id()']}
