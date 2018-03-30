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

from rest.common import exception
from rest.conf import tables as tables_conf
from rest.lib import database


class Delete:

    def execute(self, request_params, table_name):

        # ------------------------------------------------------
        # Initialaize
        # ------------------------------------------------------
        table_conf = getattr(tables_conf, table_name, {})
        table_pkey = table_conf.get('primaryKey')
        request_params_id = request_params.get('id')

        # Create Instance(LibDatabase)
        db = database.LibDatabase()

        # ------------------------------------------------------
        # Get Current Record(extension_info)
        # ------------------------------------------------------
        sel_sql = ''
        sel_param_vals = []
        sel_sql_where = ''

        sel_sql = 'SELECT * '
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
        # Delete Record
        # ------------------------------------------------------
        sql = 'DELETE FROM ' + table_name
        sql_where = ''
        param_vals = []

        sql_where = ' WHERE '
        sql_where += ' = %s AND '.join(table_pkey) + ' = %s '
        param_vals += request_params_id

        sql += sql_where

        # Execute SQL
        return db.execute_sql(sql, param_vals)
