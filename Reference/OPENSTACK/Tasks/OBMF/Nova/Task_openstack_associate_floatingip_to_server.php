<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

function list_args()
{
	create_var_def('openstack_device_id', 'String');
}

check_mandatory_param('openstack_device_id');
check_mandatory_param('floating_ip_id');
check_mandatory_param('server_id');

$openstack_device_id = substr($context['openstack_device_id'], 3);
$floating_ip_id = $context['floating_ip_id'];
$server_id = $context['server_id'];

$response = _nova_floating_ip_associate($openstack_device_id, $server_id, $floating_ip_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Floating IP $floating_ip_id associated successfully to the server $server_id.", $context, true);
echo $response;

?>