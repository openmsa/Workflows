<?php
$result[0]['create_id'] = 'system';
$result[0]['create_date'] = date("YmdHis");
$result[0]['update_id'] = 'system';
$result[0]['update_date'] = date("YmdHis");
$result[0]['delete_flg'] = 0;
$result[0]['ID'] = 133;
$result[0]['nw_resource_kind'] = 1;
$result[0]['pod_id'] = 1;
$result[0]['tenant_id'] = 'tenant1';
$result[0]['quota'] = 5;
$result[0]['threshold'] = 77;

$result[1]['create_id'] = 'system';
$result[1]['create_date'] = date("YmdHis");
$result[1]['update_id'] = 'system';
$result[1]['update_date'] = date("YmdHis");
$result[1]['delete_flg'] = 0;
$result[1]['ID'] = 133;
$result[1]['nw_resource_kind'] = 2;
$result[1]['pod_id'] = 1;
$result[1]['tenant_id'] = 'tenant2';
$result[1]['quota'] = 5;
$result[1]['threshold'] = 88;

$result[2]['create_id'] = 'system';
$result[2]['create_date'] = date("YmdHis");
$result[2]['update_id'] = 'system';
$result[2]['update_date'] = date("YmdHis");
$result[2]['delete_flg'] = 0;
$result[2]['ID'] = 133;
$result[2]['nw_resource_kind'] = 3;
$result[2]['pod_id'] = 1;
$result[2]['tenant_id'] = 'tenant3';
$result[2]['quota'] = 3;
$result[2]['threshold'] = 90;

$result[3]['create_id'] = 'system';
$result[3]['create_date'] = date("YmdHis");
$result[3]['update_id'] = 'system';
$result[3]['update_date'] = date("YmdHis");
$result[3]['delete_flg'] = 0;
$result[3]['ID'] = 133;
$result[3]['nw_resource_kind'] = 4;
$result[3]['pod_id'] = 1;
$result[3]['tenant_id'] = 'tenant4';
$result[3]['quota'] = 3;
$result[3]['threshold'] = 44;

$result[4]['create_id'] = 'system';
$result[4]['create_date'] = date("YmdHis");
$result[4]['update_id'] = 'system';
$result[4]['update_date'] = date("YmdHis");
$result[4]['delete_flg'] = 0;
$result[4]['ID'] = 133;
$result[4]['nw_resource_kind'] = 5;
$result[4]['pod_id'] = 1;
$result[4]['tenant_id'] = 'tenant5';
$result[4]['quota'] = 3;
$result[4]['threshold'] = 60;

$result[5]['create_id'] = 'system';
$result[5]['create_date'] = date("YmdHis");
$result[5]['update_id'] = 'system';
$result[5]['update_date'] = date("YmdHis");
$result[5]['delete_flg'] = 0;
$result[5]['ID'] = 133;
$result[5]['nw_resource_kind'] = 6;
$result[5]['pod_id'] = 1;
$result[5]['tenant_id'] = 'tenant6';
$result[5]['quota'] = 3;
$result[5]['threshold'] = 77;

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $result );