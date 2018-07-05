<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('floatingip_id', 'String');
}

check_mandatory_param('floatingip_id');

$floatingip_id = $context['floatingip_id'];
$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$neutron_endpoint = $endpoints[NEUTRON]['endpoints'][0][ADMIN_URL];
	
$response = _neutron_disassociate_floatingip_from_port($neutron_endpoint, $token_id, $floatingip_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$response = prepare_json_response(ENDED, "Floating IP $floatingip_id disassociated successfully.", $context, true);
echo $response;

?>