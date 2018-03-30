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
import base64

from job.lib.openstack.nova import base


class OscServers(base.OscNovaBase):

    SERVER_ACTION_RESUME = 'resume'
    SERVER_ACTION_RESETNETWORK = 'resetNetwork'
    SERVER_ACTION_SUSPEND = 'suspend'
    SERVER_ACTION_REBOOT = 'reboot'
    SERVER_ACTION_RESIZE = 'resize'
    SERVER_ACTION_CONFIRMRESIZE = 'confirmResize'
    SERVER_ACTION_OS_STOP = 'os-stop'
    SERVER_ACTION_OS_START = 'os-start'
    SERVER_ACTION_GETCONSOLE = 'os-getVNCConsole'
    SERVER_STATUS_ACTIVE = 'ACTIVE'
    SERVER_STATUS_ERROR = 'ERROR'
    SERVER_STATUS_SUSPEND = 'SUSPENDED'
    SERVER_STATUS_PAUSE = 'PAUSED'
    SERVER_STATUS_RESIZE = 'RESIZE'
    SERVER_STATUS_VERIFY_RESIZE = 'VERIFY_RESIZE'
    SERVER_STATUS_SHUTOFF = 'SHUTOFF'
    SERVER_REBOOT_TYPE_SOFT = 'SOFT'
    SERVER_REBOOT_TYPE_HARD = 'HARD'
    SERVER_ITEM_NOT_FOUND = 'itemNotFound'
    SERVER_TASK_STATE_NULL = None
    SERVER_TYPE_CONSOLE_NOVNC = 'novnc'
    SERVER_RESPONSE_BADREQUEST = 'badRequest'
    SERVER_RESPONSE_ITEMNOTFOUND = 'itemNotFound'
    SERVER_RESPONSE_CONFLICTINGREQUEST = 'conflictingRequest'
    SERVER_RESPONSE_COMPUTEFAULT = 'computeFault'

    PERSONALITY_PATH_INIT_CFG = '/config/init-cfg.txt'
    PERSONALITY_PATH_BOOTSTRAP = '/config/bootstrap.xml'
    PERSONALITY_PATH_IOSXE_CONFIG = 'iosxe_config.txt'

    def list_servers(self, endpoint_array):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/servers/detail'

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'servers' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def get_server(self, endpoint_array, server_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(server_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/servers/' + server_id

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'server' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def create_server(self, endpoint_array,
                                        name,
                                        imageRef,
                                        flavorRef,
                                        networks,
                                        security_groups=None,
                                        metadata=None,
                                        key_name=None,
                                        availability_zone=None,
                                        user_data=None,
                                        config_drive=False,
                                        personality=None):

        # Check Input Parameters
        if len(endpoint_array) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/servers'

        params = {
            'server': {
                'name': name,
                'imageRef': imageRef,
                'flavorRef': flavorRef,
                'networks': networks,
                'config_drive': config_drive,
            }
        }

        if security_groups is not None:
            params['server']['security_groups'] = security_groups

        if metadata is not None:
            params['server']['metadata'] = metadata

        if key_name is not None:
            params['server']['key_name'] = key_name

        if availability_zone is not None:
            params['server']['availability_zone'] = availability_zone

        if user_data is not None:
            user_data_encoded = base64.b64encode(
                user_data.encode(self.char_code)).decode('ascii')

            params['server']['user_data'] = user_data_encoded

        if personality is not None:
            params['server']['personality'] = personality

        # Execute Rest
        resp = self.rest.rest_post(url, token_id, params)

        # Check Response From OpenStack
        if 'server' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def delete_server(self, endpoint_array, server_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(server_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/servers/' + server_id

        # Execute Rest
        resp = self.rest.rest_delete(url, token_id)

        # Check Response From OpenStack
        if (resp == None or len(resp) == 0) == False:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def action_server(self, endpoint_array, server_id, actionkey,
                boot_type=None, resized_flavor=None, console_type=None):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(server_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/servers/' + server_id + '/action'

        params = {}

        if actionkey == self.SERVER_ACTION_REBOOT:
            params[actionkey] = {'type': boot_type}

        elif actionkey == self.SERVER_ACTION_RESIZE:
            params[actionkey] = {'flavorRef': resized_flavor}

        elif actionkey == self.SERVER_ACTION_GETCONSOLE:
            params[actionkey] = {'type': console_type}

        else:
            params = {actionkey: None}

        # Execute Rest
        resp = self.rest.rest_post(url, token_id, params)

        # Check Response From OpenStack
        if actionkey == self.SERVER_ACTION_GETCONSOLE:
            if 'console' not in resp:
                raise SystemError(self.EXCEPT_MSG12)
        else:
            if resp != None and len(resp) > 0:
                raise SystemError(self.EXCEPT_MSG12)

        return resp

    def attach_interface(self, endpoint_array, server_id,
                         port_id=None, net_id=None, ip_address=None):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(server_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/servers/' + server_id + '/os-interface'

        params = {'interfaceAttachment': {}}

        if port_id is not None:
            params['interfaceAttachment']['port_id'] = port_id

        elif net_id is not None:
            params['interfaceAttachment']['net_id'] = net_id

        elif ip_address is not None:
            params['interfaceAttachment']['fixed_ips'] = {
                                            ip_address: ip_address}

        # Execute Rest
        resp = self.rest.rest_post(url, token_id, params)

        # Check Response From OpenStack
        if 'interfaceAttachment' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def detach_interface(self, endpoint_array, server_id, port_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(
                                server_id) == 0 or len(port_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/servers/' + server_id + '/os-interface/' + port_id

        # Execute Rest
        resp = self.rest.rest_delete(url, token_id, {})

        # Check Response From OpenStack
        if resp != None and len(resp) > 0:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

    def list_interfaces(self, endpoint_array, server_id):

        # Check Input Parameters
        if len(endpoint_array) == 0 or len(server_id) == 0:
            raise SystemError(self.EXCEPT_MSG01)

        # Get Token ID
        token_id = self.get_token_id(endpoint_array)

        # Get Endpoint URL
        url = self.get_endpoint(endpoint_array)

        # Set Parameters(Rest)
        url += '/servers/' + server_id + '/os-interface'

        # Execute Rest
        resp = self.rest.rest_get(url, token_id)

        # Check Response From OpenStack
        if 'interfaceAttachments' not in resp:
            raise SystemError(self.EXCEPT_MSG12)

        return resp

