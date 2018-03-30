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
#      Along with the node removed, to remove the MSA
#
. ${NALPATH}/common/NAL_C_Common.sh

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_DELETE_PFW} ] ; then
    ###PFW delettion###
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_FORTIGATE} ] ; then
        `pyfunc device_setup_delete_for_fortigate`

    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_PALOALTO} ] ; then
        `pyfunc device_setup_delete_for_paloalto`

    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_FORTIGATE_SHARE} ] ; then
        `pyfunc device_setup_delete_for_fortigate_share`

    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_PALOALTO_SHARE} ] ; then
        `pyfunc device_setup_delete_for_paloalto_share`
    fi
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_DELETE_PLB} ] ; then
    ###PLB delettion###
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_PLB_BIGIP} ] ; then
        `pyfunc device_setup_delete_for_bigip`

    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PLB_THUNDER} ] ; then
        `pyfunc device_setup_delete_for_thunder`

    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PLB_BIGIP_SHARE} ] ; then
        `pyfunc device_setup_delete_for_bigip_share`

    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PLB_THUNDER_SHARE} ] ; then
        `pyfunc device_setup_delete_for_thunder_share`
    fi
    status=$?
fi

if [ $status != 0 ] ; then
    exit $status
fi

`pyfunc msa_setup_delete`
exit $?
