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


class ApiAppException(Exception):
    message = "An unknown exception occurred"

    def __init__(self, message=None):
        if not message:
            message = self.message


class NotFound(ApiAppException):
    message = "An object with the specified identifier was not found."
    code = "404 NotFound"


class Invalid(ApiAppException):
    message = "Data supplied was not valid."
    code = "400 Bad Request"


class InvalidRequestParam(Invalid):
    message = "Request param supplied was not valid."
