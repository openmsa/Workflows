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

from pprint import pprint
from rest.common import exception
from rest.conf import config
from rest.conf import tables as tables_conf
from rest.lib import database
from rest.lib import logger


class Select:

    def execute(self, request_params, table_name):

        # ------------------------------------------------------
        # Initialaize
        # ------------------------------------------------------
        request_id = request_params.get('request_id', '')
        log = logger.LibLogger(request_id)

        # Get Table Definition
        table_conf = getattr(tables_conf, table_name, {})

        # Get ConfigValue
        table_columns = table_conf.get('columns')
        table_extension_columns = table_conf.get('extension_columns')
        table_pkey = table_conf.get('primaryKey')
        request_params_id = request_params.get('id', [])
        request_params_query = request_params.get('query', {})

        # Create Instance(LibDatabase)
        db = database.LibDatabase()

        # ------------------------------------------------------
        # Select Record
        # ------------------------------------------------------
        # Get ColumnName
        select_columns = []
        for key in table_columns:
            select_columns.append(self._edit_select_column(key, \
                                       table_columns.get(key).get('type')))

        # Edit Query
        sql = 'SELECT ' + ',' .join(select_columns)
        sql += ' FROM ' + table_name

        param_vals = []
        sql_where = ''

        # Map Parameters
        if len(request_params_id) > 0:

            if len(request_params_id) == len(table_pkey):
                sql_where += ' = %s AND '.join(table_pkey) + ' = %s '
                param_vals = request_params_id

            else:
                raise exception.InvalidRequestParam

        if len(request_params_query) > 0:

            for column in table_columns:

                if column in request_params_query:

                    if len(sql_where) > 0:
                        sql_where += ' AND'

                    sql_where += ' ' + column + ' = %s'
                    param_vals.append(request_params_query[column])

        if len(sql_where) > 0:
            sql_where = ' WHERE ' + sql_where

        # Add Where Phrase
        sql += sql_where

        # Add Where Phrase
        sql += ' ORDER BY ID ASC'

        # Execute SQL
        res = db.execute_sql(sql, param_vals)

        # Edit ResultData to Array
        result = []
        extension_info = []
        for res_row in res:

            row = {}
            qurey_unmatch_flg = False

            # Set Columns Info
            for column_key, column_val in res_row.items():

                if column_key == 'extension_info':
                    if column_val is None:
                        extension_info = {}
                    else:
                        extension_info = json.loads(column_val)
                else:
                    if column_val is None:
                        row[column_key] = ''
                    else:
                        row[column_key] = column_val

            # Set Ext Columns Info
            for ext_column in table_extension_columns:

                if ext_column in extension_info:
                    row[ext_column] = extension_info[ext_column]
                else:
                    row[ext_column] = ''

                # Check query matching
                if ext_column in request_params_query and \
                       str(request_params_query[ext_column]) \
                            != str(extension_info[ext_column]):

                    qurey_unmatch_flg = True
                    break

            # Set Records
            if qurey_unmatch_flg == False:
                result.append(row)

        # Return ResultData
        return result

    def _edit_select_column(self, field_name, column_type):

        select_column = field_name
        if column_type in getattr(config, 'SELECT_COLUMN_TYPE_DEF', {}):
            sel_type_def = getattr(config, 'SELECT_COLUMN_TYPE_DEF', {})
            select_column = sel_type_def.get(column_type)\
                                  .replace('%field_name%', field_name)

        return select_column
