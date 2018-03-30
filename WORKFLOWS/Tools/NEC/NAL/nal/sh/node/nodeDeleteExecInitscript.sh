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
#      The license is removed due to the deletion of the node
#
. ${NALPATH}/common/NAL_C_Common.sh

if [ ${NAL_JOBNAME} = ${JOB_NAME_DELETE_VFW} -o ${NAL_JOBNAME} = ${JOB_NAME_DELETE_VLB} ] ; then
    `pyfunc license_withdraw`
    exit $?
fi
