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
#      Delete of MSA
#
. ${NALPATH}/common/NAL_C_Common.sh

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_DELETE_VPORT} ] ; then
    ###Virtual FW port delete###

    #In the case of InterSec(with Internet)
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_EXT} ] ; then
        `pyfunc msa_configuration_delete_for_intersec_sg_internet`

    #In the case of InterSec(without Internet)
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_PUB} ] ; then
        `pyfunc msa_configuration_delete_for_intersec_sg_pub`
    fi
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_DELETE_PPORT} ] ; then
    ###Physical FW port delete###

    #In the case of Fortigate
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_FORTIGATE} ] ; then
        `pyfunc msa_configuration_delete_for_fortigate`

    #In the case of Paloalto
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_PALOALTO} ] ; then
        `pyfunc msa_configuration_delete_for_paloalto`

    #In the case of Fortigate share
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_FORTIGATE_SHARE} ] ; then
        `pyfunc msa_configuration_delete_for_fortigate_share`

    #In the case of Paloalto share
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_PALOALTO_SHARE} ] ; then
        `pyfunc msa_configuration_delete_for_paloalto_share`
    fi
    status=$?
fi
exit $status
