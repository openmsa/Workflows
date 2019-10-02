<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('floatingip_id', 'String');
}

check_mandatory_param('floatingip_id');
check_mandatory_param('port_id');

$floatingip_id = $context['floatingip_id'];
$port_id = $context['port_id'];
$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$neutron_endpoint = $endpoints[NEUTRON]['endpoints'][0][ADMIN_URL];
	
$response = _neutron_associate_floatingip_to_port($neutron_endpoint, $token_id, $floatingip_id, $port_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$floating_ip_address = $response['wo_newparams']['floatingip']['floating_ip_address'];
$context['floating_ip_address'] = $floating_ip_address;
$response = prepare_json_response(ENDED, "Floating IP $floatingip_id associated successfully to the Port $port_id.\nFloating IP address : $floating_ip_address", 
									$context, true);
echo $response;

?>