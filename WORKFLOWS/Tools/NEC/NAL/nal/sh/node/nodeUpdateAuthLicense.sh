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
#      Auth license
#
. ${NALPATH}/common/NAL_C_Common.sh

#In the case of PaloaltoVM
if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_PALOALTO_LICENSE} ] ; then
    `pyfunc license_assign_palpalto_vm`
    exit $?
#In the case of vThunder
elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_VTHUNDER_LICENSE} -o ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_VTHUNDER411_LICENSE} ] ; then
    `pyfunc license_assign_vthunder`
    exit $?
fi
