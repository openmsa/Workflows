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

import mysql.connector

from rest.conf import config
from rest.lib import logger


class LibDatabase:

    def _connect_db(self):

        try:
            # Connect Database
            con = mysql.connector.connect(
                host=getattr(config, 'MYSQL_HOSTNAME', ''),
                db=getattr(config, 'MYSQL_DBNAME', ''),
                user=getattr(config, 'MYSQL_USERID', ''),
                passwd=getattr(config, 'MYSQL_PASSWORD', ''),
                buffered=True)

            # Set Autocommit Off
            con.autocommit = False

            return con

        except ConnectionError as de:
            # TODO Set request_id
            request_id = 'test_set_request_id'
            log = logger.LibLogger(request_id)
            log.log_error(__name__, 'It could not be connected.')

            raise de

    def execute_sql(self, sql, param_vals):

        try:
            # Open Database Connection
            con = self._connect_db()

            # Open Cursor
            cur = con.cursor(dictionary=True)

            # Execute SQL
            cur.execute(sql, param_vals)
            if sql.startswith('SELECT'):
                # Get Result
                return cur.fetchall()
            elif sql.startswith('INSERT'):
                # Commit Transaction
                con.commit()
                # Get Result
                sql = 'SELECT last_insert_id()'
                cur.execute(sql, [])
                return cur.fetchall()
            else:
                # Commit Transaction
                con.commit()

                # Return ResultData
                return True

        except Exception as e:
            # Rollback Transaction
            if 'con' in locals():
                con.rollback()

            raise e

        finally:
            # Close Cursor
            if 'cur' in locals():
                cur.close()

            # Close Database
            if 'con' in locals():
                con.close()
