<?php
$retData[0]['fw_id'] = '1234';
$retData[0]['fw_name'] = 'test_fw';

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $retData );