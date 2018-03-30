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
import inspect

from job.lib.soap.msa import base


class DeviceWs(base.MsaClientBase):

    def __init__(self,
        api_config_instance, nal_endpoint_config, pod_id, dc_id='system'):
        super().__init__(api_config_instance, 'device_create_endpoint',
                         nal_endpoint_config, pod_id, dc_id)

    def create_managed_device(self,
                                customer_id,
                                device_name,
                                login_user,
                                password,
                                admin_password,
                                manufacture_id,
                                model_id,
                                ip_address,
                                host_name=None):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = {
            'customerId': customer_id,
            'deviceName': device_name,
            'login': login_user,
            'password': password,
            'passwordAdmin': admin_password,
            'useNat': False,
            'logEnabled': False,
            'logMoreEnabled': False,
            'mailAlerting': False,
            'reporting': False,
            'manufacturerId': manufacture_id,
            'modelId': model_id,
            'internalInterface': {
                'connectivitySide': 'INTERNAL',
                'ipAddress': {'address': '192.168.1.10'},
                'public': False,
                'voip': False,
                'logicalName': None,
                'typeIp': 'STATIC',
                'typeEthernet': 'FAST',
            },
            'externalInterface': {
                'connectivitySide': 'EXTERNAL',
                'ipAddress': {
                    'address': ip_address,
                },
                'public': False,
                'voip': False,
                'logicalName': None,
                'typeIp': 'STATIC',
                'gateway': {
                    'address': '192.168.1.10',
                },
                'typeEthernet': 'FAST',
            },
        }

        if host_name is not None:
            msa_params['Hostname'] = host_name

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        passwords = [password, admin_password]
        self.output_log_soap_params(
                    'in', __name__, client_name, msa_params, passwords)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.createManagedDevice(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params(
                    'out', __name__, client_name, msa_result, passwords)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def delete_device_by_id(self, device_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = {'deviceId': device_id}

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.deleteDeviceById(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def do_provisioning_by_device_id(self, device_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = {'deviceId': device_id}

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.doProvisioningByDeviceId(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def get_provisioning_status_by_id(self, device_id):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = {'deviceId': device_id}

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = self.soap_client.getProvisioningStatusById(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}

    def update_device_management_port(self, device_id, management_port):

        client_name = inspect.currentframe().f_code.co_name

        # Set InputParameters(MSA)
        msa_params = {'deviceId': device_id, 'managementPort': management_port}

        # Save Client Info(Stub)
        self.save_cilent_info(client_name, msa_params)

        # Output Log(SoapClient Input Parameters)
        self.output_log_soap_params('in', __name__, client_name, msa_params)

        # Call SoapClient Method(MSA)
        msa_result = \
            self.soap_client.updateDeviceManagementPort(**msa_params)

        # Output Log(SoapClient Output Parameters)
        self.output_log_soap_params('out', __name__, client_name, msa_result)

        return {self.RES_KEY_IN: msa_params, self.RES_KEY_OUT: msa_result}
