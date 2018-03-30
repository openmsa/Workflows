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
import subprocess

from job.lib import logger


class ScriptClientBase:

    SCRIPT_NAME_LIST = {
        'a10_vthunder_authentication': 'A10_vThunder_authentication',
        'paloalto_authentication': 'Paloalto_authentication',
        'create_vxlan_gw': 'createVxlanGw',
        'delete_vxlan_gw': 'deleteVxlanGw',
        'a10_vthunder_provisioning': 'A10_vThunder_provisioning',
        'bigip_provisioning': 'BIGIP_provisioning',
        'fortivm_provisioning': 'fortiVM_provisioning',
        'paloalto_provisioning': 'Paloalto_provisioning',
        'vsrx_ff_provisioning': 'vSRX_FF_provisioning',
        'intersec_vm_get_rsa': 'intersec_vm_get_rsa',
        'intersec_vm_put_rsa': 'intersec_vm_put_rsa',
    }

    def __init__(self, api_config_instance):

        self.config = api_config_instance
        self.logger = logger.LibLogger(api_config_instance)

    def execute(self, client_function, script_params, passwords=[]):

        command = self.shebang + ' '
        command += self.config.SCRIPT_DIR + '/'
        command += self.SCRIPT_NAME_LIST[client_function]
        command += self.config.SCRIPT_EXTENSION

        esc_str = self.config.SCRIPT_PARAM_ENCLOSURE
        esc_str += self.config.SCRIPT_PARAM_ENCLOSURE

        for idx in range(len(script_params)):
            param_val = script_params[idx]
            if isinstance(param_val, str) == False:
                param_val = str(param_val)
            val = param_val.replace(
                            self.config.SCRIPT_PARAM_ENCLOSURE, esc_str)
            command += ' ' + self.config.SCRIPT_PARAM_ENCLOSURE
            command += val + self.config.SCRIPT_PARAM_ENCLOSURE

        passwords_esc = []
        for passwd in passwords:
            if len(passwd) > 0:
                passwords_esc.append(
                passwd.replace(self.config.SCRIPT_PARAM_ENCLOSURE, esc_str))

        # Output Log(Script Command)
        log_msg = '[Script]' + client_function
        log_msg += '[Command]' + command
        self.logger.log_info(__name__, log_msg, passwords_esc)

        try:
            output = subprocess.check_output(
                            command,
                            shell=True,
                            stderr=subprocess.STDOUT
                            )
        except Exception as e:
            log_msg = '[Script]' + client_function
            output = getattr(e, 'output', '').decode(self.config.CHAR_SET)\
                if getattr(e, 'output', '') != None else ''
            stderr = getattr(e, 'stderr', '').decode(self.config.CHAR_SET)\
                if getattr(e, 'stderr', '') != None else ''
            log_msg += '[Output]' + output
            log_msg += '[Error]' + stderr
            self.logger.log_info(__name__, log_msg, passwords_esc)
            raise e

        output = output.decode(self.config.CHAR_SET)

        # Output Log(Script Command)
        log_msg = '[Script]' + client_function
        log_msg += '[Output]' + output
        self.logger.log_info(__name__, log_msg, passwords_esc)

        output = output.split(self.config.SCRIPT_STDOUT_SEPARATER)
        output.pop()

        return output
