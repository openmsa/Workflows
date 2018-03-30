<?php
$result[0]['create_id'] = 'system';
$result[0]['create_date'] = date("YmdHis");
$result[0]['update_id'] = 'system';
$result[0]['update_date'] = date("YmdHis");
$result[0]['delete_flg'] = 0;
$result[0]['ID'] = 133;
$result[0]['port_id'] = "7777";
$result[0]['tenant_name'] = 'test_tenant_1';
$result[0]['ip_address'] = '196.168.1.89';

$result[1]['create_id'] = 'system';
$result[1]['create_date'] = date("YmdHis");
$result[1]['update_id'] = 'system';
$result[1]['update_date'] = date("YmdHis");
$result[1]['delete_flg'] = 0;
$result[1]['ID'] = 133;
$result[0]['port_id'] = "6666";
$result[1]['tenant_name'] = 'test_tenant_2';
$result[0]['ip_address'] = '196.168.1.89';

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $result );