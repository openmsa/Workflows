<?php

$retData[0]['device_type'] = '1';
$retData[0]['region_id']   = '';
$retData[0]['pod_id']      = '1';

$endpoint_info['vim']['endPoint']          = 'http://10.58.70.111:5000/v2.0';
$endpoint_info['vim']['userId']            = 'admin';
$endpoint_info['vim']['userPassword']      = 'admin';
$endpoint_info['vim']['userkey']           = '2953e1c876454fc3b59a1eaf09bd7a09';
$endpoint_info['vim']['role_id']           = 'cd034e1a0f774a1aa125edcc3f35598e';
$endpoint_info['vim']['admin_tenant_name'] = 'admin';

$retData[0]['endpoint_info'] = json_encode( $endpoint_info );

/*
$retData[1]['device_type'] = '1';
$retData[1]['region_id']   = '';
$retData[1]['pod_id']      = '2';

$endpoint_info['vim']['endPoint']          = 'http://10.58.79.97:5000/v2.0';
$endpoint_info['vim']['userId']            = 'admin';
$endpoint_info['vim']['userPassword']      = 'admin';
$endpoint_info['vim']['userkey']           = '2953e1c876454fc3b59a1eaf09bd7a09';
$endpoint_info['vim']['role_id']           = 'cd034e1a0f774a1aa125edcc3f35598e';
$endpoint_info['vim']['admin_tenant_name'] = 'admin';

$retData[1]['endpoint_info'] = json_encode( $endpoint_info );

$retData[2]['device_type'] = '1';
$retData[2]['region_id']   = '';
$retData[2]['pod_id']      = '1';

$endpoint_info['vim']['endPoint']          = 'http://10.58.79.97:5000/v2.0';
$endpoint_info['vim']['userId']            = 'admin';
$endpoint_info['vim']['userPassword']      = 'admin';
$endpoint_info['vim']['userkey']           = '2953e1c876454fc3b59a1eaf09bd7a09';
$endpoint_info['vim']['role_id']           = 'cd034e1a0f774a1aa125edcc3f35598e';
$endpoint_info['vim']['admin_tenant_name'] = 'admin';

$retData[2]['endpoint_info'] = json_encode( $endpoint_info );
*/

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $retData );