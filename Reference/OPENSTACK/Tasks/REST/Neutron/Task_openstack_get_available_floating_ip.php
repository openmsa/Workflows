<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('floating_ip_network', 'String');
	create_var_def('tenant', 'String');
}

check_mandatory_param('floating_ip_network');
check_mandatory_param('tenant');

$floating_ip_network = $context['floating_ip_network'];
$floating_ip_tenant = $context['tenant'];

$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$neutron_endpoint = $endpoints[NEUTRON]['endpoints'][0][ADMIN_URL];

$response = allocate_floatingip_address($token_id, $neutron_endpoint, $floating_ip_network, $floating_ip_tenant);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$context = $response['wo_newparams'];
$response = prepare_json_response(ENDED, $response['wo_comment'], $context, true);
echo $response;

?>
