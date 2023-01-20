<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
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
	
$configuration = "execute reboot";
$response = _device_do_push_configuration_by_id($device_id, $configuration);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$timeout_ignone_messasge = "closed by peer";
$response = wait_for_pushconfig_completion($device_id, $process_params, $timeout_ignone_messasge);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$pushconfig_status_message = $response['wo_comment'];

$response = prepare_json_response(ENDED, "Fortigate Device $device_id Rebooted Successfully.\n$pushconfig_status_message", 
									$context, true);
echo $response;

?>