<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
	
$device_id = substr($context['device_id'], 3);

$configuration = "";

$response = _device_do_push_configuration_by_id($device_id, $configuration);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$timeout_prompt = " # ";
$timeout_ignone_messasges = array("timeout, $timeout_prompt not found", "timeout,  #  not found");
$response = wait_for_pushconfig_completion($device_id, $process_params, $timeout_ignone_messasges);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

// Update device credentials
$response = _device_update_credentials ($device_id, $context['login'], $context['new_password']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

task_exit(ENDED, "Device user password updated successfully.");
?>