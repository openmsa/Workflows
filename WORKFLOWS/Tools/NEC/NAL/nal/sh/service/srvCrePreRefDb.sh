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
#     Referring DB
#
. ${NALPATH}/common/NAL_C_Common.sh

`pyfunc get_or_create_pod_tenant`
status=$?
if [ $status != 0 ] ; then
    exit $status
fi

`pyfunc virtual_rt_msa_lan_create`
status=$?
if [ $status != 0 ] ; then
    exit $status
fi

`pyfunc msa_customer_create`
status=$?
if [ $status != 0 ] ; then
    exit $status
fi

`pyfunc virtual_rt_tenant_vlan_port_create`
exit $?