#!/bin/bash

# variables declaration
ip=$1
id=$2
pw=$3
seg_id=$4
pod_nm=$5
iaas_net_id=$6
time_out=$7

# expect start
DIR=$(cd $(dirname $0); pwd)
/usr/bin/expect $DIR/createVxlanGw.exp $ip $id $pw $seg_id $pod_nm $iaas_net_id $time_out 1>&2
exit $?
