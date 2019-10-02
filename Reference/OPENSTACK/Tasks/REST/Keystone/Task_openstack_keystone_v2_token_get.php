<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('admin_username', 'String');
	create_var_def('admin_password', 'Password');
	create_var_def('tenant_id', 'String');
	create_var_def('keystone_public_endpoint', 'String');
}

check_mandatory_param('admin_username');
check_mandatory_param('admin_password');
check_mandatory_param('tenant_id');
check_mandatory_param('keystone_public_endpoint');

$admin_username = $context['admin_username'];
$admin_password = $context['admin_password'];
$openstack_tenant_id = $context['tenant_id'];
$keystone_public_endpoint = $context['keystone_public_endpoint'];
	
$response = _keystone_v2_token_get($keystone_public_endpoint, $admin_username, $admin_password, $openstack_tenant_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$token_id = $response['wo_newparams']['access']['token']['id'];
$endpoints = $response['wo_newparams']['access']['serviceCatalog'];
$context['token_id'] = $token_id;
$context['endpoints'] = seperate_endpoints_v2($endpoints);
$response = prepare_json_response(ENDED, "Token created successfully.\nToken Id : $token_id", $context, true);
echo $response;

?>
