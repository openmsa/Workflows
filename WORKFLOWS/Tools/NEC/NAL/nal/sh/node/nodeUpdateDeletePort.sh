#!/bin/sh

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

#
#      Delete of port
#
. ${NALPATH}/common/NAL_C_Common.sh

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_DELETE_VPORT} ] ; then
    ###Virtual FW delete port###

    #Delete virtual LAN & port of tenant
    `pyfunc virtual_fw_tenant_vlan_port_delete`
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_DELETE_PPORT} ] ; then
    ###Physical FW delete port###

    #Delete virtual LAN & port of tenant
    `pyfunc physical_fw_tenant_vlan_port_delete`
    status=$?

fi
exit $status
