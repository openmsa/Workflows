

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
#      common constant definition and common function
#
status=0

###job name###
#creation of FW
readonly JOB_NAME_CREATE_VFW="create-vfw"
readonly JOB_NAME_CREATE_PFW="create-pfw"

#creation of LB
readonly JOB_NAME_CREATE_VLB="create-vlb"
readonly JOB_NAME_CREATE_PLB="create-plb"

#port additional
readonly JOB_NAME_CREATE_VPORT="create-vport"
readonly JOB_NAME_CREATE_PPORT="create-pport"

#port delete
readonly JOB_NAME_DELETE_VPORT="delete-vport"
readonly JOB_NAME_DELETE_PPORT="delete-pport"

#auth license
readonly JOB_NAME_AUTH_LICENSE="auth-license"

#delete of FW
readonly JOB_NAME_DELETE_VFW="delete-vfw"
readonly JOB_NAME_DELETE_PFW="delete-pfw"

#delete of LB
readonly JOB_NAME_DELETE_VLB="delete-vlb"
readonly JOB_NAME_DELETE_PLB="delete-plb"

#add ipv6 of FW
readonly JOB_NAME_UPDATE_VFWIPV6ADD="update-vfwIPv6Add"
readonly JOB_NAME_UPDATE_PFWIPV6ADD="update-pfwIPv6Add"

#add ipv6 of LB
readonly JOB_NAME_UPDATE_VLBIPV6ADD="update-vlbIPv6Add"
readonly JOB_NAME_UPDATE_PLBIPV6ADD="update-plbIPv6Add"

###device type###
#virtual FW
readonly DEVTYPE_VFW_INTERSEC_SG_EXT=1
readonly DEVTYPE_VFW_FORTIGATE=2
readonly DEVTYPE_VFW_PALOALTO=3
readonly DEVTYPE_VFW_INTERSEC_SG_PUB=4
readonly DEVTYPE_VFW_FORTIGATE541=5
readonly DEVTYPE_VFW_PALOALTO_LICENSE=13

#physical FW
readonly DEVTYPE_PFW_FORTIGATE=1
readonly DEVTYPE_PFW_PALOALTO=2
readonly DEVTYPE_PFW_FORTIGATE_SHARE=3
readonly DEVTYPE_PFW_PALOALTO_SHARE=4

#virtual LB
readonly DEVTYPE_VLB_INTERSEC_LB=1
readonly DEVTYPE_VLB_BIGIP=2
readonly DEVTYPE_VLB_VTHUNDER=3
readonly DEVTYPE_VLB_VTHUNDER411=4
readonly DEVTYPE_VLB_VTHUNDER_LICENSE=23
readonly DEVTYPE_VLB_VTHUNDER411_LICENSE=24

#physical LB
readonly DEVTYPE_PLB_BIGIP=1
readonly DEVTYPE_PLB_THUNDER=2
readonly DEVTYPE_PLB_BIGIP_SHARE=3
readonly DEVTYPE_PLB_THUNDER_SHARE=4

#DC connect router
readonly DEVTYPE_DCCON_FIREFLY=11
readonly DEVTYPE_DCCON_CSR1000V=22
readonly DEVTYPE_DCCON_CSR1000V_TUNNEL=23
readonly DEVTYPE_DCCON_CSR1000V_TUNNEL_NO_ENCRYPTION=24



pyfunc () {
        jobname=$1
        logscript='/home/nsumsmgr/NAL/php/OutputLog.php';
        outflg=1
        PHPLOG=/var/log/nal/nal_job_trace.log

        echo `date '+%Y/%m/%d %H:%M:%S.%4N'` ${NAL_JOB_UUID} ${NAL_JOBNAME} start ${jobname} >> ${PHPLOG}
        python3 ${NWACMD} ${jobname} >> ${PHPLOG} 2>&1
        status=$?
        echo `date '+%Y/%m/%d %H:%M:%S.%4N'` ${NAL_JOB_UUID} ${NAL_JOBNAME} end " " ${jobname}  $status >> ${PHPLOG}

        if [ -f ${logscript} ] ; then
                php ${logscript} ${jobname}
        fi
        exit $status
}
