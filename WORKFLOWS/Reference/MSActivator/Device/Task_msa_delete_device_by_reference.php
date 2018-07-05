<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_external_reference', 'Device');
}

if(empty($context['device_external_reference'])) {

	$response = prepare_json_response(ENDED, "No device to delete", $context, true);
	echo $response;
	exit;
}

$device_external_reference = $context['device_external_reference'];
$response = _device_delete_by_reference($device_external_reference);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response['wo_status'] = WARNING;
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "MSA Device $device_external_reference deleted successfully.", $context, true);
echo $response;

?>
