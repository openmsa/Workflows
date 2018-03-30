<?php
$result[0]['create_id'] = 'system';
$result[0]['create_date'] = date("YmdHis");
$result[0]['update_id'] = 'system';
$result[0]['update_date'] = date("YmdHis");
$result[0]['delete_flg'] = 0;
$result[0]['ID'] = 133;
$result[0]['status'] = 1;
$result[0]['node_id'] = 1;
$result[0]['tenant_name'] = 'test_tenant_1';

$result[1]['create_id'] = 'system';
$result[1]['create_date'] = date("YmdHis");
$result[1]['update_id'] = 'system';
$result[1]['update_date'] = date("YmdHis");
$result[1]['delete_flg'] = 0;
$result[1]['ID'] = 133;
$result[1]['status'] = 3;
$result[1]['node_id'] = 1;
$result[1]['tenant_name'] = 'test_tenant_2';

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $result );