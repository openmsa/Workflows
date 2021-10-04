<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	#create_var_def('floating_ip_address', 'String');
	#create_var_def('server_id', 'String');
}

check_mandatory_param('floating_ip_address');
check_mandatory_param('server_id');

$floatingip_address = $context['floating_ip_address'];
$server_id = $context['server_id'];
$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$nova_endpoint = $endpoints[NOVA]['endpoints'][0][ADMIN_URL];
	
$response = _nova_floating_ip_associate($nova_endpoint, $token_id, $server_id, $floatingip_address);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Floating IP $floatingip_address associated successfully to the server $server_id.", $context, true);
echo $response;
?>