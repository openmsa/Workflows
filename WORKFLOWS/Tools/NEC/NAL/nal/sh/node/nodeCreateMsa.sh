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
#      Creation of MSA
#
. ${NALPATH}/common/NAL_C_Common.sh

#regist customer for MSA
`pyfunc msa_customer_create`
status=$?
if [ $status != 0 ] ; then
   exit $status
fi

#setup MSA
`pyfunc msa_setup_create`
status=$?
if [ $status != 0 ] ; then
   exit $status
fi

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VFW} ] ; then
    ###Virtual FW creation###

    #In the case of InterSec(with Internet)
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_EXT} ] ; then
        `pyfunc device_setup_create_for_intersec_sg_internet`

    #In the case of InterSec(without Internet)
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_PUB} ] ; then
        `pyfunc device_setup_create_for_intersec_sg_pub`

    #In the case of FortiGateVM
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_FORTIGATE} ] ; then
        `pyfunc device_setup_create_for_fortigate_vm`

    #In the case of FortiGate5.4.1
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_FORTIGATE541} ] ; then
        `pyfunc device_setup_create_for_fortigate_vm_541`

    #In the case of PaloaltoVM
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_PALOALTO} ] ; then
        `pyfunc device_setup_create_for_paloalto_vm`
    fi
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_PFW} ] ; then
    ###Physical FW creation###

    #In the case of Fortigate
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_FORTIGATE} ] ; then
        `pyfunc device_setup_create_for_fortigate`

    #In the case of Paloalto
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_PALOALTO} ] ; then
        `pyfunc device_setup_create_for_paloalto`

    #In the case of Fortigate share
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_FORTIGATE_SHARE} ] ; then
        `pyfunc device_setup_create_for_fortigate_share`

    #In the case of Paloalto share
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PFW_PALOALTO_SHARE} ] ; then
        `pyfunc device_setup_create_for_paloalto_share`
    fi
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VLB} ] ; then
    ###Virtual LB creation###

    #In the case of InterSecVM/LB
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_INTERSEC_LB} ] ; then
        `pyfunc device_setup_create_for_intersec_lb`

    #In the case of BIGIP
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_BIGIP} ] ; then
        `pyfunc device_setup_create_for_bigip_ve`

    #In the case of vThunder
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_VTHUNDER} ] ; then
        `pyfunc device_setup_create_for_vthunder`

    #In the case of vThunder4.1.1
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VLB_VTHUNDER411} ] ; then
        `pyfunc device_setup_create_for_vthunder411`
    fi
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_PLB} ] ; then
    ###Physical LB creation###

    #In the case of BIGIP
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_PLB_BIGIP} ] ; then
        `pyfunc device_setup_create_for_bigip`

    #In the case of Thunder
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PLB_THUNDER} ] ; then
        `pyfunc device_setup_create_for_thunder`

    #In the case of BIGIP share
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PLB_BIGIP_SHARE} ] ; then
        `pyfunc device_setup_create_for_bigip_share`

    #In the case of Thunder share
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_PLB_THUNDER_SHARE} ] ; then
        `pyfunc device_setup_create_for_thunder_share`
    fi
    status=$?
fi
exit $status
