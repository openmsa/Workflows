<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);

$command = "license_enable_generic";
$response = _secengine_perform_command_on_device($device_id, $command, "", 600, 600);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
if ($response['wo_newparams']['status'] !== STATUS_OK) {
	$message = $response['wo_newparams']['message'];
	$response = prepare_json_response(FAILED, "Message : $message", $context, true);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "License Enabled Successfully on the device $device_id", $context, true);
echo $response;

?>