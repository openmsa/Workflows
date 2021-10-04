<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);
$response = _device_fields_get_serial_number($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$serial_number = $response['wo_comment'];

$response = prepare_json_response(ENDED, "Serial Number for the device $device_id :\n$serial_number", $context, true);
echo $response;
?>