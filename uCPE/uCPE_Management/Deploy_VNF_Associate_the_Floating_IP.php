<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

function list_args()
{
	create_var_def('openstack_device_id', 'String');
}

check_mandatory_param('openstack_device_id');
check_mandatory_param('floating_ip_address');
check_mandatory_param('server_id');

$openstack_device_id = $context['openstack_device_id'];
$openstack_device_id = preg_replace('/\D/', '', $openstack_device_id);
$floating_ip_address = $context['floating_ip_address'];
$server_id = $context['server_id'];

$response = _nova_floating_ip_associate($openstack_device_id, $server_id, $floating_ip_address);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Floating IP $floating_ip_address associated successfully to the server $server_id.", $context, true);
echo $response;

?>
