<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('serial_number', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('serial_number');

$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);
$serial_number = $context['serial_number'];
$response = _device_fields_set_serial_number($device_id, $serial_number);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Serial Number $serial_number set for the device $device_id.", $context, true);
echo $response;
?>