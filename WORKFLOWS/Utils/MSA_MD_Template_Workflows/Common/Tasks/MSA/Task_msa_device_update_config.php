<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
}


foreach ($context['devices'] as $device){
	$device_id = substr($device['device_id'], 3);
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
}

foreach ($context['devices'] as $device){
	waitForUpdateConfigCompletion($device['device_id']);
}

task_success("All devices have been setupped.");

function getUpdateStatus($device_id) {
	//$command="/opt/ubi-etisalatFrontEndCustomization/scripts/check_config_update.sh $dev_id";
	return shell_exec("UPDATESTATUS=$(/opt/sms/bin/sms -e CHECKUPDATE -i $device_id| sed -n '3p'|tr -d '\r'); echo \"\$UPDATESTATUS\"");
}

function waitForUpdateConfigCompletion ($device_id) {

	global $context;

	$i = 0;
	$is_in_progress = true;
	$wait_count = 30;

	//Start with all true conditions to check for status atleast once
	while($i < $wait_count && $is_in_progress === true) {
		//Assume config update is completed for all devices
		$is_in_progress = false;

		//Wait for 5 seconds first before querying for update status
		sleep(5);
		$update_status = trim(getUpdateStatus($device_id));
		logToFile("Device : $device_id :: $update_status");
		if ($update_status === "W") {
			$message = "Config update of devices in progress";
			update_asynchronous_task_details($context, $message);
			$is_in_progress = true;
		} elseif ($update_status === "F") {
			$response = prepare_json_response(FAILED, "MSA Device $device_id Configuration Update status : FAILED", $context, true);
			echo $response;
			return;
		} elseif ($update_status === "E") {
			$response = prepare_json_response(ENDED, "MSA Device $device_id Configuration Update status : ENDED", $context, true);
			echo $response;
			return;
		} elseif ($update_status === "N") {
			$response = prepare_json_response(WARNING, "MSA Device $device_id Configuration Update status : NONE", $context, true);
			echo $response;
			return;
		}
		$i++;
	}
}

?>