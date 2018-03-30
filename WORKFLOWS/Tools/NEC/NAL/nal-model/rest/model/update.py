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

from rest.common import exception
from rest.conf import tables as tables_conf
from rest.lib import database


class Update:

    def execute(self, request_params, table_name):

        # ------------------------------------------------------
        # Initialaize
        # ------------------------------------------------------

        # Get ConfigValue
        table_conf = getattr(tables_conf, table_name, {})
        table_pkey = table_conf.get('primaryKey')
        table_columns = table_conf.get('columns')
        table_extension_columns = table_conf.get('extension_columns')
        request_params_id = request_params.get('id')
        request_params_body = request_params.get('body')

        # Get Date
        now_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        # Create Instance(LibDatabase)
        db = database.LibDatabase()

        # ------------------------------------------------------
        # Get Current Record(extension_info)
        # ------------------------------------------------------
        sel_sql = ''
        sel_param_vals = []
        sel_sql_where = ''

        sel_sql = 'SELECT extension_info'
        sel_sql += ' FROM ' + table_name

        if len(table_pkey) > 0 and len(request_params_id) == len(table_pkey):
            sel_sql_where = ' WHERE '
            sel_sql_where += ' = %s AND '.join(table_pkey) + ' = %s '
            sel_param_vals = request_params_id
        else:
            raise exception.InvalidRequestParam

        sel_sql += sel_sql_where

        res = db.execute_sql(sel_sql, sel_param_vals)
        if len(res) == 0:
            raise exception.NotFound

        # ------------------------------------------------------
        # Update Record
        # ------------------------------------------------------
        sql_columns = []
        param_vals = []

        for column in table_columns:

            if column in request_params_body:
                val = request_params_body.get(column)
            else:
                if column == 'update_date':
                    val = now_date
                else:
                    continue

            sql_columns.append(column)
            param_vals.append(val)

        # Set Extension Clumns
        extension_info = json.loads(res[0]['extension_info'])
        extension_info_update = {}
        for extension_column in table_extension_columns:

            if extension_column in request_params_body:
                extension_val = request_params_body.get(extension_column)
            else:
                extension_val = extension_info.get(extension_column)

            extension_info_update[extension_column] = extension_val

        sql_columns.append('extension_info')
        param_vals.append(json.dumps(extension_info_update))

        sql = 'UPDATE ' + table_name + ' SET '
        if len(sql_columns) > 0:
            sql += ' = %s, '.join(sql_columns) + ' = %s'

        sql_where = ''
        sql_where = ' WHERE '
        sql_where += ' = %s AND '.join(table_pkey) + ' = %s '
        param_vals += request_params_id

        sql += sql_where

        # Execute SQL
        return db.execute_sql(sql, param_vals)
