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
#      Port additional
#
. ${NALPATH}/common/NAL_C_Common.sh

status=0
if [ ${NAL_JOBNAME} = ${JOB_NAME_UPDATE_VFWIPV6ADD} ] ; then
    ###Virtual FW IPv6 add###

    # In case of INTERSEC_SG_EXT
    if [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_EXT} ] ; then
        `pyfunc virtual_ext_port_add_ipv6`
        status=$?

    # In case of INTERSEC_SG_PUB
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_INTERSEC_SG_PUB} ] ; then
        `pyfunc virtual_pub_port_add_ipv6`
        status=$?

    # In case of FORTIGATE or FORTIGATE541
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_FORTIGATE} -o ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_FORTIGATE541} ] ; then
        `pyfunc virtual_pub_port_add_ipv6`
        status=$?
        if [ $status != 0 ] ; then
            exit $status
        fi

        `pyfunc virtual_ext_port_add_ipv6`
        status=$?

    # In case of PALOALTO
    elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_VFW_PALOALTO} ] ; then
        `pyfunc virtual_pub_port_add_ipv6`
        status=$?
        if [ $status != 0 ] ; then
            exit $status
        fi

        `pyfunc virtual_ext_port_add_ipv6`
        status=$?
    fi


    if [ $status != 0 ] ; then
        exit $status
    fi

    `pyfunc virtual_fw_tenant_vlan_port_add_ipv6`
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_UPDATE_VLBIPV6ADD} ] ; then
    ###Virtual LB IPv6 add###

    `pyfunc virtual_lb_tenant_vlan_port_add_ipv6`
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_UPDATE_PFWIPV6ADD} ] ; then
    ###Physical FW IPv6 add###

    `pyfunc physical_pub_port_add_ipv6`
    status=$?
    if [ $status != 0 ] ; then
        exit $status
    fi

    `pyfunc physical_ext_port_add_ipv6`
    status=$?
    if [ $status != 0 ] ; then
        exit $status
    fi

    `pyfunc physical_fw_tenant_vlan_port_add_ipv6`
    status=$?

elif [ ${NAL_JOBNAME} = ${JOB_NAME_UPDATE_PLBIPV6ADD} ] ; then
    ###Physical LB IPv6 add###

    `pyfunc physical_lb_tenant_vlan_port_add_ipv6`
    status=$?

fi
exit $status
