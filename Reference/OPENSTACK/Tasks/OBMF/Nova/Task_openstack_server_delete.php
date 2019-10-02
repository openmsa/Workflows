<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

function list_args()
{
	create_var_def('openstack_device_id', 'Device');
	create_var_def('server_id', 'String');
}

check_mandatory_param('openstack_device_id');
check_mandatory_param('server_id');

$openstack_device_id = substr($context['openstack_device_id'], 3);
$server_id = $context['server_id'];
$response = _nova_server_delete($openstack_device_id, $server_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Openstack Server $server_id Deleted successfully.", $context, true);
echo $response;
        
?>