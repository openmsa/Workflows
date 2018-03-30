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
#      Output jobparam
#
PHPLOG=/var/log/nal/nal_job_trace.log
echo '--------------------start job--------------------' >> ${PHPLOG}
echo JOBUUID=${NAL_JOB_UUID} >> ${PHPLOG}
echo JOBNAME=${NAL_JOBNAME} >> ${PHPLOG}
echo NAL_DIR=${NAL_DIR} >> ${PHPLOG}
echo NAL_INPUTFILE=${NAL_INPUTFILE} >> ${PHPLOG}
echo NAL_OUTPUTFILE=${NAL_OUTPUTFILE} >> ${PHPLOG}
echo NAL_DEVICETYPE=${NAL_DEVICETYPE} >> ${PHPLOG}
echo '-------------------------------------------------' >> ${PHPLOG}