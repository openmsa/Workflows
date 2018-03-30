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
#      Delete of Msa
#
. ${NALPATH}/common/NAL_C_Common.sh

#Deletion of machine settings
if [ ${NAL_DEVICETYPE} = ${DEVTYPE_DCCON_FIREFLY} ] ; then
    `pyfunc virtual_rt_dc_disconnect_firefly`
    status=$?

elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_DCCON_CSR1000V} ] ; then
    `pyfunc virtual_rt_dc_disconnect_csr1000v`

    status=$?
    if [ $status != 0 ] ; then
        exit $status
    fi

    `pyfunc virtual_rt_msa_license_delete_csr1000v`
    status=$?

elif [ ${NAL_DEVICETYPE} = ${DEVTYPE_DCCON_CSR1000V_TUNNEL} -o ${NAL_DEVICETYPE} = ${DEVTYPE_DCCON_CSR1000V_TUNNEL_NO_ENCRYPTION} ] ; then
    `pyfunc virtual_rt_dc_disconnect_csr1000v_for_tunnel`
    status=$?

    if [ $status != 0 ] ; then
        exit $status
    fi

    `pyfunc virtual_rt_msa_license_delete_csr1000v`
    status=$?
fi

if [ $status != 0 ] ; then
   exit $status
fi

#Deletion of Msa settings
`pyfunc virtual_rt_msa_setup_delete`
exit $?

