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


import sys


class BaseException(Exception):
    """An error occurred."""
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or self.__class__.__doc__


class CommandError(BaseException):
    """Invalid usage of CLI."""


class InvalidEndpoint(BaseException):
    """The provided endpoint is invalid."""


class CommunicationError(BaseException):
    """Unable to communicate with server."""


class ClientException(Exception):
    """DEPRECATED!"""


class NalApiException(ClientException):
    """Base exception for all NAL-API exceptions."""
    code = 'N/A'

    def __init__(self, details=None):
        self.details = details or self.__class__.__name__

    def __str__(self):
        return "%s (HTTP %s)" % (self.details, self.code)


class NalBadRequest(NalApiException):
    """DEPRECATED!"""
    code = 'NAL110001'


class NalJobError(NalApiException):
    """DEPRECATED!"""
    code = 'NAL120001'


class NalRestApiError(NalApiException):
    """DEPRECATED!"""
    code = 'NAL130001'


class NalApiInternalError(NalApiException):
    """DEPRECATED!"""
    code = 'NAL140001'


class NalOpenstackApiError(NalApiException):
    """DEPRECATED!"""
    code = 'NAL150001'


_nal_code_map = {}
for obj_name in dir(sys.modules[__name__]):
    if obj_name.startswith('Nal'):
        obj = getattr(sys.modules[__name__], obj_name)
        _nal_code_map[obj.code] = obj


def nal_response(response):
    """Return an instance of an NalApiException based on httplib response."""
    cls = _nal_code_map.get(response['error-code'], NalApiException)
    # Iterate over the nested objects and retreive the "message" attribute.
    details = response['message']
    return cls(details=details)
