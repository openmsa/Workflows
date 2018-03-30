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
#      Creation of the port
#
. ${NALPATH}/common/NAL_C_Common.sh

#Creation of the MSA port
status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VFW} -o ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VLB}  ] ; then
    ###VNF creation###
    `pyfunc virtual_msa_port_create`
    status=$?
    if [ $status != 0 ] ; then
        exit $status
    fi
fi

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VFW} ] ; then
    ###Virtual FW creation###

    #if that is not InterSec(with Internet), create Pub port.
    if [ ${NAL_DEVICETYPE} != ${DEVTYPE_VFW_INTERSEC_SG_EXT} ] ; then
        `pyfunc virtual_pub_port_create`
        status=$?
        if [ $status != 0 ] ; then
           exit $status
        fi
    fi

    #if that is not InterSec(without Internet), create Ext port.
    if [ ${NAL_DEVICETYPE} != ${DEVTYPE_VFW_INTERSEC_SG_PUB} ] ; then
        `pyfunc virtual_ext_port_create`
        status=$?
        if [ $status != 0 ] ; then
           exit $status
        fi
    fi

    #Creation of the virtual LAN of tenant & port for vfw
    `pyfunc virtual_fw_tenant_vlan_port_create`
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_PFW} ] ; then
    ###Physical FW creation###

    #Creation of the Pub port.
    `pyfunc physical_pub_port_create`
    status=$?
    if [ $status != 0 ] ; then
       exit $status
    fi

    #Creation of the Ext port.
    `pyfunc physical_ext_port_create`
    status=$?
    if [ $status != 0 ] ; then
       exit $status
    fi

    #Creation of the virtual LAN of tenant & port for pfw
    `pyfunc physical_fw_tenant_vlan_port_create`
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_VLB} ] ; then
    ###Virtual LB creation###

    #Creation of the virtual LAN of tenant & port for vlb
    `pyfunc virtual_lb_tenant_vlan_port_create`
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_CREATE_PLB} ] ; then
    ###Physical LB creation###

    #Creation of the virtual LAN of tenant & port for plb
    `pyfunc physical_lb_tenant_vlan_port_create`
    status=$?
fi

exit $status