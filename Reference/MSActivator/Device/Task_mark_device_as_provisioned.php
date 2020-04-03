<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$device_id=$context['device_id'];
$device_id = preg_replace('/[A-Z]+/', '', $device_id);
$response = _device_mark_as_provisioned($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "MSA Device $device_id marked as provisioned successfully.", $context, true);
echo $response;

?>
