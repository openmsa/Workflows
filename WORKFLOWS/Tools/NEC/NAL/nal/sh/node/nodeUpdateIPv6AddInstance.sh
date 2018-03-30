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
#      Instance addition
#
. ${NALPATH}/common/NAL_C_Common.sh

if [ ${NAL_JOBNAME} = ${JOB_NAME_UPDATE_VFWIPV6ADD} ] ; then
    ###Virtual FW IPv6 add###

    #Virtual FW instance port attach
    `pyfunc virtual_fw_interface_attach_ipv6`

elif [ ${NAL_JOBNAME} = ${JOB_NAME_UPDATE_VLBIPV6ADD} ] ; then
    ###Virtual LB IPv6 add###

    #Virtual LB instance port attach
    `pyfunc virtual_lb_interface_attach_ipv6`

fi
exit $?