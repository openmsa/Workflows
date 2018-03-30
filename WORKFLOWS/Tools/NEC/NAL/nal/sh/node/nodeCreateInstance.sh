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
#      Creation of instance
#
. ${NALPATH}/common/NAL_C_Common.sh

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VFW} ] ; then
    ###Virtual FW creation###
    #In the case of InterSec(with Internet) or  InterSec(without Internet), create instance for Intersce
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_EXT} -o ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_PUB}  ] ; then
        `pyfunc virtual_server_create_intersec`
        exit $?
    #in the case of FortiGate5.4.1
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_FORTIGATE541} ] ; then
        `pyfunc virtual_server_create_with_config_drive`
        exit $?
    #in the case of PaloAltoVM
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_PALOALTO} ] ; then
        `pyfunc virtual_server_create_paloalto_vm`
        exit $?
    fi
elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VLB} ] ; then
    ###Virtual LB creation###
    #In the case of InterSec
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_INTERSEC_LB} ] ; then
        `pyfunc virtual_server_create_intersec`
        exit $?
    fi
fi


if [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VFW} -o ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VLB} ] ; then
    ###Virtual FW/LB creation(without InterSecVM/SG or FortiGate5.4.1)###
    `pyfunc virtual_server_create`
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_PFW} -o ${NAL_JOBNAME} = ${JOB_NAME_CREATE_PLB} ] ; then
    ###Physical FW/LB creation###

    `pyfunc physical_server_create`
    status=$?
fi

exit $status