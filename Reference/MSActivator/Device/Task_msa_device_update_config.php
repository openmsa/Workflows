<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$device_id = substr($context['device_id'], 3);
$response = _device_do_update_config($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
if ($response['wo_newparams']['status'] !== STATUS_OK) {
	$wo_comment = "Update Configuration Failed on the Device $device_id";
	$code = $response['wo_newparams']['code'];
	$message = $response['wo_newparams']['message'];
	$rawSmsResult = $response['wo_newparams']['rawSmsResult'];
	$result = $response['wo_newparams']['result'];
	if ($code !== null) {
		$wo_comment .= "\nCode : $code";
	}
	if ($message !== null) {
		$wo_comment .= "\nMessage : $message";
	}
	if ($rawSmsResult !== null) {
		$wo_comment .= "\nRaw SMS Result : $rawSmsResult";
	}
	if ($result !== "") {
		$wo_comment .= "\nResult : $result";
	}
	$response = prepare_json_response(FAILED, $wo_comment, $context, true);
	echo $response;
	exit;
}

$response = wait_for_update_config_completion($device_id, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response(FAILED, $response['wo_comment'], $context, true);
	echo $response;
	exit;
}
$update_config_status_message = $response['wo_comment'];

$response = prepare_json_response(ENDED, "Device $device_id Update config completed successfully.\n" . $update_config_status_message, $context, true);
echo $response;

?>
