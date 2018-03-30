#!/bin/bash

# variables declaration
ip=$1
id=$2
pw=$3
uu_id=$4
time_out=$5

# expect start
DIR=$(cd $(dirname $0); pwd)
/usr/bin/expect $DIR/deleteVxlanGw.exp $ip $id $pw $uu_id $time_out 1>&2
exit $?
