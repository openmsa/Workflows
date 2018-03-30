<?php
$result[0]['create_id']      = 'system';
$result[0]['create_date']    = '20160729000000';
$result[0]['update_id']      = 'system';
$result[0]['update_date']    = '20160729000000';
$result[0]['delete_flg']     = '0';
$result[0]['ID']             = '45';
$result[0]['tenant_name']    = 'admin';
$result[0]['IaaS_region_id'] = 'region1';
$result[0]['IaaS_tenant_id'] = '37db35eebab948e3a5431ffec38b6cd8';

$result[1]['create_id']      = 'system';
$result[1]['create_date']    = '20160729000000';
$result[1]['update_id']      = 'system';
$result[1]['update_date']    = '20160729000000';
$result[1]['delete_flg']     = '0';
$result[1]['ID']             = '67';
$result[1]['tenant_name']    = 'tenant_name2';
$result[1]['IaaS_region_id'] = 'region2';
$result[1]['IaaS_tenant_id'] = '9876';

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $result );