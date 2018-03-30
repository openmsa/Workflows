#!/bin/bash

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

##
## This file is for running tox, coverage test
##
## Jenkins tox or coverage test job will use this file on Jenkins slave server.
## The job name is "nal-dashboard_xxx_Tox" or "nal-dashboard_xxx_Coverage"
##
## nal-dashboard is depeding on
##  - NECCSPortal-dashboard
##  - nalclient
## and this is not a plugin of Horizon.
## The way of running tox test is a little bit special.
## So we write the code that way in this file.
##

##
## Variables determined by Jenkins
if [ "${WORKSPACE}" = "" ]; then
  echo "You need to export WORKSPACE env"
  exit 1
fi
if [ "${BUILD_NUMBER}" = "" ]; then
  echo "You need to export BUILD_NUMBER env"
  exit 1
fi
if [ "${GITHUB_BK_DIR}" = "" ]; then
  echo "You need to export GITHUB_BK_DIR env"
  exit 1
fi
if [ "${WITH_COVERAGE}" = "" ]; then
  echo "You need to export WITH_COVERAGE env"
  exit 1
fi
if [ "${TARGET_NALCLIENT_BR}" = "" ]; then
  echo "You need to export TARGET_NALCLIENT_BR env"
  exit 1
fi
if [ "${TARGET_NECCSPORTAL_BR}" = "" ]; then
  echo "You need to export TARGET_NECCSPORTAL_BR env"
  exit 1
fi
if [ "${TEST_TARGET_SOURCE}" = "" ]; then
  echo "You need to export TEST_TARGET_SOURCE env"
  exit 1
fi
if [ "${TARGET_HORIZON_BR}" = "" ]; then
  echo "You need to export TARGET_HORIZON_BR env"
  exit 1
fi
TARGET_HORIZON_BR_NM=${TARGET_HORIZON_BR//\//_}


##
## RPMs
yum install -y gcc libffi-devel openssl-devel

##
## Git clone Openstack/horizon
cd ${GITHUB_BK_DIR}

if ls ${GITHUB_BK_DIR}/horizon.${TARGET_HORIZON_BR_NM} > /dev/null 2>&1
then
  echo "Already github source is cloned"
else
  git clone -b ${TARGET_HORIZON_BR} --single-branch https://github.com/openstack/horizon.git
  mv horizon horizon.${TARGET_HORIZON_BR_NM}
fi
cd horizon.${TARGET_HORIZON_BR_NM}
git pull
git log -n 1 --format=%H

##
## Git clone NECCSPortal-dashboard from GitLab
cd ${WORKSPACE}
git clone -b ${TARGET_NECCSPORTAL_BR} --single-branch git@10.58.70.7:IntegratedPortal/NECCSPortal-dashboard.git

##
## Create temporary directory
mkdir ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}
cd ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}
cp -prf ${GITHUB_BK_DIR}/horizon.${TARGET_HORIZON_BR_NM} ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}/horizon

##
## Put NECCSPortal-dashboard to horizon
cd ${WORKSPACE}/../
rsync -a ${WORKSPACE}/NECCSPortal-dashboard/* ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}/horizon/ --exclude tox_temp_${BUILD_NUMBER}

##
## Put nal-dashboard to horizon
\cp -prf ${TEST_TARGET_SOURCE}/nec_portal ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}/horizon/
\cp -prf ${TEST_TARGET_SOURCE}/openstack_dashboard ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}/horizon/
\cp -prf ${TEST_TARGET_SOURCE}/run_tests.sh ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}/horizon/

##
## Edit test-requirements.txt to be able to install nalclient
cat <<EOF >> ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}/horizon/test-requirements.txt
-e git+ssh://git@10.58.79.95/nal/nalclient.git@${TARGET_NALCLIENT_BR}#egg=nalclient
EOF

##
## Run tox/coverage
cd ${WORKSPACE}/NECCSPortal-dashboard/tox_temp_${BUILD_NUMBER}/horizon/
if [ "${WITH_COVERAGE}" = "yes" ]; then
  ./run_tests.sh -V -c -n
  cp -p coverage.xml ${WORKSPACE}/NECCSPortal-dashboard/
else
  ./run_tests.sh -V nec_portal
fi

echo "bye"
