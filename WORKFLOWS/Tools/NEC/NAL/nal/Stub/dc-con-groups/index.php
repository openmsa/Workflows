<?php

$result[0]['create_id'] = 'system';
$result[0]['create_date'] = '20160729000000';
$result[0]['update_id'] = 'system';
$result[0]['update_date'] = '20160729000000';
$result[0]['delete_flg'] = '0';
$result[0]['ID'] = '23';
$result[0]['group_id'] = '1';
$result[0]['group_name']     = 'dc_gru_1';
$result[0]['group_type']     = '1';
$result[0]['tenant_name']    = 'admin';
$result[0]['IaaS_tenant_id'] = '1234';

$result[1]['create_id'] = 'system';
$result[1]['create_date'] = '20160729000000';
$result[1]['update_id'] = 'system';
$result[1]['update_date'] = '20160729000000';
$result[1]['delete_flg'] = '0';
$result[1]['ID'] = '23';
$result[1]['group_id'] = '2';
$result[1]['group_name']     = 'dc_gru_2';
$result[1]['group_type']     = '2';
$result[1]['tenant_name']     = 'tenant_name2';
$result[1]['IaaS_tenant_id'] = '9876';

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $result );