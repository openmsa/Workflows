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
#      Environment variable settings for JobScheduler
#

# To get the uuid from the input variable
uuid=`echo ${SCHEDULER_PARAM_ROOT_DIR} | awk -F'/' '{print $NF}'`

export NAL_JOB_UUID=$uuid
export NAL_DIR=${SCHEDULER_PARAM_ROOT_DIR}
export NAL_INPUTFILE=${SCHEDULER_PARAM_ROOT_DIR}/${SCHEDULER_PARAM_INPUT_FILE}
export NAL_OUTPUTFILE=${SCHEDULER_PARAM_ROOT_DIR}/${SCHEDULER_PARAM_OUTPUT_FILE}
export NAL_DEVICETYPE=${SCHEDULER_PARAM_DEVICE_TYPE}
export NAL_JOBNAME=${SCHEDULER_JOB_CHAIN}
# NAL sh directory
export NALPATH=/home/nsumsmgr/NAL/sh
# NWACMD Path
export NWACMD=/home/nsumsmgr/NAL/nwa/job/jobif.py
