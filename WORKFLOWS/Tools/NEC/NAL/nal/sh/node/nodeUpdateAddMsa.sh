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
#      Addition of MSA
#
. ${NALPATH}/common/NAL_C_Common.sh

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VPORT} ] ; then
    ###Virtual FW port create###

    #In the case of InterSec(with Internet)
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_EXT} ] ; then
        `pyfunc msa_configuration_create_for_intersec_sg_internet`

    #In the case of InterSec(without Internet)
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_PUB} ] ; then
        `pyfunc msa_configuration_create_for_intersec_sg_pub`

    #In the case of FortiGateVM
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_FORTIGATE} ] ; then
        `pyfunc msa_configuration_create_for_fortigate_vm`

    #In the case of FortiGate5.4.1
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_FORTIGATE541} ] ; then
        `pyfunc msa_configuration_create_for_fortigate_vm_541`

    #In the case of PaloaltoVM
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_PALOALTO} ] ; then
        `pyfunc msa_configuration_createfor_paloalto_vm`
    fi
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_PPORT} ] ; then
    ###Physical FW port create###

    #In the case of Fortigate
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_FORTIGATE} ] ; then
        `pyfunc msa_configuration_create_for_fortigate`

    #In the case of Paloalto
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_PALOALTO} ] ; then
        `pyfunc msa_configuration_create_for_paloalto`

    #In the case of Fortigate share
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_FORTIGATE_SHARE} ] ; then
        `pyfunc msa_configuration_create_for_fortigate_share`

    #In the case of Paloalto share
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_PALOALTO_SHARE} ] ; then
        `pyfunc msa_configuration_create_for_paloalto_share`
    fi
    status=$?
fi
exit $status
