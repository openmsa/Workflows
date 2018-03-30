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
import importlib
import inspect

from job.auto import base


class JobAutoMethod(base.JobAutoBase):

    JOB_AUTO_MODULE_PATH = 'job.auto.'
    JOB_EXTENSION_LIBRARY_PATH = 'extension.'

    def __execute_job_automation(self,
            job_module_name, job_class_name, job_method_name, job_input):

        try:
            # Import Module(Job Automation)
            job_module = importlib.import_module(
                        self.JOB_AUTO_MODULE_PATH + job_module_name)

            # Create Instance(Job Automation)
            class_attr = getattr(job_module, job_class_name)
            job_instance = class_attr(job_input.get('request-id', '-'))
            method_attr = getattr(job_instance, job_method_name)

            # Execute Method(Job Automation)
            job_output = method_attr(job_input)
        except Exception as e:
            try:
                self.set_status_error(job_input, e)
            except:
                pass

            raise e

        return job_output

    # ---------------------------------------------------------------
    # Initialize
    # ---------------------------------------------------------------
    def initialize_create_vnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'initialize'
        job_class_name = 'Initialize'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def initialize_update_vnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'initialize'
        job_class_name = 'Initialize'
        job_method_name = 'get_apl_info'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def initialize_delete_vnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'initialize'
        job_class_name = 'Initialize'
        job_method_name = 'get_apl_info_by_rec_id'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def initialize_create_pnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'initialize'
        job_class_name = 'Initialize'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def initialize_delete_pnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'initialize'
        job_class_name = 'Initialize'
        job_method_name = 'get_apl_info_by_rec_id'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def initialize(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'initialize'
        job_class_name = 'Initialize'
        job_method_name = 'get_apl_info'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Routing Pod(VIM,VXLAN-GW)
    # ---------------------------------------------------------------
    def routing_pod(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'routingpod'
        job_class_name = 'RoutingPod'
        job_method_name = 'routing_pod'

        # Execute Job Automation(Extension Library)
        job_output = self.__execute_job_automation(
                self.JOB_EXTENSION_LIBRARY_PATH + job_module_name,
                job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Tenants
    # ---------------------------------------------------------------
    def tenant_id_convert(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'tenant'
        job_class_name = 'Tenant'
        job_method_name = 'get_or_create_nal_tenant_name'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def get_or_create_pod_tenant(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'tenant'
        job_class_name = 'Tenant'
        job_method_name = 'get_or_create_pod_tenant'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def get_nal_tenant_name(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'tenant'
        job_class_name = 'Tenant'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def get_pod_tenant(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'tenant'
        job_class_name = 'Tenant'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Check PArameter
    # ---------------------------------------------------------------
    def hostname_check(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'hostname'
        job_class_name = 'Hostname'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # MSA Port
    # ---------------------------------------------------------------
    def virtual_msa_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'virtual_msa_port_create'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_msa_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'virtual_msa_port_delete'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Pub Port
    # ---------------------------------------------------------------
    def virtual_pub_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'pub_port_create'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_pub_port_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_pub_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'pub_port_delete'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_pub_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'pub_port_create'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_pub_port_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'virtual_pub_port_add_ipv6'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_pub_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'pub_port_delete'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Ext Port
    # ---------------------------------------------------------------
    def virtual_ext_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'ext_port_create'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_ext_port_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_ext_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'ext_port_delete'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_ext_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'ext_port_create'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_ext_port_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'virtual_ext_port_add_ipv6'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_ext_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'port'
        job_class_name = 'Port'
        job_method_name = 'ext_port_delete'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Tenant Port
    # ---------------------------------------------------------------
    def virtual_fw_tenant_vlan_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = 'virtual_tenant_vlan_port_create_fw'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_lb_tenant_vlan_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = 'virtual_tenant_vlan_port_create_lb'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_fw_tenant_vlan_port_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_lb_tenant_vlan_port_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_fw_tenant_vlan_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = 'virtual_tenant_vlan_port_delete_fw'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_lb_tenant_vlan_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = 'virtual_tenant_vlan_port_delete_lb'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_VR
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_fw_tenant_vlan_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = 'physical_tenant_vlan_port_create_fw'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_lb_tenant_vlan_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = 'physical_tenant_vlan_port_create_lb'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_lb_tenant_vlan_port_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_fw_tenant_vlan_port_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_fw_tenant_vlan_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = 'physical_tenant_vlan_port_delete_fw'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_lb_tenant_vlan_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlan'
        job_class_name = 'Vlan'
        job_method_name = 'physical_tenant_vlan_port_delete_lb'

        # Execute Job Automation
        job_input['apl_type'] = self.job_config.APL_TYPE_PH
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Instance
    # ---------------------------------------------------------------
    def virtual_server_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_server_create_with_config_drive(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_server_create_intersec(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_server_create_paloalto_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_fw_interface_attach(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = 'virtual_server_port_attach'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_fw_interface_attach_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_lb_interface_attach_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_server_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_fw_interface_detach(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = 'virtual_server_port_detach'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_server_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def physical_server_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'server'
        job_class_name = 'Server'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Lincense
    # ---------------------------------------------------------------
    def license_assign(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'license'
        job_class_name = 'License'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def license_assign_fortigate_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'license'
        job_class_name = 'License'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def license_assign_fortigate_vm_541(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'license'
        job_class_name = 'License'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def license_assign_bigip_ve(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'license'
        job_class_name = 'License'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def license_assign_palpalto_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'license'
        job_class_name = 'License'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def zerotouch_vthunder(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'license'
        job_class_name = 'License'
        job_method_name = 'zerotouch_vthunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def license_assign_vthunder(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'license'
        job_class_name = 'License'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def license_withdraw(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'license'
        job_class_name = 'License'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # MSA
    # ---------------------------------------------------------------
    def msa_setup_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupmsa'
        job_class_name = 'SetupMsa'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_setup_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupmsa'
        job_class_name = 'SetupMsa'
        job_method_name = 'msa_delete_device_setting'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_intersec_sg_internet(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceintersecsg'
        job_class_name = 'SetupDeviceInterSecSg'
        job_method_name = 'device_setup_intersec'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_create_for_intersec_sg_internet(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceintersecsg'
        job_class_name = 'SetupDeviceInterSecSg'
        job_method_name = 'device_add_port_intersec'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_add_ipv6_for_intersec_sg_internet(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceintersecsg'
        job_class_name = 'SetupDeviceInterSecSg'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_delete_for_intersec_sg_internet(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceintersecsg'
        job_class_name = 'SetupDeviceInterSecSg'
        job_method_name = 'device_del_port_intersec'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_fortigate_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigatevm'
        job_class_name = 'SetupDeviceFortigateVm'
        job_method_name = 'device_setup_create_for_fortigate_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_fortigate_vm_541(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigatevm541'
        job_class_name = 'SetupDeviceFortigateVm541'
        job_method_name = 'device_setup_create_for_fortigate_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_fortigate(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_fortigate_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_setup_add_ipv6_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_fortigate_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigatevm'
        job_class_name = 'SetupDeviceFortigateVm'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_fortigate_vm_541(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigatevm541'
        job_class_name = 'SetupDeviceFortigateVm541'
        job_method_name = 'device_setup_add_ipv6_for_fortigate_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_create_for_fortigate_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigatevm'
        job_class_name = 'SetupDeviceFortigateVm'
        job_method_name = 'device_add_port_for_fortigate_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_create_for_fortigate_vm_541(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigatevm541'
        job_class_name = 'SetupDeviceFortigateVm541'
        job_method_name = 'device_add_port_for_fortigate_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_paloalto_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloaltovm'
        job_class_name = 'SetupDevicePaloAltoVm'
        job_method_name = 'device_setup_paloalto_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_paloalto_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloaltovm'
        job_class_name = 'SetupDevicePaloAltoVm'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_createfor_paloalto_vm(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloaltovm'
        job_class_name = 'SetupDevicePaloAltoVm'
        job_method_name = 'device_add_port_paloalto_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_intersec_sg_pub(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceintersecsg'
        job_class_name = 'SetupDeviceInterSecSg'
        job_method_name = 'device_setup_intersec_pub'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_create_for_intersec_sg_pub(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceintersecsg'
        job_class_name = 'SetupDeviceInterSecSg'
        job_method_name = 'device_add_port_intersec'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_add_ipv6_for_intersec_sg_pub(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceintersecsg'
        job_class_name = 'SetupDeviceInterSecSg'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_delete_for_intersec_sg_pub(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceintersecsg'
        job_class_name = 'SetupDeviceInterSecSg'
        job_method_name = 'device_del_port_intersec'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_intersec_lb(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdeviceinterseclb'
        job_class_name = 'SetupDeviceInterSecLb'
        job_method_name = 'device_setup_create_intersec_lb'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_bigip_ve(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicebigipve'
        job_class_name = 'SetupDeviceBigIpVe'
        job_method_name = 'device_setup_create_bigip_ve'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_bigip_ve(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicebigipve'
        job_class_name = 'SetupDeviceBigIpVe'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_vthunder(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicevthunder'
        job_class_name = 'SetupDeviceVthunder'
        job_method_name = 'device_setup_create_vthunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_thunder(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicethunder'
        job_class_name = 'SetupDeviceThunder'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_thunder_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicethunder'
        job_class_name = 'SetupDeviceThunder'
        job_method_name = 'device_setup_add_ipv6_for_thunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_vthunder(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicevthunder'
        job_class_name = 'SetupDeviceVthunder'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_vthunder411(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicevthunder411'
        job_class_name = 'SetupDeviceVthunder411'
        job_method_name = 'device_setup_create_for_vthunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_vthunder411(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicevthunder411'
        job_class_name = 'SetupDeviceVthunder411'
        job_method_name = 'device_setup_add_ipv6_for_vthunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_fortigate(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_setup_create_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_fortigate_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_setup_create_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_create_for_fortigate(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_add_port_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_create_for_fortigate_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_add_port_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_delete_for_fortigate(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_delete_port_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_delete_for_fortigate_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_delete_port_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_delete_for_fortigate(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_setup_delete_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_delete_for_fortigate_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicefortigate'
        job_class_name = 'SetupDeviceFortigate'
        job_method_name = 'device_setup_delete_for_fortigate'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_paloalto(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_setup_create_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_paloalto_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_setup_create_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_create_for_paloalto(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_add_port_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_create_for_paloalto_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_add_port_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_paloalto(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_paloalto_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_setup_add_ipv6_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_delete_for_paloalto(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_delete_port_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_configuration_delete_for_paloalto_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_delete_port_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_delete_for_paloalto(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_setup_delete_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_delete_for_paloalto_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicepaloalto'
        job_class_name = 'SetupDevicePaloAlto'
        job_method_name = 'device_setup_delete_for_paloalto'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_bigip(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicebigip'
        job_class_name = 'SetupDeviceBigIp'
        job_method_name = 'device_setup_create_bigip'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_bigip(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicebigip'
        job_class_name = 'SetupDeviceBigIp'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_add_ipv6_for_bigip_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicebigip'
        job_class_name = 'SetupDeviceBigIp'
        job_method_name = 'device_setup_add_ipv6_for_bigip'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_bigip_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicebigip'
        job_class_name = 'SetupDeviceBigIp'
        job_method_name = 'device_setup_create_bigip'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_delete_for_bigip(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicebigip'
        job_class_name = 'SetupDeviceBigIp'
        job_method_name = 'device_setup_delete_bigip'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_delete_for_bigip_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicebigip'
        job_class_name = 'SetupDeviceBigIp'
        job_method_name = 'device_setup_delete_bigip'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_thunder(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicethunder'
        job_class_name = 'SetupDeviceThunder'
        job_method_name = 'device_setup_create_thunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_create_for_thunder_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicethunder'
        job_class_name = 'SetupDeviceThunder'
        job_method_name = 'device_setup_create_thunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_delete_for_thunder(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicethunder'
        job_class_name = 'SetupDeviceThunder'
        job_method_name = 'device_setup_delete_thunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def device_setup_delete_for_thunder_share(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicethunder'
        job_class_name = 'SetupDeviceThunder'
        job_method_name = 'device_setup_delete_thunder'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Finalize
    # ---------------------------------------------------------------
    def terminate_create_vnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = 'terminate_create_apl'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def terminate_update_vnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = 'terminate_update_apl'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def terminate_delete_vnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = 'get_job_return_value'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def terminate_create_pnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = 'terminate_create_apl'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def terminate_delete_pnf(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = 'get_job_return_value'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def terminate(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = 'terminate_update_apl'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def set_job_return_data_physical_pt_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # DC Pre
    # ---------------------------------------------------------------
    # Connect -----------------------------------------------------
    def virtual_rt_msa_lan_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'portwim'
        job_class_name = 'PortWim'
        job_method_name = 'virtual_msa_lan_create'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def msa_customer_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'customer'
        job_class_name = 'Customer'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Connect & Update ( Port Add ) -------------------------------
    def virtual_rt_tenant_vlan_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlanwim'
        job_class_name = 'VlanWim'
        job_method_name = 'tenant_vlan_port_create'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Update ( Port Add ) & Disconnect ----------------------------
    def virtual_rt_dc_connected_info_get(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'preparewim'
        job_class_name = 'PrepareWim'
        job_method_name = 'get_rt_dc_connected_info_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Update ( Port Add ) For IPv6 --------------------------------
    def virtual_rt_tenant_vlan_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlanwim'
        job_class_name = 'VlanWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Connect -----------------------------------------------------
    def set_job_return_data_virtual_rt_connect_prepare(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Update ( Port Add ) -----------------------------------------
    def set_job_return_data_virtual_rt_connect_update_prepare(self,
                                                              job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Disconnect --------------------------------------------------
    def set_job_return_data_virtual_rt_disconnect_prepare(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # DC WIM
    # ---------------------------------------------------------------
    # Connect -----------------------------------------------------
    def virtual_rt_dc_member_create_info(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'memberwim'
        job_class_name = 'MemberWim'
        job_method_name = 'dc_member_create_info_get'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_wan_vlan_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlanwim'
        job_class_name = 'VlanWim'
        job_method_name = 'wan_vlan_create'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_port_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'portwim'
        job_class_name = 'PortWim'
        job_method_name = 'port_create_wim'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_port_create_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'portwim'
        job_class_name = 'PortWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_port_create_csr1000v_for_tunnel(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'portwim'
        job_class_name = 'PortWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_port_create_add_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'portwim'
        job_class_name = 'PortWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_server_create_firefly(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'serverwim'
        job_class_name = 'ServerWim'
        job_method_name = 'server_create_rt_vm_firefly'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_server_create_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'serverwim'
        job_class_name = 'ServerWim'
        job_method_name = 'server_create_rt_vm_csr1000v'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_msa_setup(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupmsawim'
        job_class_name = 'SetupMsaWim'
        job_method_name = 'msa_setup_vm_wim'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_device_setup_create_firefly(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = 'device_setup_create_firefly_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_device_setup_create_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = 'device_setup_create_csr1000v_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_connect_firefly(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = 'dc_connect_firefly_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_connect_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = 'dc_connect_csr1000v_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def set_job_return_data_virtual_rt_connect_create(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Update ( Port Add ) -----------------------------------------
    def virtual_rt_dc_member_update_info(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'memberwim'
        job_class_name = 'MemberWim'
        job_method_name = 'dc_member_update_info_get'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_server_update(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'serverwim'
        job_class_name = 'ServerWim'
        job_method_name = 'server_attach_interface_rt_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_server_update_ipv6(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'serverwim'
        job_class_name = 'ServerWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_update_msa_group_id_firefly(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = 'get_new_nic_name'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_update_msa_group_id_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = 'get_new_nic_name'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_device_setup_update_firefly(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = 'device_setup_update_firefly_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_device_setup_update_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = 'device_setup_update_csr1000v_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_device_setup_add_ipv6_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_device_setup_add_ipv6_csr1000v_for_tunnel(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_connect_update_firefly(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = 'dc_connect_update_firefly_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_connect_update_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = 'dc_connect_update_csr1000v_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def set_job_return_data_virtual_rt_connect_update(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Disconnect --------------------------------------------------
    def virtual_rt_dc_member_delete_info(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'memberwim'
        job_class_name = 'MemberWim'
        job_method_name = 'dc_member_delete_info_get'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_disconnect_firefly(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = 'dc_disconnect_firefly_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_disconnect_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = 'dc_disconnect_csr1000v_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_msa_license_delete_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_msa_setup_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupmsawim'
        job_class_name = 'SetupMsaWim'
        job_method_name = 'msa_delete_device_setting_vm_wim'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_tenant_vlan_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlanwim'
        job_class_name = 'VlanWim'
        job_method_name = 'tenant_vlan_port_delete'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_wan_vlan_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlanwim'
        job_class_name = 'VlanWim'
        job_method_name = 'wan_vlan_delete'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_msa_port_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'portwim'
        job_class_name = 'PortWim'
        job_method_name = 'msa_port_delete_wim'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_server_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'serverwim'
        job_class_name = 'ServerWim'
        job_method_name = 'server_delete_rt_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_member_vlan_group_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'memberwim'
        job_class_name = 'MemberWim'
        job_method_name = 'dc_member_vlan_group_delete'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def set_job_return_data_virtual_rt_disconnect_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # DC Fin
    # ---------------------------------------------------------------
    # Connect & Update ( Port Add ) -------------------------------
    def virtual_rt_dc_finalize_connect(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'finalizewim'
        job_class_name = 'FinalizeWim'
        job_method_name = 'finalize_dc_connect_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Disconnect --------------------------------------------------
    def virtual_rt_tenant_vlan_port_iaas_delete(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'vlanwim'
        job_class_name = 'VlanWim'
        job_method_name = 'tenant_vlan_port_iaas_delete'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_finalize_disconnect(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'finalizewim'
        job_class_name = 'FinalizeWim'
        job_method_name = 'finalize_dc_disconnect_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # BandWidth
    # ---------------------------------------------------------------
    def virtual_rt_bandwidth_info_get(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'preparewim'
        job_class_name = 'PrepareWim'
        job_method_name = 'get_rt_dc_connected_info_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_bandwidth_update_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def set_job_return_data_virtual_rt_bandwidth_update_prepare(self,
                                                              job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def set_job_return_data_virtual_rt_bandwidth_update(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_finalize_bandwidth(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'finalizewim'
        job_class_name = 'FinalizeWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Service Setting
    # ---------------------------------------------------------------
    def virtual_rt_dc_setting_info_get(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'preparewim'
        job_class_name = 'PrepareWim'
        job_method_name = 'get_rt_dc_connected_info_vm'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_setting_update_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def set_job_return_data_virtual_rt_setting_update_prepare(self,
                                                              job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def set_job_return_data_virtual_rt_setting_update(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_finalize_setting_update(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'finalizewim'
        job_class_name = 'FinalizeWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def license_assign_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'licensewim'
        job_class_name = 'LicenseWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def license_withdraw_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'licensewim'
        job_class_name = 'LicenseWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_device_setup_create_csr1000v_extra(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_msa_license_create_csr1000v(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # ---------------------------------------------------------------
    # Tunnel
    # ---------------------------------------------------------------
    def virtual_rt_device_setup_create_csr1000v_for_tunnel(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_connect_csr1000v_for_tunnel(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_device_setup_update_csr1000v_for_tunnel(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'setupdevicewim'
        job_class_name = 'SetupDeviceWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_connect_update_csr1000v_for_tunnel(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def virtual_rt_dc_disconnect_csr1000v_for_tunnel(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'connectwim'
        job_class_name = 'ConnectWim'
        job_method_name = inspect.currentframe().f_code.co_name

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    # Commnon ( terminate ) -----------------------------------------
    def get_job_return_value(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = 'get_job_return_value'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output

    def get_job_return_value_wim(self, job_input):

        # Set Job Automation Info(Module/Class/Method)
        job_module_name = 'return'
        job_class_name = 'Return'
        job_method_name = 'get_job_return_value_wim'

        # Execute Job Automation
        job_output = self.__execute_job_automation(
                job_module_name, job_class_name, job_method_name, job_input)

        return job_output
