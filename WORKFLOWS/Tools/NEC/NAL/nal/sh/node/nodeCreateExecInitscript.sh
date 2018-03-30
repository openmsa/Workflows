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
#      Execute initialization script
#
. ${NALPATH}/common/NAL_C_Common.sh

# In the case of VNF creation, execute license auth script

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VFW} ] ; then
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_EXT} -o ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_PUB} ] ; then
        `pyfunc license_assign`
        status=$?
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_FORTIGATE} ] ; then
        `pyfunc license_assign_fortigate_vm`
        status=$?
    fi
elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VLB} ] ; then
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_INTERSEC_LB} ] ; then
        `pyfunc license_assign`
        status=$?
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_BIGIP} ] ; then
        `pyfunc license_assign_bigip_ve`
        status=$?
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_VTHUNDER} ] ; then
        `pyfunc zerotouch_vthunder`
        status=$?
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_VTHUNDER411} ] ; then
        `pyfunc zerotouch_vthunder`
        status=$?
    fi
fi
exit $status
