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
#       Create Return Value
#
. ${NALPATH}/common/NAL_C_Common.sh

`pyfunc set_job_return_data_virtual_rt_setting_update`
status=$?
if [ $status != 0 ] ; then
    exit $status
fi

`pyfunc get_job_return_value_wim`
exit $?