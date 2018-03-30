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
#
#      Environment variable settings for JobCenter
#

# To get the job name from the environment variable(jobname:singlejobname)
jobname=`echo ${NSJNW_JNWNAME} | cut -d ":" -f 1`

ary=(`echo $NSJNW_PARAM`)

# To get the uuid from the input variable
uuid=`echo ${ary[0]} | awk -F'/' '{print $NF}'`

echo EXPORTVAR
# Job uuid
echo NAL_JOB_UUID=$uuid
# Directory
echo NAL_DIR=${ary[0]}
# INPUT FILE
echo NAL_INPUTFILE=${ary[0]}/${ary[1]}
# OUTPUT FILE
echo NAL_OUTPUTFILE=${ary[0]}/${ary[2]}
# DEVICE_TYPE
echo NAL_DEVICETYPE=${ary[3]}
# JOBNAME
echo NAL_JOBNAME=$jobname
# NAL sh directory
echo NALPATH=/home/nsumsmgr/NAL/sh
# NWACMD Path
echo NWACMD=/home/nsumsmgr/NAL/nwa/job/jobif.py
echo EXPORTVAR

# for comInit.sh
export NAL_JOB_UUID=$uuid
export NAL_DIR=${ary[0]}
export NAL_INPUTFILE=${ary[0]}/${ary[1]}
export NAL_OUTPUTFILE=${ary[0]}/${ary[2]}
export NAL_DEVICETYPE=${ary[3]}
export NAL_JOBNAME=$jobname
export NALPATH=/home/nsumsmgr/NAL/sh
export NWACMD=/home/nsumsmgr/NAL/nwa/job/jobif.py
